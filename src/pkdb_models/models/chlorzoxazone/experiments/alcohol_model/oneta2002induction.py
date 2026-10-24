"""Induction of CYP2E1 by ethanol and its withdrawal (Oneta2002, Lucas1995).

Three simulations with chlorzoxazone (tablet) every day:

- `ethanol_25_czx_500`: 500 mg at 8:00, 40 g ethanol at 20:00 on 30 days after 5
  days without ethanol, followed by 20 days without ethanol (non-alcoholics of
  Oneta2002, drinking).
- `ethanol_25_czx_750`: 750 mg at 8:00 on 16 days, starting with a 1.575-fold
  induced CYP2E1 (alcoholics of Oneta2002, withdrawal).
- `ethanol_withdrawal_500`: 500 mg at 10:00 on 22 days, starting with a 2.7-fold
  induced CYP2E1 (alcoholics of Lucas1995, withdrawal).

The metabolic ratio 6-OH-CZX/CZX two hours after the dose, compared with the data.
"""

from typing import ClassVar, override

import matplotlib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure as FigureMPL
from matplotlib.legend_handler import HandlerTuple
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator
from pkpdsim.metadata import ApplicationForm
from sbmlsim import Q
from sbmlsim.result import ScanResult
from sbmlsim.simulation import Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.chlorzoxazone import DATA_PATH_CHLORZOXAZONE, MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    LineStyle,
    Sids,
    metabolic_ratio,
    required,
)
from pkdb_models.models.chlorzoxazone.models import rcParams


