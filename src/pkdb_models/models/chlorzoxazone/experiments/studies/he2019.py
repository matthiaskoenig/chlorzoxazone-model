"""Simulation experiment of He2019.

Chlorzoxazone (400 mg po), test and reference tablet of a bioequivalence study;
chlorzoxazone in plasma.
"""

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

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    Sids,
)
from pkdb_models.models.chlorzoxazone.plot_colors import plot_colors_sid


class He2019(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of He2019.

    Chlorzoxazone single 400 mg dose.
    """

    #: labels of the datasets with the label of their curve: the test and the
    #: reference tablet were given to the same 20 subjects (crossover)
    dset_labels: ClassVar[dict[str, str]] = {
        "CZX400_TEST": "Data test tablet",
        "CZX400_REF": "Data reference tablet",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig4")
        for label, df_label in df.groupby("label"):
            label = str(label)
            dset = DataSet.from_df(df_label, self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.czx)
            dsets[f"dset_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        # 20 healthy Chinese men, mean 62.4 kg and 172 cm, 12 hr fast
        tcsims["CZX400"] = Simulation(
            time_unit="min",
            end=9 * 60,
            preinit_changes={
                **self.default_changes(ApplicationForm.TABLET),
                "PODOSE_czx": Q(400, "mg"),
                "BW": Q(62.4, "kg"),
                "HEIGHT": Q(172, "cm"),
            },
        )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        # the SD of Fig4 are nearly constant for the test tablet and the pre-dose
        # point has an SD of about 1 µg/ml, they are kept as the error of the means
        for label in self.dset_labels:
            mappings[f"fm_{label}_400"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"dset_{label}",
                    xid="time",
                    yid="mean",
                    count="count",
                    yid_sd="mean_sd",
                ),
                observable=FitData(
                    self, task="task_CZX400", xid="time", yid=Sids.cpl_czx
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

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Fig4"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__} {name} (400 mg)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(label=self.label_czx, unit="µM", scale="linear")
        plots[0].add_data(
            task="task_CZX400",
            xid="time",
            yid=Sids.cpl_czx,
            label="Sim",
            color=plot_colors_sid[Sids.cpl_czx],
        )
        for (label, data_label), marker in zip(
            self.dset_labels.items(), ["s", "v"], strict=True
        ):
            plots[0].add_data(
                dataset=f"dset_{label}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=data_label,
                color=plot_colors_sid[Sids.cpl_czx],
                marker=marker,
            )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(He2019, output_dir="test")
