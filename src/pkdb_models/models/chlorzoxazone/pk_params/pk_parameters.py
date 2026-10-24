"""Pharmacokinetic parameters of the curated chlorzoxazone studies.

The parameters (Cmax, AUC, elimination rate, clearance, half-life) of the groups
of the studies are collected from the tables of the curation in the data of the
model (`data/chlorzoxazone/<study>/.<study>_Tab<n>.tsv`), for the comparison with
the simulations.
"""

import re
from enum import StrEnum
from pathlib import Path
from typing import NamedTuple

import pandas as pd

from pkdb_models.models.chlorzoxazone import DATA_PATH_CHLORZOXAZONE, RESULTS_PATH_PKP


class StudyMapping(NamedTuple):
    """A group and intervention of a study with its dose and simulation results."""

    study: str
    intervention: str
    group: str
    dose: float
    task: str


class Pkps(StrEnum):
    """Pharmacokinetic parameters of the curation (the measurement types)."""

    kel = "kel"
    auc_inf = "auc_inf"
    cmax = "cmax"
    cl = "clearance"
    thalf = "thalf"


#: the control groups of the studies
all_control: list[StudyMapping] = [
    StudyMapping("Bedada2016", "CZX250", "all", 250, "Bedada2016_task_czx250.tsv"),
    StudyMapping("Bedada2017", "CZX250", "all", 250, "Bedada2017_task_czx250.tsv"),
    StudyMapping("Bedada2018", "CZX250", "all", 250, "Bedada2018_task_czx250.tsv"),
    StudyMapping(
        "Burckart1998", "CZX250", "healthy", 250, "Burckart1998_task_czx250.tsv"
    ),
    StudyMapping("Desiraju1983", "CZX", "all", 750, "Desiraju1983_task_Fig1_czx.tsv"),
    StudyMapping("DeVries1994", "CZX", "all", 250, "DeVries1994Mean_task_interpol.tsv"),
    StudyMapping(
        "Dreisbach1995", "CZX500", "all", 500, "Dreisbach1995_task_czx500.tsv"
    ),
    StudyMapping("Emery2003", "CZX750", "control", 750, "Frye1998_task_czx750.tsv"),
    StudyMapping("Frye1998", "CZX250", "all", 250, "Frye1998_task_czx250.tsv"),
    StudyMapping(
        "Frye1998", "CZX750", "dose_250_and_750", 750, "Frye1998_task_czx750.tsv"
    ),
    StudyMapping(
        "Frye1998", "CZX250", "dose_250_and_750", 250, "Frye1998_task_czx250.tsv"
    ),
    StudyMapping("Gade2018", "CZX250", "nonobese", 250, "Gade2018_task_nw.tsv"),
    StudyMapping("Girre1994", "CZX500", "healthy", 500, "Girre1994_task_czx.tsv"),
    StudyMapping("He2019", "TEST", "all", 400, "He2019_task_CZX400.tsv"),
    StudyMapping("He2019", "REF", "all", 400, "He2019_task_CZX400.tsv"),
    StudyMapping(
        "Hohmann2019", "CZX005", "all", 0.05, "Hohmann2019_task_po_czx0p05.tsv"
    ),
    StudyMapping("Hohmann2019", "CZX01", "all", 0.1, "Hohmann2019_task_po_czx0p1.tsv"),
    StudyMapping("Hohmann2019", "CZX05", "all", 0.5, "Hohmann2019_task_po_czx0p5.tsv"),
    StudyMapping("Hohmann2019", "CZX5", "all", 5, "Hohmann2019_task_po_czx5.tsv"),
    StudyMapping("Hohmann2019", "CZX50", "all", 50, "Hohmann2019_task_po_czx50.tsv"),
    StudyMapping("Hohmann2019", "CZX250", "all", 250, "Hohmann2019_task_po_czx250.tsv"),
    StudyMapping("Hohmann2019", "CZX500", "all", 500, "Hohmann2019_task_po_czx500.tsv"),
    StudyMapping(
        "LaMaza2000",
        "CZX750",
        "nonalcoholics_nw",
        750,
        "LaMaza2000_task_Fig1_na_nw.tsv",
    ),
    StudyMapping("Leclercq1998", "CZX500", "all", 500, "Leclercq1998_task_czx500.tsv"),
    StudyMapping(
        "Liangpunsakul2005",
        "CZX",
        "no_alcohol",
        500,
        "Liangpunsakul2005_task_control.tsv",
    ),
    StudyMapping("Lucas1993", "CZX500", "healthy", 500, "Lucas1993_task_czx500.tsv"),
    StudyMapping("OShea1994", "CZX250", "healthy", 250, "OShea1994_task_mean_man.tsv"),
    StudyMapping(
        "OShea1994", "CZX250", "control_women", 250, "OShea1994_task_mean_woman.tsv"
    ),
    StudyMapping("Park2006", "CZX", "all", 400, "Park2006_task_czx400.tsv"),
    StudyMapping(
        "Puris2019", "CZX", "healthy", 62.5, "Puris2019_task_Fig1_healthy.tsv"
    ),
    StudyMapping(
        "Rajnarayana2008", "CZX", "all", 250, "Rajnarayana2008_task_Fig1_CZX_REF.tsv"
    ),
    StudyMapping("Wang2003", "CZX500", "healthy", 500, "Wang2003_task_czx500.tsv"),
    StudyMapping("Vesell1995", "CZX500", "all", 500, "Vesell1995_task_czx500.tsv"),
    StudyMapping("Vesell1995", "CZX250", "all", 250, "Vesell1995_task_czx250.tsv"),
]


