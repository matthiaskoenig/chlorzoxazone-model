"""Simulation experiment of Gade2018.

Chlorzoxazone (250 mg po, tablet) in obese and nonobese adolescents (11 to 18
years); chlorzoxazone and 6-hydroxychlorzoxazone in plasma.
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


class Gade2018(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Gade2018.

    Pharmacokinetics in children of 11 to 18 years, chlorzoxazone single 250 mg
    dose.
    """

    @property
    def FigMeta(self) -> dict[str, HelperMapping]:
        """Datasets of the study by curve, with the task of their group."""
        return {
            "Fig1_no_czx": HelperMapping(
                id="Fig1",
                mr=self.Mr.czx,
                dset_label="Fig1_chlorzoxazone_nonobese",
                plot_ylabel=self.label_czx,
                plot_legend_label="nonobese",
                yid=Sids.cpl_czx,
                unit="µM",
                task_id="nw",
            ),
            "Fig1_no_czx6oh": HelperMapping(
                id="Fig1",
                mr=self.Mr.czx6oh,
                dset_label="Fig1_6-hydroxychlorzoxazone_nonobese",
                plot_ylabel=self.label_czx6oh_all,
                plot_legend_label="nonobese",
                yid=Sids.cve_czx6oh_all,
                unit="µM",
                task_id="nw",
            ),
            "Fig1_o_czx": HelperMapping(
                id="Fig1",
                mr=self.Mr.czx,
                dset_label="Fig1_chlorzoxazone_obese",
                plot_ylabel=self.label_czx,
                plot_legend_label="obese",
                yid=Sids.cpl_czx,
                unit="µM",
                task_id="obese",
            ),
            "Fig1_o_czx6oh": HelperMapping(
                id="Fig1",
                mr=self.Mr.czx6oh,
                dset_label="Fig1_6-hydroxychlorzoxazone_obese",
                plot_ylabel=self.label_czx6oh_all,
                plot_legend_label="obese",
                yid=Sids.cve_czx6oh_all,
                unit="µM",
                task_id="obese",
            ),
        }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig1")
        for fig_id, fig_map in self.FigMeta.items():
            dset = DataSet.from_df(df[df["label"] == fig_map.dset_label], self.ureg)
            dset.unit_conversion("mean", 1 / required(fig_map.mr))
            dsets[f"dset_{fig_id}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        # the median body weights of the groups (Table 1); the height is not
        # reported and has no effect on the pharmacokinetics
        return {
            task_id: Simulation(
                time_unit="min",
                end=7 * 60,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "PODOSE_czx": Q(250, "mg"),
                    "BW": Q(bw, "kg"),
                },
            )
            for task_id, bw in [("obese", 78), ("nw", 56)]
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        # the error bars of Fig1 are not described in the paper, the means are
        # used without their error; the obese group differs from the nonobese
        # group in the body weight only (no induction of CYP2E1 in the model)
        for fig_id, fig_map in self.FigMeta.items():
            mappings[f"fm_{fig_id}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"dset_{fig_id}",
                    xid="time",
                    yid="mean",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=f"task_{fig_map.task_id}",
                    xid="time",
                    yid=required(fig_map.yid),
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    health=Health.OBESE
                    if fig_map.task_id == "obese"
                    else Health.HEALTHY,
                    fasting=Fasting.NR,
                    data_type=DataType.MEAN,
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
            name=f"{self.__class__.__name__} 250 mg oral",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"))
        plots[0].set_yaxis(label=self.label_czx, unit="µM", scale="linear")
        plots[1].set_yaxis(label=self.label_czx6oh_all, unit="µM", scale="linear")

        for fig_id, fig_map in self.FigMeta.items():
            color = "orange" if fig_map.task_id == "obese" else "black"
            plot = plots[0] if fig_map.yid == Sids.cpl_czx else plots[1]
            plot.add_data(
                task=f"task_{fig_map.task_id}",
                xid="time",
                yid=required(fig_map.yid),
                label=f"Sim {fig_map.plot_legend_label}",
                color=color,
            )

            plot.add_data(
                dataset=f"dset_{fig_id}",
                xid="time",
                yid="mean",
                count="count",
                label=f"Data {fig_map.plot_legend_label}",
                color=color,
            )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Gade2018, output_dir="test")
