"""Simulation experiment of Girre1994.

Chlorzoxazone (500 mg po, tablet) in the healthy subjects (nonalcoholics) of
the study; chlorzoxazone and 6-hydroxychlorzoxazone in plasma and the cumulative
amount of 6-hydroxychlorzoxazone in urine.
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
from sbmlsim.plot.plotting import AxisScale
from sbmlsim.simulation import Simulation

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    HelperMapping,
    Sids,
    required,
)
from pkdb_models.models.chlorzoxazone.plot_colors import plot_colors_sid


class Girre1994(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Girre1994.

    Chlorzoxazone single 500 mg dose.
    """

    @property
    def FigMeta(self) -> dict[str, HelperMapping]:
        """Datasets of the healthy controls by figure.

        `sim_time_factor` is the end of the time axis of the figure in hr. The
        plasma 6-hydroxychlorzoxazone (Fig2) and the urine (Fig3) were measured
        after the hydrolysis with Helix pomatia juice, i.e. the total
        6-hydroxychlorzoxazone. The alcoholics of the study are compared in
        `alcohol_model/girre1994_lucas1993_induction.py`.
        """
        return {
            "Fig1": HelperMapping(
                id="czx",
                sim_time_factor=9,
                mr=self.Mr.czx,
                yid=Sids.cpl_czx,
                plot_ylabel=self.label_czx,
                unit="µM",
            ),
            "Fig2": HelperMapping(
                id="czx6oh",
                sim_time_factor=9,
                mr=self.Mr.czx6oh,
                yid=Sids.cve_czx6oh_all,
                plot_ylabel=self.label_czx6oh_all,
                unit="µM",
            ),
            "Fig3": HelperMapping(
                id="cumulative amount",
                sim_time_factor=25,
                mr=self.Mr.czx6oh,
                yid=Sids.aurine_czxoglu,
                plot_ylabel=self.label_czxoglu_urine,
                unit="mmole",
            ),
        }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id, fig_meta in self.FigMeta.items():
            df = self.load_dataframe(fig_id)
            for group, df_label in df.groupby("group"):
                if group == "healthy":
                    dset = DataSet.from_df(df_label, self.ureg)
                    dset.unit_conversion("mean", 1 / required(fig_meta.mr))
                    dsets[self.to_sid(f"ds_{fig_meta.id}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        # 12 hr fast; the body weight is not reported ("within 20 % of ideal"),
        # the reference weight of the model
        tcsims["czx"] = Simulation(
            time_unit="min",
            end=25 * 60,
            preinit_changes={
                **self.default_changes(ApplicationForm.TABLET),
                "PODOSE_czx": Q(500, "mg"),
            },
        )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for fig_id, fig_meta in self.FigMeta.items():
            mappings[self.to_sid(f"fm_{fig_meta.id}_500")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"ds_{fig_meta.id}"),
                    xid="time",
                    yid="mean",
                    count="count",
                    yid_sd="mean_sd",
                ),
                observable=FitData(
                    self,
                    task="task_czx",
                    xid="time",
                    yid=required(fig_meta.yid),
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.URINE if fig_id == "Fig3" else Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
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
        for fig_id, fig_meta in self.FigMeta.items():
            sim_time = required(fig_meta.sim_time_factor)
            color = plot_colors_sid[required(fig_meta.yid)]
            fig = Figure(
                experiment=self,
                sid=self.to_sid(fig_id),
                num_rows=1,
                num_cols=1,
                name=f"{self.__class__.__name__} {fig_id} (500 mg)",
            )

            plot = fig.create_plots(
                xaxis=Axis(
                    self.label_time,
                    unit="hr",
                    min=-0.05 * sim_time,
                    max=sim_time,
                ),
                # the SD of the means of 20 subjects reach below 0
                yaxis=Axis(
                    fig_meta.plot_ylabel,
                    unit=fig_meta.unit,
                    scale=AxisScale.LINEAR,
                    min=0,
                ),
                legend=True,
            )[0]

            plot.add_data(
                task="task_czx",
                xid="time",
                yid=required(fig_meta.yid),
                label="Sim",
                color=color,
            )

            plot.add_data(
                dataset=self.to_sid(f"ds_{fig_meta.id}"),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="Data nonalcoholics",
                color=color,
            )
            figures[self.to_sid(fig_id)] = fig

        return figures


if __name__ == "__main__":
    MODEL.run_experiments(Girre1994, output_dir="test")
