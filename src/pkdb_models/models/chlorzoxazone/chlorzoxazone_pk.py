"""Pharmacokinetic parameters of chlorzoxazone in the simulations of the scans.

The pharmacokinetic parameters are the non-compartmental analysis of
`pkpdutils`, named like the variables of its `NCAResult`: e.g. `auc_last`,
`auc_inf_obs`, `cmax`, `tmax`, `thalf`, `lambda_z`, and `cl_f`, `vz_f` after the
oral doses of chlorzoxazone.

The simulations decay to the numerical noise of the integrator (about 1e-26 mM
after days), which the best-fit terminal phase would take as the terminal phase:
the concentrations below 1e-6 of the maximum are below the limit of quantification
of the analysis (`LLOQ_FRACTION`).

`calculate_chlorzoxazone_pk` analyses every simulation of a scan of one
dimension: chlorzoxazone in plasma with its oral dose and the total
6-hydroxychlorzoxazone (free and glucuronide) without a dose. A run over the
draws of the fitted parameters (`run_simulation
pkdb_models.models.chlorzoxazone --uncertainty`) adds the dimension of the
draws; the parameters are calculated for every point of every dimension, a row
per point with its position along each dimension (the columns `point` and,
with draws, `draw`), see `summarize`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from pkpdsim.pk import nca_frame, scan_nca
from pkpdsim.scan import scan_dimensions, start_values
from pkpdutils import NCAResult, Route
from sbmlsim import Q
from sbmlsim.result import ScanResult
from sbmlsim.units import Quantity

if TYPE_CHECKING:
    from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
        ChlorzoxazoneSimulationExperiment,
    )

#: oral dose of the scans
DOSE = "PODOSE_czx"
#: the analytes -> their concentration and whether the dose is theirs
ANALYTES: dict[str, tuple[str, bool]] = {
    "czx": ("[Cveplasma_czx]", True),
    "czx6oh_all": ("Cve_czx6oh_all", False),
}

#: the limit of quantification of the analysis relative to the maximal concentration
LLOQ_FRACTION = 1e-6


def scan_analysis(
    res: ScanResult,
    key: str,
    dose: Quantity | None = None,
    substance: str = "chlorzoxazone",
) -> NCAResult:
    """Non-compartmental analysis of a timecourse in plasma after an oral dose.

    All points of the result are analysed at once (`scan_nca`).

    Args:
        res: the result, of any number of dimensions.
        key: the concentration in plasma.
        dose: the oral dose as an amount of substance, which the clearance and
            the volume of distribution require: one dose of all points, or the
            dose of every point in the shape of the dimensions of the result;
            `None` for the parameters of the curve alone (e.g. the AUC of a
            metabolite).
        substance: the substance of the timecourse.

    Returns:
        The analysis over the dimensions of the result.
    """
    return scan_nca(
        res,
        key,
        dose=dose,
        route=None if dose is None else Route.ORAL,
        substance=substance,
        lloq_fraction=LLOQ_FRACTION,
    )


def _scan_dimension(res: ScanResult, across: str | None) -> str:
    """Get the dimension of a scan besides the draws `across`.

    Raises:
        ValueError: if the scan has not one dimension besides the draws.
    """
    dims = scan_dimensions(res, across)
    if len(dims) != 1:
        raise ValueError(
            f"A scan of one dimension is required, not of {dims} (draws: {across})."
        )
    return dims[0]


def calculate_chlorzoxazone_pk(
    experiment: ChlorzoxazoneSimulationExperiment,
    res: ScanResult,
    across: str | None = None,
) -> pd.DataFrame:
    """Calculate the pharmacokinetic parameters of every simulation of a scan.

    Every analyte is analysed at all points of the scan at once
    (`scan_analysis`).

    Args:
        experiment: experiment of the scan.
        res: result of the scan, a scan with an oral dose of chlorzoxazone.
        across: the dimension of the draws of the fitted parameters, `None`
            for a scan without draws.

    Returns:
        One row per simulation of the scan and analyte, with its position
        (`point`, and `draw` with draws), the parameters and their units
        (`<name>_unit`).
    """
    names = {_scan_dimension(res, across): "point"}
    if across is not None:
        names[across] = "draw"
    positions = list(names.values())
    dfs = []
    for substance, (concentration, with_dose) in ANALYTES.items():
        dose = None
        if with_dose:
            dose = (
                Q(start_values(res, DOSE).values, res.units[DOSE]) / experiment.Mr.czx
            )
        result = scan_analysis(res, concentration, dose=dose, substance=substance)
        df = nca_frame(result).drop(columns="nca_flags").rename(columns=names)
        df.insert(len(positions), "substance", substance)
        df = df[[*positions, *df.columns.drop(positions)]]
        dfs.append(df.sort_values(positions, kind="stable"))
    return pd.concat(dfs, ignore_index=True)


def summarize(
    df: pd.DataFrame, key: str, quantiles: tuple[float, float]
) -> pd.DataFrame:
    """Get the median and the quantiles of a parameter over the draws of every point.

    Args:
        df: the parameters with the columns `point` and `draw`.
        key: the parameter.
        quantiles: the lower and the upper quantile.

    Returns:
        One row per point (the index), the columns `lower`, `median`, `upper`.
    """
    low, high = quantiles
    grouped = df.groupby("point")[key]
    return pd.DataFrame(
        {
            "lower": grouped.quantile(low),
            "median": grouped.median(),
            "upper": grouped.quantile(high),
        }
    ).astype(np.float64)
