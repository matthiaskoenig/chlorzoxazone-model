"""Simulation experiment of Desiraju1983.

Chlorzoxazone (750 mg po, aqueous suspension) with acetaminophen (900 mg po in
the same suspension) in 23 healthy men; chlorzoxazone in plasma and the
cumulative urinary excretion of 6-hydroxychlorzoxazone glucuronide.
"""

from typing import override

import numpy as np
import pandas as pd
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
    Sids,
)
from pkdb_models.models.chlorzoxazone.plot_colors import plot_colors_sid

#: the limit of quantification of chlorzoxazone in plasma [µg/ml]; the means at
#: 8 and 10 hr (0.46, 0.45 µg/ml) are below it, "for most subjects either zero
#: or below the assay quantitation limit", i.e. means of the few subjects with
#: a value, which are biased high
LLOQ_CZX = 0.5

#: the length of the urine collection intervals [hr], 0-2, ..., 8-10 hr
URINE_INTERVAL = 2.0


class Desiraju1983(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Desiraju1983.

    Fig1: chlorzoxazone in plasma, mean +- SEM of 23 subjects (SEM converted to
    SD in the data). Fig3B: urinary excretion rates of the 6-hydroxychlorzoxazone
    glucuronide of the mean data as chlorzoxazone equivalents (5 collections of
    2 hr), summed to the cumulative amount at the end of every collection
    (73.8 % of the dose in 10 hr, the text gives 74 +- 3.4 %).

    The dose is an aqueous suspension (15 mg/ml chlorzoxazone, 18 mg/ml
    acetaminophen, tragacanth); it is simulated as the solution (no dissolution):
    the drug is dispersed finely and the peak is early (tmax 38 +- 16 min).
    Acetaminophen is taken as not interacting: it is a minor, low affinity
    substrate of CYP2E1 at 900 mg, and a competition would lower, not raise,
    the clearance of chlorzoxazone.
    """

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig1")
        dset = DataSet.from_df(df, self.ureg)
        dset.unit_conversion("mean", 1 / self.Mr.czx)
        dsets["dset_czx"] = dset

        # the data of the fit, without the means below the LLOQ
        dset = DataSet.from_df(df[df["mean"] >= LLOQ_CZX], self.ureg)
        dset.unit_conversion("mean", 1 / self.Mr.czx)
        dsets["dset_czx_lloq"] = dset

        # urine: excretion rates (mmole/hr, chlorzoxazone equivalents) at the
        # midpoints of the collections to cumulative amounts at their ends
        df = self.load_dataframe("Fig3")
        df = df[df["measurement"] == "excretion rate"].sort_values("time")
        dsets["dset_urine"] = DataSet.from_df(
            pd.DataFrame(
                {
                    "time": df["time"].to_numpy() + URINE_INTERVAL / 2,
                    "time_unit": "hr",
                    "mean": np.cumsum(df["mean"].to_numpy() * URINE_INTERVAL),
                    "unit": "mmole",
                    "count": df["count"].to_numpy(),
                }
            ),
            self.ureg,
        )

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        tcsims["czx750"] = Simulation(
            time_unit="min",
            end=11 * 60,
            preinit_changes={
                # the suspension as the solution, see the class
                **self.default_changes(ApplicationForm.SOLUTION),
                "PODOSE_czx": Q(750, "mg"),
            },
        )

        return tcsims

    @staticmethod
    def mapping_metadata(tissue: Tissue) -> PKPDMappingMetaData:
        """Healthy men, the suspension with acetaminophen after a 12 hr fast."""
        return PKPDMappingMetaData(
            tissue=tissue,
            route=Route.PO,
            application_form=ApplicationForm.SUSPENSION,
            dosing=Dosing.SINGLE,
            health=Health.HEALTHY,
            fasting=Fasting.FASTED,
            data_type=DataType.MEAN,
            coadministration=Coadministration.ACETAMINOPHEN,
        )

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        mappings["fm_Fig1_czx750"] = FitMapping(
            self,
            reference=FitData(
                self,
                dataset="dset_czx_lloq",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
            ),
            observable=FitData(self, task="task_czx750", xid="time", yid=Sids.cpl_czx),
            metadata=self.mapping_metadata(Tissue.PLASMA),
        )
        mappings["fm_Fig3_urine_czx750"] = FitMapping(
            self,
            reference=FitData(
                self, dataset="dset_urine", xid="time", yid="mean", count="count"
            ),
            observable=FitData(
                self, task="task_czx750", xid="time", yid=Sids.aurine_czxoglu
            ),
            metadata=self.mapping_metadata(Tissue.URINE),
        )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig1_Fig3",
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} (750 mg suspension)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(label=self.label_czx, unit="µM", scale="linear")
        plots[1].set_yaxis(label=self.label_czxoglu_urine, unit="mmole")

        for plot, yid, dset_id, yid_sd in [
            (plots[0], Sids.cpl_czx, "dset_czx", "mean_sd"),
            (plots[1], Sids.aurine_czxoglu, "dset_urine", None),
        ]:
            color = plot_colors_sid[yid]
            plot.add_data(
                task="task_czx750", xid="time", yid=yid, label="Sim", color=color
            )
            plot.add_data(
                dataset=dset_id,
                xid="time",
                yid="mean",
                yid_sd=yid_sd,
                count="count",
                label="Data",
                color=color,
            )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Desiraju1983, output_dir="test")
