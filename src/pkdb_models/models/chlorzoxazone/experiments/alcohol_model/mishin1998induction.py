"""Induction of CYP2E1 in alcoholics, compared with Mishin1998.

Mishin1998 measured chlorzoxazone (750 mg) in recently drinking alcoholics on day 0
and after 8 days of abstinence, and in alcoholics which were abstinent for 25.8
days on average. The simulation starts with an induced CYP2E1 (3-fold) which
returns to the baseline without alcohol, with 750 mg chlorzoxazone every day for
35 days: chlorzoxazone and 6-OH-CZX + CZX-Glu in plasma on day 1, 8 and 26,
compared with the data.

TODO: parametrize alcohol absorption and degradation with time course data
TODO: calculate 6OHCZX/CZX ratio for all and plot against data from Oneta2002
"""

from collections.abc import Sequence
from typing import Any, ClassVar, override

import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.dates import DayLocator, HourLocator
from matplotlib.figure import Figure as FigureMPL
from pkpdsim.metadata import ApplicationForm
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.simulation import Simulation

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    HelperMapping,
    LineStyle,
    Sids,
    required,
)
from pkdb_models.models.chlorzoxazone.models import rcParams


def mishin1998_datasets(
    experiment: ChlorzoxazoneSimulationExperiment,
) -> dict[str, DataSet]:
    """Get the datasets of Mishin1998.

    Chlorzoxazone (Fig1, Fig7) and 6-OH-CZX (Fig2, Fig8) of the recently drinking
    alcoholics (rda) on day 0 and after 8 days of abstinence (Fig7, Fig8), and of
    the abstinent alcoholics (aa).

    Args:
        experiment: the experiment which loads the data.

    Returns:
        The datasets by key.
    """
    fig_meta = {
        "Fig1_rda": HelperMapping(
            id="Fig1",
            mr=experiment.Mr.czx,
            dset_label="Fig1_alcoholic_drinking",
            plot_ylabel=experiment.label_czx,
            plot_legend_label=r"Recently drinking alcoholics",
            yid=Sids.cpl_czx,
            unit="µM",
            task_id="rda",
        ),
        "Fig1_aa": HelperMapping(
            id="Fig1",
            mr=experiment.Mr.czx,
            dset_label="Fig1_alcoholic_abstinent",
            plot_ylabel=experiment.label_czx,
            plot_legend_label=r"abstinent alcoholics",
            yid=Sids.cpl_czx,
            unit="µM",
            task_id="aa",
        ),
        "Fig2_rda": HelperMapping(
            id="Fig2",
            mr=experiment.Mr.czx6oh,
            dset_label="Fig2_alcoholic_drinking",
            plot_ylabel=experiment.label_czx6oh_all,
            plot_legend_label=r"Recently drinking alcoholics",
            yid=Sids.cve_czx6oh_all,
            unit="µM",
            task_id="rda",
        ),
        "Fig2_aa": HelperMapping(
            id="Fig2",
            mr=experiment.Mr.czx6oh,
            dset_label="Fig2_alcoholic_abstinent",
            plot_ylabel=experiment.label_czx6oh_all,
            plot_legend_label=r"abstinent alcoholics",
            yid=Sids.cve_czx6oh_all,
            unit="µM",
            task_id="aa",
        ),
        "Fig7": HelperMapping(
            id="Fig7",
            mr=experiment.Mr.czx,
            plot_ylabel=experiment.label_czx,
            plot_legend_label=r"after 8-day abstinence",
            yid=Sids.cpl_czx,
            unit="µM",
            dset_label="Fig7_alcoholic_drinking_stopped",
            task_id="rda_abstinent",
        ),
        "Fig8": HelperMapping(
            id="Fig8",
            mr=experiment.Mr.czx6oh,
            plot_ylabel=experiment.label_czx6oh_all,
            plot_legend_label=r"after 8-day abstinence",
            yid=Sids.cve_czx6oh_all,
            unit="µM",
            dset_label="Fig8_alcoholic_drinking_stopped",
            task_id="rda_abstinent",
        ),
    }

    dsets = {}
    for fig_id, hm in fig_meta.items():
        df = experiment.load_dataframe(required(hm.id), study="Mishin1998")
        dset = DataSet.from_df(
            df[df["label"] == required(hm.dset_label)], experiment.ureg
        )
        dset.unit_conversion("mean", 1 / required(hm.mr))
        dsets[f"dset_{fig_id}"] = dset

    return dsets


