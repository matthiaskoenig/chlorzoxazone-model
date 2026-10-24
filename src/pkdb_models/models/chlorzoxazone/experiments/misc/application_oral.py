"""Oral application of chlorzoxazone in different doses."""

from typing import ClassVar, override

from pkpdsim.metadata import ApplicationForm
from sbmlsim import Q
from sbmlsim.plot import Axis, Figure, Plot
from sbmlsim.simulation import Simulation

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
)


class ApplicationExperiment(ChlorzoxazoneSimulationExperiment):
    """Tests oral application of chlorzoxazone."""

    doses: ClassVar[list[int]] = [50, 250, 750]  # [mg]

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}
        tend = 5 * 60  # [min]

        for dose in self.doses:
            tcsims[f"czx_or_{dose}"] = Simulation(
                time_unit="min",
                end=tend,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "PODOSE_czx": Q(dose, "mg"),
                },
            )
        return tcsims

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Oral chlorzoxazone application"
        fig = Figure(
            experiment=self,
            sid="Fig_oral_application",
            num_rows=3,
            num_cols=2,
            name=name,
        )
        plots = fig.create_plots(xaxis=Axis("time", unit="hr"), legend=True)

        sids = [
            "[Cveplasma_czx]",
            "[Cve_czx6oh]",
            "Cve_czx6oh_all",
            "[LI__czx]",
            "[LI__czx6oh]",
            "Aurine_czxoglu",
        ]

        for k, sid in enumerate(sids):
            self.plot_grouped_species(sid, plots[k])

        return self.figures_by_sid(fig)

    def plot_grouped_species(self, sid: str, plot: Plot) -> None:
        """Plot a species in the simulations of all doses.

        Args:
            sid: id of the species.
            plot: plot to add the curves to.
        """
        plot.set_yaxis(self.labels[sid], unit=self.units[sid])

        for dose in self.doses:
            plot.add_data(
                task=f"task_czx_or_{dose}",
                xid="time",
                yid=sid,
                label=f"CZX {dose} mg PO",
            )


if __name__ == "__main__":
    MODEL.run_experiments(ApplicationExperiment, output_dir="test")
