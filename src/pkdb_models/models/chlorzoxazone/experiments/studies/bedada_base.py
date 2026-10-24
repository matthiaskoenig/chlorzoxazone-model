"""Base of the simulation experiments of Bedada2016, Bedada2017 and Bedada2018.

The three studies of Bedada et al. have one protocol: healthy men take
chlorzoxazone 250 mg as a tablet (Paraflex) with 240 ml water after an overnight
fast of more than 10 hr, standard meals at 4 hr and 10 hr; plasma is sampled
from 0.25 to 8 hr. Chlorzoxazone and the free 6-hydroxychlorzoxazone are
measured by HPLC without the hydrolysis of the glucuronide. Only the control
phase is simulated, the phase after 10 days of an inhibitor (resveratrol,
piperine, quercetin) is not: there is no factor of these inhibitors on CYP2E1
which does not come from these studies themselves.

The 6-hydroxychlorzoxazone of the three studies is one figure: the control
curves of the three papers and the treatment curves of resveratrol and
piperine are the same, and they contradict the tables of the papers (a Cmax of
0.31, 0.22 and 0.20 µg/ml against a peak of the mean of 0.17 µg/ml). Its
mappings are outliers.
"""

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
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    Sids,
)
from pkdb_models.models.chlorzoxazone.plot_colors import plot_colors_sid


class BedadaSimulationExperiment(ChlorzoxazoneSimulationExperiment):
    """Base of the experiments of Bedada: chlorzoxazone single 250 mg dose."""

    #: figure of the study by analyte (chlorzoxazone, free 6-hydroxychlorzoxazone)
    fig_ids: ClassVar[Mapping[str, str]]
    #: body weight of the subjects in kg
    body_weight: ClassVar[float]

    #: observable by analyte, both in plasma
    yids: ClassVar[Mapping[str, Sids]] = {
        "czx": Sids.cpl_czx,
        "czx6oh": Sids.cve_czx6oh,
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        mrs = {"czx": self.Mr.czx, "czx6oh": self.Mr.czx6oh}
        for substance, fig_id in self.fig_ids.items():
            df = self.load_dataframe(fig_id)
            dset = DataSet.from_df(df, self.ureg)
            # the control phase, without the inhibitor
            dset = dset[dset.intervention == "CZX250"]
            dset.unit_conversion("mean", 1 / mrs[substance])
            dsets[substance] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            "czx250": Simulation(
                time_unit="min",
                end=9 * 60,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "PODOSE_czx": Q(250, "mg"),
                    "BW": Q(self.body_weight, "kg"),
                },
            )
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        study = self.__class__.__name__.lower()
        return {
            f"fm_{study}_{substance}_250": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=substance,
                    xid="time",
                    yid="mean",
                    count="count",
                    yid_sd="mean_sd",
                ),
                observable=FitData(
                    self, task="task_czx250", xid="time", yid=self.yids[substance]
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.FASTED,
                    data_type=DataType.MEAN,
                ),
            )
            for substance in self.fig_ids
        }

    @override
    def figures(self) -> dict[str, Figure]:
        figures = {}
        labels = {"czx": self.label_czx, "czx6oh": self.label_czx6oh}
        for substance, fig_id in self.fig_ids.items():
            yid = self.yids[substance]
            fig = Figure(
                experiment=self,
                sid=fig_id,
                num_rows=1,
                num_cols=1,
                name=f"{self.__class__.__name__} {fig_id} (250 mg)",
            )
            plot = fig.create_plots(
                xaxis=Axis(self.label_time, unit="hr"), legend=True
            )[0]
            plot.set_yaxis(label=labels[substance], unit="µM", scale="linear")
            plot.add_data(
                task="task_czx250",
                xid="time",
                yid=yid,
                label="Sim",
                color=plot_colors_sid[yid],
            )
            plot.add_data(
                dataset=substance,
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="Data",
                color=plot_colors_sid[yid],
            )
            figures[fig_id] = fig

        return figures
