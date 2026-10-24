"""Simulation experiment of the study Puris2019."""

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
from pkdb_models.models.chlorzoxazone.plot_colors import plot_colors_sid


class Puris2019(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Puris2019.

    Chlorzoxazone single 62.5 mg dose as a part of a phenotyping cocktail
    (crushed tablets compounded into capsules, simulated as a tablet) in 6
    healthy subjects and 8 obese patients (7 analyzed for chlorzoxazone) before
    a Roux-en-Y gastric bypass. Serum at 0, 1, 2, 4 and 6 hr (Fig1, mean and
    SE).

    The body weight is not reported, it is the BMI times the square of an
    assumed height: obese BMI 41.0 kg/m² (6 women, 2 men, Finnish heights of
    about 1.65 m and 1.79 m, 1.685 m) is 116 kg, healthy BMI 18-25 kg/m² (21.5)
    at 1.72 m is 64 kg. 7 of the 8 obese patients have a fatty liver (CYP2E1
    induction in NAFLD is the likely cause of their 2.1x higher CL/F, the model
    has only the scaling by the body weight). The arm one year after the
    surgery is not simulated: the model has no representation of the bypassed
    stomach and duodenum (Cmax +89 %).
    """

    @property
    def FigMeta(self) -> dict[str, HelperMapping]:
        """Datasets of the study by their id, one per group."""
        return {
            "Fig1_healthy": HelperMapping(
                id="Fig1_healthy",
                mr=self.Mr.czx,
                dset_label="Fig1_healthy_chlorzoxazone",
                plot_ylabel=self.label_czx,
                plot_legend_label="healthy, BMI 18-25 kg/m²",
                body_weight=64,
                yid=Sids.cpl_czx,
                unit="µM",
            ),
            "Fig1_obese": HelperMapping(
                id="Fig1_obese",
                mr=self.Mr.czx,
                dset_label="Fig1_obese_chlorzoxazone",
                plot_ylabel=self.label_czx,
                plot_legend_label=r"obese, BMI $41.0\pm4.9$ kg/m²",
                body_weight=116,
                yid=Sids.cpl_czx,
                unit="µM",
            ),
        }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig1")
        for fig_id, fig_map in self.FigMeta.items():
            dset = DataSet.from_df(df[df["label"] == fig_map.dset_label], self.ureg)
            dset.unit_conversion("mean", 1 / required(fig_map.mr))
            dsets[self.to_sid(f"dset_{fig_id}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        for fig_id, fig_map in self.FigMeta.items():
            tcsims[self.to_sid(fig_id)] = Simulation(
                time_unit="min",
                end=7 * 60,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "PODOSE_czx": Q(62.5, "mg"),
                    "BW": Q(required(fig_map.body_weight), "kg"),
                },
            )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for fig_id, fig_map in self.FigMeta.items():
            mappings[self.to_sid(f"fm_{fig_id}_62.5")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"dset_{fig_id}"),
                    xid="time",
                    yid="mean",
                    count="count",
                    yid_sd="mean_sd",
                ),
                observable=FitData(
                    self,
                    task=self.to_sid(f"task_{fig_id}"),
                    xid="time",
                    yid=required(fig_map.yid),
                ),
                metadata=PKPDMappingMetaData(
                    # cocktail compounded from crushed tablets into capsules
                    tissue=Tissue.SERUM,
                    route=Route.PO,
                    application_form=ApplicationForm.CAPSULE,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY if fig_id == "Fig1_healthy" else Health.OBESE,
                    fasting=Fasting.NR,
                    data_type=DataType.MEAN,
                    coadministration=Coadministration.COCKTAIL,
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
            name=f"{self.__class__.__name__} Fig1 (62.5 mg)",
        )

        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"))

        for i, (fig_id, fig_map) in enumerate(self.FigMeta.items()):
            plots[i].set_yaxis(
                self.label_czx, unit=fig_map.unit, scale=AxisScale.LINEAR
            )

            yid = required(fig_map.yid)
            plots[i].add_data(
                task=self.to_sid(f"task_{fig_id}"),
                xid="time",
                yid=yid,
                label=f"Sim 62.5 [mg]\n{fig_map.plot_legend_label}",
                color=plot_colors_sid[yid],
            )

            plots[i].add_data(
                dataset=self.to_sid(f"dset_{fig_id}"),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"Data 62.5 [mg]\n{fig_map.plot_legend_label}",
                color=plot_colors_sid[yid],
            )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Puris2019, output_dir="test")
