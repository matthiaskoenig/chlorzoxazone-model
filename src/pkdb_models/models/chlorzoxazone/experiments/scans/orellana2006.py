"""Scan of the CYP2E1 activity, compared with Orellana2006.

500 mg chlorzoxazone (tablet) with the body weight of the mean BMI of the groups
at a height of 1.66 m and the CYP2E1 activity scanned: the metabolic ratio (2 hr)
over the CYP2E1 activity, with the groups of Orellana2006 (control, steatosis and
steatohepatitis) over their CYP2E1 content relative to the controls.
"""

from typing import ClassVar, override

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure as FigureMPL
from pkpdsim.metadata import ApplicationForm
from sbmlsim import Q
from sbmlsim.simulation import Dimension, Scan, Simulation

from pkdb_models.models.chlorzoxazone import DATA_PATH_CHLORZOXAZONE, MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    LineStyle,
)
from pkdb_models.models.chlorzoxazone.models import rcParams


class Orellana2006(ChlorzoxazoneSimulationExperiment):
    """Scan of the CYP2E1 activity, compared with Orellana2006."""

    cyp2e1: ClassVar[np.ndarray] = np.linspace(0.2, 2, 21)

    @override
    def simulations(self) -> dict[str, Scan]:
        tcsims = {}

        tcsims["sim"] = Scan(
            simulation=Simulation(
                time_unit="min",
                end=7 * 60,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "PODOSE_czx": Q(500, "mg"),
                    "BW": Q(((36 * 6 + 36 * 10 + 49 * 10) / 26) * 1.66**2, "kg"),
                },
            ),
            dimensions=[
                Dimension(
                    "dim_cyp2e1",
                    values={"LI__f_cyp2e1": Q(self.cyp2e1, "dimensionless")},
                )
            ],
        )
        return tcsims

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        xlsx_path = DATA_PATH_CHLORZOXAZONE / "Orellana2006" / "Orellana2006.xlsx"
        mrs = pd.read_excel(xlsx_path, sheet_name="Fig1", skiprows=1)
        cyp_amounts = pd.read_excel(xlsx_path, sheet_name="Fig2", skiprows=1)
        result = self.results[self.to_sid("task_sim")]
        ratios = self.mr_at(result, 2)

        colordict = {
            "control": "#636363",
            "steatosis": "#fec44f",
            "steatohepatitis": "red",
        }

        with plt.rc_context(rcParams):
            ax: Axes
            fig, ax = plt.subplots(1, 1, figsize=(7, 5))
            self.plot_band(
                ax,
                self.cyp2e1,
                ratios,
                LineStyle(color="black", marker="o", label="Sim (500 mg)"),
            )
            mr_groupby = mrs.groupby("group")
            # the CYP2E1 content relative to the controls
            control_mean = cyp_amounts[cyp_amounts["group"] == "control"][
                "mean"
            ].values[0]
            for label, df in cyp_amounts.groupby("group"):
                label = str(label)
                cyp_norm = df["mean"] / control_mean
                sd_norm = df["sd"] / control_mean
                mr_df = mr_groupby.get_group(label)
                n = df["count"].values[0]
                ax.errorbar(
                    x=cyp_norm,
                    xerr=sd_norm,
                    y=mr_df["mean"],
                    yerr=mr_df["sd"],
                    marker="o",
                    markersize=8,
                    color=colordict[label],
                    markeredgecolor="black",
                    linestyle="none",
                    label=rf"{label} (mean$\pm$SD, n={n})",
                )

            ax.legend(frameon=False)
            ax.set_xlabel("CYP2E1 activity [-]")
            ax.set_ylabel("Metabolic ratio (2hr) [-]")
            ax.set_title("Orellana2006")
            return {"fig": fig}


if __name__ == "__main__":
    MODEL.run_experiments(Orellana2006, output_dir="test")
