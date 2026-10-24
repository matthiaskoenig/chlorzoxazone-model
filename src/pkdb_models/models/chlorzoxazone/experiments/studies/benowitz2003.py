"""Simulation experiment of Benowitz2003.

Chlorzoxazone (250 mg po) after an overnight fast in healthy male smokers, the
week without smoking or carbon monoxide (air); chlorzoxazone in plasma (n = 10)
and the recovery of 6-hydroxychlorzoxazone in urine in 24 hr (n = 9). Caffeine
(250 mg po) was given 16 hr before chlorzoxazone (4 PM of the day before), it
does not interact with chlorzoxazone. The weeks with smoking (oral clearance
x1.24) and carbon monoxide are not simulated: the model has no effect of
smoking on CYP2E1.
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


class Benowitz2003(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Benowitz2003.

    Chlorzoxazone single 250 mg dose.
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
                dset_label="chlorzoxazone_Air",
                unit_conversion=1 / self.Mr.czx,
                sim_time_factor=9,
            ),
            "Tab1": HelperMapping(
                id="Tab1",
                plot_ylabel=self.label_czxoglu_urine,
                yid=Sids.aurine_czxoglu,
                unit="mmole",
                dset_label="Tab1_recovery_Dcaf_Dchlo",
                unit_conversion=Q(250, "mg") / self.Mr.czx,
                sim_time_factor=25,
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
        tcsims["czx250"] = Simulation(
            time_unit="min",
            end=25 * 60,
            preinit_changes={
                **self.default_changes(ApplicationForm.TABLET),
                "PODOSE_czx": Q(250, "mg"),
                # Table I: the oral clearance 396 ml/min is 4.8 ml/min/kg (414
                # and 5.0, 488 and 5.9 of the other weeks), 82.5 kg
                "BW": Q(82.5, "kg"),
            },
        )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        tissues = {"Fig1": Tissue.PLASMA, "Tab1": Tissue.URINE}
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
                    self, task="task_czx250", xid="time", yid=required(hm.yid)
                ),
                metadata=PKPDMappingMetaData(
                    tissue=tissues[fig_id],
                    route=Route.PO,
                    application_form=ApplicationForm.NR,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
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
                name=f"{self.__class__.__name__} {hm.id} (250 mg)",
            )
            plot = fig.create_plots(
                xaxis=Axis(self.label_time, unit="hr", max=hm.sim_time_factor),
                legend=True,
            )[0]

            plot.set_yaxis(label=hm.plot_ylabel, unit=hm.unit, scale="linear")

            plot.add_data(
                task="task_czx250",
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
    MODEL.run_experiments(Benowitz2003, output_dir="test")
