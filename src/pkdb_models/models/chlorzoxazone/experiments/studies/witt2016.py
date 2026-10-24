"""Simulation experiment of the study Witt2016."""

from typing import ClassVar, override

import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.artist import Artist
from matplotlib.axes import Axes
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
from sbmlsim.units import Quantity

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    LineStyle,
    Sids,
    hex_color,
)
from pkdb_models.models.chlorzoxazone.models import rcParams
from pkdb_models.models.chlorzoxazone.plot_colors import cmap_blues, cmap_greys


def get_observable(substance: str) -> str:
    """Get the plasma concentration of the model for a substance of the data.

    Args:
        substance: substance of the data, chlorzoxazone or 6-hydroxychlorzoxazone.

    Returns:
        The id of the observable.
    """
    return "[Cveplasma_czx]" if substance == "chlorzoxazone" else "[Cve_czx6oh]"


class Witt2016(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Witt2016.

    Ascending single oral doses of chlorzoxazone as an aqueous solution (Paraflex
    tablets dissolved) in two healthy volunteers, 48 hr apart: volunteer 1 2.5,
    25, 250 and 2500 µg, volunteer 2 5, 50, 500 and 5000 µg. Plasma
    chlorzoxazone and free 6-hydroxychlorzoxazone (UPLC-MS/MS without
    hydrolysis), individual data (Fig3). The pharmacokinetics are linear over
    the 2000x range (Vz/F 33-77 l, CL/F 17-47 l/hr without a trend). Sex, age
    and body weight are not reported, the model has its default body weight.
    """

    dose_dict: ClassVar[dict[str, float]] = {
        "CZX1": 0.0025,
        "CZX2": 0.005,
        "CZX3": 0.025,
        "CZX4": 0.05,
        "CZX5": 0.250,
        "CZX6": 0.5,
        "CZX7": 2.5,
        "CZX8": 5,
    }  # [mg]

    substances: ClassVar[list[str]] = ["chlorzoxazone", "6-hydroxychlorzoxazone"]

    def get_mr(self, label: str) -> Quantity:
        """Get the molecular weight of the substance of a dataset.

        Args:
            label: label of the dataset.

        Returns:
            The molecular weight.
        """
        return self.Mr.czx6oh if "6-hydroxy" in label else self.Mr.czx

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig3")
        df = df[df["time"] > 0]
        for label, df_label in df.groupby("label"):
            label = str(label)
            dset = DataSet.from_df(df_label, self.ureg)
            dset.unit_conversion("value", 1 / self.get_mr(label))
            dsets[self.to_sid(label)] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}

        for dose in self.dose_dict:
            tcsims[self.to_sid(f"{dose}")] = Simulation(
                time_unit="min",
                end=9 * 60,
                preinit_changes={
                    **self.default_changes(ApplicationForm.SOLUTION),
                    "PODOSE_czx": Q(self.dose_dict[dose], "mg"),
                },
            )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for substance in self.substances:
            for dose in self.dose_dict:
                if substance == "6-hydroxychlorzoxazone" and dose == "CZX1":
                    continue
                mappings[self.to_sid(f"fm_{dose}_{substance}")] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"Fig3_{dose}_{substance}"),
                        xid="time",
                        yid="value",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=self.to_sid(f"task_{dose}"),
                        xid="time",
                        yid=get_observable(substance),
                    ),
                    metadata=PKPDMappingMetaData(
                        # microdoses of dissolved Paraflex tablets, one volunteer per dose
                        tissue=Tissue.PLASMA,
                        route=Route.PO,
                        application_form=ApplicationForm.SOLUTION,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.NR,
                        data_type=DataType.INDIVIDUAL,
                    ),
                )

        return mappings

    def plot_witt(self) -> dict[str, FigureMPL]:
        """Plot the concentrations of all doses on a log scale (Fig3).

        Returns:
            The matplotlib figures by the label of the substance as an id
            (`to_sid`, e.g. `6_OH_CZX`).
        """
        figures: dict[str, FigureMPL] = {}
        cmaps = [cmap_greys, cmap_blues]
        dsets = self._datasets

        for k, (sid, label, cmap) in enumerate(
            zip(
                [Sids.cpl_czx, Sids.cve_czx6oh],
                [self.label_czx, self.label_czx6oh],
                cmaps,
                strict=True,
            )
        ):
            fig: FigureMPL
            ax: Axes
            fig, ax = plt.subplots(1, 1, figsize=(7, 5), dpi=300)
            ax.set_xlabel("time [hr]")
            ax.set_ylabel(f"{label} [µM]")
            ax.set_yscale("log")
            fig.suptitle("Witt2016 Fig3")
            dose_handles: list[Artist] = []
            dose_labels: list[str] = []
            for i, (intervention, dose) in enumerate(self.dose_dict.items()):
                color = hex_color(cmap(i / (len(self.dose_dict) - 1)))
                dset = dsets.get(
                    self.to_sid(f"Fig3_{intervention}_{self.substances[k]}")
                )
                if dset is None:
                    continue
                ax.plot(
                    dset["time"],
                    Q(dset["value"], dset["value_unit"].values[0]).to("µM").magnitude,
                    color=color,
                    marker="v"
                    if intervention in ["CZX1", "CZX3", "CZX5", "CZX7"]
                    else "s",
                    linestyle="--",
                    markeredgecolor="black",
                )
                res = self.results[self.to_sid(f"task_{intervention}")]
                self.plot_timecourse(ax, res, sid, ("hr", "µM"), LineStyle(color=color))
                dose_handles.append(Patch(color=color))
                dose_labels.append(f"{dose} mg")

            line1 = Line2D([], [], marker="v", ls="--", color="black")
            line2 = Line2D([], [], marker="s", ls="--", color="black")
            line_sim = Line2D([], [], ls="-", color="black")

            handles: list[Artist] = [line_sim, line1, line2]
            labels = ["Sim", "Subject 1", "Subject 2"]

            handles.extend(dose_handles)
            labels.extend(dose_labels)

            ax.legend(
                handles=handles,
                labels=labels,
                loc="upper left",
                bbox_to_anchor=(1, 1),
                frameon=False,
            )

            ax.set_ylim(bottom=1e-8)
            # the label of the substance as an id, the name of the file
            figures[self.to_sid(label)] = fig

        return figures

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        with mpl.rc_context(rcParams):
            return self.plot_witt()

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Fig3"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(name),
            num_rows=2,
            num_cols=1,
            name=f"{self.__class__.__name__} {name}",
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        for plot, label in zip(plots, [self.label_czx, self.label_czx6oh], strict=True):
            # the doses span 2000x, the concentrations 5 decades
            plot.set_yaxis(label=label, unit="µM", scale="log", min=1e-6)

        cmap = plt.get_cmap("coolwarm")

        for i, substance in enumerate(self.substances):
            for k_dose, dose in enumerate(self.dose_dict):
                # the two individuals
                marker = "v" if dose in ["CZX1", "CZX3", "CZX5", "CZX7"] else "s"
                if substance == "6-hydroxychlorzoxazone" and dose == "CZX1":
                    continue
                # simulation
                plots[i].add_data(
                    task=self.to_sid(f"task_{dose}"),
                    xid="time",
                    yid=get_observable(substance),
                    label=f"Sim {self.dose_dict[dose]} [mg]",
                    color=hex_color(cmap(k_dose / (len(self.dose_dict) - 1))),
                )

                plots[i].add_data(
                    dataset=self.to_sid(f"Fig3_{dose}_{substance}"),
                    xid="time",
                    yid="value",
                    count="count",
                    label=f"{self.dose_dict[dose]} [mg]",
                    color=hex_color(cmap(k_dose / (len(self.dose_dict) - 1))),
                    marker=marker,
                )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Witt2016, output_dir="test")
