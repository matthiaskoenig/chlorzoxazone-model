"""Simulation experiment of the study LaMaza2000."""

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

#: the height of all groups in cm: only the body mass index is reported, the
#: body weight of a group is its BMI x (1.70 m)^2
HEIGHT_CM = 170.0


class LaMaza2000(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of LaMaza2000.

    Chlorzoxazone single 750 mg dose (Parafon Forte) after an overnight fast in
    38 Chilean men, a light breakfast after the 1.5 hr sample; serum. Four
    groups: normal-weight (n=10) and obese nonalcoholics (n=11), normal-weight
    (n=9) and obese alcoholics (n=8; Tables 1-3, the abstract and Fig. 2, the
    methods say 8 and 9) after 4 days of abstinence in a detoxification ward.

    The model has no induction of CYP2E1 by alcoholism or obesity: the groups
    differ only by their body weight (BMI x (1.70 m)^2, the height is not
    reported).
    """

    @property
    def FigMeta(self) -> dict[str, HelperMapping]:
        """Datasets of the study by their id, one per group."""
        return {
            "Fig1_na_nw": HelperMapping(
                id="Fig1",
                mr=self.Mr.czx,
                dset_label="Fig1_nonalcoholics_nw",
                plot_legend_label="nonalcoholic normal-weight",
                yid=Sids.cpl_czx,
                unit="µM",
                # BMI 22.1 kg/m^2
                body_weight=63.9,
            ),
            "Fig1_na_o": HelperMapping(
                id="Fig1",
                mr=self.Mr.czx,
                dset_label="Fig1_nonalcoholics_obese",
                plot_legend_label="nonalcoholic obese",
                yid=Sids.cpl_czx,
                unit="µM",
                # BMI 33.0 kg/m^2
                body_weight=95.4,
            ),
            "Fig1_a_nw": HelperMapping(
                id="Fig1",
                mr=self.Mr.czx,
                dset_label="Fig1_alcoholics_nw",
                plot_legend_label="alcoholic normal-weight",
                yid=Sids.cpl_czx,
                unit="µM",
                # BMI 23.6 kg/m^2
                body_weight=68.2,
            ),
            "Fig1_a_o": HelperMapping(
                id="Fig1",
                mr=self.Mr.czx,
                dset_label="Fig1_alcoholics_obese",
                plot_legend_label="alcoholic obese",
                yid=Sids.cpl_czx,
                unit="µM",
                # BMI 30.3 kg/m^2
                body_weight=87.6,
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
        tcsims = {}
        for fig_id, hm in self.FigMeta.items():
            tcsims[fig_id] = Simulation(
                time_unit="min",
                end=9 * 60,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "PODOSE_czx": Q(750, "mg"),
                    "BW": Q(required(hm.body_weight), "kg"),
                    "HEIGHT": Q(HEIGHT_CM, "cm"),
                },
            )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        # the alcoholics drank at least 150 g ethanol per day for more than 5
        # years; the obese alcoholics are mapped by their alcoholism
        health = {
            "Fig1_na_nw": Health.HEALTHY,
            "Fig1_na_o": Health.OBESE,
            "Fig1_a_nw": Health.ALCOHOLISM,
            "Fig1_a_o": Health.ALCOHOLISM,
        }
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
                ),
                observable=FitData(
                    self, task=f"task_{fig_id}", xid="time", yid=required(fig_map.yid)
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.SERUM,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    health=health[fig_id],
                    # overnight fast, a light breakfast after the 1.5 hr sample
                    fasting=Fasting.FASTED,
                    data_type=DataType.MEAN,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig1",
            num_rows=2,
            num_cols=2,
            name=f"{self.__class__.__name__} (750 mg)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr"),
            yaxis=Axis(self.label_czx, unit="µM", scale=AxisScale.LINEAR),
            legend=True,
        )
        for plot, (fig_id, fig_map) in zip(plots, self.FigMeta.items(), strict=True):
            plot.set_title(required(fig_map.plot_legend_label))
            yid = required(fig_map.yid)
            plot.add_data(
                task=f"task_{fig_id}",
                xid="time",
                yid=yid,
                label=f"Sim ({fig_map.body_weight} kg)",
                color=plot_colors_sid[yid],
            )
            plot.add_data(
                dataset=f"dset_{fig_id}",
                xid="time",
                yid="mean",
                count="count",
                label="Data",
                color=plot_colors_sid[yid],
            )

        return {"fig_Fig1": fig}


if __name__ == "__main__":
    MODEL.run_experiments(LaMaza2000, output_dir="test")
