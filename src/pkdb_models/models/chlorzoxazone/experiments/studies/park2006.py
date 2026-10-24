"""Simulation experiment of the study Park2006."""

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

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    HelperMapping,
    Sids,
    required,
)
from pkdb_models.models.chlorzoxazone.plot_colors import plot_colors_sid


class Park2006(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Park2006.

    Chlorzoxazone single 400 mg dose in 10 healthy Korean men, crossover of
    placebo and aspirin 1 g three times daily for 6 days. Plasma chlorzoxazone
    and 6-hydroxychlorzoxazone (Fig1, mean and SD).

    Aspirin has no effect on the pharmacokinetics of chlorzoxazone (AUC 95 %,
    90 % CI 87-103 %; 6-hydroxychlorzoxazone AUC 101 %), it is simulated without
    an interaction factor and the aspirin phase is the same simulation as the
    placebo phase.

    6-hydroxychlorzoxazone is the total (free and glucuronide): the method of
    Frye & Stiff 1996 is not described in the paper, but the AUC ratio of
    6-hydroxychlorzoxazone to chlorzoxazone of 0.32 and the Cmax of 3.0 µg/ml
    are 10x the free metabolite of the methods without hydrolysis (ratio at
    Cmax 0.014-0.041 in Witt2016, below 0.025 µg/ml in 9 of 10 subjects in
    Wang2003).
    """

    #: the phases of the crossover: the label of the data and the
    #: coadministration
    phases: ClassVar[Mapping[str, tuple[str, Coadministration]]] = {
        "": ("Fig1_CZX", Coadministration.NONE),
        "_asa": ("Fig1_CZX_ASP", Coadministration.ASA),
    }

    @property
    def FigMeta(self) -> dict[str, HelperMapping]:
        """Datasets of the study by their id, one per substance."""
        return {
            "Fig1_czx": HelperMapping(
                id="Fig1_czx",
                mr=self.Mr.czx,
                yid=Sids.cpl_czx,
                plot_ylabel=self.label_czx,
                dset_label="chlorzoxazone",
                unit="µM",
            ),
            "Fig1_czx6oh": HelperMapping(
                id="Fig1_czx6oh",
                mr=self.Mr.czx6oh,
                yid=Sids.cve_czx6oh_all,
                plot_ylabel=self.label_czx6oh_all,
                dset_label="6-hydroxychlorzoxazone",
                unit="µM",
            ),
        }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig1")
        for phase, (label, _) in self.phases.items():
            for hm in self.FigMeta.values():
                dset = DataSet.from_df(
                    df[df["label"] == f"{label}_{hm.dset_label}"], self.ureg
                )
                dset.unit_conversion("mean", 1 / required(hm.mr))
                dsets[f"dset_{hm.id}{phase}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        tcsims["czx400"] = Simulation(
            time_unit="min",
            end=9 * 60,
            preinit_changes={
                **self.default_changes(ApplicationForm.TABLET),
                "PODOSE_czx": Q(400, "mg"),
                # the body weight is not reported, the middle of 63-75 kg
                "BW": Q(69, "kg"),
            },
        )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for phase, (_, coadministration) in self.phases.items():
            for hm in self.FigMeta.values():
                mappings[f"fm_{hm.id}{phase}_400"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"dset_{hm.id}{phase}",
                        xid="time",
                        yid="mean",
                        count="count",
                        yid_sd="mean_sd",
                    ),
                    observable=FitData(
                        self,
                        task="task_czx400",
                        xid="time",
                        yid=required(hm.yid),
                    ),
                    metadata=PKPDMappingMetaData(
                        # dosage form not named in the paper (a marketed tablet),
                        # a light meal 4 hr after the dose
                        tissue=Tissue.PLASMA,
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
        fig = Figure(
            experiment=self,
            sid="Fig1",
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} Fig1 (400 mg)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        for plot, hm in zip(plots, self.FigMeta.values(), strict=True):
            plot.set_yaxis(label=hm.plot_ylabel, unit=hm.unit, scale="linear")
            yid = required(hm.yid)
            plot.add_data(
                task="task_czx400",
                xid="time",
                yid=yid,
                label="Sim",
                color=plot_colors_sid[yid],
            )
            for phase, label, marker in [
                ("", "placebo", "o"),
                ("_asa", "aspirin", "s"),
            ]:
                plot.add_data(
                    dataset=f"dset_{hm.id}{phase}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"Data {label}",
                    color=plot_colors_sid[yid],
                    marker=marker,
                )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Park2006, output_dir="test")
