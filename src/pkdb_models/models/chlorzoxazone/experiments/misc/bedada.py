"""Combined figures of Bedada2016, Bedada2017 and Bedada2018.

Chlorzoxazone (250 mg po, tablet); chlorzoxazone and 6-hydroxychlorzoxazone in
plasma of the three studies with a single simulation. The free
6-hydroxychlorzoxazone of the three papers is one figure (see
`studies.bedada_base`).
"""

from typing import override

from pkpdsim.metadata import ApplicationForm
from sbmlsim import Q
from sbmlsim.data import DataSet
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


class Bedada(ChlorzoxazoneSimulationExperiment):
    """Combined simulation experiment of Bedada2016, Bedada2017 and Bedada2018.

    Chlorzoxazone single 250 mg dose.
    """

    @property
    def FigMeta(self) -> dict[str, HelperMapping]:
        """Datasets of the studies by study and substance."""
        return {
            "Bedada2016_CZX": HelperMapping(
                study="Bedada2016",
                id="Fig1",
                mr=self.Mr.czx,
                plot_ylabel=self.label_czx,
                yid=Sids.cpl_czx,
                unit="µM",
                dset_label="Fig1_chlorzoxazone_CZX250",
            ),
            "Bedada2016_CZX6OH": HelperMapping(
                study="Bedada2016",
                id="Fig2",
                mr=self.Mr.czx6oh,
                plot_ylabel=self.label_czx6oh,
                yid=Sids.cve_czx6oh,
                unit="µM",
                dset_label="Fig2_6-hydroxychlorzoxazone_CZX250",
            ),
            "Bedada2017_CZX": HelperMapping(
                study="Bedada2017",
                id="Fig2",
                mr=self.Mr.czx,
                plot_ylabel=self.label_czx,
                yid=Sids.cpl_czx,
                unit="µM",
                dset_label="Fig2_chlorzoxazone_CZX250",
            ),
            "Bedada2017_CZX6OH": HelperMapping(
                study="Bedada2017",
                id="Fig3",
                mr=self.Mr.czx6oh,
                plot_ylabel=self.label_czx6oh,
                yid=Sids.cve_czx6oh,
                unit="µM",
                dset_label="Fig3_6-hydroxychlorzoxazone_CZX250",
            ),
            "Bedada2018_CZX": HelperMapping(
                study="Bedada2018",
                id="Fig1",
                mr=self.Mr.czx,
                plot_ylabel=self.label_czx,
                yid=Sids.cpl_czx,
                unit="µM",
                dset_label="Fig1_chlorzoxazone_CZX250",
            ),
            "Bedada2018_CZX6OH": HelperMapping(
                study="Bedada2018",
                id="Fig2",
                mr=self.Mr.czx6oh,
                plot_ylabel=self.label_czx6oh,
                yid=Sids.cve_czx6oh,
                unit="µM",
                dset_label="Fig2_6-hydroxychlorzoxazone_CZX250",
            ),
        }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id, hm in self.FigMeta.items():
            df = self.load_dataframe(required(hm.id), study=hm.study)
            df = df[df["label"] == hm.dset_label]
            dset = DataSet.from_df(df, self.ureg)
            dset.unit_conversion("mean", 1 / required(hm.mr))
            dsets[self.to_sid(f"dset_{fig_id}")] = dset
        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        tcsims["czx250"] = Simulation(
            time_unit="min",
            end=9 * 60,
            preinit_changes={
                **self.default_changes(ApplicationForm.TABLET),
                "PODOSE_czx": Q(250, "mg"),
                # the mean of Bedada2016 and Bedada2017 (Bedada2018: 56-76 kg)
                "BW": Q(66.42, "kg"),
            },
        )

        return tcsims

    @override
    def figures(self) -> dict[str, Figure]:
        figures = {}
        years = {"Bedada2016": 2016, "Bedada2017": 2017, "Bedada2018": 2018}
        markers = {"Bedada2016": "s", "Bedada2017": "o", "Bedada2018": "v"}
        for sid, label in zip(
            [Sids.cpl_czx, Sids.cve_czx6oh],
            [self.label_czx, self.label_czx6oh],
            strict=True,
        ):
            fig = Figure(
                experiment=self,
                sid=self.to_sid(f"fig_{label}"),
                num_rows=1,
                num_cols=1,
                name=f"{self.__class__.__name__} {label} (250 mg)",
            )
            plot = fig.create_plots(
                xaxis=Axis(self.label_time, unit="hr"), legend=True
            )[0]

            plot.set_yaxis(label=label, unit="µM", scale="linear")
            for i, (fig_id, hm) in enumerate(self.FigMeta.items()):
                if hm.yid != sid:
                    continue
                yid = required(hm.yid)
                study = required(hm.study)
                plot.add_data(
                    task="task_czx250",
                    xid="time",
                    yid=yid,
                    # the simulation in the legend once
                    label="Sim" if i in [0, 1] else None,
                    color=plot_colors_sid[yid],
                )

                plot.add_data(
                    dataset=self.to_sid(f"dset_{fig_id}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{years[study]}",
                    marker=markers[study],
                    color=plot_colors_sid[yid],
                )
            figures[self.to_sid(f"fig_{label}")] = fig

        return figures


if __name__ == "__main__":
    MODEL.run_experiments(Bedada, output_dir="test")
