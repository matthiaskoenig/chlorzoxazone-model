"""Simulation experiment of the study Kharasch1993.

Chlorzoxazone (750 mg po, tablet) in 6 healthy men without and with disulfiram
(500 mg 10 hr before, crossover); chlorzoxazone in plasma of one subject (Fig2)
and the urinary recovery of 6-hydroxychlorzoxazone in 24 hr (Table II, total
after hydrolysis).
"""

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
from sbmlsim.plot import Figure
from sbmlsim.simulation import Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    Sids,
)


class Arm(NamedTuple):
    """A phase of the study (control or disulfiram) for the subjects of a dataset."""

    #: body weight of the subjects [kg]
    bw: float
    #: disulfiram before chlorzoxazone
    disulfiram: bool


class Data(NamedTuple):
    """A dataset of the study with its simulation and observable."""

    #: figure or table of the data
    fig_id: str
    #: label of the data
    dset_label: str
    #: the arm (simulation) of the data
    arm: str
    #: the observable
    yid: Sids
    #: individual data (`value`) or the mean of the group (`mean`)
    individual: bool


class Kharasch1993(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Kharasch1993.

    Chlorzoxazone single 750 mg dose, control and disulfiram phase.
    """

    #: the arms by their task: the group (79 +- 12 kg, Table I) and the
    #: "representative subject" of Fig2, subject 5 (89 kg): the peaks of 15.9
    #: (control) and 27.9 µg/ml (disulfiram) and the half-life of 0.96 hr of the
    #: figure are the Cmax of 15.6 and 27.6 µg/ml and the half-life of 0.91 hr of
    #: subject 5 in Table I, no other subject fits
    arms: ClassVar[dict[str, Arm]] = {
        "czx750": Arm(bw=79, disulfiram=False),
        "czx750_dsf": Arm(bw=79, disulfiram=True),
        "czx750_s5": Arm(bw=89, disulfiram=False),
        "czx750_dsf_s5": Arm(bw=89, disulfiram=True),
    }

    #: the datasets by their key: chlorzoxazone in plasma of subject 5 (Fig2,
    #: the control starts at 1.3 hr, the concentrations before were below the
    #: limit of quantification) and 6-hydroxychlorzoxazone in urine in 24 hr in
    #: percent of the dose (Table II)
    curves: ClassVar[dict[str, Data]] = {
        "Fig2": Data("Fig2", "Fig2_TC_1_CZX_", "czx750_s5", Sids.cpl_czx, True),
        "Fig2_dsf": Data(
            "Fig2", "Fig2_TC_1_DSF_CZX", "czx750_dsf_s5", Sids.cpl_czx, True
        ),
        "Tab2Mean": Data(
            "Tab2Mean", "Tab2_recovery_CZX_", "czx750", Sids.aurine_czxoglu, False
        ),
        "Tab2Mean_dsf": Data(
            "Tab2Mean",
            "Tab2_recovery_DSF_CZX",
            "czx750_dsf",
            Sids.aurine_czxoglu,
            False,
        ),
    }

    @staticmethod
    def dset_yid(data: Data) -> str:
        """Get the column of the values of a dataset."""
        return "value" if data.individual else "mean"

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for key, data in self.curves.items():
            df = self.load_dataframe(data.fig_id)
            dset = DataSet.from_df(df[df["label"] == data.dset_label], self.ureg)
            conversion = (
                1 / self.Mr.czx
                if data.yid == Sids.cpl_czx
                # percent of the molar dose
                else Q(750, "mg") / self.Mr.czx
            )
            dset.unit_conversion(self.dset_yid(data), conversion)
            dsets[f"dset_{key}"] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        # overnight fast, a light breakfast 1 hr after the dose
        for task, arm in self.arms.items():
            changes: dict[str, Quantity] = {
                **self.default_changes(ApplicationForm.TABLET),
                "PODOSE_czx": Q(750, "mg"),
                "BW": Q(arm.bw, "kg"),
            }
            if arm.disulfiram:
                # disulfiram 500 mg 10 hr before inactivates CYP2E1 irreversibly,
                # the activities of the literature (`interactions`)
                changes.update(
                    {
                        k: Q(v, "dimensionless")
                        for k, v in self.interactions["disulfiram"].items()
                    }
                )
            tcsims[task] = Simulation(
                time_unit="min", end=25 * 60, preinit_changes=changes
            )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for key, data in self.curves.items():
            arm = self.arms[data.arm]
            mappings[f"fm_{key}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"dset_{key}",
                    xid="time",
                    yid=self.dset_yid(data),
                    count="count",
                    yid_sd=None if data.individual else "mean_sd",
                ),
                observable=FitData(
                    self, task=f"task_{data.arm}", xid="time", yid=data.yid
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA if data.individual else Tissue.URINE,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    # pkpdsim has no vocabulary member of disulfiram
                    coadministration=Coadministration.COMEDICATION
                    if arm.disulfiram
                    else Coadministration.NONE,
                    data_type=DataType.INDIVIDUAL if data.individual else DataType.MEAN,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig2",
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} (750 mg)",
        )
        plots = fig.create_plots(legend=True)
        plots[0].set_xaxis(self.label_time, unit="hr", min=0, max=12.5)
        plots[0].set_yaxis(self.label_czx, unit="µM", scale="log", min=1, max=300)
        plots[1].set_xaxis(self.label_time, unit="hr", min=0, max=25)
        plots[1].set_yaxis(self.label_czxoglu_urine, unit="mmole", scale="linear")
        for plot, keys, subjects in [
            (plots[0], ["Fig2", "Fig2_dsf"], " subject 5"),
            (plots[1], ["Tab2Mean", "Tab2Mean_dsf"], ""),
        ]:
            for key in keys:
                data = self.curves[key]
                disulfiram = self.arms[data.arm].disulfiram
                phase = "disulfiram" if disulfiram else "control"
                color = "tab:red" if disulfiram else "black"
                plot.add_data(
                    task=f"task_{data.arm}",
                    xid="time",
                    yid=data.yid,
                    label=f"Sim {phase}",
                    color=color,
                )
                plot.add_data(
                    dataset=f"dset_{key}",
                    xid="time",
                    yid=self.dset_yid(data),
                    yid_sd=None if data.individual else "mean_sd",
                    count="count",
                    label=f"Data {phase}{subjects}",
                    color=color,
                )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Kharasch1993, output_dir="test")
