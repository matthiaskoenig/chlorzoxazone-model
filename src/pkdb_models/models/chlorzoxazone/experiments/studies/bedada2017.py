"""Simulation experiment of Bedada2017.

Chlorzoxazone (250 mg po, tablet) in healthy men, the control phase before
piperine (20 mg capsule once daily for 10 days); chlorzoxazone and the free
6-hydroxychlorzoxazone in plasma.
"""

from collections.abc import Mapping
from typing import ClassVar

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.studies.bedada_base import (
    BedadaSimulationExperiment,
)


class Bedada2017(BedadaSimulationExperiment):
    """Simulation experiment of Bedada2017.

    Chlorzoxazone single 250 mg dose.
    """

    fig_ids: ClassVar[Mapping[str, str]] = {"czx": "Fig2", "czx6oh": "Fig3"}
    # the mean of the 12 men (Table of the subjects, the same as Bedada2016)
    body_weight: ClassVar[float] = 66.42


if __name__ == "__main__":
    MODEL.run_experiments(Bedada2017, output_dir="test")
