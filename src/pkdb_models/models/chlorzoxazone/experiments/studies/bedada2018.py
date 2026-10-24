"""Simulation experiment of Bedada2018.

Chlorzoxazone (250 mg po, tablet) in healthy men, the control phase before
quercetin (500 mg capsule twice daily for 10 days); chlorzoxazone and the free
6-hydroxychlorzoxazone in plasma.
"""

from collections.abc import Mapping
from typing import ClassVar

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.experiments.studies.bedada_base import (
    BedadaSimulationExperiment,
)


class Bedada2018(BedadaSimulationExperiment):
    """Simulation experiment of Bedada2018.

    Chlorzoxazone single 250 mg dose.
    """

    fig_ids: ClassVar[Mapping[str, str]] = {"czx": "Fig1", "czx6oh": "Fig2"}
    # the paper gives only the range of the 12 men (56-76 kg), its midpoint
    body_weight: ClassVar[float] = 66.0


if __name__ == "__main__":
    MODEL.run_experiments(Bedada2018, output_dir="test")
