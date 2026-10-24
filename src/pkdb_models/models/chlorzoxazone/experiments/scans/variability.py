"""Variability of chlorzoxazone from the CYP2E1 activity and the absorption.

250 mg chlorzoxazone (tablet) with the CYP2E1 activity sampled from a log-normal
distribution (coefficient of variation 0.4), alone and together with the absorption
rate (coefficient of variation 0.8): the distribution of chlorzoxazone over time,
with the individuals of DeVries1994.
"""

from typing import ClassVar, override

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure as FigureMPL
from pkpdsim.metadata import ApplicationForm
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.simulation import Dimension, Scan, Simulation

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    Sids,
)
from pkdb_models.models.chlorzoxazone.experiments.scans.ethnicity import (
    sample_log_normal,
)
from pkdb_models.models.chlorzoxazone.models import rcParams


class VariabilitySampling(ChlorzoxazoneSimulationExperiment):
    """Variability of chlorzoxazone from the CYP2E1 activity and the absorption."""

    #: the figures of the individual timecourses of DeVries1994
    fig_ids: ClassVar[list[str]] = ["Fig1", "Fig2"]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in self.fig_ids:
            df = self.load_dataframe(fig_id, study="DeVries1994")
            for label, df_label in df.groupby("individual"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion("value", 1 / self.Mr.czx)
                dsets[f"Timecourse_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Scan]:
        tcscans = {}

        tcscans["scan_f_cyp2e1"] = Scan(
            simulation=Simulation(
                time_unit="min",
                end=10 * 60,
                # a coarse grid for the samples: the steps of the
                # integrator of every sample need too much memory
                steps=50,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "PODOSE_czx": Q(250, "mg"),
                },
            ),
            dimensions=[
                Dimension(
                    "dim_cyp2e1",
                    values={
                        "LI__f_cyp2e1": Q(
                            self.population(
                                sample_log_normal(cv=0.4, mean=1, seed=5), size=50
                            ),
                            "dimensionless",
                        )
                    },
                ),
            ],
        )

        tcscans["scan_f_kabs"] = Scan(
            simulation=Simulation(
                time_unit="min",
                end=10 * 60,
                # a coarse grid for the samples: the steps of the
                # integrator of every sample need too much memory
                steps=50,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "PODOSE_czx": Q(250, "mg"),
                },
            ),
            dimensions=[
                Dimension(
                    "dim_kabs",
                    values={
                        "GU__f_Ka_czx": Q(
                            self.population(
                                sample_log_normal(cv=0.8, mean=1, seed=6), size=50
                            ),
                            "dimensionless",
                        ),
                        "LI__f_cyp2e1": Q(
                            self.population(
                                sample_log_normal(cv=0.4, mean=1, seed=7), size=50
                            ),
                            "dimensionless",
                        ),
                    },
                ),
            ],
        )

        return tcscans

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return self.fig_dose_cyp2e1_sampling()

    def fig_dose_cyp2e1_sampling(self) -> dict[str, FigureMPL]:
        """Boxplots over time of chlorzoxazone of the scans, with the individuals.

        Returns:
            A figure per scan, of the CYP2E1 activity (`cyp2e1`) and of the CYP2E1
            activity and the absorption rate (`kabs`).
        """
        figures = {}
        for key in ["cyp2e1", "kabs"]:
            with mpl.rc_context(rcParams):
                f, axes = plt.subplots(1, 2, figsize=(2 * 5, 5), dpi=300)
                for ax in axes:
                    ax.set_xlabel("time [hr]")

                axes[0].set_ylabel(f"CZX plasma conc. [{self.units[Sids.cpl_czx]}]")

                axes[0].set_title("Simulation")
                axes[1].set_title("DeVries1994")

                result = self.result_on_time_grid(f"task_scan_f_{key}")
                uinfo = result.units
                times = result.ds["time"]

                width = Q(times[1].values - times[0].values, uinfo[Sids.time]).to(
                    self.units[Sids.time]
                )
                for t in times:
                    res_for_t = result.ds.sel(time=t)

                    sid = Sids.cpl_czx
                    ax: Axes = axes[0]
                    # the individuals (times the draws in a run over them)
                    ax.boxplot(
                        x=Q(res_for_t[sid].values.ravel(), uinfo[sid])
                        .to(self.units[sid])
                        .magnitude,
                        positions=Q([t], uinfo[Sids.time])
                        .to(self.units[Sids.time])
                        .magnitude,
                        manage_ticks=False,
                        widths=[width.magnitude],
                        patch_artist=True,
                        showfliers=True,
                        flierprops={"markersize": 1, "alpha": 0.3},
                    )

                for dset in self._datasets.values():
                    axes[1].plot(
                        Q(dset["time"].values, dset["time_unit"].values[0])
                        .to("hr")
                        .magnitude,
                        Q(dset["value"].values, dset["value_unit"].values[0])
                        .to("µM")
                        .magnitude,
                        color="black",
                        linestyle="-",
                        marker="o",
                        alpha=0.5,
                    )

                max_ys = [ax.get_ylim()[1] for ax in axes]
                min_ys = [ax.get_ylim()[0] for ax in axes]
                max_xs = [ax.get_xlim()[1] for ax in axes]
                min_xs = [ax.get_xlim()[0] for ax in axes]

                for ax in axes:
                    ax.set_ylim(bottom=min(min_ys), top=max(max_ys))
                    ax.set_xlim(left=min(min_xs), right=max(max_xs))

                f.tight_layout()
                figures[key] = f
        return figures


if __name__ == "__main__":
    MODEL.run_experiments(VariabilitySampling, output_dir="test")
