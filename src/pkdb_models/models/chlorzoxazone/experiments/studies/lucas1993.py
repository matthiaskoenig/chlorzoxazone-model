"""Simulation experiment of the study Lucas1993."""

from collections.abc import Mapping
from typing import ClassVar, override

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
from sbmlsim.plot import Figure
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


class Lucas1993(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Lucas1993.

    Chlorzoxazone single 500 mg tablet after a 12 hr fast in 5 healthy men and
    5 alcoholic patients without cirrhosis (body weight not reported); serum and
    urine after hydrolysis with Helix pomatia juice (total
    6-hydroxychlorzoxazone). Fig. 2 mean +- SD, Table V the urinary
    6-hydroxychlorzoxazone per interval (70 % of the dose in 24 hr).

    The model has no induction of CYP2E1 by alcoholism: the alcoholic patients
    are simulated as the controls.
    """

    #: the groups of the curation with their health
    groups: ClassVar[Mapping[str, Health]] = {
        "healthy": Health.HEALTHY,
        "alcoholics": Health.ALCOHOLISM,
    }

    @property
    def FigMeta(self) -> dict[str, HelperMapping]:
        """Datasets of the study by their measurement."""
        return {
            "Fig2_czx": HelperMapping(
                mr=self.Mr.czx,
                plot_ylabel=self.label_czx,
                yid=Sids.cpl_czx,
                unit="µM",
                dset_label="Fig2_{group}_chlorzoxazone",
                excel_sheet="Fig2",
                sim_time_factor=9,
            ),
            "Fig2_czx6oh": HelperMapping(
                mr=self.Mr.czx6oh,
                plot_ylabel=self.label_czx6oh_all,
                yid=Sids.cve_czx6oh_all,
                unit="µM",
                dset_label="Fig2_{group}_6-hydroxychlorzoxazone",
                excel_sheet="Fig2",
                sim_time_factor=9,
            ),
            # cumulative amounts of Table V, the SD of the intermediate times
            # under the assumption of independent intervals
            "Tab5_czx6oh": HelperMapping(
                mr=self.Mr.czx6oh,
                plot_ylabel=self.label_czxoglu_urine,
                yid=Sids.aurine_czxoglu,
                unit="mmole",
                dset_label="Tab5_{group}_6-hydroxychlorzoxazone",
                excel_sheet="Tab5",
                sim_time_factor=25,
            ),
        }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id, fig_map in self.FigMeta.items():
            df = self.load_dataframe(required(fig_map.excel_sheet))
            for group in self.groups:
                label = required(fig_map.dset_label).format(group=group)
                dset = DataSet.from_df(df[df["label"] == label], self.ureg)
                dset.unit_conversion("mean", 1 / required(fig_map.mr))
                dsets[f"dset_{fig_id}_{group}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            "czx500": Simulation(
                time_unit="min",
                end=25 * 60,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "PODOSE_czx": Q(500, "mg"),
                },
            )
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for fig_id, fig_map in self.FigMeta.items():
            for group, health in self.groups.items():
                mappings[f"fm_{fig_id}_{group}_500"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"dset_{fig_id}_{group}",
                        xid="time",
                        yid="mean",
                        count="count",
                        yid_sd="mean_sd",
                    ),
                    observable=FitData(
                        self, task="task_czx500", xid="time", yid=required(fig_map.yid)
                    ),
                    metadata=PKPDMappingMetaData(
                        # serum concentrations, cumulative urinary 6-OH-CZX
                        tissue=Tissue.URINE
                        if fig_id.startswith("Tab5")
                        else Tissue.SERUM,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.SINGLE,
                        health=health,
                        fasting=Fasting.FASTED,
                        data_type=DataType.MEAN,
                    ),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig2",
            num_rows=1,
            num_cols=3,
            name=f"{self.__class__.__name__} (500 mg)",
        )
        plots = fig.create_plots(legend=True)
        colors = {"healthy": None, "alcoholics": "tab:red"}
        for plot, (fig_id, fig_map) in zip(plots, self.FigMeta.items(), strict=True):
            plot.set_xaxis(self.label_time, unit="hr", max=fig_map.sim_time_factor)
            plot.set_yaxis(
                required(fig_map.plot_ylabel),
                unit=fig_map.unit,
                scale=AxisScale.LINEAR,
            )
            yid = required(fig_map.yid)
            plot.add_data(
                task="task_czx500",
                xid="time",
                yid=yid,
                label="Sim",
                color=plot_colors_sid[yid],
            )
            for group, color in colors.items():
                plot.add_data(
                    dataset=f"dset_{fig_id}_{group}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"Data {group}",
                    color=color or plot_colors_sid[yid],
                )

        return {"fig_Fig2": fig}


if __name__ == "__main__":
    MODEL.run_experiments(Lucas1993, output_dir="test")
