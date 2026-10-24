"""Simulation experiment of Eap1998.

Chlorzoxazone (250 mg po, tablet) in healthy drug-free volunteers and in
patients with alcoholism entering withdrawal who take chlormethiazole;
chlorzoxazone and 6-hydroxychlorzoxazone in plasma.
"""

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

#: the activities of CYP2E1 and of the CYP2E1 independent elimination of the
#: patients with chlormethiazole: chlormethiazole inhibits the expression of
#: CYP2E1 (the authors, after their ref. 16 and 22). CL/F is 0.315 of the control (4.0 vs
#: 12.7 l/hr) and the AUC of 6-hydroxychlorzoxazone 0.64 (4.56 vs 7.11 mg*h/l);
#: with the fraction of CYP2E1 `FM_CYP2E1` 0.7 both ratios give the CYP2E1
#: activity 0.64 * 0.315 / 0.7 = 0.20 (the formation clearance) and the
#: remaining activity (0.315 - 0.7 * 0.20) / 0.3 = 0.58 (a CYP2E1 inhibition
#: alone, 0.02, would leave almost no 6-hydroxychlorzoxazone). Confounders: the
#: preceding induction of CYP2E1 by alcohol (1-3 days of abstinence), elevated
#: liver enzymes in 14 of 16, clorazepate (no effect on CYP2E1, their ref. 22),
#: triazolam/oxazepam. Literature values, not fitted.
CHLORMETHIAZOLE: dict[str, float] = {"LI__f_cyp2e1": 0.20, "LI__f_czxother": 0.58}


class Eap1998(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Eap1998.

    Fig1: chlorzoxazone and 6-hydroxychlorzoxazone in plasma, mean +- SD, after
    a single 250 mg tablet (Escoflex) at about 7 AM, a standard breakfast at
    90 min. Healthy: 5 drug-free volunteers (4 men, 80 kg, 2 smokers, no
    alcohol for 1 week). Patients: 16 patients with alcoholism entering
    withdrawal (14 men, 71 kg, 14 smokers) with chlormethiazole 1.2 or
    2.4 g/day for 1-3 days, simulated with the CYP2E1 activities
    `CHLORMETHIAZOLE`. The paper does not state whether the glucuronide was
    hydrolysed; 6-hydroxychlorzoxazone is mapped to the total (free and
    glucuronide), its AUC (7.11 mg*h/l) is close to the total of Frye1998
    (5.5 mg*h/l at the same dose).
    """

    #: the body weight of the groups [kg]
    body_weights: ClassVar[dict[str, float]] = {"healthy": 80, "alcoholics": 71}

    @property
    def FigMeta(self) -> dict[str, HelperMapping]:
        """Datasets of the study by curve."""
        return {
            "czx": HelperMapping(
                id="Fig1",
                mr=self.Mr.czx,
                plot_ylabel=self.label_czx,
                yid=Sids.cpl_czx,
                unit="µM",
                dset_label="chlorzoxazone",
            ),
            "czx6oh": HelperMapping(
                id="Fig1",
                mr=self.Mr.czx6oh,
                plot_ylabel=self.label_czx6oh_all,
                yid=Sids.cve_czx6oh_all,
                unit="µM",
                dset_label="6-hydroxychlorzoxazone",
            ),
        }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig1")
        for group in self.body_weights:
            for key, hm in self.FigMeta.items():
                dset = DataSet.from_df(
                    df[df["label"] == f"Fig1_{group}_{hm.dset_label}"], self.ureg
                )
                dset.unit_conversion("mean", 1 / required(hm.mr))
                dsets[f"dset_Fig1_{key}_{group}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        for group, bw in self.body_weights.items():
            changes = (
                {k: Q(v, "dimensionless") for k, v in CHLORMETHIAZOLE.items()}
                if group == "alcoholics"
                else {}
            )
            tcsims[f"czx250_{group}"] = Simulation(
                time_unit="min",
                end=11 * 60,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "PODOSE_czx": Q(250, "mg"),
                    "BW": Q(bw, "kg"),
                    **changes,
                },
            )

        return tcsims

    @staticmethod
    def mapping_metadata(group: str) -> PKPDMappingMetaData:
        """Single tablet after an overnight fast, breakfast at 90 min."""
        patients = group == "alcoholics"
        return PKPDMappingMetaData(
            tissue=Tissue.PLASMA,
            route=Route.PO,
            application_form=ApplicationForm.TABLET,
            dosing=Dosing.SINGLE,
            health=Health.ALCOHOLISM if patients else Health.HEALTHY,
            fasting=Fasting.FASTED,
            data_type=DataType.MEAN,
            coadministration=(
                Coadministration.COMEDICATION if patients else Coadministration.NONE
            ),
        )

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for group in self.body_weights:
            for key, hm in self.FigMeta.items():
                mappings[f"fm_Fig1_{key}_250_{group}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"dset_Fig1_{key}_{group}",
                        xid="time",
                        yid="mean",
                        count="count",
                        yid_sd="mean_sd",
                    ),
                    observable=FitData(
                        self,
                        task=f"task_czx250_{group}",
                        xid="time",
                        yid=required(hm.yid),
                    ),
                    metadata=self.mapping_metadata(group),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig1",
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} Fig1 (250 mg)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        for plot, (key, hm) in zip(plots, self.FigMeta.items(), strict=True):
            plot.set_yaxis(label=hm.plot_ylabel, unit=hm.unit, scale="linear")
            color = plot_colors_sid[required(hm.yid)]
            for group, label, marker, linestyle in [
                ("healthy", "healthy", "s", "-"),
                ("alcoholics", "alcoholism + chlormethiazole", "o", "--"),
            ]:
                plot.add_data(
                    task=f"task_czx250_{group}",
                    xid="time",
                    yid=required(hm.yid),
                    label=f"Sim {label}",
                    color=color,
                    linestyle=linestyle,
                )
                plot.add_data(
                    dataset=f"dset_Fig1_{key}_{group}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"Data {label}",
                    color=color,
                    marker=marker,
                    linestyle=linestyle,
                )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Eap1998, output_dir="test")
