"""Simulation experiment of Wilkinson1977.

Single oral doses of 15, 30, 45 and 60 ml 95% ethanol (11.2 to 45.0 g) diluted with
orange juice in eight fasted subjects: capillary blood ethanol of the individuals.
"""

from typing import ClassVar, override

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
    Sids,
)


class Wilkinson1977(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Wilkinson1977 (individuals)."""

    #: the doses, the volume of 95% ethanol [ml] and its amount of ethanol [g]
    doses: ClassVar[dict[int, float]] = {
        15: 11.24325,
        30: 22.4865,
        45: 33.72975,
        60: 44.973,
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig1_2")
        for label, label_df in df.groupby("label"):
            label = str(label)
            dset = DataSet.from_df(label_df, self.ureg)
            dset.unit_conversion("value", 1 / self.Mr.ethanol)
            dsets[self.to_sid(f"Timecourse_{label}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        df = self.load_dataframe("TabIndividuals")
        for dose, ethanol in self.doses.items():
            for _, row in df.iterrows():
                name = row["name"]
                tcsims[self.to_sid(f"{name}_{dose}")] = Simulation(
                    time_unit="min",
                    end=9 * 60,
                    preinit_changes={
                        **self.default_changes(ApplicationForm.TABLET),
                        "GU__PODOSE_ethanol": Q(ethanol, "g"),
                        "BW": Q(row["weight"], "kg"),
                        "HEIGHT": Q(row["height"], "cm"),
                    },
                )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for i in range(1, 9):
            for dose in self.doses:
                mappings[self.to_sid(f"fm_Subject{i}_eth{dose}")] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(f"Timecourse_Subject{i}_ETH{dose}"),
                        xid="time",
                        yid="value",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=self.to_sid(f"task_Subject{i}_{dose}"),
                        xid="time",
                        yid=Sids.cve_ethanol,
                    ),
                    metadata=PKPDMappingMetaData(
                        # 95% ethanol diluted with orange juice, capillary blood ethanol
                        tissue=Tissue.BLOOD,
                        route=Route.PO,
                        application_form=ApplicationForm.SOLUTION,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        data_type=DataType.INDIVIDUAL,
                    ),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Wilkinson Fig1 and Fig2"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(name),
            num_rows=4,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
            # the panels show the same doses: one legend, right of the first
            # row, instead of a legend over the data of every panel
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hour"),
            yaxis=Axis("ethanol plasma conc", unit="mM"),
            legend=True,
        )

        # one panel per subject, one colour per dose
        colors = ["tab:blue", "tab:orange", "tab:green", "tab:red"]
        for i in range(8):
            plots[i].set_title(f"Subject {i + 1}")
            plots[i].legend = i < 2
            for dose, color in zip(self.doses, colors, strict=True):
                plots[i].add_data(
                    task=self.to_sid(f"task_Subject{i + 1}_{dose}"),
                    xid="time",
                    yid=Sids.cve_ethanol,
                    label=f"Sim {dose} ml ethanol 95 %",
                    color=color,
                )
                plots[i].add_data(
                    dataset=self.to_sid(f"Timecourse_Subject{i + 1}_ETH{dose}"),
                    xid="time",
                    yid="value",
                    label=f"{dose} ml ethanol 95 %",
                    color=color,
                )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Wilkinson1977, output_dir="test")
