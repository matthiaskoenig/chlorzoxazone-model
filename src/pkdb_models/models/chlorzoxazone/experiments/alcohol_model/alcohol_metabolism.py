"""Single oral doses of ethanol.

Oral doses of 5 to 45 g ethanol: ethanol in plasma and in the liver.
"""

from typing import ClassVar, override

from pkpdsim.metadata import ApplicationForm
from sbmlsim import Q
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    Sids,
)


class AlcoholMetabolism(ChlorzoxazoneSimulationExperiment):
    """Single oral doses of ethanol."""

    #: the doses of ethanol [g]
    doses: ClassVar[list[int]] = [5, 15, 25, 35, 45]

    @override
    def simulations(self) -> dict[str, Simulation]:
        tcsims = {}

        for dose in self.doses:
            tcsims[self.to_sid(f"eth{dose}")] = Simulation(
                time_unit="min",
                end=4 * 60,
                preinit_changes={
                    **self.default_changes(ApplicationForm.TABLET),
                    "GU__PODOSE_ethanol": Q(dose, "g"),
                },
            )

        return tcsims

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Fig1 and Fig2"
        fig = Figure(
            experiment=self,
            sid=self.to_sid(name),
            num_rows=1,
            num_cols=2,
            name=f"{self.__class__.__name__} {name}",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hour"), legend=True)

        plots[0].set_yaxis(label="plasma ethanol conc", unit="mM")
        plots[1].set_yaxis(label="liver ethanol conc", unit="mM")

        for dose in self.doses:
            plots[0].add_data(
                task=self.to_sid(f"task_eth{dose}"),
                xid="time",
                yid=Sids.cve_ethanol,
                label=f"Sim {dose} [g]",
                color="black",
            )
            plots[1].add_data(
                task=self.to_sid(f"task_eth{dose}"),
                xid="time",
                yid=Sids.cli_ethanol,
                label=f"Sim {dose} [g]",
                color="black",
            )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(AlcoholMetabolism, output_dir="test")
