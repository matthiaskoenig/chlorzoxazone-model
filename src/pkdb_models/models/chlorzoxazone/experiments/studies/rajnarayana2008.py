"""Simulation experiment of the study Rajnarayana2008."""

from collections.abc import Mapping
from typing import ClassVar, override

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
from sbmlsim.units import Quantity

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    Sids,
)
from pkdb_models.models.chlorzoxazone.plot_colors import plot_colors_sid


class Rajnarayana2008(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Rajnarayana2008.

    Chlorzoxazone single 250 mg dose (Paraflex tablet) in 12 healthy Indian
    men, before and after diosmin 500 mg daily for 9 days. Serum
    chlorzoxazone (Fig. 3 of the paper, Fig1 of the data, mean and SD).

    Diosmin inhibits CYP2E1 (AUC x1.66, CL/F -40 %), simulated with the
    literature factor of the CYP2E1 activity (`interactions`, not fitted).

    The exposure of the reference phase is far below the other studies (dose
    normalized Cmax 2.8x lower than Park2006 and Wang2003, CL/F 40.7 l/hr vs
    13-19 l/hr) and most concentrations are below the lowest calibrator of
    2 µg/ml: the reference curve is not training data.
    """

    #: the phases: the coadministration and the changes of the interaction
    phases: ClassVar[Mapping[str, Coadministration]] = {
        "REF": Coadministration.NONE,
        "TEST": Coadministration.COMEDICATION,
    }

    def interaction_changes(self, phase: str) -> dict[str, Quantity]:
        """Get the changes of the interaction of a phase.

        Args:
            phase: the phase, `REF` or `TEST` (diosmin).

        Returns:
            The changes of the CYP2E1 activity, none for the reference.
        """
        if phase == "REF":
            return {}
        return {
            k: Q(v, "dimensionless") for k, v in self.interactions["diosmin"].items()
        }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig1")
        for phase in self.phases:
            label = f"Fig1_CZX_{phase}"
            dset = DataSet.from_df(df[df["label"] == label], self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.czx)
            dsets[f"dset_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        for phase in self.phases:
            tcsims[f"Fig1_CZX_{phase}"] = Simulation(
                time_unit="min",
                end=9 * 60,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "PODOSE_czx": Q(250, "mg"),
                    "BW": Q(61.8, "kg"),
                    "HEIGHT": Q(172.4, "cm"),
                    **self.interaction_changes(phase),
                },
            )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for phase, coadministration in self.phases.items():
            key = "fm_Fig1_250" if phase == "REF" else "fm_Fig1_diosmin_250"
            mappings[key] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"dset_Fig1_CZX_{phase}",
                    xid="time",
                    yid="mean",
                    count="count",
                    yid_sd="mean_sd",
                ),
                observable=FitData(
                    self, task=f"task_Fig1_CZX_{phase}", xid="time", yid=Sids.cpl_czx
                ),
                metadata=PKPDMappingMetaData(
                    # diosmin 500 mg/day for 9 days before the test phase
                    tissue=Tissue.SERUM,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    fasting=Fasting.NR,
                    data_type=DataType.MEAN,
                    coadministration=coadministration,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Fig1"
        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__} {name} (250 mg)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(label=self.label_czx, unit="µM", scale="linear")

        for phase, label, color in [
            ("REF", "control", plot_colors_sid[Sids.cpl_czx]),
            ("TEST", "diosmin", "tab:red"),
        ]:
            plots[0].add_data(
                task=f"task_Fig1_CZX_{phase}",
                xid="time",
                yid=Sids.cpl_czx,
                label=f"Sim {label}",
                color=color,
            )
            plots[0].add_data(
                dataset=f"dset_Fig1_CZX_{phase}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=f"Data {label}",
                color=color,
            )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Rajnarayana2008, output_dir="test")
