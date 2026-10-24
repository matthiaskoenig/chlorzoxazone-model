"""Scan of the CYP2E1 activity and of the degree of cirrhosis.

250 mg chlorzoxazone (tablet) with the CYP2E1 activity scanned against the degree
of cirrhosis: the metabolic ratio (2 hr), AUC, clearance and elimination rate of
chlorzoxazone, as arrays over both and over the CYP2E1 activity for the
Child-Pugh classes of cirrhosis.
"""

from collections.abc import Collection
from typing import ClassVar, override

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from matplotlib.axes import Axes
from matplotlib.figure import Figure as FigureMPL
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from pkpdsim.metadata import ApplicationForm
from sbmlsim import Q
from sbmlsim.result import ScanResult
from sbmlsim.simulation import Dimension, Scan, Simulation

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.chlorzoxazone_pk import scan_analysis
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    LineStyle,
    Sids,
    metabolic_ratio,
)
from pkdb_models.models.chlorzoxazone.models import rcParams


class CirrhosisScan(ChlorzoxazoneSimulationExperiment):
    """Scan of the CYP2E1 activity and of the degree of cirrhosis."""

    #: the points of the grid of a scan, fewer in a run over the draws
    points: ClassVar[int] = 101
    points_over_draws: ClassVar[int] = 21

    auc_unit: ClassVar[str] = "min*mmol/L"
    kel_unit: ClassVar[str] = "1/hr"
    cl_unit: ClassVar[str] = "L/min"

    @property
    def cirrhosis_values(self) -> np.ndarray:
        """The degrees of cirrhosis of the scan."""
        return np.linspace(0, 0.9, self._n_points)

    @property
    def cyp2e1_values(self) -> np.ndarray:
        """The CYP2E1 activities of the scan."""
        return np.linspace(0.5, 4, self._n_points)

    @property
    def _n_points(self) -> int:
        return self.points if self.draws is None else self.points_over_draws

    @property
    def _steps(self) -> int:
        """The output steps of 20 hr, fewer in a run over the draws (memory)."""
        return 1000 if self.draws is None else 200

    @property
    def cpt_cyp2e1_values(self) -> np.ndarray:
        """The CYP2E1 activities of the scan of the Child-Pugh classes, every fifth."""
        return self.cyp2e1_values[::5]

    def calc_array(self, values: xr.DataArray) -> np.ndarray:
        """Get the values of every simulation of the scan of cirrhosis and CYP2E1.

        Args:
            values: the values of the result, e.g. at a time.

        Returns:
            The values, cirrhosis in the rows, the CYP2E1 activity in the
            columns and the draws as the last axis.
        """
        return self.draw_values(values.transpose("dim_cirrhosis", "dim_cyp2e1", ...))

    @staticmethod
    def calc_effective_activity(
        cirrhosis_values: Collection[float], cyp2e1_values: Collection[float]
    ) -> np.ndarray:
        """Get the effective CYP2E1 activity, reduced by the cirrhosis.

        Args:
            cirrhosis_values: the degrees of cirrhosis.
            cyp2e1_values: the CYP2E1 activities.

        Returns:
            The effective activity, cirrhosis in the rows and the CYP2E1 activity
            in the columns.
        """
        arr = np.empty(shape=(len(cirrhosis_values), len(cyp2e1_values)))
        for a, c_val in enumerate(cirrhosis_values):
            for b, cyp_val in enumerate(cyp2e1_values):
                arr[a, b] = (1 - c_val) ** 2 * cyp_val
        return arr

    @override
    def simulations(self) -> dict[str, Scan]:
        tcscans = {}

        tcscans["scan"] = Scan(
            simulation=Simulation(
                time_unit="min",
                end=20 * 60,
                steps=self._steps,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "PODOSE_czx": Q(250, "mg"),
                },
            ),
            dimensions=[
                Dimension(
                    "dim_cyp2e1",
                    values={"LI__f_cyp2e1": Q(self.cyp2e1_values, "dimensionless")},
                ),
                Dimension(
                    "dim_cirrhosis",
                    values={"f_cirrhosis": Q(self.cirrhosis_values, "dimensionless")},
                ),
            ],
        )

        tcscans["CPT"] = Scan(
            simulation=Simulation(
                time_unit="min",
                end=20 * 60,
                steps=self._steps,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "PODOSE_czx": Q(250, "mg"),
                },
            ),
            dimensions=[
                Dimension(
                    "dim_cyp2e1",
                    values={"LI__f_cyp2e1": Q(self.cpt_cyp2e1_values, "dimensionless")},
                ),
                Dimension(
                    "dim_cirrhosis",
                    values={
                        "f_cirrhosis": Q(
                            list(self.cirrhosis_map.values()), "dimensionless"
                        )
                    },
                ),
            ],
        )

        return tcscans

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        figures = {}
        figures.update(self.fig_cyp2e1_cpt_score())
        figures.update(self.fig_cyp2e1_cirrhosis_array())
        return figures

    def fig_cyp2e1_cpt_score(self) -> dict[str, FigureMPL]:
        """Get the parameters over the CYP2E1 activity for the Child-Pugh classes.

        Returns:
            The figures of the metabolic ratio, AUC, clearance, elimination rate
            and effective CYP2E1 activity.
        """
        res = self.result_on_time_grid("task_CPT")

        # metabolic ratio
        arr = self.calc_array(metabolic_ratio(res, self.at_time(res, 2 * 60)))
        fig_cpt_mr = self.plot_cpt(arr, "MR (2hr)", "-")

        pk_arrays = self.calc_pk_arrays(res, 250)

        # auc
        fig_cpt_auc_inf = self.plot_cpt(pk_arrays["auc_last"], "AUC", self.auc_unit)

        # clearance
        fig_cpt_cl = self.plot_cpt(pk_arrays["cl_f"], "Clearance", self.cl_unit)

        # kel
        fig_cpt_kel = self.plot_cpt(pk_arrays["lambda_z"], "kel", self.kel_unit)

        # effective activity
        eff_arr = self.calc_effective_activity(
            list(self.cirrhosis_map.values()), self.cpt_cyp2e1_values
        )[..., np.newaxis]
        fig_eff_activity = self.plot_cpt(eff_arr, "Effective CYP2E1 activity", "-")

        return {
            "fig_cpt_mr": fig_cpt_mr,
            "fig_cpt_auc_inf": fig_cpt_auc_inf,
            "fig_cpt_cl": fig_cpt_cl,
            "fig_cpt_kel": fig_cpt_kel,
            "fig_cpt_eff_act": fig_eff_activity,
        }

    def fig_cyp2e1_cirrhosis_array(self) -> dict[str, FigureMPL]:
        """Get the parameters over the CYP2E1 activity and the degree of cirrhosis.

        Returns:
            The figures of the metabolic ratio, AUC, clearance, elimination rate
            and effective CYP2E1 activity.
        """
        res = self.result_on_time_grid("task_scan")

        # metabolic ratio
        arr = self.calc_array(metabolic_ratio(res, self.at_time(res, 2 * 60)))
        fig_mr = self.plot_array(arr, "MR (2hr)", "-")

        pk_arrays = self.calc_pk_arrays(res, 250)

        # auc
        fig_auc_inf = self.plot_array(pk_arrays["auc_last"], "AUC", self.auc_unit)

        # clearance
        fig_cl = self.plot_array(pk_arrays["cl_f"], "Clearance", self.cl_unit)

        # kel
        fig_kel = self.plot_array(pk_arrays["lambda_z"], "kel", self.kel_unit)

        # effective activity
        eff_arr = self.calc_effective_activity(
            self.cirrhosis_values, self.cyp2e1_values
        )[..., np.newaxis]
        fig_eff_act = self.plot_array(eff_arr, "Effective CYP2E1 activity", "-")

        return {
            "fig_mr": fig_mr,
            "fig_auc_inf": fig_auc_inf,
            "fig_cl": fig_cl,
            "fig_kel": fig_kel,
            "fig_eff_act": fig_eff_act,
        }

    def plot_array(self, arr: np.ndarray, label: str, unit: str) -> FigureMPL:
        """Plot a parameter over the CYP2E1 activity and the degree of cirrhosis.

        Args:
            arr: the values, cirrhosis in the rows, CYP2E1 in the columns and
                the draws as the last axis.
            label: the label of the parameter.
            unit: the unit of the parameter.

        Returns:
            The figure, colored relative to the value of the model (no cirrhosis,
            CYP2E1 activity 1); the median of the draws in a run over them.
        """
        arr = self.band(arr)[1]
        with mpl.rc_context(rcParams):
            min_arr, max_arr = np.min(arr), np.max(arr)

            base_idx_cirrhosis = np.argmin(abs(self.cirrhosis_values - 0))
            base_idx_cyp2e1 = np.argmin(abs(self.cyp2e1_values - 1))

            fig: FigureMPL
            ax: Axes
            fig, ax = plt.subplots(1, 1, figsize=(6, 5))
            cmap = mpl.colormaps["seismic"].with_extremes(bad="grey")
            base = arr[base_idx_cirrhosis, base_idx_cyp2e1]
            norm = mpl.colors.CenteredNorm(vcenter=base)

            ax.matshow(arr, origin="lower", cmap=cmap, norm=norm)

            cs_base = ax.contour(arr, [base], origin="lower", colors="black")
            cs = ax.contour(
                arr,
                10,
                origin="lower",
                linestyles="dashed",
                colors="black",
                linewidths=0.5,
            )

            # every level is labeled
            ax.clabel(cs, inline=True, fmt=lambda x: f"{x:.2f}")
            ax.clabel(cs_base, inline=True, fmt=lambda x: f"{x:.2f}")

            axins = inset_axes(
                ax, width="100%", height="5%", loc="upper center", borderpad=-4.5
            )
            cb = fig.colorbar(
                mappable=mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                ax=ax,
                cax=axins,
                orientation="horizontal",
            )
            # the gradient as vector cells: matplotlib rasterizes it into an
            # embedded image, which some SVG viewers do not show; the edges of
            # the cells in their color close the seams between them
            if cb.solids is not None:
                cb.solids.set_rasterized(False)
                cb.solids.set_edgecolor("face")
            cb.set_label(label=f"{label} [{unit}]", size=15, weight="bold")
            cb.ax.set_xlim(left=min_arr, right=max_arr)
            # five ticks, so that the labels do not overlap
            cb.ax.xaxis.set_major_locator(MaxNLocator(nbins=5))

            ax.set_xlabel("CYP2E1 activity [-]")
            ax.set_ylabel("Cirrhosis [-]")
            ax.xaxis.set_ticks_position("bottom")
            # six ticks per axis
            step = (self._n_points - 1) // 5
            ax.xaxis.set_ticks(
                range(len(self.cyp2e1_values))[::step],
                [f"{x:.2f}" for x in self.cyp2e1_values[::step]],
            )
            ax.yaxis.set_ticks(
                range(len(self.cirrhosis_values))[::step],
                [f"{x:.2f}" for x in self.cirrhosis_values[::step]],
            )

            return fig

    def plot_cpt(self, arr: np.ndarray, label: str, unit: str) -> FigureMPL:
        """Plot a parameter over the CYP2E1 activity, a line per Child-Pugh class.

        Args:
            arr: the values, the classes in the rows, CYP2E1 in the columns and
                the draws as the last axis.
            label: the label of the parameter.
            unit: the unit of the parameter.

        Returns:
            The figure.
        """
        with mpl.rc_context(rcParams):
            colors = ["black", "#fdcc8a", "#fc8d59", "#d7301f"]
            # the Child-Pugh classes of the rows, see `cirrhosis_map`
            labels = list(self.cirrhosis_map)
            ax: Axes
            fig, ax = plt.subplots(1, 1, figsize=(5, 5))
            ax.set_ylabel(f"{label} [{unit}]")
            ax.set_xlabel("CYP2E1 activity [-]")
            ax.axvline(1, linestyle="--", color="grey")
            for i in range(arr.shape[0]):
                self.plot_band(
                    ax,
                    self.cpt_cyp2e1_values,
                    arr[i],
                    LineStyle(
                        color=colors[i],
                        marker="o",
                        markeredgecolor="black",
                        label=labels[i],
                    ),
                )
            ax.legend(frameon=False)

            return fig

    def calc_pk_arrays(self, res: ScanResult, dose: float) -> dict[str, np.ndarray]:
        """Clearance, AUC and elimination rate of every simulation of the scan.

        The pharmacokinetic parameters of all simulations are calculated at
        once (`scan_analysis`).

        Args:
            res: the result of a scan of cirrhosis and CYP2E1 on its time grid.
            dose: the oral dose of chlorzoxazone in mg.

        Returns:
            The parameters, cirrhosis in the rows, CYP2E1 in the columns and
            the draws as the last axis.
        """
        result = scan_analysis(res, Sids.cpl_czx, dose=Q(dose, "mg") / self.Mr.czx)
        units = {
            "cl_f": self.cl_unit,
            "auc_last": self.auc_unit,
            "lambda_z": self.kel_unit,
        }
        return {
            key: Q(
                self.draw_values(
                    result.ds[key].transpose("dim_cirrhosis", "dim_cyp2e1", ...)
                ),
                result.units(key),
            ).m_as(unit)
            for key, unit in units.items()
        }


if __name__ == "__main__":
    MODEL.run_experiments(CirrhosisScan, output_dir="test")
