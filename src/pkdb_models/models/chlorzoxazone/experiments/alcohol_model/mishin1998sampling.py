"""Induction of CYP2E1 in alcoholics with sampled individuals (Mishin1998).

The simulation of `Mishin1998Induction` (induced CYP2E1 which returns to the
baseline without alcohol, 750 mg chlorzoxazone every day for 35 days) with 50
individuals of sampled CYP2E1 activity, glucuronidation and absorption:
the mean and SD of chlorzoxazone and 6-OH-CZX + CZX-Glu in plasma on day 1, 8 and
26, compared with the data of Mishin1998.

TODO: parametrize alcohol absorption and degradation with time course data
TODO: calculate 6OHCZX/CZX ratio for all and plot against data from Oneta2002
"""

from collections.abc import Sequence
from typing import override

import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure as FigureMPL
from pkpdsim.metadata import ApplicationForm
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Dimension, Scan

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.cyp2e1_amounts.helper import sample_cyp2e1
from pkdb_models.models.chlorzoxazone.experiments.alcohol_model.mishin1998induction import (
    mishin1998_datasets,
    set_broken_axes,
)
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    Sids,
)
from pkdb_models.models.chlorzoxazone.models import rcParams


class Mishin1998Sampling(ChlorzoxazoneSimulationExperiment):
    """Induction of CYP2E1 in alcoholics with sampled individuals (Mishin1998)."""

    @property
    def steps_per_timecourse(self) -> int:
        """Output steps per segment (day), fewer in a run over the draws (memory)."""
        return 200 if self.draws is None else 100

    @override
    def datasets(self) -> dict[str, DataSet]:
        return mishin1998_datasets(self)

    @override
    def simulations(self) -> dict[str, Scan]:
        czx_dose = Q(750, "mg")
        days = 35

        # induced CYP2E1 at the start, 750 mg chlorzoxazone at the start of every day
        changes = [
            {
                **self.default_changes(ApplicationForm.TABLET),
                "LI__cyp2e1": Q(3, "dimensionless"),
                "PODOSE_czx": czx_dose,
            },
            *({"PODOSE_czx": czx_dose} for _ in range(days - 1)),
        ]

        simulation = self.segments_simulation(
            durations=[24] * days,
            changes=changes,
            steps_per_segment=self.steps_per_timecourse,
        )
        return {
            "sim": Scan(
                simulation=simulation,
                dimensions=[
                    Dimension(
                        "dim_cyp2e1",
                        values={
                            "LI__f_cyp2e1": Q(
                                self.population(
                                    sample_cyp2e1(0.1, 1, seed=11, size=50), size=10
                                ),
                                "dimensionless",
                            ),
                            "LI__f_GLU": Q(
                                self.population(
                                    sample_cyp2e1(0.4, 1, seed=12, size=50), size=10
                                ),
                                "dimensionless",
                            ),
                            "GU__f_Ka_czx": Q(
                                self.population(
                                    sample_cyp2e1(0.4, 1, seed=13, size=50), size=10
                                ),
                                "dimensionless",
                            ),
                        },
                    ),
                ],
            )
        }

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        with matplotlib.rc_context(rcParams):
            return {"fig_mishin": self.fig_time_courses()}

    def fig_time_courses(self) -> FigureMPL:
        """Mean and SD of the individuals on day 1, 8 and 26 with the data.

        Returns:
            The figure, a row per substance and a column per day.
        """
        fig, [axes_czx, axes_czx6oh] = plt.subplots(2, 3, figsize=(3 * 7, 2 * 5))
        fig.subplots_adjust(wspace=0.05)

        self.setup_axes(axes_czx, axes_czx6oh)

        res = self.result_on_time_grid("task_sim")
        uinfo = res.units

        # the individuals, times the draws in a run over them
        dims = ["dim_cyp2e1", *([self.draws] if self.draws is not None else [])]
        mean = res.ds.mean(dim=dims)
        std = res.ds.std(dim=dims)
        n = int(np.prod([res.ds.sizes[d] for d in dims]))
        for sid, axes in zip(
            [Sids.cpl_czx, Sids.cve_czx6oh_all], [axes_czx, axes_czx6oh], strict=True
        ):
            for ax in axes:
                mean_sid = Q(mean[sid].values, uinfo[sid]).to("µM")
                std_sid = Q(std[sid].values, uinfo[sid]).to("µM")
                ax.plot(
                    Q(mean["time"].values, uinfo["time"]).to("hr").magnitude,
                    mean_sid.magnitude,
                    color="black",
                    label=f"Sim Mean (n={n})",
                )
                ax.fill_between(
                    x=Q(mean["time"].values, uinfo["time"]).to("hr").magnitude,
                    y1=(mean_sid - std_sid).magnitude,
                    y2=(mean_sid + std_sid).magnitude,
                    facecolor="grey",
                    alpha=0.3,
                    label=f"Sim SD (n={n})",
                )

        # the data of day 1 (day 0 of the study), day 8 and day 26: the datasets of
        # chlorzoxazone and of 6-OH-CZX, the day, the marker and the label
        data: list[tuple[list[str], int, str, str]] = [
            (
                ["Fig1_rda", "Fig2_rda"],
                1,
                "s",
                "Mishin 1998 recently drinking\nalcoholics (Data$\\pm$SD)",
            ),
            (
                ["Fig7", "Fig8"],
                8,
                "s",
                "Mishin1998 recently drinking\nalcoholics (Data$\\pm$SD)",
            ),
            (
                ["Fig1_aa", "Fig2_aa"],
                26,
                "o",
                "Mishin1998 abstinent\nalcoholics (Data$\\pm$SD)",
            ),
        ]
        for k, (ds_labels, day, marker, label) in enumerate(data):
            for ds_label, axes in zip(ds_labels, [axes_czx, axes_czx6oh], strict=True):
                dset = self._datasets[f"dset_{ds_label}"]
                axes[k].errorbar(
                    x=Q(dset["time"], dset["time_unit"].values[0]).to("hr")
                    + Q(day * 24, "hr"),
                    y=Q(dset["mean"], dset["mean_unit"].values[0]).to("µM"),
                    yerr=Q(dset["mean_sd"], dset["mean_unit"].values[0]).to("µM"),
                    marker=marker,
                    markeredgecolor="black",
                    color="orange",
                    label=label,
                )
        for axes in [axes_czx, axes_czx6oh]:
            mins = [ax.get_ylim()[0] for ax in axes]
            maxs = [ax.get_ylim()[1] for ax in axes]

            for ax in axes:
                ax.set_ylim(bottom=min(mins), top=max(maxs))

        for ax in axes_czx:
            ax.legend(frameon=False)
        return fig

    def setup_axes(self, axes_czx: Sequence[Axes], axes_czx6oh: Sequence[Axes]) -> None:
        """Set up the broken time axes of day 1, 8 and 26 and the labels.

        Args:
            axes_czx: the row of axes of chlorzoxazone.
            axes_czx6oh: the row of axes of 6-OH-CZX + CZX-Glu.
        """
        for ax in [axes_czx[0], axes_czx6oh[0]]:
            ax.set_xlim(-(0.05 * 8) + 1 * 24, 1 * 24 + 8 * 1.05)
        for ax in [axes_czx[1], axes_czx6oh[1]]:
            ax.set_xlim(-(0.05 * 8) + 8 * 24, 8 * 24 + 8 * 1.05)
        for ax in [axes_czx[2], axes_czx6oh[2]]:
            ax.set_xlim(-(0.05 * 8) + 26 * 24, 26 * 24 + 8 * 1.05)
        for axes in [axes_czx, axes_czx6oh]:
            set_broken_axes(axes)
        axes_czx6oh[0].set_ylabel(f"{self.label_czx6oh_all} [µM]")
        axes_czx[0].set_ylabel(f"{self.label_czx} [µM]")
        for ax, day in zip(axes_czx, [1, 8, 26], strict=True):
            ax.set_title(f"Simulation day {day}")
        for ax in axes_czx6oh:
            ax.set_xlabel("Time [hr]")

    @override
    def figures(self) -> dict[str, Figure]:
        name = "750 mg CZX "
        fig = Figure(
            experiment=self,
            sid="Fig_alcohol",
            num_rows=1,
            num_cols=3,
            name=name,
        )
        plots = fig.create_plots(xaxis=Axis("time", unit="day"), legend=True)

        sids = [
            Sids.cli_cyp2e1,
            Sids.cpl_czx,
            Sids.cve_czx6oh_all,
        ]

        for k, sid in enumerate(sids):
            # simulation
            plots[k].add_data(
                task="task_sim", xid="time", yid=sid, label="PO", over="dim_cyp2e1"
            )
            plots[k].set_yaxis(label=sid, unit=self.units[sid])

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Mishin1998Sampling, output_dir="test")
