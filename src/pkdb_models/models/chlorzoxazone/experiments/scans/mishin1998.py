"""Scan of the CYP2E1 activity, compared with Mishin1998.

750 mg chlorzoxazone (tablet) with the mean body weight of the groups and the
CYP2E1 activity scanned: the Cmax of 6-hydroxychlorzoxazone and its glucuronide
over the CYP2E1 activity, with the individuals of Mishin1998 (alcoholics, recently
drinking and abstinent, and non-alcoholic liver disease) over their CYP2E1 content
relative to the abstinent alcoholics.
"""

from typing import ClassVar, override

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.collections import LineCollection
from matplotlib.container import ErrorbarContainer
from matplotlib.figure import Figure as FigureMPL
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from pkpdsim.metadata import ApplicationForm
from sbmlsim import Q
from sbmlsim.simulation import Dimension, Scan, Simulation

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    LineStyle,
    Sids,
)
from pkdb_models.models.chlorzoxazone.models import rcParams


class Mishin1998Scan(ChlorzoxazoneSimulationExperiment):
    """Scan of the CYP2E1 activity, compared with Mishin1998."""

    cyp2e1: ClassVar[np.ndarray] = np.linspace(0.1, 3, 21)

    @override
    def simulations(self) -> dict[str, Scan]:
        tcsims = {}

        tcsims["sim"] = Scan(
            simulation=Simulation(
                time_unit="min",
                end=7 * 60,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "PODOSE_czx": Q(750, "mg"),
                    "BW": Q((85.5 * 6 + 80.2 * 5 + 103.1 * 5) / 16, "kg"),
                },
            ),
            dimensions=[Dimension("dim_cyp2e1", values={"LI__f_cyp2e1": self.cyp2e1})],
        )
        return tcsims

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        dset = self.load_dataframe("Fig6", study="Mishin1998")
        result = self.results["task_sim"]
        # the maximum of every point of the scan, per draw, over its output
        # points (the steps of the integrator, padded with NaN)
        tdim = "_point" if result.ragged else "time"
        cmaxs = Q(
            self.draw_values(result.ds[Sids.cve_czx6oh_all].max(dim=tdim)),
            result.units[Sids.cve_czx6oh_all],
        ).to("µM")

        with plt.rc_context(rcParams):
            ax: Axes
            fig, ax = plt.subplots(1, 1, figsize=(7, 5))
            sim = self.plot_band(
                ax,
                self.cyp2e1,
                cmaxs.m,
                LineStyle(color="black", marker="o", label="Sim (750 mg)"),
            )

            groupby = dset.groupby("group")

            labeldict = {
                "alcoholic_drinking": "recently drinking",
                "alcoholic_abstinent": "abstinent",
                "NALD": "NALD",
            }

            color_dict = {
                "alcoholic_drinking": "red",
                "alcoholic_abstinent": "#636363",
                "NALD": "#fec44f",
            }

            # the CYP2E1 content relative to the abstinent alcoholics
            dset_anchor = np.mean(groupby.get_group("alcoholic_abstinent")["x_value"])
            for label, df in groupby:
                label = str(label)
                dset_y = (
                    Q(df["y_value"].values, df["y_units"].values[0]) / self.Mr.czx6oh
                )
                dset_y = dset_y.to("µM")
                n = df["count"].values[0]
                ax.scatter(
                    df["x_value"] / dset_anchor,
                    dset_y.magnitude,
                    marker="s",
                    color=color_dict[label],
                    label=f"{labeldict[label]} individuals",
                    edgecolor="black",
                )
                ax.errorbar(
                    np.mean(df["x_value"]) / dset_anchor,
                    np.mean(dset_y.magnitude),
                    xerr=np.std(df["x_value"]) / dset_anchor,
                    yerr=np.std(dset_y.magnitude),
                    marker="o",
                    color=color_dict[label],
                    label=f"{labeldict[label]} Mean+SD (n={n})",
                    markeredgecolor="black",
                    markersize=8,
                )

            # the handles of the legend
            individual = Line2D(
                [], [], ls="none", marker="s", color="white", markeredgecolor="black"
            )
            line = Line2D(
                [],
                [],
                ls="none",
                marker="o",
                markersize=8,
                markerfacecolor="white",
                markeredgecolor="black",
            )
            barline = LineCollection(
                list(np.empty((2, 2, 2))), facecolors="white", edgecolors="black"
            )

            patches = [Patch(color=c) for c in color_dict.values()]
            patch_labels = list(labeldict.values())

            err = ErrorbarContainer(
                (line, (), (barline,)), has_xerr=True, has_yerr=True
            )

            handles: list[Artist | ErrorbarContainer] = [sim, individual, err]
            handles.extend(patches)
            labels = ["Sim (750 mg)", "Individual", r"Data Mean$\pm$SD"]
            labels.extend(patch_labels)

            ax.legend(
                handles=handles,
                labels=labels,
                loc="upper left",
                bbox_to_anchor=(1, 1),
                frameon=False,
            )

            ax.set_xlabel("CYP2E1 activity [-]")
            ax.set_ylabel("Cmax 6-OH-CZX + Glu [µM]")
            ax.set_title("Mishin1998")
            return {"fig": fig}


if __name__ == "__main__":
    MODEL.run_experiments(Mishin1998Scan, output_dir="test")
