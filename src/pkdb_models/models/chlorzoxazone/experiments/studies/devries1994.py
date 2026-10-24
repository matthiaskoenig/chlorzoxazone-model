"""Simulation experiment of DeVries1994.

Chlorzoxazone (250 mg po, tablet) in 17 healthy volunteers; the individual
chlorzoxazone time courses in whole blood.
"""

from typing import override

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
from pkdb_models.models.chlorzoxazone.plot_colors import plot_colors_sid

#: notes on the subjects of the study (the abstinence from alcohol)
SUBJECT_NOTES: dict[int, str] = {
    5: "did not abstain from alcohol",
    11: "did not abstain from alcohol, t1/2 3.27 hr",
    13: "abstinence not reported",
    17: "abstinence not reported",
}


class DeVries1994(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of DeVries1994.

    Individual chlorzoxazone time courses in whole blood after a single oral
    250 mg tablet (Geneva Generics, subjects 1-7; McNeil, subjects 8-17) after an
    8 hr fast (7 men, 10 women, 24-52 yr, mixed ethnicity, body weight not
    reported). The data are blood concentrations (blood to plasma ratio 0.51,
    one volunteer), mapped to the blood of the model. The individuals show the
    variability of the CYP2E1 activity (CL/F 258-644 ml/min); subjects 5 and 11
    did not abstain from alcohol, 13 and 17 did not answer (`SUBJECT_NOTES`).
    """

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Fig2"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("individual"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion("value", 1 / self.Mr.czx)
                dsets[f"Timecourse_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        tcsims["po_CZX250"] = Simulation(
            time_unit="min",
            end=11 * 60,
            preinit_changes={
                **self.default_changes(ApplicationForm.TABLET),
                "PODOSE_czx": Q(250, "mg"),
            },
        )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for i in range(1, 18):
            mappings[f"fm_Subject_{i}_po_CZX250"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Timecourse_Subject_{i}",
                    xid="time",
                    yid="value",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_po_CZX250", xid="time", yid=Sids.cbl_czx
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.BLOOD,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    data_type=DataType.INDIVIDUAL,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        figures = {}
        for i in range(1, 18):
            name = f"Subject_{i}"
            note = f" ({SUBJECT_NOTES[i]})" if i in SUBJECT_NOTES else ""
            fig = Figure(
                experiment=self,
                sid=name,
                num_rows=1,
                num_cols=1,
                name=f"{self.__class__.__name__} Subject {i}{note}",
            )

            plots = fig.create_plots(
                xaxis=Axis(self.label_time, unit="hr"), legend=True
            )

            plots[0].set_yaxis(
                label=f"{self.label_czx} (blood)", unit="µM", scale="linear"
            )

            # simulation
            plots[0].add_data(
                task="task_po_CZX250",
                xid="time",
                yid=Sids.cbl_czx,
                label="Sim 250 [mg]",
                color=plot_colors_sid[Sids.cbl_czx],
            )

            plots[0].add_data(
                dataset=f"Timecourse_Subject_{i}",
                xid="time",
                yid="value",
                label=f"Data Subject {i}",
                color=plot_colors_sid[Sids.cbl_czx],
            )

            figures[name] = fig

        return figures


if __name__ == "__main__":
    MODEL.run_experiments(DeVries1994, output_dir="test")
