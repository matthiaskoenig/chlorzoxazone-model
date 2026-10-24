"""Proof of concept of the sampling of the CYP2E1 amounts.

The amounts of the studies with at least 30 subjects against the log-normal
samples with the coefficient of variation of the study.
"""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pkdb_models.models.chlorzoxazone.cyp2e1_amounts.helper import sample_cyp2e1
from pkdb_models.models.chlorzoxazone.models import rcParams


def calc_cv(data: np.ndarray | pd.Series) -> float:
    """Coefficient of variation of a log-normal distribution of decadic logarithms."""
    return float(np.sqrt(np.power(10, np.log(10) * np.var(data)) - 1))


if __name__ == "__main__":
    cyp_amounts = pd.read_excel(Path(__file__).parent / "cyp2e1_amounts.xlsx", "Data")
    study_cvs = {}
    for ethnicity in ["caucasian", "japanese", "chinese"]:
        cyp_df = cyp_amounts[cyp_amounts["ethnicity"].str.contains(ethnicity)]
        for label, label_df in cyp_df.groupby("study"):
            if len(label_df) < 30:
                continue
            data = label_df["amount"]
            cv = calc_cv(np.log10(data))
            study_cvs[f"{ethnicity}_{label}"] = cv, data

    with mpl.rc_context(rcParams):
        fig, axes = plt.subplots(
            2, len(study_cvs), figsize=(len(study_cvs) * 5, 2 * 5), dpi=300
        )
        fig.supxlabel("protein amount [pmol/mg(protein)]")
        for ax, label in zip(axes[:, 0], ("Data", "Simulation"), strict=True):
            ax.set_ylabel(f"frequency ({label})")
        for i, (label, (cv, data)) in enumerate(study_cvs.items()):
            bins = int(np.sqrt(len(data)))
            sampled = sample_cyp2e1(cv, fac=float(np.mean(data)), seed=i)
            _, bins_edges, _ = axes[0, i].hist(
                data, bins=bins, color="grey", edgecolor="black"
            )
            axes[1, i].hist(sampled, bins=bins_edges, color="grey", edgecolor="black")
            ethnicity, study = label.split("_")
            axes[0, i].set_title(f"{study} ({ethnicity})")

        for ax_col in axes.T:
            limits = [ax.get_xlim() for ax in ax_col]
            for ax in ax_col:
                ax.set_xlim(
                    min(lim[0] for lim in limits), max(lim[1] for lim in limits)
                )

        plt.show()
