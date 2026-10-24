"""Simulation experiment of Dreisbach1995.

Chlorzoxazone (500 mg po, tablet); the mean of the individual cumulative amounts
of 6-hydroxychlorzoxazone in urine and the chlorzoxazone and
6-hydroxychlorzoxazone time courses in plasma of a single subject.
"""

from typing import override

import pandas as pd
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


def get_mean_dset(df: pd.DataFrame) -> pd.DataFrame:
    """Get the mean of the individual time courses.

    The mean, the standard deviation and the number of individuals of every
    time point; the other columns are taken from the first row of the time
    point (the same for all individuals), the individual values are dropped.

    Args:
        df: individual time courses.

    Returns:
        The mean time course, sorted by time.
    """
    groupby = df.groupby("time")
    return (
        groupby.first()
        .drop(columns=["value", "proxy", "individual", "label", "count"])
        .assign(
            mean=groupby["value"].mean(),
            sd=groupby["value"].std(),
            count=groupby["individual"].nunique(),
        )
        .reset_index()
    )


class Dreisbach1995(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Dreisbach1995.

    Chlorzoxazone single oral 500 mg caplet (Parafon Forte DSC) after a 12 hr
    fast in healthy men, lunch at 4 hr. Fig1: the cumulative amount of
    6-hydroxychlorzoxazone (total, after hydrolysis) in urine of 15 subjects,
    from their hydroxylation index (dose over the amount in urine) at 4-8 hr,
    averaged. Fig4: chlorzoxazone and total 6-hydroxychlorzoxazone in plasma of
    one representative subject (the sample at 0.75 hr was digitized as 0.45 hr
    in the curation).
    """

    @property
    def FigMeta(self) -> dict[str, HelperMapping]:
        """Datasets of the study by figure."""
        return {
            "Fig1": HelperMapping(
                id="Fig1",
                yid=Sids.aurine_czxoglu,
                unit="mmole",
                plot_ylabel=self.label_czxoglu_urine,
            ),
            "Fig4_czx": HelperMapping(
                id="Fig4",
                yid=Sids.cpl_czx,
                unit="µM",
                plot_ylabel=self.label_czx,
                dset_label="chlorzoxazone",
                mr=self.Mr.czx,
            ),
            "Fig4_czx6oh": HelperMapping(
                id="Fig4",
                yid=Sids.cve_czx6oh_all,
                unit="µM",
                plot_ylabel=self.label_czx6oh_all,
                dset_label="6-hydroxychlorzoxazone",
                mr=self.Mr.czx6oh,
            ),
        }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for key, hm in self.FigMeta.items():
            df = self.load_dataframe(required(hm.id))
            if hm.id == "Fig1":
                dsets[f"dset_{key}"] = DataSet.from_df(get_mean_dset(df), self.ureg)
            else:
                dset = DataSet.from_df(df[df["substance"] == hm.dset_label], self.ureg)
                dset.unit_conversion("value", 1 / required(hm.mr))
                dsets[f"dset_{key}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        tcsims["czx500"] = Simulation(
            time_unit="min",
            end=11 * 60,
            preinit_changes={
                **self.default_changes(ApplicationForm.TABLET),
                "PODOSE_czx": Q(500, "mg"),
            },
        )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for key, hm in self.FigMeta.items():
            if hm.id == "Fig1":
                mappings[f"fm_{key}_500"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"dset_{key}",
                        xid="time",
                        yid="mean",
                        count="count",
                        yid_sd="mean_sd",
                    ),
                    observable=FitData(
                        self, task="task_czx500", xid="time", yid=required(hm.yid)
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.URINE,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        data_type=DataType.MEAN,
                    ),
                )
            else:
                mappings[f"fm_{key}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"dset_{key}",
                        xid="time",
                        yid="value",
                        count="count",
                    ),
                    observable=FitData(
                        self, task="task_czx500", xid="time", yid=required(hm.yid)
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.PLASMA,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED,
                        data_type=DataType.INDIVIDUAL,
                    ),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        figures = {}
        for key, hm in self.FigMeta.items():
            color = plot_colors_sid[required(hm.yid)]
            fig = Figure(
                experiment=self,
                sid=key,
                num_rows=1,
                num_cols=1,
                name=f"{self.__class__.__name__} {hm.id}",
            )

            plot = fig.create_plots(
                xaxis=Axis(self.label_time, unit="hr"),
                yaxis=Axis(label=hm.plot_ylabel, unit=hm.unit, scale=AxisScale.LINEAR),
                legend=True,
            )[0]

            # simulation
            plot.add_data(
                task="task_czx500",
                xid="time",
                yid=required(hm.yid),
                label="Sim",
                color=color,
            )

            plot.add_data(
                dataset=f"dset_{key}",
                xid="time",
                yid="value" if hm.id == "Fig4" else "mean",
                yid_sd="mean_sd" if hm.id == "Fig1" else None,
                label="Data",
                color=color,
                count="count",
            )

            figures[key] = fig

        return figures


if __name__ == "__main__":
    MODEL.run_experiments(Dreisbach1995, output_dir="test")