def set_broken_axes(axes: Sequence[Axes]) -> None:
    """Join a row of three axes to a broken x axis.

    The spines between the axes are hidden and slanted lines mark the breaks.

    Args:
        axes: the row of axes.
    """
    axes[1].spines.left.set_visible(False)
    axes[2].spines.left.set_visible(False)
    axes[0].spines.right.set_visible(False)
    axes[1].spines.right.set_visible(False)
    axes[1].set_yticks([])
    axes[2].set_yticks([])

    d = 0.5  # proportion of vertical to horizontal extent of the slanted line
    kwargs: dict[str, Any] = {
        "marker": [(-d, -1), (d, 1)],
        "markersize": 12,
        "linestyle": "none",
        "color": "k",
        "mec": "k",
        "mew": 1,
        "clip_on": False,
    }
    axes[0].plot([1, 1], [1, 0], transform=axes[0].transAxes, **kwargs)
    axes[1].plot([0, 1, 0, 1], [0, 0, 1, 1], transform=axes[1].transAxes, **kwargs)
    axes[2].plot([0, 0], [0, 1], transform=axes[2].transAxes, **kwargs)


class Mishin1998Induction(ChlorzoxazoneSimulationExperiment):
    """Induction of CYP2E1 in alcoholics, compared with Mishin1998."""

    #: output steps per segment (day) of the simulation
    steps_per_timecourse: ClassVar[int] = 200

    @override
    def datasets(self) -> dict[str, DataSet]:
        return mishin1998_datasets(self)

    @override
    def simulations(self) -> dict[str, Simulation]:
        czx_dose = Q(750, "mg")
        days = 35

        # induced CYP2E1 at the start, 750 mg chlorzoxazone at the start of every day
        changes = [
            {
                **self.default_changes(ApplicationForm.TABLET),
                "LI__cyp2e1": Q(3, "dimensionless"),
                "PODOSE_czx": czx_dose,
                # mean body weight of the groups (6 and 5 subjects)
                "BW": Q((85.5 * 6 + 80.2 * 5) / 11, "kg"),
            },
            *({"PODOSE_czx": czx_dose} for _ in range(days - 1)),
        ]

        simulation = self.segments_simulation(
            durations=[24] * days,
            changes=changes,
            steps_per_segment=self.steps_per_timecourse,
        )
        return {"sim": simulation}

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        with matplotlib.rc_context(rcParams):
            return {
                "fig_mishin": self.fig_time_courses(),
                **self.fig_mishin_dosing(),
            }

    def fig_time_courses(self) -> FigureMPL:
        """Chlorzoxazone and 6-OH-CZX + CZX-Glu on day 1, 8 and 26 with the data.

        Returns:
            The figure, a row per substance and a column per day.
        """
        fig, [axes_czx, axes_czx6oh] = plt.subplots(2, 3, figsize=(3 * 5, 2 * 5))
        fig.subplots_adjust(wspace=0.05)

        for ax in [axes_czx[0], axes_czx6oh[0]]:
            ax.set_xlim(-(0.05 * 8 / 24) + 1, 1 + 8 / 24 * 1.05)
        for ax in [axes_czx[1], axes_czx6oh[1]]:
            ax.set_xlim(-(0.05 * 8 / 24) + 8, 8 + 8 / 24 * 1.05)
        for ax in [axes_czx[2], axes_czx6oh[2]]:
            ax.set_xlim(-(0.05 * 8 / 24) + 26, 26 + 8 / 24 * 1.05)

        for axes in [axes_czx, axes_czx6oh]:
            set_broken_axes(axes)

        for ax, day in zip(axes_czx, [1, 8, 26], strict=True):
            ax.set_title(f"Day {day}")

        for ax in axes_czx6oh:
            ax.set_xlabel("Time [day]")

        res = self.results["task_sim"]
        for sid, axes in zip(
            [Sids.cpl_czx, Sids.cve_czx6oh_all], [axes_czx, axes_czx6oh], strict=True
        ):
            for ax in axes:
                self.plot_timecourse(
                    ax, res, sid, ("day", "µM"), LineStyle(color="black")
                )

        # the data of day 1 (day 0 of the study), day 8 and day 26: the datasets of
        # chlorzoxazone and of 6-OH-CZX, the column and the label
        data: list[tuple[list[str], int, str]] = [
            (["Fig1_rda", "Fig2_rda"], 1, "Mishin 1998 recently drinking\nalcoholics"),
            (["Fig7", "Fig8"], 8, "Mishin1998 recently drinking\nalcoholics"),
            (["Fig1_aa", "Fig2_aa"], 26, "Mishin1998 abstinent\nalcoholics"),
        ]
        for k, (ds_labels, day, label) in enumerate(data):
            for ds_label, axes in zip(ds_labels, [axes_czx, axes_czx6oh], strict=True):
                dset = self._datasets[f"dset_{ds_label}"]
                c = dset["count"].values[0]
                axes[k].errorbar(
                    x=Q(dset["time"], dset["time_unit"].values[0]).to("day")
                    + Q(day, "day"),
                    y=Q(dset["mean"], dset["mean_unit"].values[0]).to("µM"),
                    yerr=Q(dset["mean_sd"], dset["mean_unit"].values[0]).to("µM"),
                    marker="s",
                    markeredgecolor="black",
                    color="red",
                    label=f"{label} (Data$\\pm$SD, n={c})",
                )

        for axes in [axes_czx, axes_czx6oh]:
            mins = [ax.get_ylim()[0] for ax in axes]
            maxs = [ax.get_ylim()[1] for ax in axes]

            for ax in axes:
                ax.set_ylim(bottom=min(mins), top=max(maxs))
                ax.xaxis.set_major_locator(DayLocator())
                ax.xaxis.set_minor_locator(HourLocator())

                y = ax.get_ylim()[1]
                span = y - ax.get_ylim()[0]
                ax.set_ylim(top=y + span * 0.08)
                # the band of the phase above the plot, in data coordinates
                ax.axhspan(ymin=y, ymax=y + span * 0.08, facecolor="#a6bddb", alpha=0.6)

        for ax in axes_czx:
            ax.legend(frameon=False, loc="upper right", bbox_to_anchor=(1, 0.91))
        return fig

    def fig_mishin_dosing(self) -> dict[str, FigureMPL]:
        """Chlorzoxazone and 6-OH-CZX + CZX-Glu over the 35 days.

        The days of the data (1, 8 and 26) are black, the others grey.

        Returns:
            The figure by its key.
        """
        res = self.results["task_sim"]
        labels = [self.label_czx, self.label_czx6oh_all]
        fig, axes = plt.subplots(2, 1, figsize=(5, 2 * 5))
        axes[0].set_title("Mishin1998")
        # the days of the data and the days between them [day]
        segments = [
            (0, 1, "grey"),
            (0.99, 2, "black"),
            (1.99, 8, "grey"),
            (7.99, 9, "black"),
            (8.99, 26, "grey"),
            (25.99, 27, "black"),
            (26.99, np.inf, "grey"),
        ]
        for i, sid in enumerate([Sids.cpl_czx, Sids.cve_czx6oh_all]):
            ax = axes[i]
            ax.set_ylabel(f"{labels[i]} [µM]")
            t, *band = self.timecourse_band(res, sid, ("day", "µM"))
            for start, end, color in segments:
                mask = (t >= start) & (t < end)
                self.plot_bands(
                    ax, t[mask], *(b[mask] for b in band), style=LineStyle(color=color)
                )
            ax.set_xlabel("Time [day]")
            ax.set_ylim(bottom=0)
        for ax in axes:
            y = ax.get_ylim()[1]
            span = y - ax.get_ylim()[0]
            ax.set_ylim(top=y + span * 0.08)
            # the band of the phase above the plot, in data coordinates
            ax.axhspan(ymin=y, ymax=y + span * 0.08, facecolor="#a6bddb", alpha=0.6)
        return {"fig_dosing_mishin": fig}


if __name__ == "__main__":
    MODEL.run_experiments(Mishin1998Induction, output_dir="test")
