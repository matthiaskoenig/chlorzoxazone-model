"""Simulation experiment of the study Mishin1998."""

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
from sbmlsim.plot.plotting import AxisScale
from sbmlsim.simulation import Simulation

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    HelperMapping,
    Sids,
    required,
)


class Mishin1998(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Mishin1998.

    Chlorzoxazone single 750 mg dose (Paraflex, 250 mg tablets) within 1 hr
    after a diagnostic liver biopsy in men with alcoholic liver disease:
    recently drinking alcoholics (n=6, last drink within 24 hr, 85.5 kg; one
    cirrhosis, one septal fibrosis), the same subjects again after 8 days of
    observed abstinence (Fig. 7, 8) and abstinent alcoholics (n=5, at least 14
    days, 80.2 kg; steatosis, perivenular fibrosis). Plasma after hydrolysis
    with beta-glucuronidase (total chlorzoxazone and 6-hydroxychlorzoxazone),
    mean +- SEM (converted to SD). All subjects received codeine after the
    biopsy, the drinkers chlordiazepoxide, one abstinent subject disulfiram.

    The model has no induction of CYP2E1 by drinking (the drinkers have an
    AUC of 0.18 of the abstinent alcoholics): the groups differ only by their
    body weight. The nonalcoholic liver disease group is not encoded.
    """

    @property
    def FigMeta(self) -> dict[str, HelperMapping]:
        """Datasets of the study by their id, one per figure and group."""
        return {
            "Fig1_rda": HelperMapping(
                id="Fig1",
                mr=self.Mr.czx,
                dset_label="Fig1_alcoholic_drinking",
                plot_ylabel=self.label_czx,
                plot_legend_label="Recently drinking alcoholics",
                yid=Sids.cpl_czx,
                unit="µM",
                task_id="rda",
            ),
            "Fig1_aa": HelperMapping(
                id="Fig1",
                mr=self.Mr.czx,
                dset_label="Fig1_alcoholic_abstinent",
                plot_ylabel=self.label_czx,
                plot_legend_label="abstinent alcoholics",
                yid=Sids.cpl_czx,
                unit="µM",
                task_id="aa",
            ),
            "Fig2_rda": HelperMapping(
                id="Fig2",
                mr=self.Mr.czx6oh,
                dset_label="Fig2_alcoholic_drinking",
                plot_ylabel=self.label_czx6oh_all,
                plot_legend_label="Recently drinking alcoholics",
                yid=Sids.cve_czx6oh_all,
                unit="µM",
                task_id="rda",
            ),
            "Fig2_aa": HelperMapping(
                id="Fig2",
                mr=self.Mr.czx6oh,
                dset_label="Fig2_alcoholic_abstinent",
                plot_ylabel=self.label_czx6oh_all,
                plot_legend_label="abstinent alcoholics",
                yid=Sids.cve_czx6oh_all,
                unit="µM",
                task_id="aa",
            ),
            # the drinkers after 8 days of abstinence: the simulation of the
            # drinkers (same subjects and body weight, no CYP2E1 state)
            "Fig7": HelperMapping(
                id="Fig7",
                mr=self.Mr.czx,
                plot_ylabel=self.label_czx,
                plot_legend_label="after 8-day abstinence",
                yid=Sids.cpl_czx,
                unit="µM",
                dset_label="Fig7_alcoholic_drinking_stopped",
                task_id="rda",
            ),
            "Fig8": HelperMapping(
                id="Fig8",
                mr=self.Mr.czx6oh,
                plot_ylabel=self.label_czx6oh_all,
                plot_legend_label="after 8-day abstinence",
                yid=Sids.cve_czx6oh_all,
                unit="µM",
                dset_label="Fig8_alcoholic_drinking_stopped",
                task_id="rda",
            ),
        }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id, fig_map in self.FigMeta.items():
            df = self.load_dataframe(required(fig_map.id))
            dset = DataSet.from_df(df[df["label"] == fig_map.dset_label], self.ureg)
            dset.unit_conversion("mean", 1 / required(fig_map.mr))
            dsets[f"dset_{fig_id}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        # body weight of the recently drinking (rda) and abstinent (aa)
        # alcoholics (Table 1)
        return {
            task_id: Simulation(
                time_unit="min",
                end=7 * 60,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "PODOSE_czx": Q(750, "mg"),
                    "BW": Q(bw, "kg"),
                },
            )
            for task_id, bw in [("rda", 85.5), ("aa", 80.2)]
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for fig_id, fig_map in self.FigMeta.items():
            mappings[f"fm_{fig_id}_750"] = FitMapping(
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
                    self,
                    task=f"task_{fig_map.task_id}",
                    xid="time",
                    yid=required(fig_map.yid),
                ),
                metadata=PKPDMappingMetaData(
                    # recently drinking and abstinent alcoholics with liver
                    # disease, Paraflex tablets
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    health=Health.ALCOHOLISM,
                    fasting=Fasting.NR,
                    data_type=DataType.MEAN,
                    # codeine after the biopsy, chlordiazepoxide, disulfiram
                    coadministration=Coadministration.COMEDICATION,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Mishin1998",
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} 750 mg oral",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"))
        plots[0].set_yaxis(self.label_czx, unit="µM", scale=AxisScale.LINEAR)
        plots[1].set_yaxis(self.label_czx6oh_all, unit="µM", scale=AxisScale.LINEAR)

        fig_meta = self.FigMeta
        for fig_ids, plot in zip(
            [["Fig1_rda", "Fig7", "Fig1_aa"], ["Fig2_rda", "Fig8", "Fig2_aa"]],
            plots,
            strict=True,
        ):
            for fig_id, color in zip(fig_ids, ["black", "gray", "blue"], strict=True):
                fig_map = fig_meta[fig_id]
                if fig_id not in {"Fig7", "Fig8"}:
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
                    yid_sd="mean_sd",
                    count="count",
                    label=f"Data {fig_map.plot_legend_label}",
                    color=color,
                )

        return {"fig": fig}


if __name__ == "__main__":
    MODEL.run_experiments(Mishin1998, output_dir="test")
