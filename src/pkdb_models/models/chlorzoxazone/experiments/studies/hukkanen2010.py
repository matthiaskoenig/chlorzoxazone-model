"""Simulation experiment of the study Hukkanen2010.

Chlorzoxazone (250 mg po, tablet) in 12 smokers after 7 days of placebo
patches (crossover with nicotine patches, which had no effect); the urinary
recovery of 6-hydroxychlorzoxazone in 24 hr (Table 5, total after hydrolysis).
"""

from typing import override

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
    HelperMapping,
    Sids,
    required,
)
from pkdb_models.models.chlorzoxazone.plot_colors import plot_colors_sid


class Hukkanen2010(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Hukkanen2010.

    Chlorzoxazone single 250 mg dose.
    """

    @property
    def FigMeta(self) -> dict[str, HelperMapping]:
        """Datasets of the study by their figure id."""
        return {
            "Tab5": HelperMapping(
                id="Tab5",
                plot_ylabel=self.label_czxoglu_urine,
                yid=Sids.aurine_czxoglu,
                sim_time_factor=25,
                unit="mmole",
                dset_label="Tab1_placebo_recovery_6-hydroxychlorzoxazone",
                unit_conversion=Q(250, "mg") / self.Mr.czx,
                dset_yid="mean",
            ),
        }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for hm in self.FigMeta.values():
            df = self.load_dataframe(required(hm.id))
            df = df[df["label"] == hm.dset_label]

            dset = DataSet.from_df(df, self.ureg)
            dset.unit_conversion(hm.dset_yid, required(hm.unit_conversion))
            dsets[f"dset_{hm.id}"] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}

        # the mean body weight of the 12 subjects (67 +- 11 kg)
        tcsims["czx250"] = Simulation(
            time_unit="min",
            end=25 * 60,
            preinit_changes={
                **self.default_changes(ApplicationForm.TABLET),
                "PODOSE_czx": Q(250, "mg"),
                "BW": Q(67, "kg"),
            },
        )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for hm in self.FigMeta.values():
            mappings[f"fm_{hm.id}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"dset_{hm.id}",
                    xid="time",
                    yid=required(hm.dset_yid),
                    count="count",
                    yid_sd="mean_sd" if hm.dset_yid == "mean" else None,
                ),
                observable=FitData(
                    self, task="task_czx250", xid="time", yid=required(hm.yid)
                ),
                # placebo arm; bupropion 75 mg (CYP2B6 probe) 4 hr and breakfast 2 hr before
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.URINE,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FED,
                    data_type=DataType.MEAN,
                    coadministration=Coadministration.COCKTAIL,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        figures = {}
        for fig_id, hm in self.FigMeta.items():
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

            yid = required(hm.yid)
            plot.add_data(
                task="task_czx250",
                xid="time",
                yid=yid,
                label="Sim",
                color=plot_colors_sid[yid],
            )

            plot.add_data(
                dataset=f"dset_{fig_id}",
                xid="time",
                yid=required(hm.dset_yid),
                yid_sd="mean_sd" if hm.dset_yid == "mean" else None,
                count="count",
                label="Data",
                color=plot_colors_sid[yid],
            )
            figures[f"fig_{fig_id}"] = fig

        return figures


if __name__ == "__main__":
    MODEL.run_experiments(Hukkanen2010, output_dir="test")
