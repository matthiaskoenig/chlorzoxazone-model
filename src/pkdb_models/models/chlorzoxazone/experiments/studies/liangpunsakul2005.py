"""Simulation experiment of the study Liangpunsakul2005."""

from collections.abc import Mapping
from typing import ClassVar, override

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
from sbmlsim.plot.plotting import AxisScale
from sbmlsim.simulation import Simulation

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    HelperMapping,
    Sids,
    required,
)


class Liangpunsakul2005(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Liangpunsakul2005.

    Chlorzoxazone single 500 mg dose (formulation not reported) in 20 moderate
    drinkers (140-210 g ethanol per week, 91 kg, 178 cm) and 20 matched
    non-drinkers (95 kg, 177 cm, Table 1); serum, urinary
    6-hydroxychlorzoxazone after hydrolysis with beta-glucuronidase (65 % and
    61 % of the dose). Chlorzoxazone 8 hr after iv midazolam (CYP3A probe) and
    4 hr after a standard meal.

    The collection interval of the urine is not reported: the subjects were
    discharged after the 8 hr sample, the recovery is compared at 8 hr. The
    model has no induction of CYP2E1 by drinking (CL/F 31.5 against 23.4 l/hr).
    """

    @property
    def FigMeta(self) -> dict[str, HelperMapping]:
        """Datasets of the study by their id, one per group and measurement."""
        return {
            "Fig1_control": HelperMapping(
                id="Fig1",
                yid=Sids.cpl_czx,
                plot_ylabel=self.label_czx,
                unit="µM",
                unit_conversion=1 / self.Mr.czx,
                task_id="control",
                plot_legend_label="non-drinkers",
                dset_label="Fig1_CZX_no_alcohol",
            ),
            "Fig1_alcohol": HelperMapping(
                id="Fig1",
                yid=Sids.cpl_czx,
                plot_ylabel=self.label_czx,
                unit="µM",
                unit_conversion=1 / self.Mr.czx,
                task_id="alcohol",
                plot_legend_label="moderate drinkers",
                dset_label="Fig1_CZX_alcohol",
            ),
            # the recovery in percent of the dose, as mmole of the dose
            "Tab2_control": HelperMapping(
                id="Tab2",
                yid=Sids.aurine_czxoglu,
                plot_ylabel=self.label_czxoglu_urine,
                unit="mmole",
                unit_conversion=Q(500, "mg") / self.Mr.czx,
                task_id="control",
                plot_legend_label="non-drinkers",
                dset_label="Tab2_CZX_no_alcohol_recovery",
            ),
            "Tab2_alcohol": HelperMapping(
                id="Tab2",
                yid=Sids.aurine_czxoglu,
                plot_ylabel=self.label_czxoglu_urine,
                unit="mmole",
                unit_conversion=Q(500, "mg") / self.Mr.czx,
                task_id="alcohol",
                plot_legend_label="moderate drinkers",
                dset_label="Tab2_CZX_alcohol_recovery",
            ),
        }

    #: body weight (kg) and height (cm) of the groups (Table 1)
    groups: ClassVar[Mapping[str, tuple[float, float]]] = {
        "control": (95.0, 177.0),
        "alcohol": (91.0, 178.0),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id, hm in self.FigMeta.items():
            df = self.load_dataframe(required(hm.id))
            dset = DataSet.from_df(df[df["label"] == hm.dset_label], self.ureg)
            dset.unit_conversion("mean", required(hm.unit_conversion))
            dsets[f"dset_{fig_id}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            task_id: Simulation(
                time_unit="min",
                end=9 * 60,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "PODOSE_czx": Q(500, "mg"),
                    "BW": Q(bw, "kg"),
                    "HEIGHT": Q(height, "cm"),
                },
            )
            for task_id, (bw, height) in self.groups.items()
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for fig_id, hm in self.FigMeta.items():
            mappings[f"fm_{fig_id}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"dset_{fig_id}",
                    xid="time",
                    yid="mean",
                    count="count",
                    yid_sd="mean_sd",
                ),
                observable=FitData(
                    self, task=f"task_{hm.task_id}", xid="time", yid=required(hm.yid)
                ),
                # chlorzoxazone 8 hr after iv midazolam (a CYP3A probe without an
                # interaction with chlorzoxazone, `COCKTAIL`) and 4 hr after a
                # standard meal; dosage form not reported
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.URINE if fig_id.startswith("Tab2") else Tissue.SERUM,
                    route=Route.PO,
                    application_form=ApplicationForm.NR,
                    dosing=Dosing.SINGLE,
                    health=(
                        Health.MODERATE_DRINKING
                        if hm.task_id == "alcohol"
                        else Health.HEALTHY
                    ),
                    fasting=Fasting.FED,
                    data_type=DataType.MEAN,
                    coadministration=Coadministration.COCKTAIL,
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
            name=f"{self.__class__.__name__} (500 mg)",
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(label=self.label_czx, unit="µM", scale=AxisScale.LINEAR)
        plots[1].set_yaxis(
            label=self.label_czxoglu_urine, unit="mmole", scale=AxisScale.LINEAR
        )
        colors = {"control": "black", "alcohol": "tab:red"}
        for plot, prefix in zip(plots, ["Fig1", "Tab2"], strict=True):
            for task_id, color in colors.items():
                fig_id = f"{prefix}_{task_id}"
                hm = self.FigMeta[fig_id]
                yid = required(hm.yid)
                plot.add_data(
                    task=f"task_{task_id}",
                    xid="time",
                    yid=yid,
                    label=f"Sim {hm.plot_legend_label}",
                    color=color,
                )
                plot.add_data(
                    dataset=f"dset_{fig_id}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"Data {hm.plot_legend_label}",
                    color=color,
                )

        return {"fig_Fig1": fig}


if __name__ == "__main__":
    MODEL.run_experiments(Liangpunsakul2005, output_dir="test")
