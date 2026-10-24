"""Collect the data of the chlorzoxazone studies from the PK-DB study folders.

The studies are copied from a `pkdb_data` checkout (`PKDB_DATA`, else
`../pkdb_data`, see `pkpdsim.data.studies_dir`) into the data folder of the
model, see `pkpdsim.data.collect_tsv_files`.
Besides the chlorzoxazone studies, the experiments use the ethanol study
Wilkinson1977 (alcohol) and Benowitz2003 (caffeine), which has chlorzoxazone
groups. The experiments of Lucas1995, Oneta2002 and Orellana2006 read the
curation spreadsheets of the studies, which are copied as well.
"""

import shutil
from pathlib import Path

from pkpdsim.data import collect_tsv_files
from pkpdsim.data import studies_dir as pkdb_studies_dir

from pkdb_models.models.chlorzoxazone import (
    DATA_PATH_ALCOHOL,
    DATA_PATH_BASE,
    DATA_PATH_CAFFEINE,
    DATA_PATH_CHLORZOXAZONE,
)

#: the studies of other substances which the chlorzoxazone experiments use
ALCOHOL_STUDIES = {"Wilkinson1977"}
CAFFEINE_STUDIES = {"Benowitz2003"}

#: spreadsheets of the chlorzoxazone studies which the experiments read
CHLORZOXAZONE_SPREADSHEETS = [
    "Lucas1995/Lucas1995.xlsx",
    "Oneta2002/Oneta2002.xlsx",
    "Orellana2006/Orellana2006.xlsx",
]


def collect_data(studies_dir: Path | None = None) -> None:
    """Copy the data of the chlorzoxazone studies into the data folder of the model.

    Args:
        studies_dir: the `studies` folder of pkdb_data, by default the one of
            the checkout `pkpdsim.data.studies_dir` finds.
    """
    if studies_dir is None:
        studies_dir = pkdb_studies_dir()
    DATA_PATH_BASE.mkdir(exist_ok=True)
    collect_tsv_files(
        source_dir=studies_dir / "chlorzoxazone", target_dir=DATA_PATH_CHLORZOXAZONE
    )
    for filename in CHLORZOXAZONE_SPREADSHEETS:
        target = DATA_PATH_CHLORZOXAZONE / filename
        target.parent.mkdir(exist_ok=True)
        shutil.copy2(studies_dir / "chlorzoxazone" / filename, target)
    collect_tsv_files(
        source_dir=studies_dir / "alcohol",
        target_dir=DATA_PATH_ALCOHOL,
        filter_study=lambda study: study in ALCOHOL_STUDIES,
    )
    collect_tsv_files(
        source_dir=studies_dir / "caffeine",
        target_dir=DATA_PATH_CAFFEINE,
        filter_study=lambda study: study in CAFFEINE_STUDIES,
    )


if __name__ == "__main__":
    collect_data()
