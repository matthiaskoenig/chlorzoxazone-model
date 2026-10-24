"""Simulation experiment of the study Wang2003."""

from collections.abc import Mapping
from typing import ClassVar, NamedTuple, override

from pkpdsim.metadata import (
    ApplicationForm,
    Coadministration,
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


class Group(NamedTuple):
    """A group of the study."""

    #: the body weight in kg
    body_weight: float
    health: Health
    coadministration: Coadministration
    label: str
    color: str


class Wang2003(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Wang2003.

    Chlorzoxazone single 500 mg dose (dosage form not reported, a light
    breakfast 2 hr before) in 10 healthy subjects, 14 patients with type 1
    diabetes and 8 obese patients with type 2 diabetes (BMI 37.5 kg/m²). Serum
    chlorzoxazone (Fig1, mean and SD) and the urinary recovery of total
    6-hydroxychlorzoxazone (after beta-glucuronidase) in 24 hr (Tab3).

    The CL/F of the obese patients with type 2 diabetes is 3.4x that of the
    healthy subjects, an induction of CYP2E1 in obesity which the model has not
    (only the scaling by the body weight): the patients are validation of the
    population, not training data.
    """

    groups: ClassVar[Mapping[str, Group]] = {
        "healthy": Group(
            74.1, Health.HEALTHY, Coadministration.NONE, "healthy", "black"
        ),
        # insulin
        "DT1": Group(
            77.2, Health.T1DM, Coadministration.INSULIN, "type 1 diabetes", "tab:blue"
        ),
        # obese, ACE inhibitors, statins, diuretics, metformin and others
        "DT2": Group(
            106.6,
            Health.T2DM,
            Coadministration.COMEDICATION,
            "obese type 2 diabetes",
            "tab:red",
        ),
    }

    @staticmethod
    def task(group: str) -> str:
        """Get the id of the simulation task of a group.

        Args:
            group: the group.

        Returns:
            The id of the task.
        """
        return "task_czx500" if group == "healthy" else f"task_czx500_{group}"

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df_fig1 = self.load_dataframe("Fig1")
        df_tab3 = self.load_dataframe("Tab3")
        for group in self.groups:
            dset = DataSet.from_df(
                df_fig1[df_fig1["label"] == f"Fig1_{group}"], self.ureg
            )
            dset.unit_conversion("mean", 1 / self.Mr.czx)
            dsets[f"dset_Fig1_{group}"] = dset

            # the recovery in % of the dose as the molar amount of
            # 6-hydroxychlorzoxazone
            dset = DataSet.from_df(
                df_tab3[df_tab3["label"] == f"Tab3_{group}_recovery"], self.ureg
            )
            dset.unit_conversion("mean", Q(500, "mg") / self.Mr.czx)
            dsets[f"dset_Tab3_recovery_{group}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        for group, g in self.groups.items():
            tcsims[self.task(group).removeprefix("task_")] = Simulation(
                time_unit="min",
                end=25 * 60,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "PODOSE_czx": Q(500, "mg"),
                    "BW": Q(g.body_weight, "kg"),
                },
            )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for group, g in self.groups.items():
            for key, dataset, yid, tissue in [
                (f"fm_Fig1_{group}", f"dset_Fig1_{group}", Sids.cpl_czx, Tissue.SERUM),
                (
                    f"fm_Tab3_recovery_{group}",
                    f"dset_Tab3_recovery_{group}",
                    Sids.aurine_czxoglu,
                    Tissue.URINE,
                ),
            ]:
                mappings[key] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=dataset,
                        xid="time",
                        yid="mean",
                        count="count",
                        yid_sd="mean_sd",
                    ),
                    observable=FitData(
                        self, task=self.task(group), xid="time", yid=yid
                    ),
                    metadata=PKPDMappingMetaData(
                        # dosage form not reported, light breakfast 2 hr before
                        tissue=tissue,
                        route=Route.PO,
                        application_form=ApplicationForm.NR,
                        dosing=Dosing.SINGLE,
                        health=g.health,
                        fasting=Fasting.LIGHT_BREAKFAST,
                        data_type=DataType.MEAN,
                        coadministration=g.coadministration,
                    ),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig1",
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} Fig1 and Tab3 (500 mg)",
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_xaxis(label=self.label_time, unit="hr", min=0, max=11)
        plots[0].set_yaxis(label=self.label_czx, unit="µM", scale="log", min=0.1)
        plots[1].set_yaxis(
            label=self.labels[Sids.aurine_czxoglu], unit="mmole", scale="linear"
        )
        for group, g in self.groups.items():
            for plot, dataset, yid in [
                (plots[0], f"dset_Fig1_{group}", Sids.cpl_czx),
                (plots[1], f"dset_Tab3_recovery_{group}", Sids.aurine_czxoglu),
            ]:
                plot.add_data(
                    task=self.task(group),
                    xid="time",
                    yid=yid,
                    label=f"Sim {g.label}",
                    color=g.color,
                )
                plot.add_data(
                    dataset=dataset,
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"Data {g.label}",
                    color=g.color,
                )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Wang2003, output_dir="test")
