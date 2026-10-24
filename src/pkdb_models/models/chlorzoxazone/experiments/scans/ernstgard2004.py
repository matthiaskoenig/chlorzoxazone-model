"""Scan of the body weight and of the dose, compared with Ernstgard2004.

Oral doses of 250, 500 and 750 mg chlorzoxazone (tablet) with the body weight
scanned from 50 to 110 kg: the Cmax of chlorzoxazone and of 6-hydroxychlorzoxazone
and the metabolic ratio (2 hr) over the dose per body weight, with the individuals
of Ernstgard2004.
"""

from typing import ClassVar, override

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from matplotlib.axes import Axes
from matplotlib.figure import Figure as FigureMPL
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from pkpdsim.metadata import ApplicationForm
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.simulation import Dimension, Scan, Simulation

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    LineStyle,
    Sids,
    metabolic_ratio,
)
from pkdb_models.models.chlorzoxazone.models import rcParams


class Ernstgard2004(ChlorzoxazoneSimulationExperiment):
    """Scan of the body weight and of the dose, compared with Ernstgard2004."""

    doses: ClassVar[list[int]] = [250, 500, 750]

    #: the datasets of the dose per body weight and of the value of a panel
    dset_labels: ClassVar[dict[str, list[str]]] = {
        "czx": ["dosing_czx", "cmax_czx"],
        "czx6oh": ["dosing_czx6oh", "cmax_czx6oh"],
        "mr": ["dosing_mr", "MR"],
    }

    #: keys of the datasets of the curated labels
    dset_keys: ClassVar[dict[str, str]] = {
        "dosing_cmax_chlorzoxazone": "dosing_czx",
        "cmax_chlorzoxazone_chlorzoxazone": "cmax_czx",
        "dosing_cmax_6-hydroxychlorzoxazone": "dosing_czx6oh",
        "cmax_6-hydroxychlorzoxazone_6-hydroxychlorzoxazone": "cmax_czx6oh",
        "dosing_metabolic ratio_6-hydroxychlorzoxazone/chlorzoxazone": "dosing_mr",
        "metabolic ratio_6-hydroxychlorzoxazone/chlorzoxazone_6-hydroxychlorzoxazone/chlorzoxazone": "MR",
    }

    @property
    def bws(self) -> np.ndarray:
        """The body weights of the scan [kg], fewer in a run over the draws."""
        return np.linspace(50, 110, 50 if self.draws is None else 11)

    @override
    def simulations(self) -> dict[str, Scan]:
        tcsims = {}

        tcsims["sim"] = Scan(
            simulation=Simulation(
                time_unit="min",
                end=10 * 60,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "HEIGHT": Q(190, "cm"),
                },
            ),
            dimensions=[
                Dimension(
                    "dim_bw",
                    values={"BW": Q(self.bws, "kg")},  # Price2003
                ),
                Dimension("dim_dose", values={"PODOSE_czx": Q(self.doses, "mg")}),
            ],
        )
        return tcsims

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig5")
        for label, label_df in df.groupby("label"):
            label = str(label)
            dsets[f"dset_{self.dset_keys[label]}"] = DataSet.from_df(
                label_df, self.ureg
            )
        return dsets

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        result = self.result_on_time_grid("task_sim")
        ds = result.ds
        order = ("dim_dose", "dim_bw", ...)

        def per_point(values: xr.DataArray) -> np.ndarray:
            """Get the values of every dose and body weight, the draws as columns."""
            array = self.draw_values(values.transpose(*order))
            return array.reshape(-1, array.shape[-1])

        ratios = per_point(metabolic_ratio(result, self.at_time(result, 2 * 60)))
        cmax_czxs = Q(
            per_point(ds[Sids.cpl_czx].max(dim="time")), result.units[Sids.cpl_czx]
        ).to("µM")
        cmax_czx6ohs = Q(
            per_point(ds[Sids.cve_czx6oh_all].max(dim="time")),
            result.units[Sids.cve_czx6oh_all],
        ).to("µM")
        # the dose per body weight of every point, sorted
        dose_per_bw = (np.array(self.doses)[:, np.newaxis] / self.bws).ravel()
        idx = np.argsort(dose_per_bw)
        doses = dose_per_bw[idx]

        dsets = {}
        for key, label_tuple in self.dset_labels.items():
            df_dose = self._datasets[f"dset_{label_tuple[0]}"]
            df_value = self._datasets[f"dset_{label_tuple[1]}"]

            dsets[key] = pd.merge(
                df_dose[["individual", "intervention", "value"]],
                df_value[["individual", "value"]],
                on="individual",
                how="left",
            )

        with plt.rc_context(rcParams):
            fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(3 * 5, 5))

            for ax, values in zip(
                (ax0, ax1, ax2),
                (cmax_czxs.magnitude, cmax_czx6ohs.magnitude, ratios),
                strict=True,
            ):
                self.plot_band(ax, doses, values[idx], LineStyle(color="black"))

            color_dict = {"CZX250": "#ffffb2", "CZX500": "#fd8d3c", "CZX750": "#b10026"}
            ax: Axes
            for ax, dset in zip([ax0, ax1, ax2], dsets.values(), strict=True):
                for intervention, df in dset.groupby("intervention"):
                    ax.scatter(
                        df["value_x"],
                        df["value_y"],
                        edgecolor="black",
                        color=color_dict[str(intervention)],
                    )

            handles: list[Line2D | Patch] = [
                Line2D(
                    [],
                    [],
                    marker="none",
                    color="black",
                    linestyle="-",
                    label="Simulation",
                ),
                Line2D(
                    [],
                    [],
                    marker="o",
                    markeredgecolor="black",
                    markerfacecolor="white",
                    linestyle="none",
                    label="individuals\nErnstgard2004",
                ),
            ]
            for intervention, color in color_dict.items():
                handles.append(Patch(color=color, label=intervention.split("CZX")[1]))

            ax2.legend(handles=handles, frameon=False)

            for ax in (ax0, ax1, ax2):
                ax.set_xlabel("dose [mg/kg (BW)]")

            ax0.set_ylabel("Cmax CZX [µM]")
            ax1.set_ylabel("Cmax 6-OH-CZX + Glu [µM]")
            ax2.set_ylabel("MR (2hr) [-]")

            fig.tight_layout()
        return {"fig": fig}


if __name__ == "__main__":
    MODEL.run_experiments(Ernstgard2004, output_dir="test")