class Oneta2002Induction(ChlorzoxazoneSimulationExperiment):
    """Induction of CYP2E1 by ethanol and its withdrawal (Oneta2002, Lucas1995).

    Repeated ethanol results in the induction of CYP2E1.
    """

    #: ethanol per day of the drinking [g]
    alcohol_dose: ClassVar[int] = 40
    #: days of the phases: without ethanol, drinking, withdrawal
    pre_days: ClassVar[int] = 5
    drinking_days: ClassVar[int] = 30
    withdrawal_days: ClassVar[int] = 20

    #: output steps per segment of the simulations
    steps_per_timecourse: ClassVar[int] = 200

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            "ethanol_25_czx_500": self.create_alcohol_induction_sim(),
            "ethanol_25_czx_750": self.create_withdrawal_sim(
                czx_dose=Q(750, "mg"), czx_hour=8, cyp2e1=1.575, days=15
            ),
            "ethanol_withdrawal_500": self.create_withdrawal_sim(
                czx_dose=Q(500, "mg"), czx_hour=10, cyp2e1=2.7, days=21
            ),
        }

    def create_alcohol_induction_sim(self) -> Simulation:
        """Get the simulation of the phases without ethanol, drinking and withdrawal.

        The simulation starts at 0:00, 500 mg chlorzoxazone at 8:00 of every day,
        ethanol at 20:00 of the days of drinking.

        Returns:
            The simulation.
        """
        czx_dose = Q(500, "mg")
        eth_dose = Q(self.alcohol_dose, "g")
        # application of chlorzoxazone at 8:00 (morning), of ethanol at 20:00
        czx_hour = 8
        eth_hour = 20

        # from 0:00 to 8:00
        durations: list[float] = [czx_hour]
        changes: list[dict[str, Quantity]] = [
            self.default_changes(ApplicationForm.TABLET),
        ]
        # without ethanol, only chlorzoxazone, starting at 8:00
        for _ in range(self.pre_days):
            durations.append(24)
            changes.append({"PODOSE_czx": czx_dose})

        # ethanol and chlorzoxazone, starting at 8:00
        tdelta_czx2eth = eth_hour - czx_hour  # 12 hr
        tdelta_eth2czx = 24 - tdelta_czx2eth  # 12 hr
        for _ in range(self.drinking_days):
            durations.append(tdelta_czx2eth)
            changes.append({"PODOSE_czx": czx_dose})
            durations.append(tdelta_eth2czx)
            changes.append({"GU__PODOSE_ethanol": eth_dose})

        # withdrawal, only chlorzoxazone, starting at 8:00
        for _ in range(self.withdrawal_days):
            durations.append(24)
            changes.append({"PODOSE_czx": czx_dose})

        # the rest of the day
        durations.append(24 - czx_hour)
        changes.append({"PODOSE_czx": czx_dose})

        return self.segments_simulation(
            durations=durations,
            changes=changes,
            steps_per_segment=self.steps_per_timecourse,
        )

    def create_withdrawal_sim(
        self, czx_dose: Quantity, czx_hour: int, cyp2e1: float, days: int
    ) -> Simulation:
        """Get the simulation of the withdrawal of alcoholics.

        The simulation starts at 0:00 with an induced CYP2E1, chlorzoxazone every
        day at the same hour.

        Args:
            czx_dose: dose of chlorzoxazone.
            czx_hour: hour of the dose of chlorzoxazone.
            cyp2e1: CYP2E1 at the start relative to the baseline.
            days: days with chlorzoxazone before the last one.

        Returns:
            The simulation.
        """
        # from 0:00 to the first dose
        durations: list[float] = [czx_hour]
        changes: list[dict[str, Quantity]] = [
            {
                **self.default_changes(ApplicationForm.TABLET),
                "LI__cyp2e1": Q(cyp2e1, "dimensionless"),
            }
        ]

        # only chlorzoxazone, starting at the hour of the dose
        for _ in range(days):
            durations.append(24)
            changes.append({"PODOSE_czx": czx_dose})

        # the rest of the day
        durations.append(24 - czx_hour)
        changes.append({"PODOSE_czx": czx_dose})

        return self.segments_simulation(
            durations=durations,
            changes=changes,
            steps_per_segment=self.steps_per_timecourse,
        )

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        with matplotlib.rc_context(rcParams):
            fig_oneta, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(3 * 7, 5))

            self.fig_drinking_oneta(ax0)
            self.fig_withdrawal_oneta(ax1)
            self.fig_withdrawal_lucas(ax2)
            ax0.set_title("Oneta2002 drinking")
            ax1.set_title("Oneta2002 withdrawal")
            ax2.set_title("Lucas1995 withdrawal")
            return {
                **self.fig_alcohol_czx_czx6oh_mr(),
                **self.fig_alcohol_multidosing(),
                "fig_oneta": fig_oneta,
            }

    def fig_drinking_oneta(self, ax: Axes) -> None:
        """Metabolic ratio (2 hr) of the drinking with the non-alcoholics of Oneta2002.

        Args:
            ax: the axes.
        """
        ax.set_ylabel("6-OH-CZX/CZX MR [-]")
        ax.set_xlabel("Time [day]")

        data_df = pd.read_excel(
            DATA_PATH_CHLORZOXAZONE / "Oneta2002" / "Oneta2002.xlsx",
            sheet_name="Fig2",
            header=1,
        )

        res = self.result_on_time_grid("task_ethanol_25_czx_500")
        times = np.linspace(10 * 60, 60 * (10 + 35 * 24), 36)

        sim_line = self.plot_mr(ax, res, times, offset=self.pre_days)

        markers = ["v", "d", "s", "o", "p"]
        tcs = []
        groups = []
        data_times = None
        for i, (_, individual_df) in enumerate(data_df.groupby("individual")):
            data_times = individual_df["time"] * 7 + 10 / 24
            (gr,) = ax.plot(
                data_times,
                individual_df["value"],
                marker=markers[i],
                linestyle="none",
                color="snow",
                markeredgecolor="black",
            )
            tcs.append(individual_df["value"].values)
            groups.append(gr)
        values = np.vstack(tcs)
        eb = ax.errorbar(
            required(data_times),
            np.mean(values, axis=0),
            yerr=np.std(values, axis=0),
            marker="s",
            capsize=5,
            color="red",
            markeredgecolor="black",
        )
        y = ax.get_ylim()[1]
        span = y - ax.get_ylim()[0]
        ax.set_ylim(top=y + span * 0.08)
        ax.axvspan(-7, 0, ymin=0.91, facecolor="gainsboro", zorder=0, alpha=0.6)
        ax.axvspan(0, 29, ymin=0.91, facecolor="#fdbb84", zorder=0, alpha=0.6)
        ax.axvspan(29, 61, ymin=0.91, facecolor="#a6bddb", zorder=0, alpha=0.6)

        ax.set_xlim(left=-3, right=29)

        ax.legend(
            [sim_line, eb, tuple(groups)],
            [
                "Simulation (500 mg)",
                "Oneta2002 non-alcoholics\n(Data$\\pm$SD)",
                "Oneta2002 non-alcoholics\nindividuals",
            ],
            numpoints=1,
            handler_map={tuple: HandlerTuple(ndivide=None)},
            frameon=False,
            loc="upper left",
            bbox_to_anchor=(0, 0.91),
        )

    def fig_withdrawal_oneta(self, ax: Axes) -> None:
        """Metabolic ratio (2 hr) of the withdrawal with the alcoholics of Oneta2002.

        Args:
            ax: the axes.
        """
        ax.set_xlabel("Time [day]")
        data_df = pd.read_excel(
            DATA_PATH_CHLORZOXAZONE / "Oneta2002" / "Oneta2002.xlsx",
            sheet_name="Fig3",
            header=1,
        )
        data_df = data_df[data_df["group"] != "NALD"]
        res = self.result_on_time_grid("task_ethanol_25_czx_750")
        freq = np.linspace(0, 14, 15)
        times = 10 * 60 + freq * 24 * 60

        sim_line = self.plot_mr(ax, res, times)

        markers = ["v", "d", "s", "o", "p"]
        tcs = []
        groups = []
        data_times = None
        for i, (_, individual_df) in enumerate(data_df.groupby("individual")):
            data_times = individual_df["time"] - 1 + 10 / 24
            (gr,) = ax.plot(
                data_times,
                individual_df["value"],
                marker=markers[i],
                linestyle="none",
                color="snow",
                markeredgecolor="black",
            )
            groups.append(gr)
            tcs.append(individual_df["value"].values)

        values = np.vstack(tcs)
        eb = ax.errorbar(
            required(data_times),
            np.mean(values, axis=0),
            yerr=np.std(values, axis=0),
            marker="s",
            capsize=5,
            color="red",
            markeredgecolor="black",
        )

        y = ax.get_ylim()[1]
        span = y - ax.get_ylim()[0]
        ax.set_ylim(top=y + span * 0.08)

        ax.axhspan(ymin=y, ymax=ax.get_ylim()[1], color="#a6bddb", alpha=0.6)

        ax.set_xlim(left=0, right=15)

        ax.legend(
            [sim_line, eb, tuple(groups)],
            [
                "Simulation (750 mg)",
                "Oneta2002 alcoholics\n(Data$\\pm$SD)",
                "Oneta2002 alcoholics\nindividuals",
            ],
            numpoints=1,
            handler_map={tuple: HandlerTuple(ndivide=None)},
            frameon=False,
            loc="upper right",
            bbox_to_anchor=(1, 0.91),
        )

    def fig_withdrawal_lucas(self, ax: Axes) -> None:
        """Metabolic ratio (2 hr) of the withdrawal with the alcoholics of Lucas1995.

        Args:
            ax: the axes.
        """
        ax.set_xlabel("Time [day]")
        data_df = pd.read_excel(
            DATA_PATH_CHLORZOXAZONE / "Lucas1995" / "Lucas1995.xlsx",
            sheet_name="Tab2",
            header=1,
        )
        res = self.result_on_time_grid("task_ethanol_withdrawal_500")
        freq = np.linspace(0, 20, 21)
        times = 12 * 60 + freq * 24 * 60

        sim_line = self.plot_mr(ax, res, times)

        mean = data_df.groupby("time")["value"].mean()
        mean.loc[21] = 0.31  # from Tab1
        sd = data_df.groupby("time")["value"].std()
        sd.loc[21] = 0.03 * np.sqrt(34)  # from Tab1

        eb = ax.errorbar(
            mean.index + 10 / 24 - 1,
            mean.values,
            yerr=sd.values,
            marker="s",
            capsize=5,
            color="red",
            markeredgecolor="black",
        )

        y = ax.get_ylim()[1]
        span = y - ax.get_ylim()[0]
        ax.set_ylim(top=y + span * 0.08)

        ax.axhspan(ymin=y, ymax=ax.get_ylim()[1], color="#a6bddb", alpha=0.6)

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        ax.set_xlim(left=0, right=21)

        ax.legend(
            [sim_line, eb],
            ["Simulation (500 mg)", "Lucas1995 alcoholics\n(Data$\\pm$SD)"],
            numpoints=1,
            handler_map={tuple: HandlerTuple(ndivide=None)},
            frameon=False,
            loc="upper right",
            bbox_to_anchor=(1, 0.91),
        )

    def fig_alcohol_czx_czx6oh_mr(self) -> dict[str, FigureMPL]:
        """Chlorzoxazone, 6-OH-CZX + CZX-Glu and the metabolic ratio of the drinking.

        Returns:
            The figures by key, one per quantity.
        """
        figures = {}
        res = self.result_on_time_grid("task_ethanol_25_czx_500")
        uinfo = res.units

        labels = [self.label_czx, self.label_czx6oh_all, "6-OH-CZX/CZX MR"]
        units = ["µM", "µM", "dimensionless"]
        unit_label = ["µM", "µM", "-"]
        sids = [Sids.cpl_czx, Sids.cve_czx6oh_all]

        mr = metabolic_ratio(res)
        days = Q(res.ds["time"].values, uinfo["time"]).to("day").magnitude
        for i in range(3):
            fig, ax = plt.subplots(1, 1, figsize=(7, 5))
            if i < 2:
                t, *band = self.timecourse_band(res, sids[i], ("day", units[i]))
                self.plot_bands(
                    ax, t - self.pre_days, *band, style=LineStyle(color="black")
                )
            else:
                self.plot_band(
                    ax,
                    days - self.pre_days,
                    self.draw_values(mr),
                    LineStyle(color="black"),
                )
                # 2 hr after the chlorzoxazone at 8:00 of every day of the
                # simulation [min]
                days = self.pre_days + self.drinking_days + self.withdrawal_days
                times = np.linspace(10 * 60, 60 * (10 + days * 24), days + 1)
                self.plot_mr(
                    ax, res, times, offset=self.pre_days, linestyle="", label="MR (2hr)"
                )
            ax.set_ylabel(f"{labels[i]} [{unit_label[i]}]")
            ax.set_xlabel("Time [day]")
            ax.set_xlim(
                left=-self.pre_days, right=self.drinking_days + self.withdrawal_days
            )
            self.set_phase_bars(ax)

            figures[f"base_{i}"] = fig

        return figures

    def fig_alcohol_multidosing(self) -> dict[str, FigureMPL]:
        """Ethanol in plasma and CYP2E1 in the liver of the drinking.

        Returns:
            The figures by key, one per quantity.
        """
        fig1, ax_0 = plt.subplots(1, 1, figsize=(7, 5))
        fig2, ax_1 = plt.subplots(1, 1, figsize=(7, 5))
        res = self.result_on_time_grid("task_ethanol_25_czx_500")

        labels = ["Ethanol", "Liver CYP2E1"]
        units = ["mM", "dimensionless"]
        unit_label = ["mM", "-"]
        sids = [Sids.cve_ethanol, Sids.cli_cyp2e1]
        for i, (ax, sid) in enumerate(zip([ax_0, ax_1], sids, strict=True)):
            t, *band = self.timecourse_band(res, sid, ("day", units[i]))
            self.plot_bands(
                ax, t - self.pre_days, *band, style=LineStyle(color="black")
            )
            ax.set_ylabel(f"{labels[i]} [{unit_label[i]}]")
            ax.set_xlabel("Time [day]")
            ax.set_xlim(
                left=-self.pre_days, right=self.drinking_days + self.withdrawal_days
            )
            self.set_phase_bars(ax)
        return {"base_ethanol_multiple_dosing": fig1, "base_li_cyp2e1": fig2}

    def plot_mr(
        self,
        ax: Axes,
        res: ScanResult,
        times: np.ndarray,
        offset: float = 0,
        linestyle: str = "-",
        label: str | None = None,
    ) -> Line2D:
        """Plot the metabolic ratio 6-OH-CZX/CZX at times, the median of the draws.

        Args:
            ax: the axes.
            res: the result on its time grid, see `result_on_time_grid`.
            times: the times [min], 2 hr after a dose of chlorzoxazone.
            offset: the days before the drinking, the time 0 of the plot.
            linestyle: the style of the line between the times.
            label: the label of the line.

        Returns:
            The line of the median.
        """
        # the state at the times, interpolated linearly between the time points
        at = res.interpolate(times)
        return self.plot_band(
            ax,
            times / 60 / 24 - offset,
            self.draw_values(metabolic_ratio(at)),
            LineStyle(
                color="black",
                marker="o",
                markerfacecolor="#252525",
                markeredgecolor="black",
                linestyle=linestyle,
                label=label,
            ),
        )

    def set_phase_bars(self, ax: Axes) -> None:
        """Mark the phases without ethanol, drinking and withdrawal above a plot.

        Args:
            ax: the axes.
        """
        y = ax.get_ylim()[1]
        span = y - ax.get_ylim()[0]
        # a legend only of a plot with labelled curves
        if ax.get_legend_handles_labels()[0]:
            ax.legend(frameon=False, loc="upper right", bbox_to_anchor=(1, 0.9))
        ax.set_ylim(top=y + span * 0.08)

        ax.axvspan(
            -self.pre_days, 0, ymin=0.91, facecolor="gainsboro", zorder=0, alpha=0.6
        )
        ax.axvspan(
            0, self.drinking_days, ymin=0.91, facecolor="#fdbb84", zorder=0, alpha=0.6
        )
        ax.axvspan(
            self.drinking_days,
            self.drinking_days + self.withdrawal_days,
            ymin=0.91,
            facecolor="#a6bddb",
            zorder=0,
            alpha=0.6,
        )

        k = y + 0.05 * span
        ax.text(
            -self.pre_days / 2,
            k,
            "pre",
            ha="center",
            va="top",
            fontsize=14,
            fontweight="bold",
        )
        ax.text(
            self.drinking_days / 2,
            k,
            "drinking",
            ha="center",
            va="top",
            fontsize=14,
            fontweight="bold",
        )
        ax.text(
            self.drinking_days + self.withdrawal_days / 2,
            k,
            "withdrawal",
            ha="center",
            va="top",
            fontsize=14,
            fontweight="bold",
        )


if __name__ == "__main__":
    MODEL.run_experiments(Oneta2002Induction, output_dir="test")
