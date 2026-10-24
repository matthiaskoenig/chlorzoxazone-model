"""Sampling of the CYP2E1 activity of caucasians and japanese.

The CYP2E1 activities are sampled from log-normal distributions with a coefficient
of variation of 0.4, with a mean of 1 for caucasians and of 0.9/1.4 for japanese,
for 200 mg chlorzoxazone (tablet) with the body weight and height of the groups:
the distributions of chlorzoxazone and its metabolites over time.
"""

from typing import ClassVar, override

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure as FigureMPL
from pkpdsim.metadata import ApplicationForm
from sbmlsim import Q
from sbmlsim.simulation import Dimension, Scan, Simulation

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    Sids,
)


def sample_log_normal(cv: float, mean: float, seed: int) -> np.ndarray:
    """Sample from a log-normal distribution with a mean and coefficient of variation.

    Args:
        cv: coefficient of variation of the distribution.
        mean: mean of the distribution.
        seed: seed of the generator, so that the samples are the same in every run.

    Returns:
        500 samples.
    """
    rng = np.random.default_rng(seed)
    return np.exp(
        rng.normal(
            loc=np.log(mean) - 0.5 * np.log(cv**2 + 1),
            scale=np.sqrt(np.log(cv**2 + 1)),
            size=500,
        )
    )


class EthnicitySampling(ChlorzoxazoneSimulationExperiment):
    """Sampling of the CYP2E1 activity of caucasians and japanese."""

    #: colors of the boxes of the groups
    colors: ClassVar[list[str]] = ["white", "grey"]

    cyp2e1_caucasian_sampled: ClassVar[np.ndarray] = sample_log_normal(
        cv=0.4, mean=1, seed=1
    )
    cyp2e1_japanese_sampled: ClassVar[np.ndarray] = sample_log_normal(
        cv=0.4, mean=0.9 / 1.4, seed=2
    )

    @override
    def simulations(self) -> dict[str, Scan]:
        tcscans = {}

        for i, cyp2e1_amounts in enumerate(
            [self.cyp2e1_caucasian_sampled, self.cyp2e1_japanese_sampled]
        ):
            tcscans[f"scan_f_cyp2e1_{i}"] = Scan(
                simulation=Simulation(
                    time_unit="min",
                    end=10 * 60,
                    # a coarse grid for the samples: the steps of the
                    # integrator of every sample need too much memory
                    steps=50,
                    preinit_changes={
                        **self.default_changes(ApplicationForm.TABLET),
                        "PODOSE_czx": Q(200, "mg"),
                        "BW": Q(78.8 if i == 0 else 63.8, "kg"),
                        "HEIGHT": Q(180 if i == 0 else 171.9, "cm"),
                    },
                ),
                dimensions=[
                    Dimension(
                        "dim_cyp2e1",
                        values={
                            "LI__f_cyp2e1": Q(
                                self.population(cyp2e1_amounts, size=50),
                                "dimensionless",
                            )
                        },
                    ),
                ],
            )

        return tcscans

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return {"fig_dose_cyp2e1_sampling": self.fig_dose_cyp2e1_sampling()}

    def fig_dose_cyp2e1_sampling(self) -> FigureMPL:
        """Boxplots over time of chlorzoxazone and its metabolites of the groups.

        Returns:
            The figure, a column per group.
        """
        f, axes = plt.subplots(3, 2, figsize=(7.5, 7.5), dpi=300)
        for ax in axes[-1, :]:
            ax.set_xlabel("time [hr]")

        axes[0, 0].set_ylabel(f"CZX plasma conc. [{self.units[Sids.cpl_czx]}]")
        axes[1, 0].set_ylabel(
            f"6-OH-CZX + Glu plasma\nconc. [{self.units[Sids.cve_czx6oh_all]}]"
        )
        axes[2, 0].set_ylabel(
            f"CZX-O-Glu urinary\nrecovery [{self.units[Sids.aurine_czxoglu]}]"
        )

        axes[0, 0].set_title("caucasian")
        axes[0, 1].set_title("japanese")

        for ax in axes[:2, 0]:
            ax.set_xticklabels([])
        for ax in axes[:2, 1]:
            ax.set_xticklabels([])
            ax.set_yticklabels([])
        axes[-1, -1].set_yticklabels([])

        # caucasian and japanese
        for i in range(2):
            result = self.result_on_time_grid(f"task_scan_f_cyp2e1_{i}")
            uinfo = result.units
            times = result.ds["time"]

            width = Q(times[1].values - times[0].values, uinfo[Sids.time]).to(
                self.units[Sids.time]
            )
            for t in times:
                res_for_t = result.ds.sel(time=t)

                for k, sid in enumerate(
                    [Sids.cpl_czx, Sids.cve_czx6oh_all, Sids.aurine_czxoglu]
                ):
                    ax: Axes = axes[k, i]
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
                        boxprops={"facecolor": self.colors[i]},
                        flierprops={"markersize": 1, "alpha": 0.3},
                    )

        for ax_row in axes:
            max_y = 0
            for ax in ax_row:
                if ax.get_ylim()[1] > max_y:
                    max_y = ax.get_ylim()[1]

            for ax in ax_row:
                ax.set_ylim(top=max_y)
        f.tight_layout()
        return f


if __name__ == "__main__":
    MODEL.run_experiments(EthnicitySampling, output_dir="test")
