"""Scan of the CYP2E1 activity and of the Km of CYP2E1 for three oral doses.

Oral doses of 250, 500 and 750 mg chlorzoxazone (tablet) with the CYP2E1 activity
and the Km of the hydroxylation by CYP2E1 scanned from 0.1 to 10 times their
values in the model: the timecourses and the metabolic ratio (2 hr), AUC,
elimination rate and clearance of chlorzoxazone.
"""

from typing import ClassVar, override

import matplotlib as mpl
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure as FigureMPL
from matplotlib.lines import Line2D
from matplotlib.ticker import ScalarFormatter
from pkpdsim.metadata import ApplicationForm
from sbmlsim import Q
from sbmlsim.result import ScanResult
from sbmlsim.simulation import Dimension, Scan, Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.chlorzoxazone_pk import scan_analysis
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    LineStyle,
    Sids,
)
from pkdb_models.models.chlorzoxazone.models import rcParams


class PKPScan(ChlorzoxazoneSimulationExperiment):
    """Scan of the CYP2E1 activity and of the Km of CYP2E1 for three oral doses."""

    doses: ClassVar[list[int]] = [250, 500, 750]

    #: the values of the scanned parameters in the model
    base_vals: ClassVar[dict[str, Quantity]] = {
        "LI__f_cyp2e1": Q(1, "dimensionless"),
        "LI__f_cyp2e1_Km": Q(1, "dimensionless"),
    }
    #: the scanned values relative to the values of the model
    scan_factors: ClassVar[dict[str, np.ndarray]] = {
        "LI__f_cyp2e1": np.logspace(-1, 1, 21),
        "LI__f_cyp2e1_Km": np.logspace(-1, 1, 21),
    }

    param_names: ClassVar[dict[str, str]] = {
        "LI__f_cyp2e1": "CYP2E1 activity [-]",
        "LI__f_cyp2e1_Km": "CYP2E1 Km (relative) [-]",
    }

    def get_changes(self) -> dict[str, Quantity]:
        """Get the scanned values of the parameters.

        A run over the draws scans every second value, on a shorter time grid
        which still has the terminal phase (memory).

        Returns:
            The values of every scanned parameter.
        """
        step = 1 if self.draws is None else 2
        return {
            param: self.base_vals[param] * factors[::step]
            for param, factors in self.scan_factors.items()
        }

    @override
    def simulations(self) -> dict[str, Scan]:
        tcscans = {}
        end_hr = 1000 if self.draws is None else 72
        for param, change in self.get_changes().items():
            for dose in self.doses:
                tcscans[f"scan_{param}_{dose}"] = Scan(
                    simulation=Simulation(
                        time_unit="min",
                        end=end_hr * 60,
                        preinit_changes={
                            **self.default_changes(ApplicationForm.TABLET),
                            "PODOSE_czx": Q(dose, "mg"),
                        },
                    ),
                    dimensions=[
                        Dimension(
                            "dim_param",
                            values={param: change},
                        ),
                    ],
                )
        return tcscans

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        with mpl.rc_context(rcParams):
            fig, axes = plt.subplots(4, 4, figsize=(4 * 7, 4 * 5))
            ax: Axes
            for row in axes[:, [1, 3]]:
                for ax in row:
                    ax.set_xscale("log")
                    ax.set_yscale("log")

            for row in axes[:, [0, 2]]:
                for ax in row:
                    ax.set_yscale("log")
            self.figure_time_course_scan(axes[:, [0, 2]])
            self.figure_pkp_scan(axes[:, [1, 3]])
            figs = {"fig_pkp_scan": fig}
            figs.update(self.fig_supplementary())
            return figs

    def figure_pkp_scan(self, axes: np.ndarray) -> None:
        """Plot the pharmacokinetic parameters over the scanned values.

        Args:
            axes: the axes, a row per parameter and a column per scanned parameter.
        """
        param_vals = self.get_changes()
        colors = ["#c7e9c0", "#74c476", "#006d2c"]
        ylabels: list[str] = []
        for k, param in enumerate(param_vals):
            axes[-1, k].set_xlabel(self.param_names[param])
            for i, dose in enumerate(self.doses):
                # the analyses read the steps of the integrator of every point
                res = self.results[self.to_sid(f"task_scan_{param}_{dose}")]

                mr_2hr = self.mr_at(res, 2)
                pks = self.calc_pk_parameters(res, dose)
                aucs = pks["auc_last"]
                kels = pks["lambda_z"].to("1/hr")
                clearance = pks["cl_f"]
                # the units of the last dose label the rows
                ylabels = [
                    "Metabolic ratio (2hr) [-]",
                    f"AUC [{aucs.units:~P}]",
                    f"kel [{kels.units:~P}]",
                    f"Clearance [{clearance.units:~P}]",
                ]
                for row, values in enumerate(
                    [mr_2hr, aucs.magnitude, kels.magnitude, clearance.magnitude]
                ):
                    self.plot_band(
                        axes[row, k],
                        param_vals[param].magnitude,
                        values,
                        LineStyle(
                            color=colors[i],
                            marker="o",
                            label=f"{dose} mg" if row == 0 else None,
                            markeredgecolor="black",
                        ),
                    )

        for k, label in enumerate(ylabels):
            for ax in axes[k, :]:
                ax.set_ylabel(label)
                if k == 2:
                    formatter = ScalarFormatter()
                    ax.yaxis.set_minor_formatter(formatter)

        axes[0, 0].legend(frameon=False, loc="upper left")

        for i, param in enumerate(param_vals):
            for ax in axes[:, i]:
                ymin, ymax = ax.get_ylim()

                ax.autoscale(False)

                ax.vlines(
                    self.base_vals[param].m,
                    ymin,
                    ymax,
                    colors=["grey"],
                    linestyles=":",
                )

    def fig_supplementary(self) -> dict[str, FigureMPL]:
        """Timecourses of every dose, a figure per scanned parameter.

        Returns:
            The figures of the scans of the CYP2E1 activity (`vmax`) and of the
            Km (`km`).
        """
        (fig1, axes1), (fig2, axes2) = [
            plt.subplots(4, 3, figsize=(3 * 7, 4 * 5)) for _ in range(2)
        ]
        for axes in axes1, axes2:
            for ax in axes.flatten():
                ax.set_yscale("log")
        for i, dose in enumerate([250, 500, 750]):
            self.figure_time_course_scan(
                np.vstack([axes1[:, i], axes2[:, i]]).T, dose=dose
            )

        for axes in axes1, axes2:
            for row in axes:
                max_y = max([ax.get_ylim()[1] for ax in row])
                for ax in row:
                    ax.set_ylim(top=max_y)

        return {"vmax": fig1, "km": fig2}

    def figure_time_course_scan(self, axes: np.ndarray, dose: int = 250) -> None:
        """Plot the timecourses of the scans of a dose.

        Args:
            axes: the axes, a row per selection and a column per scanned parameter.
            dose: the dose in mg.
        """
        units = {
            Sids.cpl_czx: "µM",
            Sids.cve_czx6oh: "µM",
            Sids.cve_czx6oh_all: "µM",
            Sids.aurine_czxoglu: "percent",
        }
        param_vals = self.get_changes()
        sids = [Sids.cpl_czx, Sids.cve_czx6oh, Sids.cve_czx6oh_all, Sids.aurine_czxoglu]

        cmap = mpl.colormaps["coolwarm"]
        labels = (
            self.label_czx,
            self.label_czx6oh,
            self.label_czx6oh_all,
            self.label_czxoglu_urine,
        )
        for i, sid in enumerate(sids):
            for ax in axes[i]:
                if sid == Sids.aurine_czxoglu:
                    ax.set_ylabel("Urinary recovery [%]")
                else:
                    ax.set_ylabel(f"{labels[i]} [{units[sid]}]")
        for k, param in enumerate(param_vals):
            change = param_vals[param]
            base_val = self.base_vals[param]
            norm = mplc.TwoSlopeNorm(
                vcenter=base_val.m, vmin=min(change.m), vmax=max(change.m)
            )
            axes[-1, k].set_xlabel("Time [hr]")

            res = self.results[f"task_scan_{param}_{dose}"]
            base_idx = np.argmin(np.abs((change - base_val).m))
            # the colorbar is drawn once per selection, on top of each other
            cb_axes: list[Axes] = []
            for i, sid in enumerate(sids):
                for p_value in range(len(change.m)):
                    is_base = p_value == base_idx
                    if sid == Sids.aurine_czxoglu:
                        # the recovery in percent of the dose
                        t, *band = self.timecourse_band(
                            res, sid, ("hr", "mmole"), point={"dim_param": p_value}
                        )
                        factor = (
                            (Q(1, "mmole") / (Q(dose, "mg") / self.Mr.czx))
                            .to("percent")
                            .magnitude
                        )
                        band = [b * factor for b in band]
                    else:
                        t, *band = self.timecourse_band(
                            res, sid, ("hr", units[sid]), point={"dim_param": p_value}
                        )
                    # the first 10 hr, the band of the draws of the baseline
                    mask = t <= 10
                    lower, median, upper = (b[mask] for b in band)
                    if not is_base:
                        lower = upper = median
                    self.plot_bands(
                        axes[i, k],
                        t[mask],
                        lower,
                        median,
                        upper,
                        style=LineStyle(
                            color="black" if is_base else cmap(norm(change.m[p_value])),
                            zorder=2 if is_base else 1,
                        ),
                    )

                cb_ax = axes[0, k].inset_axes([0.05, 1.10, 0.9, 0.07])
                cb_ax.set_title(self.param_names[param])
                cb = plt.colorbar(
                    mappable=mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                    cax=cb_ax,
                    ax=axes[0, k],
                    orientation="horizontal",
                )
                # the gradient as vector cells: matplotlib rasterizes it into an
                # embedded image, which some SVG viewers do not show; the edges of
                # the cells in their color close the seams between them
                if cb.solids is not None:
                    cb.solids.set_rasterized(False)
                    cb.solids.set_edgecolor("face")
                cb.ax.set_xscale("log")
                cb_axes.append(cb_ax)
            ymin, ymax = cb_axes[-1].get_ylim()

            cb_axes[-1].autoscale(False)

            axes[0, 0].legend(
                handles=[
                    Line2D([], [], linestyle="-", color="black", label="baseline")
                ],
                frameon=False,
            )

            cb_axes[-1].vlines(base_val.m, ymin, ymax, colors=["black"], linestyles="-")

        for i in range(axes.shape[0]):
            bottoms = []
            tops = []
            for ax in axes[i, :]:
                ax_min_y, ax_max_y = ax.get_ylim()
                bottoms.append(ax_min_y)
                tops.append(ax_max_y)
            for ax in axes[i, :]:
                ax.set_ylim(bottom=min(bottoms), top=max(tops))

    def calc_pk_parameters(self, xres: ScanResult, dose: float) -> dict[str, Quantity]:
        """Get the pharmacokinetic parameters of every simulation of a scan.

        Args:
            xres: the result of the scan.
            dose: the oral dose of chlorzoxazone in mg.

        Returns:
            The pharmacokinetic parameters of chlorzoxazone, every point of the
            scan in the rows and the draws in the columns.
        """
        result = scan_analysis(xres, Sids.cpl_czx, dose=Q(dose, "mg") / self.Mr.czx)
        return {
            key: Q(
                self.draw_values(result.ds[key].transpose("dim_param", ...)),
                result.units(key),
            )
            for key in ["auc_last", "lambda_z", "cl_f"]
        }


if __name__ == "__main__":
    MODEL.run_experiments(PKPScan, output_dir="test")
