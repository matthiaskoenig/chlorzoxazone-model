"""Simulation experiment of Frye1998.

Chlorzoxazone (250 mg and 750 mg po, tablet) in healthy men; chlorzoxazone and
6-hydroxychlorzoxazone in plasma and the cumulative amount of
6-hydroxychlorzoxazone in urine.
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
    HelperMapping,
    Sids,
    required,
)
from pkdb_models.models.chlorzoxazone.plot_colors import plot_colors_sid


class Frye1998(ChlorzoxazoneSimulationExperiment):
    """Simulation experiment of Frye1998.

    Fig1A: time courses for czx and 6-oh-czx plasma concentration after a single
    250mg oral dose (n=16)
    Fig1B: cumulative amount of 6-oh-czx in urine after a single 250mg dose (n=16)

    Fig3: time courses for czx and 6-oh-czx plasma concentration after a single
    250mg or 750mg oral dose (n=6)
    Fig4: cumulative amount of 6-oh-czx in urine after a single 250mg or 750mg
    dose (n=6)

    Chlorzoxazone single oral doses (250, 750) mg, Paraflex tablets, after an
    overnight fast in 16 healthy white men (79.7 kg); 6 of them took both doses
    (crossover), so the 250 mg data of Fig3 and Fig4 are subjects of Fig1
    (aggregate). 6-hydroxychlorzoxazone was measured after enzymatic hydrolysis
    (total) in plasma and urine. The urinary recovery in percent is the mass of
    6-hydroxychlorzoxazone over the mass of the dose (Table I: 159 mg, 63.5 %),
    the amounts are converted with the molecular weight of
    6-hydroxychlorzoxazone.
    """

    doses: ClassVar[list[int]] = [250, 750]  # [mg]

    @property
    def FigMeta(self) -> dict[str, HelperMapping]:
        """Datasets of the study by figure."""
        return {
            "Fig1A_czx": HelperMapping(
                id="Fig1A_czx",
                mr=self.Mr.czx,
                plot_ylabel=self.label_czx,
                yid=Sids.cpl_czx,
                unit="µM",
                dset_label="chlorzoxazone",
            ),
            "Fig1A_czx6oh": HelperMapping(
                id="Fig1A_czx6oh",
                mr=self.Mr.czx6oh,
                plot_ylabel=self.label_czx6oh_all,
                yid=Sids.cve_czx6oh_all,
                unit="µM",
                dset_label="6-hydroxychlorzoxazone",
            ),
            "Fig1B": HelperMapping(
                id="Fig1B",
                mr=self.Mr.czx6oh,
                plot_ylabel=self.label_czxoglu_urine,
                yid=Sids.aurine_czxoglu,
                unit="mmole",
            ),
            "Fig3A": HelperMapping(
                id="Fig3A",
                mr=self.Mr.czx,
                plot_ylabel=self.label_czx,
                yid=Sids.cpl_czx,
                unit="µM",
            ),
            "Fig3B": HelperMapping(
                id="Fig3B",
                mr=self.Mr.czx6oh,
                plot_ylabel=self.label_czx6oh_all,
                yid=Sids.cve_czx6oh_all,
                unit="µM",
            ),
            "Fig4": HelperMapping(
                id="Fig4",
                plot_ylabel=self.label_czxoglu_urine,
                yid=Sids.aurine_czxoglu,
                unit="mmole",
            ),
        }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets: dict[str, DataSet] = {}

        self.add_dset_fig4(dsets)
        self.add_dset_fig1a(dsets)
        self.add_dset_fig1b(dsets)
        self.add_dset_fig3(dsets)

        return dsets

    def add_dset_fig3(self, dsets: dict[str, DataSet]) -> None:
        """Add the plasma time courses of both doses (Fig3)."""
        for fig_id in ["Fig3A", "Fig3B"]:
            hm = self.FigMeta[fig_id]
            df = self.load_dataframe(fig_id)
            for dose in [250, 750]:
                dset = DataSet.from_df(
                    df[df["intervention"] == f"CZX{dose}"], self.ureg
                )
                dset.unit_conversion("mean", 1 / required(hm.mr))
                dsets[f"dset_{hm.id}_{dose}"] = dset

    def add_dset_fig4(self, dsets: dict[str, DataSet]) -> None:
        """Add the cumulative amounts in urine of both doses (Fig4).

        The 750 mg data has a point at 0 hr, which the 250 mg data has not; it
        is left out (no information).
        """
        df = self.load_dataframe("Fig4")
        hm = self.FigMeta["Fig4"]
        for dose in [250, 750]:
            dset = DataSet.from_df(
                df[
                    (df["intervention"] == f"CZX{dose}")
                    & (df["measurement"] == "cumulative amount")
                    & (df["time"] > 0)
                ],
                self.ureg,
            )
            dset.unit_conversion("mean", 1 / self.Mr.czx6oh)
            dsets[f"dset_{hm.id}_{dose}"] = dset

    def add_dset_fig1a(self, dsets: dict[str, DataSet]) -> None:
        """Add the plasma time courses of the 250 mg dose (Fig1A)."""
        df = self.load_dataframe("Fig1A")
        for fig_id in ["Fig1A_czx", "Fig1A_czx6oh"]:
            hm = self.FigMeta[fig_id]
            dset = DataSet.from_df(df[df["substance"] == hm.dset_label], self.ureg)
            dset.unit_conversion("mean", 1 / required(hm.mr))
            dsets[f"dset_{hm.id}"] = dset

    def add_dset_fig1b(self, dsets: dict[str, DataSet]) -> None:
        """Add the cumulative amount in urine of the 250 mg dose (Fig1B)."""
        df = self.load_dataframe("Fig1B")
        hm = self.FigMeta["Fig1B"]
        dset = DataSet.from_df(df[df["measurement"] == "cumulative amount"], self.ureg)
        dset.unit_conversion("mean", 1 / required(hm.mr))
        dsets[f"dset_{hm.id}"] = dset

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        for dose in self.doses:
            tcsims[f"czx{dose}"] = Simulation(
                time_unit="min",
                end=11 * 60,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "PODOSE_czx": Q(dose, "mg"),
                    "BW": Q(79.7, "kg"),
                },
            )
        return tcsims

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings: dict[str, FitMapping] = {}
        self.add_fit_mapping_fig1(mappings)
        self.add_fit_mapping_fig4(mappings)
        self.add_fit_mapping_fig3(mappings)

        return mappings

    @staticmethod
    def mapping_metadata(tissue: Tissue) -> PKPDMappingMetaData:
        """Healthy men, single Paraflex tablet after an overnight fast."""
        return PKPDMappingMetaData(
            tissue=tissue,
            route=Route.PO,
            application_form=ApplicationForm.TABLET,
            dosing=Dosing.SINGLE,
            health=Health.HEALTHY,
            fasting=Fasting.FASTED,
            data_type=DataType.MEAN,
        )

    def add_fit_mapping_fig4(self, mappings: dict[str, FitMapping]) -> None:
        """Add the mappings of the cumulative amounts in urine (Fig4)."""
        hm = self.FigMeta["Fig4"]
        for dose in [250, 750]:
            mappings[f"fm_{hm.id}_{dose}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"dset_{hm.id}_{dose}",
                    xid="time",
                    yid="mean",
                    count="count",
                    yid_sd="mean_sd",
                ),
                observable=FitData(
                    self,
                    task=f"task_czx{dose}",
                    xid="time",
                    yid=required(hm.yid),
                ),
                metadata=self.mapping_metadata(Tissue.URINE),
            )

    def add_fit_mapping_fig1(self, mappings: dict[str, FitMapping]) -> None:
        """Add the mappings of the 250 mg dose in plasma and urine (Fig1)."""
        for fig_id in ["Fig1A_czx", "Fig1A_czx6oh", "Fig1B"]:
            hm = self.FigMeta[fig_id]
            mappings[f"fm_{hm.id}_250"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"dset_{hm.id}",
                    xid="time",
                    yid="mean",
                    count="count",
                    yid_sd="mean_sd",
                ),
                observable=FitData(
                    self,
                    task="task_czx250",
                    xid="time",
                    yid=required(hm.yid),
                ),
                metadata=self.mapping_metadata(
                    Tissue.URINE if fig_id == "Fig1B" else Tissue.PLASMA
                ),
            )

    def add_fit_mapping_fig3(self, mappings: dict[str, FitMapping]) -> None:
        """Add the mappings of the plasma time courses of both doses (Fig3)."""
        for fig_id in ["Fig3A", "Fig3B"]:
            hm = self.FigMeta[fig_id]
            for dose in [250, 750]:
                mappings[f"fm_{hm.id}_{dose}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"dset_{hm.id}_{dose}",
                        xid="time",
                        yid="mean",
                        count="count",
                        yid_sd="mean_sd",
                    ),
                    observable=FitData(
                        self,
                        task=f"task_czx{dose}",
                        xid="time",
                        yid=required(hm.yid),
                    ),
                    metadata=self.mapping_metadata(Tissue.PLASMA),
                )

    @override
    def figures(self) -> dict[str, Figure]:
        return self.figures_by_sid(
            *self.create_fig1a(),
            self.create_fig1b(),
            *self.create_fig3(),
            *self.create_fig4(),
        )

    def create_fig4(self) -> list[Figure]:
        """Create the figures of the cumulative amounts in urine (Fig4)."""
        hm = self.FigMeta["Fig4"]
        yid = required(hm.yid)
        figures = []
        for dose in [250, 750]:
            fig = Figure(
                experiment=self,
                sid=f"{hm.id}_{dose}",
                num_rows=1,
                num_cols=1,
                name=f"{self.__class__.__name__} {hm.id} ({dose} mg)",
            )
            plots = fig.create_plots(
                xaxis=Axis(self.label_time, unit="hr"), legend=True
            )
            plots[0].set_yaxis(label=hm.plot_ylabel, unit=hm.unit, scale="linear")

            # simulation
            plots[0].add_data(
                task=f"task_czx{dose}",
                xid="time",
                yid=yid,
                label="Sim",
                color=plot_colors_sid[yid],
            )

            plots[0].add_data(
                dataset=f"dset_{hm.id}_{dose}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="Data",
                color=plot_colors_sid[yid],
            )

            figures.append(fig)
        return figures

    def create_fig1a(self) -> list[Figure]:
        """Create the figures of the plasma time courses of the 250 mg dose.

        The figures show the data of Fig1A together with the 250 mg data of Fig3.
        """
        figures = []
        fig_ids_1a = ["Fig1A_czx", "Fig1A_czx6oh"]
        fig_ids_250 = ["Fig3A", "Fig3B"]

        for fig_id1, fig_id3 in zip(fig_ids_1a, fig_ids_250, strict=True):
            hm1 = self.FigMeta[fig_id1]
            hm3 = self.FigMeta[fig_id3]
            yid1 = required(hm1.yid)
            fig = Figure(
                experiment=self,
                sid=fig_id1,
                num_rows=1,
                num_cols=1,
                name=f"{self.__class__.__name__} Fig1A/{fig_id3[-2:]} (250 mg)",
            )
            plots = fig.create_plots(
                xaxis=Axis(self.label_time, unit="hr"), legend=True
            )
            plots[0].set_yaxis(label=hm1.plot_ylabel, unit="µM", scale="linear")

            # simulation
            plots[0].add_data(
                task="task_czx250",
                xid="time",
                yid=yid1,
                label="Sim",
                color=plot_colors_sid[yid1],
            )

            plots[0].add_data(
                dataset=f"dset_{hm1.id}",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="Data",
                color=plot_colors_sid[yid1],
            )

            plots[0].add_data(
                dataset=f"dset_{hm3.id}_250",
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label="Data",
                color=plot_colors_sid[required(hm3.yid)],
                marker="v",
            )

            figures.append(fig)
        return figures

    def create_fig1b(self) -> Figure:
        """Create the figure of the cumulative amount in urine of the 250 mg dose.

        The figure shows the data of Fig1B together with the 250 mg data of Fig4.
        """
        name = "Fig1"
        hm = self.FigMeta["Fig1B"]
        hm4 = self.FigMeta["Fig4"]
        yid = required(hm.yid)

        fig = Figure(
            experiment=self,
            sid=name,
            num_rows=1,
            num_cols=1,
            name=f"{self.__class__.__name__} {hm.id}/4 (250 mg)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(label=hm.plot_ylabel, unit=hm.unit, scale="linear")

        plots[0].add_data(
            task="task_czx250",
            xid="time",
            yid=yid,
            label="Sim",
            color=plot_colors_sid[yid],
        )

        plots[0].add_data(
            dataset=f"dset_{hm.id}",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="Data",
            color=plot_colors_sid[yid],
            marker="s",
        )

        plots[0].add_data(
            dataset=f"dset_{hm4.id}_250",
            xid="time",
            yid="mean",
            yid_sd="mean_sd",
            count="count",
            label="Data",
            color=plot_colors_sid[yid],
            marker="v",
        )

        return fig

    def create_fig3(self) -> list[Figure]:
        """Create the figures of the plasma time courses of both doses (Fig3)."""
        figures = []
        fig_ids = ["Fig3A", "Fig3B"]

        for dose in [250, 750]:
            for fig_id in fig_ids:
                hm = self.FigMeta[fig_id]
                yid = required(hm.yid)
                fig = Figure(
                    experiment=self,
                    sid=f"{fig_id}_{dose}",
                    num_rows=1,
                    num_cols=1,
                    name=f"{self.__class__.__name__} {fig_id} ({dose} mg)",
                )
                plots = fig.create_plots(
                    xaxis=Axis(self.label_time, unit="hr"), legend=True
                )
                plots[0].set_yaxis(label=hm.plot_ylabel, unit="µM", scale="linear")

                plots[0].add_data(
                    task=f"task_czx{dose}",
                    xid="time",
                    yid=yid,
                    label="Sim",
                    color=plot_colors_sid[yid],
                )

                plots[0].add_data(
                    dataset=f"dset_{hm.id}_{dose}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label="Data",
                    color=plot_colors_sid[yid],
                )
                figures.append(fig)
        return figures


if __name__ == "__main__":
    MODEL.run_experiments(Frye1998, output_dir="test")
