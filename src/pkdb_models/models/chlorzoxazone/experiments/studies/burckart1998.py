"""Simulation experiment of Burckart1998.

Chlorzoxazone (250 mg po, formulation not reported) as part of the Pittsburgh
cocktail (caffeine, dapsone, mephenytoin, debrisoquine) after an overnight fast
in healthy subjects, the controls of the study of liver transplantation;
chlorzoxazone and the total 6-hydroxychlorzoxazone (after beta-glucuronidase)
in plasma (Fig 4A, n = 16) and the cumulative amount of 6-hydroxychlorzoxazone
in urine in 0-8 hr (Table II). The liver transplant patients are not
simulated.
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


class Burckart1998(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Burckart1998.

    Chlorzoxazone single 250 mg dose.
    """

    @property
    def FigMeta(self) -> dict[str, HelperMapping]:
        """Datasets of the study by figure or table."""
        return {
            "Fig4czx": HelperMapping(
                id="Fig4",
                mr=self.Mr.czx,
                plot_ylabel=self.label_czx,
                yid=Sids.cpl_czx,
                unit="µM",
                dset_label="Fig1_healthy_chlorzoxazone",
            ),
            "Fig4czx6oh": HelperMapping(
                id="Fig4",
                mr=self.Mr.czx6oh,
                plot_ylabel=self.label_czx6oh_all,
                yid=Sids.cve_czx6oh_all,
                unit="µM",
                dset_label="Fig1_healthy_6-hydroxychlorzoxazone",
            ),
            "Tab2urine": HelperMapping(
                id="Tab2",
                # Table II: 158.6 mg of 6-hydroxychlorzoxazone in 0-8 hr
                mr=self.Mr.czx6oh,
                plot_ylabel=self.label_czxoglu_urine,
                yid=Sids.aurine_czxoglu,
                unit="mmole",
                dset_label="Tab2_healthy_cumulative amount_6-hydroxychlorzoxazone",
            ),
        }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id, hm in self.FigMeta.items():
            df = self.load_dataframe(required(hm.id))
            dset = DataSet.from_df(df[df["label"] == hm.dset_label], self.ureg)
            dset.unit_conversion("mean", 1 / required(hm.mr))
            dsets[f"dset_{fig_id}"] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        tcsims["czx250"] = Simulation(
            time_unit="min",
            end=11 * 60,
            preinit_changes={
                **self.default_changes(ApplicationForm.TABLET),
                "PODOSE_czx": Q(250, "mg"),
                "BW": Q(80.6, "kg"),
            },
        )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        tissues = {
            "Fig4czx": Tissue.PLASMA,
            "Fig4czx6oh": Tissue.PLASMA,
            "Tab2urine": Tissue.URINE,
        }
        for fig_id, hm in self.FigMeta.items():
            mappings[f"fm_{fig_id}_250"] = FitMapping(
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
                    coadministration=Coadministration.COCKTAIL,
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
                xaxis=Axis(self.label_time, unit="hr"), legend=True
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
    MODEL.run_experiments(Burckart1998, output_dir="test")
