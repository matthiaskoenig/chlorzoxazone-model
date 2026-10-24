"""Scan of the parameters which determine the metabolic ratios.

250 mg chlorzoxazone (tablet) with the CYP2E1 activity, the UGT activity, the
absorption rate and the Km of CYP2E1 scanned: the change of the metabolic ratios
at 2 hr and 4 hr and of the ratio of the AUCs relative to the values of the model.
"""

from typing import ClassVar, override

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure as FigureMPL
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


class MetabolicRatiosScan(ChlorzoxazoneSimulationExperiment):
    """Scan of the parameters which determine the metabolic ratios."""

    dose: ClassVar[int] = 250

    #: the values of the scanned parameters in the model
    base_vals: ClassVar[dict[str, Quantity]] = {
        "LI__f_cyp2e1": Q(1, "dimensionless"),
        "LI__f_GLU": Q(1, "dimensionless"),
        "GU__f_Ka_czx": Q(1, "dimensionless"),
        "LI__f_cyp2e1_Km": Q(1, "dimensionless"),
    }
    #: the scanned values relative to the values of the model
    scan_factors: ClassVar[dict[str, np.ndarray]] = {
        "LI__f_cyp2e1": np.linspace(0.5, 2, 21),
        "LI__f_GLU": np.linspace(0.5, 2, 21),
        "GU__f_Ka_czx": np.linspace(0.5, 2, 21),
        "LI__f_cyp2e1_Km": np.linspace(0.15, 5, 21),
    }

    param_names: ClassVar[dict[str, str]] = {
        "LI__f_cyp2e1": "CYP2E1 activity",
        "LI__f_GLU": "UGT activity",
        "GU__f_Ka_czx": "Absorption rate (relative)",
        "LI__f_cyp2e1_Km": "CYP2E1 Km (relative)",
    }

    def get_changes(self) -> dict[str, Quantity]:
        """Get the scanned values of the parameters.

        Returns:
            The values of every scanned parameter.
        """
        return {
            param: self.base_vals[param] * factors
            for param, factors in self.scan_factors.items()
        }

    @override
    def simulations(self) -> dict[str, Scan]:
        tcscans = {}

        for param, change in self.get_changes().items():
            tcscans[f"scan_{param}"] = Scan(
                simulation=Simulation(
                    time_unit="min",
                    end=10 * 60,
                    preinit_changes={
                        **self.default_changes(ApplicationForm.TABLET),
                        "PODOSE_czx": Q(self.dose, "mg"),
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
        param_vals = self.get_changes()
        with mpl.rc_context(rcParams):
            fig, axes = plt.subplots(2, 4, figsize=(4 * 5, 2 * 5))
            for k, param in enumerate(param_vals):
                axes[-1, k].set_xlabel(
                    f"{self.param_names[param]} [{self.base_vals[param].units:~P}]"
                )

            for ax, label in zip(
                axes[:, 0],
                [
                    "6-OH-CZX/CZX ratios\nrelative change [%]",
                    "(6-OH-CZX + Glu)/CZX ratios\nrelative change [%]",
                ],
                strict=True,
            ):
                ax.set_ylabel(label)

            for k, (param, changes) in enumerate(param_vals.items()):
                base_val = self.base_vals[param]
                # the analyses read the steps of the integrator of every point
                res = self.results[self.to_sid(f"task_scan_{param}")]
                colors = ["black", "darkgreen", "lightgreen"]
                for i, sid in enumerate([Sids.cve_czx6oh, Sids.cve_czx6oh_all]):
                    ratio_2hr = self.mr_at(res, 2, sid=sid)
                    ratio_4hr = self.mr_at(res, 4, sid=sid)
                    ratio_auc = self.calc_auc_ratio(res, sid)
                    base_idx = np.argmin(abs(changes.m - base_val.m))
                    for n, (ratios, marker, label) in enumerate(
                        zip(
                            [ratio_2hr, ratio_4hr, ratio_auc],
                            ["o", "s", "x"],
                            ["2hr MR", "4hr MR", "AUC ratio"],
                            strict=True,
                        )
                    ):
                        # the change relative to the value of the model, per draw
                        norm = (ratios - ratios[base_idx]) / ratios[base_idx] * 100
                        self.plot_band(
                            axes[i, k],
                            changes.magnitude,
                            norm,
                            LineStyle(color=colors[n], marker=marker, label=label),
                        )

            axes[0, -1].legend(frameon=False)

            for i in range(axes.shape[1]):
                bottoms = []
                tops = []
                for ax in axes[:, i]:
                    ax_min_y, ax_max_y = ax.get_ylim()
                    bottoms.append(ax_min_y)
                    tops.append(ax_max_y)
                for ax in axes[:, i]:
                    ax.set_ylim(bottom=min(bottoms), top=max(tops))

            for i, param in enumerate(param_vals):
                for ax in axes[:, i]:
                    xmin, xmax = ax.get_xlim()
                    ymin, ymax = ax.get_ylim()

                    ax.autoscale(False)

                    ax.vlines(
                        self.base_vals[param].m,
                        ymin,
                        ymax,
                        colors=["grey"],
                        linestyles=":",
                    )
                    ax.hlines(0, xmin, xmax, colors=["grey"], linestyles=":")

            return {"fig": fig}

    def calc_auc_ratio(self, xres: ScanResult, czx6oh_sid: str) -> np.ndarray:
        """Get the ratio of the AUCs of every simulation of a scan.

        Args:
            xres: the result of the scan.
            czx6oh_sid: the metabolite of the ratio.

        Returns:
            The ratio of the AUC (to infinity) of the metabolite and of
            chlorzoxazone of every simulation, the draws as the last axis.
        """
        aucs = [
            self.draw_values(
                scan_analysis(xres, sid).ds["auc_inf_obs"].transpose("dim_param", ...)
            )
            for sid in [czx6oh_sid, Sids.cpl_czx]
        ]
        return aucs[0] / aucs[1]


if __name__ == "__main__":
    MODEL.run_experiments(MetabolicRatiosScan, output_dir="test")
