"""Simulation experiment of Chalasani2003.

Chlorzoxazone (500 mg po, formulation not reported) in obese subjects without
NASH (BMI 31), the control group of the study; chlorzoxazone in serum and the
recovery of 6-hydroxychlorzoxazone (after beta-glucuronidase) in urine in
0-8 hr. The patients with NASH (oral clearance 41 vs 33 l/hr) are not
simulated: the model has no factor of CYP2E1 in NASH.
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
    HelperMapping,
    Sids,
    required,
)
from pkdb_models.models.chlorzoxazone.plot_colors import plot_colors_sid


class Chalasani2003(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Chalasani2003.

    Chlorzoxazone single 500 mg dose.
    """

    @property
    def FigMeta(self) -> dict[str, HelperMapping]:
        """Datasets of the study by figure or table.

        The recovery of 6-hydroxychlorzoxazone in urine is a percentage of the
        dose, converted to the amount with the dose.
        """
        return {
            "Fig1": HelperMapping(
                id="Fig1",
                plot_ylabel=self.label_czx,
                yid=Sids.cpl_czx,
                unit="µM",
                dset_label="Fig1_healthy_chlorzoxazone",
                unit_conversion=1 / self.Mr.czx,
            ),
            "Tab1": HelperMapping(
                id="Tab1",
                plot_ylabel=self.label_czxoglu_urine,
                yid=Sids.aurine_czxoglu,
                unit="mmole",
                dset_label="Tab1_healthy_recovery_6-hydroxychlorzoxazone",
                unit_conversion=Q(500, "mg") / self.Mr.czx,
            ),
        }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for hm in self.FigMeta.values():
            df = self.load_dataframe(required(hm.id))
            df = df[df["label"] == hm.dset_label]

            dset = DataSet.from_df(df, self.ureg)
            dset.unit_conversion("mean", required(hm.unit_conversion))
            dsets[f"dset_{hm.id}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        tcsims["czx500"] = Simulation(
            time_unit="min",
            end=9 * 60,
            preinit_changes={
                **self.default_changes(ApplicationForm.TABLET),
                "PODOSE_czx": Q(500, "mg"),
                # body weight from the BMI of the group (31 kg/m^2), assumed height 1.70 m
                "BW": Q(31 * 1.70**2, "kg"),
            },
        )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        tissues = {"Fig1": Tissue.SERUM, "Tab1": Tissue.URINE}
        for fig_id, hm in self.FigMeta.items():
            mappings[f"fm_{fig_id}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"dset_{hm.id}",
                    xid="time",
                    yid="mean",
                    count="count",
                    yid_sd="mean_sd",
                ),
                observable=FitData(
                    self, task="task_czx500", xid="time", yid=required(hm.yid)
                ),
                metadata=PKPDMappingMetaData(
                    tissue=tissues[fig_id],
                    route=Route.PO,
                    application_form=ApplicationForm.NR,
                    dosing=Dosing.SINGLE,
                    health=Health.OBESE,
                    fasting=Fasting.NR,
                    data_type=DataType.MEAN,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        figures = {}
        for fig_id, hm in self.FigMeta.items():
            color = plot_colors_sid[required(hm.yid)]
            fig = Figure(
                experiment=self,
                sid=fig_id,
                num_rows=1,
                num_cols=1,
                name=f"{self.__class__.__name__} {hm.id} (500 mg)",
            )
            plot = fig.create_plots(
                xaxis=Axis(self.label_time, unit="hr"), legend=True
            )[0]

            plot.set_yaxis(label=hm.plot_ylabel, unit=hm.unit, scale="linear")

            plot.add_data(
                task="task_czx500",
                xid="time",
                yid=required(hm.yid),
                label="Sim",
                color=color,
            )

            plot.add_data(
                dataset=f"dset_{fig_id}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="Data",
                color=color,
            )
            figures[f"fig_{fig_id}"] = fig

        return figures


if __name__ == "__main__":
    MODEL.run_experiments(Chalasani2003, output_dir="test")
