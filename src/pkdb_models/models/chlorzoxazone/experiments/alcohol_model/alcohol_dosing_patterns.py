"""Drinking patterns of ethanol and the induction of CYP2E1.

Ethanol on 40 days in 1 to 10 drinks per day between 8:00 and 20:00, either 40 g per
day split into the drinks (exp1) or 10 g per drink (exp2), so that the amount per
day increases with the frequency. The inhibition constant of the degradation of
CYP2E1 by ethanol is scanned from 1e-3 to 1e3 µM: the metabolic ratio
6-OH-CZX/CZX two hours after 500 mg chlorzoxazone (tablet) at 8:00 after the last
day of drinking, over the drinking frequency.
"""

from typing import ClassVar, override

import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure as FigureMPL
from matplotlib.patches import Patch
from pkpdsim.metadata import ApplicationForm
from sbmlsim import Q
from sbmlsim.simulation import Dimension, Scan
from sbmlsim.units import Quantity

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    LineStyle,
    Sids,
    metabolic_ratio,
)
from pkdb_models.models.chlorzoxazone.models import rcParams
from pkdb_models.models.chlorzoxazone.plot_colors import cmap_blues


class AlcoholDosing(ChlorzoxazoneSimulationExperiment):
    """Drinking patterns of ethanol and the induction of CYP2E1.

    Repeated ethanol results in the induction of CYP2E1.
    """

    #: maximal number of drinks per day
    drinking_frequency: ClassVar[int] = 10
    #: days of drinking
    days: ClassVar[int] = 40
    #: the time of the metabolic ratio, 2 hr after the chlorzoxazone at 8:00
    #: after the days of drinking [hr]
    mr_time: ClassVar[float] = 8 + 40 * 24 + 2

    @property
    def kis(self) -> np.ndarray:
        """Inhibition constants of the degradation of CYP2E1 by ethanol [µM].

        A run over the draws scans every third value (memory).
        """
        return np.logspace(-3, 3, 7)[:: 1 if self.draws is None else 3]

    @property
    def output_times(self) -> list[float]:
        """The output times [hr].

        The first day and the day of chlorzoxazone every 0.05 hr, the days of
        drinking every hr.
        """
        end = 8 + self.days * 24 + 16
        return np.unique(
            np.concatenate(
                [
                    np.linspace(0, 24, 481),
                    np.arange(24, end - 16, 1.0),
                    np.linspace(end - 16, end, 321),
                ]
            )
        ).tolist()

    @override
    def simulations(self) -> dict[str, Scan]:
        tcsims = {}
        for n in range(self.drinking_frequency):
            # 40 g per day split into the drinks
            tcsims[f"sim_{n}_exp1"] = self.create_alcohol_ndoses(n + 1, 40, True)
            # 10 g per drink
            tcsims[f"sim_{n}_exp2"] = self.create_alcohol_ndoses(n + 1, 10, False)
        return tcsims

    def create_alcohol_ndoses(self, n: int, dose: float, split_dose: bool) -> Scan:
        """Get the scan of the inhibition constants for a number of drinks per day.

        The simulation starts at 0:00. Ethanol is drunk on 40 days between 8:00
        and 20:00, followed by 500 mg chlorzoxazone at 8:00 after the last day.

        Args:
            n: number of drinks per day.
            dose: ethanol per day if it is split, otherwise per drink [g].
            split_dose: split the dose of a day into the drinks.

        Returns:
            The scan of the inhibition constants `kis`.
        """
        eth_dose = Q(dose, "g")
        if split_dose:
            eth_dose = eth_dose / n

        # from 0:00 to 8:00
        durations: list[float] = [8]
        changes: list[dict[str, Quantity]] = [
            self.default_changes(ApplicationForm.TABLET),
        ]

        # 40 days with the drinks evenly spaced from 8:00 to 20:00, starting at 8:00
        drinks = np.sort(20 - np.linspace(0, 12, n))
        for _ in range(self.days):
            if n == 1:
                changes.append({})
                durations.append(12)
            else:
                for idx, hour in enumerate(drinks[1:]):
                    durations.append(hour - drinks[idx])
                    changes.append({"GU__PODOSE_ethanol": eth_dose})
            changes.append({"GU__PODOSE_ethanol": eth_dose})
            durations.append(12)

        # single dose of chlorzoxazone at 8:00 after the last day of drinking,
        # simulation of the rest of the day
        changes.append({"PODOSE_czx": Q(500, "mg")})
        durations.append(16)

        simulation = self.segments_simulation(
            durations=durations, changes=changes, times=self.output_times
        )

        return Scan(
            simulation=simulation,
            dimensions=[
                Dimension(
                    "dim_ki", values={"LI__Ki_cyp2e1_deg_ethanol": Q(self.kis, "µM")}
                )
            ],
        )

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        with matplotlib.rc_context(rcParams):
            return {
                "mr": self.fig_frequency(),
                "dosing": self.fig_dosing_patterns(),
            }

    def _task_ids(self, exp_key: str) -> list[str]:
        """Get the tasks of an experiment, ordered by the number of drinks per day.

        Args:
            exp_key: the experiment, `exp1` or `exp2`.

        Returns:
            The ids of the tasks.
        """
        return [key for key in self.results if exp_key in key]

    def _mr(self, task_id: str) -> np.ndarray:
        """Get the metabolic ratio 2 hr after the chlorzoxazone of a task.

        Args:
            task_id: the task, a scan of the inhibition constants.

        Returns:
            The ratio of every inhibition constant, the draws as the last axis.
        """
        # the state at the time, interpolated linearly between the time points
        at = self.results[task_id].interpolate([self.mr_time * 60])
        return self.draw_values(
            metabolic_ratio(at, at.ds.isel(time=0)).transpose("dim_ki", ...)
        )

    def fig_frequency(self) -> FigureMPL:
        """Metabolic ratio (2 hr) over the drinking frequency per inhibition constant.

        Returns:
            The figure, a panel per experiment.
        """
        fig, axes = plt.subplots(1, 2, figsize=(2 * 7, 5))
        axes[0].set_ylabel("MR (2hr)")
        axes[0].set_xlabel("drinking frequency [1/day]")
        axes[0].set_title("40 g alcohol per day")

        axes[1].set_ylabel("MR (2hr)")
        axes[1].set_xlabel("drinking frequency [1/day]")
        axes[1].set_title("10 g alcohol per drink")

        for exp_key, ax in zip(["exp1", "exp2"], axes, strict=True):
            task_ids = self._task_ids(exp_key)
            frequencies = list(range(1, len(task_ids) + 1))
            # the frequencies in the rows, the inhibition constants in the
            # columns and the draws as the last axis
            mr_values = np.stack([self._mr(task_id) for task_id in task_ids])

            handles = []
            for i, ki in enumerate(self.kis):
                color = cmap_blues(1 - (i / (len(self.kis) - 1)))
                self.plot_band(
                    ax,
                    frequencies,
                    mr_values[:, i],
                    LineStyle(color=color, marker="o", markeredgecolor="black"),
                )
                handles.append(Patch(color=color, label=int(np.log10(ki))))
            if exp_key == "exp2":
                ax.legend(
                    handles=handles,
                    title="log Ki [µM]",
                    frameon=False,
                    loc="upper left",
                    bbox_to_anchor=(1, 1),
                )
        return fig

    def fig_dosing_patterns(self) -> FigureMPL:
        """Ethanol in plasma over the first day per number of drinks.

        Returns:
            The figure, a row per number of drinks and a column per experiment.
        """
        fig, axes = plt.subplots(self.drinking_frequency, 2, figsize=(2 * 7, 5))
        for i, exp_key in enumerate(["exp1", "exp2"]):
            for n, task_id in enumerate(self._task_ids(exp_key)):
                # ethanol does not depend on the inhibition constant
                self.plot_timecourse(
                    axes[n, i],
                    self.results[task_id],
                    Sids.cve_ethanol,
                    ("hr", "mM"),
                    LineStyle(color="black"),
                    point={"dim_ki": 0},
                )

        for k, row in enumerate(axes):
            for ax in row:
                ax.set_xlim(0, 24)
                ax.set_yticks([])
                ax.annotate(
                    str(k + 1),
                    xy=(1, 0.5),
                    xytext=(1.02, 0.5),
                    xycoords="axes fraction",
                    textcoords="axes fraction",
                    verticalalignment="center",
                    fontsize=12,
                    arrowprops={"arrowstyle": "-"},
                )
        for row in axes[:-1]:
            for ax in row:
                ax.set_xticks([])
        for i in range(axes.shape[1]):
            maxs = [ax.get_ylim()[1] for ax in axes[:, i]]
            for ax in axes[:, i]:
                ax.set_ylim(top=max(maxs))
        for ax in axes[-1, :]:
            ax.set_xlabel("Time (hr)")

        return fig


if __name__ == "__main__":
    MODEL.run_experiments(AlcoholDosing, output_dir="test")
