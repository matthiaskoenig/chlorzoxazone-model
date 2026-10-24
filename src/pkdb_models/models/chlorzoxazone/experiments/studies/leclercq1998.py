"""Simulation experiment of the study Leclercq1998."""

from collections.abc import Mapping
from dataclasses import dataclass
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
from sbmlsim.units import Quantity

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    HelperMapping,
    Sids,
    required,
)


@dataclass(frozen=True)
class Arm:
    """An arm of the crossover: the curation label and the interaction."""

    #: prefix of the labels of the curation
    label: str
    #: key of the interaction (`interactions` of the base), None at baseline
    interaction: str | None
    #: label of the figure
    legend: str
    #: color of the figure
    color: str


class Leclercq1998(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Leclercq1998.

    Chlorzoxazone single 500 mg dose (one capsule of the hospital pharmacy) with
    250 ml water after an overnight fast, no food until 2 hr after the dose, in
    a crossover of 10 healthy volunteers: at baseline (day 1), after 50 g of
    watercress homogenate the evening before (day 7) and after isoniazid 300
    mg/day for 7 days, the last dose 2 hr before chlorzoxazone (day 14). Plasma
    after hydrolysis with Helix pomatia juice (total chlorzoxazone and
    6-hydroxychlorzoxazone). Fig. 1 shows subject 4 in all arms (AUC 34.6,
    56.9 and 115.9 mg*h/l against the means 46.7, 70.9 and 104.9).

    The body weight of subject 4 is not reported (group 48-80 kg): the default
    body weight of the model. The inhibition of CYP2E1 by watercress and
    isoniazid are the literature factors of the mean AUC ratios of the study
    (`interactions` of the base), not fitted.
    """

    arms: ClassVar[Mapping[str, Arm]] = {
        "czx500": Arm("CZX500", None, "baseline", "black"),
        "czx500_watercress": Arm(
            "WATERCRESS_CZX500", "watercress", "watercress", "tab:green"
        ),
        "czx500_isoniazid": Arm(
            "ISONIAZID_CZX500", "isoniazid", "isoniazid", "tab:red"
        ),
    }

    @property
    def FigMeta(self) -> dict[str, HelperMapping]:
        """Datasets of the study by their substance."""
        return {
            "czx": HelperMapping(
                yid=Sids.cpl_czx,
                plot_ylabel=self.label_czx,
                dset_label="chlorzoxazone",
                mr=self.Mr.czx,
                unit="µM",
            ),
            "czx6oh": HelperMapping(
                yid=Sids.cve_czx6oh_all,
                plot_ylabel=self.label_czx6oh_all,
                dset_label="6-hydroxychlorzoxazone",
                mr=self.Mr.czx6oh,
                unit="µM",
            ),
        }

    @staticmethod
    def dset_key(substance: str, task: str) -> str:
        """Get the key of the dataset of a substance and arm."""
        suffix = task.removeprefix("czx500")
        return f"dset_Fig1_{substance}{suffix}"

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig1")
        for substance, hm in self.FigMeta.items():
            for task, arm in self.arms.items():
                label = f"{arm.label}_{hm.dset_label}"
                dset = DataSet.from_df(df[df["label"] == label], self.ureg)
                dset.unit_conversion("value", 1 / required(hm.mr))
                dsets[self.dset_key(substance, task)] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        for task, arm in self.arms.items():
            changes: dict[str, Quantity] = {
                **self.default_changes(ApplicationForm.TABLET),
                "PODOSE_czx": Q(500, "mg"),
            }
            if arm.interaction:
                # inhibition of CYP2E1, the activity of the literature
                changes.update(
                    {
                        k: Q(v, "dimensionless")
                        for k, v in self.interactions[arm.interaction].items()
                    }
                )
            tcsims[task] = Simulation(
                time_unit="min", end=9 * 60, preinit_changes=changes
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for substance, hm in self.FigMeta.items():
            for task, arm in self.arms.items():
                dset_key = self.dset_key(substance, task)
                mappings[f"fm_{dset_key.removeprefix('dset_')}_500"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=dset_key,
                        xid="time",
                        yid="value",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_{task}", xid="time", yid=required(hm.yid)
                    ),
                    # subject 4, one 500 mg capsule
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.PLASMA,
                        route=Route.PO,
                        application_form=ApplicationForm.CAPSULE,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        # pkpdsim has no vocabulary member of watercress or
                        # isoniazid
                        coadministration=Coadministration.COMEDICATION
                        if arm.interaction
                        else Coadministration.NONE,
                        data_type=DataType.INDIVIDUAL,
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
            name=f"{self.__class__.__name__} Fig1 (500 mg, subject 4)",
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        for plot, (substance, hm) in zip(plots, self.FigMeta.items(), strict=True):
            plot.set_yaxis(
                label=required(hm.plot_ylabel), unit=hm.unit, scale=AxisScale.LINEAR
            )
            yid = required(hm.yid)
            for task, arm in self.arms.items():
                color = arm.color
                plot.add_data(
                    task=f"task_{task}",
                    xid="time",
                    yid=yid,
                    label=f"Sim {arm.legend}",
                    color=color,
                )
                plot.add_data(
                    dataset=self.dset_key(substance, task),
                    xid="time",
                    yid="value",
                    count="count",
                    label=f"Data {arm.legend}",
                    color=color,
                )

        return {"fig_Fig1": fig}


if __name__ == "__main__":
    MODEL.run_experiments(Leclercq1998, output_dir="test")