#: the collections of study mappings by name
STUDY_MAPPINGS: dict[str, list[StudyMapping]] = {"all_control": all_control}


def load_pk_params(name: str) -> pd.DataFrame:
    """Load the pharmacokinetic parameters of a collection of study mappings.

    The parameters are collected on first use and stored in `RESULTS_PATH_PKP`.

    Args:
        name: name of the collection, a key of `STUDY_MAPPINGS`.

    Returns:
        The pharmacokinetic parameters with the dose of the mapping.
    """
    path = RESULTS_PATH_PKP / f"pkp_{name}.tsv"
    if not path.exists():
        # the parameters were not collected yet
        RESULTS_PATH_PKP.mkdir(parents=True, exist_ok=True)
        pkp_df = PKPCollector().collect_pk_params(STUDY_MAPPINGS[name])
        pkp_df.to_csv(path, sep="\t", na_rep="NaN")
    return pd.read_csv(path, sep="\t")


class PKPCollector:
    """Collector of the pharmacokinetic parameters from the tables of the studies."""

    @staticmethod
    def load_data_set(path: Path) -> pd.DataFrame:
        """Load a table of a study."""
        return pd.read_csv(path, delimiter="\t")

    @staticmethod
    def get_paths() -> list[Path]:
        """Get the paths of the tables of the studies."""
        regex = re.compile(r".*Tab[0-9]\.tsv")
        return [
            path
            for directory in DATA_PATH_CHLORZOXAZONE.iterdir()
            if directory.is_dir()
            for path in directory.iterdir()
            if regex.match(path.name)
        ]

    @staticmethod
    def filter_pkp_df(
        df: pd.DataFrame, study_mappings: list[StudyMapping]
    ) -> list[pd.DataFrame]:
        """Get the pharmacokinetic parameters of the study mappings in a table.

        Args:
            df: table of a study.
            study_mappings: the groups and interventions to select.

        Returns:
            The selected rows per study mapping, with the dose of the mapping.
        """
        subset = []
        if "measurement" in df.columns.values and "group" in df.columns.values:
            pk_df = df[df["measurement"].isin(list(Pkps))]
            for sm in study_mappings:
                filtered = pk_df[
                    (pk_df["study"] == sm.study)
                    & (pk_df["intervention"] == sm.intervention)
                    & (pk_df["group"] == sm.group)
                ]
                filtered.insert(1, "dose", [sm.dose for _ in range(len(filtered))])
                subset.append(filtered)
        return subset

    def collect_pk_params(self, study_mappings: list[StudyMapping]) -> pd.DataFrame:
        """Collect the pharmacokinetic parameters of the study mappings.

        Args:
            study_mappings: the groups and interventions to select.

        Returns:
            The pharmacokinetic parameters of all tables of the studies.
        """
        pkp_dfs = []
        for path in self.get_paths():
            df = self.load_data_set(path)
            pkp_dfs.extend(self.filter_pkp_df(df, study_mappings))
        return pd.concat(pkp_dfs, axis=0, ignore_index=True)


if __name__ == "__main__":
    collector = PKPCollector()
    RESULTS_PATH_PKP.mkdir(parents=True, exist_ok=True)
    for name, mappings in STUDY_MAPPINGS.items():
        pkp_df = collector.collect_pk_params(mappings)
        pkp_df.to_csv(RESULTS_PATH_PKP / f"pkp_{name}.tsv", sep="\t", na_rep="NaN")
