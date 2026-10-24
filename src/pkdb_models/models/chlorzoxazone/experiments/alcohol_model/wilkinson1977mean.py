"""Simulation experiment of Wilkinson1977 (mean of the subjects).

Single oral doses of 15, 30, 45 and 60 ml 95% ethanol (11.2 to 45.0 g) diluted with
orange juice in eight fasted subjects: the mean of the capillary blood ethanol of
the subjects (Table II), simulated with their mean body weight and height.
"""

from typing import ClassVar, override

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.collections import LineCollection
from matplotlib.container import ErrorbarContainer
from matplotlib.figure import Figure as FigureMPL
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from pkpdsim.metadata import (
    ApplicationForm,
    DataType,
    Dosing,
    Fasting,
    Health,
    PKPDMappingMetaData,
    Route,
    Tissue,
)
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    LineStyle,
    Sids,
    hex_color,
)
from pkdb_models.models.chlorzoxazone.models import rcParams
from pkdb_models.models.chlorzoxazone.plot_colors import cmap_greys


class Wilkinson1977Mean(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Wilkinson1977 (mean of the subjects)."""

    #: the doses, the volume of 95% ethanol [ml] and its amount of ethanol [g]
    doses: ClassVar[dict[int, float]] = {
        15: 11.24325,
        30: 22.4865,
        45: 33.72975,
        60: 44.973,
    }

    #: the digitized individual curves which are wrong (pkdb_data): Subject2_ETH15
    #: is 10x too low (peak 0.018 against 0.18 mg/ml of Table III and Fig. 1),
    #: Subject4_ETH30 is a copy of Subject3_ETH30 and Subject3_ETH45 a copy of
    #: Subject2_ETH45
    wrong_curves: ClassVar[frozenset[str]] = frozenset(
        {"Subject2_ETH15", "Subject4_ETH30", "Subject3_ETH45"}
    )
    #: the published mean which is a misprint: 0.019 mg/ml at 0.133 hr of 30 ml,
    #: between 0.071 (0.067 hr) and 0.25 (0.2 hr), the curves give 0.16
    misprints: ClassVar[frozenset[tuple[int, float]]] = frozenset({(30, 0.133)})

    @override
    def datasets(self) -> dict[str, DataSet]:
        """The published means of the eight subjects (Table II) with their SD.

        The means are those of Table II, which the digitized individual curves
        of Fig. 1 and 2 reproduce but for three wrong curves (`wrong_curves`);
        the SD is the SD of the correct individual curves at the times of the
        table (the paper gives none). The time 0 (no ethanol) and the misprint
        (`misprints`) are left out.
        """
        dsets = {}
        means = self.load_dataframe("Tab2", study="Wilkinson1977")
        curves = self.load_dataframe("Fig1_2", study="Wilkinson1977")
        curves = curves[~curves["label"].isin(self.wrong_curves)]
        for dose in self.doses:
            df = means[(means["intervention"] == f"ETH{dose}") & (means["time"] > 0)]
            df = df[[(dose, t) not in self.misprints for t in df["time"]]]
            individual = curves[curves["intervention"] == f"ETH{dose}"]
            sd = (
                individual.groupby("time")["value"]
                .std(ddof=1)
                .reindex(df["time"].values)
            )
            count = df["count"].to_numpy()
            pkdb_dummy = pd.DataFrame(
                {
                    "time": df["time"].to_numpy(),
                    "mean": df["mean"].to_numpy(),
                    "sd": sd.to_numpy(),
                    "se": sd.to_numpy() / np.sqrt(count),
                    "unit": df["unit"].to_numpy(),
                    "time_unit": df["time_unit"].to_numpy(),
                    "count": count,
                }
            )

            dset = DataSet.from_df(pkdb_dummy, self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.ethanol)

            dsets[self.to_sid(f"Timecourse_all_ETH{dose}")] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        df = self.load_dataframe("TabIndividuals", study="Wilkinson1977")
        for dose, ethanol in self.doses.items():
            tcsims[self.to_sid(f"sim_{dose}")] = Simulation(
                time_unit="min",
                end=8 * 60,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "GU__PODOSE_ethanol": Q(ethanol, "g"),
                    "BW": Q(np.mean(df["weight"]), "kg"),
                    "HEIGHT": Q(np.mean(df["height"]), "cm"),
                },
            )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for dose in self.doses:
            mappings[self.to_sid(f"fm_{dose}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Timecourse_all_ETH{dose}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    yid_se="mean_se",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_sim_{dose}"),
                    xid="time",
                    yid=Sids.cve_ethanol,
                ),
                metadata=PKPDMappingMetaData(
                    # mean of the eight subjects, capillary blood ethanol
                    tissue=Tissue.BLOOD,
                    route=Route.PO,
                    application_form=ApplicationForm.SOLUTION,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    data_type=DataType.MEAN,
                ),
            )

        return mappings

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        with matplotlib.rc_context(rcParams):
            fig, ax = plt.subplots(1, 1, figsize=(7, 5))

            # legend of the simulations and the data
            handles: list[Line2D | ErrorbarContainer | Patch] = [
                Line2D([], [], color="black")
            ]
            labels = ["Sim"]
            line = Line2D([], [], marker="s", ls="--", color="black")
            barline = LineCollection(list(np.empty((2, 2, 2))), color="black")
            handles.append(
                ErrorbarContainer((line, (), (barline,)), has_xerr=True, has_yerr=True)
            )
            labels.append(r"Wilkinson1977$\pm$SD (n=8)")

            for i, (dose, ethanol) in enumerate(self.doses.items()):
                res = self.results[self.to_sid(f"task_sim_{dose}")]
                dset = self._datasets[self.to_sid(f"Timecourse_all_ETH{dose}")]
                color = hex_color(cmap_greys(i / (len(self.doses) - 1)))

                self.plot_timecourse(
                    ax, res, Sids.cve_ethanol, ("hr", "mM"), LineStyle(color=color)
                )

                ax.errorbar(
                    x=dset["time"],
                    y=Q(dset["mean"], dset["mean_unit"].values[0]).to("mM").magnitude,
                    yerr=Q(dset["mean_sd"], dset["mean_unit"].values[0])
                    .to("mM")
                    .magnitude,
                    color=color,
                    marker="s",
                    markeredgecolor="black",
                    linestyle="--",
                )
                # legend of the dose
                handles.append(Patch(facecolor=color))
                labels.append(f"{dose} mL 95% vol. ({ethanol:.1f} g)")

            ax.legend(handles=handles, labels=labels, frameon=False)
            ax.set_xlabel("Time [hr]")
            ax.set_ylabel("Ethanol [mM]")

            return {"fig": fig}

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Ethanol model"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(name),
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__}",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hour"),
            yaxis=Axis("Ethanol (plasma)", unit="mM"),
            legend=True,
        )
        cmap = matplotlib.colormaps["coolwarm"]
        for i, (dose, ethanol) in enumerate(self.doses.items()):
            color = hex_color(cmap(i / (len(self.doses) - 1)))
            plots[0].add_data(
                task=self.to_sid(f"task_sim_{dose}"),
                xid="time",
                yid=Sids.cve_ethanol,
                label=f"Sim {ethanol:.1f} [g]",
                color=color,
            )
            plots[0].add_data(
                dataset=self.to_sid(f"Timecourse_all_ETH{dose}"),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                label=f"Data {ethanol:.1f} [g]",
                color=color,
            )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Wilkinson1977Mean, output_dir="test")
