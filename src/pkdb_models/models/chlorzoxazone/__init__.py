"""Chlorzoxazone: PBPK model of chlorzoxazone, its CYP2E1 metabolism and ethanol.

The paths of the model and its model object `MODEL`, which the commands
`run_simulation`, `run_fit`, `run_report` and `run_identifiability` of pkpdsim
run by its package `pkdb_models.models.chlorzoxazone`.
"""

from pathlib import Path

from pkpdsim.model import FigureSettings, PKPDModel, SimulatorSettings
from pkpdsim.release.settings import Author, ReleaseSettings

from pkdb_models.models.chlorzoxazone.tolerances import ABSOLUTE_TOLERANCE

CHLORZOXAZONE_PATH = Path(__file__).parent

MODEL_BASE_PATH = CHLORZOXAZONE_PATH / "models" / "output" / "models"
MODEL_PATH = MODEL_BASE_PATH / "chlorzoxazone_body_flat.xml"

DATA_PATH_BASE = CHLORZOXAZONE_PATH / "data"
DATA_PATH_CHLORZOXAZONE = DATA_PATH_BASE / "chlorzoxazone"
DATA_PATH_ALCOHOL = DATA_PATH_BASE / "alcohol"
DATA_PATH_CAFFEINE = DATA_PATH_BASE / "caffeine"
DATA_PATHS = [
    DATA_PATH_CHLORZOXAZONE,
    DATA_PATH_ALCOHOL,
    DATA_PATH_CAFFEINE,
]

MODEL = PKPDModel(
    name="chlorzoxazone",
    package=__name__,
    title="Chlorzoxazone PBPK model",
    path=CHLORZOXAZONE_PATH,
    model_path=MODEL_PATH,
    data_paths=tuple(DATA_PATHS),
    archive_path=MODEL_BASE_PATH.parent / "chlorzoxazone_model.omex",
    factory=".models.factory:create_chlorzoxazone_models",
    experiments=".simulations:EXPERIMENTS",
    fit_definitions=".fitting.fitting:FIT_DEFINITIONS",
    simulator=SimulatorSettings(
        absolute_tolerance=ABSOLUTE_TOLERANCE, relative_tolerance=1e-10
    ),
    figures=FigureSettings(formats=("svg",), legend_fontsize=10),
    fit_identifiability=True,
    # the adopted fits in `models/output/fits`, whose values and uncertainty the
    # factory takes (`models/fits.py`)
    fits=("PK_20261020_035132__b4a12", "ALCOHOL_20261020_043001__556d3"),
    # the release of the model repository
    release=ReleaseSettings(
        title="Physiologically based pharmacokinetic (PBPK) model of chlorzoxazone",
        repository="matthiaskoenig/chlorzoxazone-model",
        doi="10.5281/zenodo.7760665",
        authors=(
            Author(
                "Küttner, Jonas",
                "0000-0001-7315-9715",
                "Humboldt-University Berlin, Institute for Theoretical Biology, Berlin",
            ),
            Author(
                "König, Matthias",
                "0000-0003-1725-179X",
                (
                    "Humboldt-Universität zu Berlin, Faculty of Life Sciences, Department of Biology, Institute of Theoretical Biology, Systems Medicine of the Liver; University of Stuttgart, Institute of Structural Mechanics and Dynamics in Aerospace Engineering; University of Southern Denmark, Clinical Pharmacology, Pharmacy and Environmental Medicine, Department of Public Health; University Hospital Schleswig-Holstein, Campus Lübeck, First Department of Medicine, Lübeck, Germany"
                ),
            ),
        ),
        keywords=(
            "model",
            "chlorzoxazone",
            "CYP2E1",
            "ethanol",
            "pharmacokinetics",
            "PBPK",
            "physiologically based pharmacokinetic model",
            "SBML",
        ),
        docker_image="matthiaskoenig/chlorzoxazone",
        funding=(
            "Matthias König was supported by the Federal Ministry of Research, Technology and Space (BMFTR, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA). This work was supported by the BMBF-funded de.NBI Cloud within the German Network for Bioinformatics Infrastructure (de.NBI) (031A537B, 031A533A, 031A538A, 031A533B, 031A535A, 031A537C, 031A534A, 031A532B)."
        ),
        description=(
            "This repository provides the chlorzoxazone physiologically based"
            " pharmacokinetic (PBPK) model: the probe of CYP2E1, its oral"
            " absorption, its distribution in the tissues, its 6-hydroxylation by"
            " CYP2E1 and a second elimination in the liver, the glucuronidation"
            " of 6-hydroxychlorzoxazone and the renal excretion of the"
            " glucuronide, and the induction of CYP2E1 by ethanol."
        ),
        first_year=2022,
    ),
)
"""The chlorzoxazone model: its commands, see `pkpdsim.model`."""

RESULTS_PATH_CYP_AMOUNTS = MODEL.results_dir / "cyp_amounts"
RESULTS_PATH_PKP = MODEL.results_dir / "pk_params"
