"""Simulation experiment of the study Vesell1995."""

from typing import ClassVar, override

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
    """Get the mean and standard deviation of the individual data per time point.

    The time points and the other columns are taken from the subject BL.

    Args:
        df: individual data with the columns `time`, `individual` and `value`,
            the same time points for every individual.

    Returns:
        The data with the columns `mean`, `sd` and `count` instead of `value`
        and `individual`.
    """
    groupby = df.groupby("time")
    count = len(df["individual"].unique())
    mean = groupby["value"].mean().values
    std = groupby["value"].std().values
    new_df = df[df["individual"] == "BL"]
    new_df = new_df.drop(["value", "individual"], axis=1)
    counts = [count for _ in range(len(new_df))]
    return new_df.assign(mean=mean, sd=std, count=counts)


class Vesell1995(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Vesell1995.

    Individual chlorzoxazone plasma concentrations after a single oral dose of
    500 mg (250 mg for W.S., Fig3) and individual cumulative amounts of total
    6-hydroxychlorzoxazone (after beta-glucuronidase, the glucuronide of the
    model) in urine after 250 mg Paraflex in the fasting state (Fig1). The
    amounts of Fig1 are read from sigma-minus plots whose axis says µg: they
    are mg, 116-210 mg of 6-hydroxychlorzoxazone are 43-77 % of the dose.

    W.S. has a delayed renal elimination of 6-hydroxychlorzoxazone (urinary
    half-life 3.1 hr vs 1.42 hr) with a normal clearance of chlorzoxazone: his
    urine data are an outlier and not part of the mean of Fig1 (the five other
    subjects), his plasma data are normal.

    The body weight is not reported (49-83 kg), the middle of the range, 66 kg.
    """

    #: the subject with the delayed renal elimination of 6-hydroxychlorzoxazone
    outlier: ClassVar[str] = "WS"

    # doses in mg of the individuals of Fig1 and Fig3
    dose_dicts: ClassVar[list[dict[str, int]]] = [
        {"BL": 250, "EG": 250, "SM": 250, "MF": 250, "CN": 250, "WS": 250},
        {"JR": 500, "TG": 500, "CM": 500, "WS": 250, "EG": 500, "JW": 500},
    ]

    @property
    def FigMeta(self) -> dict[str, HelperMapping]:
        """Datasets of the study by their figure id."""
        return {
            "Fig1": HelperMapping(
                id="Fig1",
                yid=Sids.aurine_czxoglu,
                mr=self.Mr.czx6oh,
                plot_ylabel=self.label_czxoglu_urine,
                unit="mmole",
            ),
            "Fig3": HelperMapping(
                id="Fig3",
                yid=Sids.cpl_czx,
                mr=self.Mr.czx,
                plot_ylabel=self.label_czx,
                unit="µM",
            ),
        }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id, hm in self.FigMeta.items():
            df = self.load_dataframe(fig_id)
            if fig_id == "Fig1":
                df_mean = get_mean_dset(df[df["individual"] != self.outlier])
                dset = DataSet.from_df(df_mean, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.czx6oh)
                dsets[f"dset_{hm.id}_mean"] = dset
            for label, df_label in df.groupby("individual"):
                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion("value", 1 / required(hm.mr))
                dsets[f"dset_{fig_id}_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        for dose in [250, 500]:
            tcsims[f"czx{dose}"] = Simulation(
                time_unit="min",
                end=11 * 60,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "PODOSE_czx": Q(dose, "mg"),
                    "BW": Q(66, "kg"),
                },
            )

        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}

        mappings["fm_Fig1_mean"] = FitMapping(
            self,
            reference=FitData(
                self,
                dataset="dset_Fig1_mean",
                xid="time",
                yid="mean",
                count="count",
                yid_sd="mean_sd",
            ),
            observable=FitData(
                self, task="task_czx250", xid="time", yid=Sids.aurine_czxoglu
            ),
            metadata=PKPDMappingMetaData(
                # mean of the five normal subjects of Fig1 (without W.S.), 250 mg
                # Paraflex in the fasting state
                tissue=Tissue.URINE,
                route=Route.PO,
                application_form=ApplicationForm.TABLET,
                dosing=Dosing.SINGLE,
                health=Health.HEALTHY,
                fasting=Fasting.FASTED,
                data_type=DataType.MEAN,
            ),
        )

        # Fig1 urine, Fig3 plasma; fasting is only reported for the 250 mg dose
        tissues = {"Fig1": Tissue.URINE, "Fig3": Tissue.PLASMA}
        fig_meta = self.FigMeta
        for fig_id, dose_dict in zip(fig_meta, self.dose_dicts, strict=True):
            hm = fig_meta[fig_id]

            for individual, dose in dose_dict.items():
                mappings[f"fm_{fig_id}_{individual}_{dose}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"dset_{fig_id}_{individual}",
                        xid="time",
                        yid="value",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=f"task_czx{dose}",
                        xid="time",
                        yid=required(hm.yid),
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=tissues[fig_id],
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.SINGLE,
                        health=Health.HEALTHY,
                        fasting=Fasting.FASTED if dose == 250 else Fasting.NR,
                        data_type=DataType.INDIVIDUAL,
                    ),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        figures = {}
        fig_meta = self.FigMeta
        hm = fig_meta["Fig1"]
        yid = required(hm.yid)
        fig1_mean = Figure(
            experiment=self,
            sid="Fig1_mean",
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__} Fig1 (250 mg)",
        )

        plots = fig1_mean.create_plots(
            xaxis=Axis(self.label_time, unit="hr"),
            yaxis=Axis(hm.plot_ylabel, unit=hm.unit),
            legend=True,
        )

        plots[0].add_data(
            task="task_czx250",
            xid="time",
            yid=yid,
            label="Sim",
            color=plot_colors_sid[yid],
        )

        plots[0].add_data(
            dataset="dset_Fig1_mean",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            label="Data",
            color=plot_colors_sid[yid],
            count="count",
        )

        figures["Fig1_mean"] = fig1_mean

        for fig_id, dose_dict in zip(fig_meta, self.dose_dicts, strict=True):
            hm = fig_meta[fig_id]
            yid = required(hm.yid)
            fig = Figure(
                experiment=self,
                sid=fig_id,
                num_rows=3,
                num_cols=2,
                name=f"{self.__class__.__name__} {fig_id}",
            )

            plots = fig.create_plots(
                xaxis=Axis(self.label_time, unit="hr"),
                yaxis=Axis(hm.plot_ylabel, unit=hm.unit),
                legend=True,
            )

            for i, (individual, dose) in enumerate(dose_dict.items()):
                # simulation
                plots[i].add_data(
                    task=f"task_czx{dose}",
                    xid="time",
                    yid=yid,
                    label=f"Sim {dose} [mg]",
                    color=plot_colors_sid[yid],
                )
                plots[i].add_data(
                    dataset=f"dset_{fig_id}_{individual}",
                    xid="time",
                    yid="value",
                    label=f"{individual} {dose} mg",
                    color=plot_colors_sid[yid],
                    count="count",
                )
            figures[fig_id] = fig

        return figures


if __name__ == "__main__":
    MODEL.run_experiments(Vesell1995, output_dir="test")
