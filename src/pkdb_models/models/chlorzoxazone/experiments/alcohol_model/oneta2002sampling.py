"""Induction of CYP2E1 by ethanol and its withdrawal with sampled individuals.

Two simulations with chlorzoxazone (tablet) every day at 8:00, each with 100
individuals of sampled CYP2E1 activity:

- `ethanol_25_czx_500`: 500 mg, 40 g ethanol at 20:00 on 28 days after 7 days
  without ethanol, followed by 30 days without ethanol (non-alcoholics of
  Oneta2002, drinking).
- `ethanol_25_czx_750`: 750 mg on 16 days, starting with a 1.5-fold induced CYP2E1
  (alcoholics of Oneta2002, withdrawal).

The distribution of the metabolic ratio 6-OH-CZX/CZX two hours after the dose,
compared with the individuals of Oneta2002.

TODO: parametrize alcohol absorption and degradation with time course data
TODO: calculate 6OHCZX/CZX ratio for all and plot against data from Oneta2002
"""

from typing import ClassVar, override

import matplotlib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure as FigureMPL
from pkpdsim.metadata import ApplicationForm
from sbmlsim import Q
from sbmlsim.plot import Axis, Figure
from sbmlsim.result import ScanResult
from sbmlsim.simulation import Dimension, Scan, Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.chlorzoxazone import DATA_PATH_CHLORZOXAZONE, MODEL
from pkdb_models.models.chlorzoxazone.cyp2e1_amounts.helper import sample_cyp2e1
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    Sids,
    metabolic_ratio,
)
from pkdb_models.models.chlorzoxazone.models import rcParams


class Oneta2002Sampling(ChlorzoxazoneSimulationExperiment):
    """Induction of CYP2E1 by ethanol and its withdrawal with sampled individuals."""

    #: ethanol per day of the drinking [g]
    alcohol_dose: ClassVar[int] = 40

    @property
    def steps_per_timecourse(self) -> int:
        """Output steps per segment, fewer in a run over the draws (memory).

        The metabolic ratio 2 hr after a dose is interpolated linearly between
        the time points.
        """
        return 200 if self.draws is None else 48

    @override
    def simulations(self) -> dict[str, Scan]:
        return {
            "ethanol_25_czx_500": self.create_scan_sim(
                self.create_alcohol_induction_sim(), 1.2, seed=9
            ),
            "ethanol_25_czx_750": self.create_scan_sim(
                self.create_alcohol_withdrawal_sim(), 1.0, seed=10
            ),
        }

    def create_scan_sim(self, tc_sim: Simulation, cyp_mean: float, seed: int) -> Scan:
        """Get the scan of a simulation over 100 sampled CYP2E1 activities.

        Args:
            tc_sim: the simulation.
            cyp_mean: mean of the CYP2E1 activities.
            seed: seed of the sampling.

        Returns:
            The scan.
        """
        return Scan(
            simulation=tc_sim,
            dimensions=[
                Dimension(
                    "dim_cyp2e1",
                    values={
                        "LI__f_cyp2e1": Q(
                            self.population(
                                sample_cyp2e1(0.4, cyp_mean, seed=seed, size=100),
                                size=10,
                            ),
                            "dimensionless",
                        )
                    },
                ),
            ],
        )

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
            {
                **self.default_changes(ApplicationForm.TABLET),
            }
        ]
        # 7 days without ethanol, only chlorzoxazone, starting at 8:00
        for _ in range(7):
            durations.append(24)
            changes.append({"PODOSE_czx": czx_dose})

        # 28 days of ethanol and chlorzoxazone, starting at 8:00
        tdelta_czx2eth = eth_hour - czx_hour  # 12 hr
        tdelta_eth2czx = 24 - tdelta_czx2eth  # 12 hr
        for _ in range(28):
            durations.append(tdelta_czx2eth)
            changes.append({"PODOSE_czx": czx_dose})
            durations.append(tdelta_eth2czx)
            changes.append({"GU__PODOSE_ethanol": eth_dose})

        # 30 days of withdrawal, only chlorzoxazone, starting at 8:00
        for _ in range(30):
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

    def create_alcohol_withdrawal_sim(self) -> Simulation:
        """Get the simulation of the withdrawal of alcoholics.

        The simulation starts at 0:00 with an induced CYP2E1, 750 mg chlorzoxazone
        at 8:00 of every day.

        Returns:
            The simulation.
        """
        czx_dose = Q(750, "mg")
        czx_hour = 8

        # from 0:00 to 8:00
        durations: list[float] = [czx_hour]
        changes: list[dict[str, Quantity]] = [
            {
                **self.default_changes(ApplicationForm.TABLET),
                "LI__cyp2e1": Q(1.5, "dimensionless"),
            }
        ]

        # 15 days of withdrawal, only chlorzoxazone, starting at 8:00
        for _ in range(15):
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
            fig_oneta, axes = plt.subplots(1, 2, figsize=(2 * 7, 5))
            self.fig_alcohol_onset(axes[0])
            self.fig_alcohol_withdrawal(axes[1])
            return {"fig_oneta": fig_oneta}

    def fig_alcohol_onset(self, ax: Axes) -> None:
        """Metabolic ratio (2 hr) of the drinking with the non-alcoholics of Oneta2002.

        Args:
            ax: the axes.
        """
        data_df = pd.read_excel(
            DATA_PATH_CHLORZOXAZONE / "Oneta2002" / "Oneta2002.xlsx",
            sheet_name="Fig2",
            header=1,
        )

        res = self.result_on_time_grid("task_ethanol_25_czx_500")
        times = np.linspace(10 * 60, 60 * (10 + 54 * 24), 55)

        self.plot_boxes(ax, res, times, 7)

        markers = ["v", "d", "s", "o", "p"]
        for i, (_, individual_df) in enumerate(data_df.groupby("individual")):
            ax.plot(
                individual_df["time"] * 7 + 10 / 24,
                individual_df["value"],
                marker=markers[i],
                linestyle="none",
                color="deepskyblue",
                markeredgecolor="black",
                markersize=7,
            )
        ax.set_xlabel("time [days]")
        ax.set_ylabel("6-OH-CZX/CZX MR (2hr)\n[dimensionless]")

    def fig_alcohol_withdrawal(self, ax: Axes) -> None:
        """Metabolic ratio (2 hr) of the withdrawal with the alcoholics of Oneta2002.

        Args:
            ax: the axes.
        """
        data_df = pd.read_excel(
            DATA_PATH_CHLORZOXAZONE / "Oneta2002" / "Oneta2002.xlsx",
            sheet_name="Fig3",
            header=1,
        )
        data_df = data_df[data_df["group"] != "NALD"]
        res = self.result_on_time_grid("task_ethanol_25_czx_750")
        freq = np.linspace(0, 14, 15)
        times = 10 * 60 + freq * 24 * 60
        self.plot_boxes(ax, res, times, 0)

        markers = ["v", "d", "s", "o", "p"]
        for i, (_, individual_df) in enumerate(data_df.groupby("individual")):
            ax.plot(
                individual_df["time"] - 1 + 10 / 24,
                individual_df["value"],
                marker=markers[i],
                linestyle="none",
                color="deepskyblue",
                markeredgecolor="black",
            )

        ax.set_xlabel("time [days]")

    def plot_boxes(
        self, ax: Axes, res: ScanResult, times: np.ndarray, offset: float = 0
    ) -> None:
        """Plot boxes of the metabolic ratio 6-OH-CZX/CZX of the individuals.

        Args:
            ax: the axes.
            res: the result of the scan on its time grid.
            times: the times of the boxes [min].
            offset: offset of the times [day].
        """
        uinfo = res.units
        width = Q(times[1] - times[0], uinfo[Sids.time]).to("day")
        # the state at the times, interpolated linearly between the time points
        at = res.interpolate(times)
        for k, t in enumerate(times):
            # the individuals, times the draws in a run over them
            mr = metabolic_ratio(at, at.ds.isel(time=k)).values.ravel()
            t_pos = Q([t], uinfo[Sids.time]) - Q(offset, "day")
            bplot = ax.boxplot(
                x=mr,
                positions=t_pos.to("day").magnitude,
                manage_ticks=False,
                widths=[width.magnitude],
                patch_artist=True,
                showfliers=True,
                whiskerprops={"alpha": 0.6},
                medianprops={"color": "black"},
                capprops={"alpha": 0.6},
                flierprops={"markersize": 1, "alpha": 0.4},
            )

            for patch in bplot["boxes"]:
                patch.set_facecolor("orange")
                patch.set_alpha(0.6)

    @override
    def figures(self) -> dict[str, Figure]:
        name = (
            "Oral chlorzoxazone application 500 mg at 8 am\n"
            f"with {self.alcohol_dose} g alcohol at 8 pm for 28 days."
        )
        fig = Figure(
            experiment=self,
            sid="Fig_alcohol",
            num_rows=2,
            num_cols=2,
            name=name,
        )
        plots = fig.create_plots(xaxis=Axis("time", unit="day"), legend=True)

        sids = [Sids.cli_ethanol, Sids.cli_cyp2e1, Sids.cve_ethanol, Sids.cpl_czx]

        for k, sid in enumerate(sids):
            # simulation
            plots[k].add_data(
                task="task_ethanol_25_czx_500",
                xid="time",
                yid=sid,
                label=f"ethanol {self.alcohol_dose} g PO",
                over="dim_cyp2e1",
            )
            plots[k].set_yaxis(label=sid, unit=self.units[sid])

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Oneta2002Sampling, output_dir="test")
