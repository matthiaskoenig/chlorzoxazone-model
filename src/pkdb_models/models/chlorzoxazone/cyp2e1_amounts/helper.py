"""Log-normal distributions of the CYP2E1 amounts and samples of CYP2E1 activities."""

import json
import tempfile
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import norm

from pkdb_models.models.chlorzoxazone import RESULTS_PATH_CYP_AMOUNTS


def get_data_dict(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Get the data points of the CYP2E1 amounts of a table."""
    return [
        {
            "study": row["study"],
            "source": row["source"],
            "donor type": row["subjects"],
            "amount": row["amount"],
            "amount_unit": row["amount_unit"],
            "ethnicity": row["ethnicity"],
        }
        for _, row in df.iterrows()
    ]


def save_result(df: pd.DataFrame, mu: float, sigma: float, identifier: str) -> None:
    """Save the log-normal distribution of CYP2E1 amounts with its data.

    Args:
        df: the CYP2E1 amounts of the distribution.
        mu: mean of the logarithm of the amounts.
        sigma: standard deviation of the logarithm of the amounts.
        identifier: the ethnicity of the amounts, e.g. `caucasian`.
    """
    result_dict = {
        "dist": "log-normal",
        "mu": mu,
        "sigma": sigma,
        "data": get_data_dict(df),
    }
    save(result_dict, identifier)


def save(result_dict: dict[str, Any], identifier: str) -> None:
    """Save the distribution of the CYP2E1 amounts of an ethnicity.

    The file is written under a temporary name and renamed, so that a process
    which loads it at the same time (the scans load it when they are imported,
    e.g. by every worker of pytest) never reads a partial file.
    """
    RESULTS_PATH_CYP_AMOUNTS.mkdir(parents=True, exist_ok=True)
    path = RESULTS_PATH_CYP_AMOUNTS / f"cyp2e1_amounts_{identifier}.json"
    with tempfile.NamedTemporaryFile(
        "w", dir=path.parent, prefix=f"{path.name}.", suffix=".tmp", delete=False
    ) as f:
        f.write(json.dumps(result_dict))
    Path(f.name).replace(path)


def load_cyp_amounts(identifier: str) -> dict[str, Any]:
    """Load the distribution of the CYP2E1 amounts of an ethnicity.

    The distribution is fitted on first use, see `fit_cyp_amounts`.

    Args:
        identifier: the ethnicity, e.g. `caucasian`.

    Returns:
        The distribution: `mu` and `sigma` of the logarithm and its data.
    """
    path = RESULTS_PATH_CYP_AMOUNTS / f"cyp2e1_amounts_{identifier}.json"
    if not path.exists():
        # the fit of the amounts was not run yet
        fit_cyp_amounts(identifier)
    with open(path) as f:
        return json.load(f)


def fit_cyp_amounts(identifier: str) -> None:
    """Fit a log-normal distribution to the CYP2E1 amounts of an ethnicity and save it.

    The fit of `cyp2e1_amount.fit_and_plot_cyp2e1` without the figures.

    Args:
        identifier: the ethnicity, e.g. `caucasian`.
    """
    df_all = pd.read_excel(Path(__file__).parent / "cyp2e1_amounts.xlsx", "Data")
    df = df_all[df_all["ethnicity"].str.contains(identifier)]
    mu, sigma = norm.fit(np.log(df["amount"]))
    save_result(df=df, mu=mu, sigma=sigma, identifier=identifier)


def sample_cyp2e1(cv: float, fac: float, seed: int, size: int = 500) -> np.ndarray:
    """Sample CYP2E1 activities from a log-normal distribution.

    The samples of the normal distribution of the logarithm with the mean and
    standard deviation of a log-normal distribution with mean `fac` and the
    coefficient of variation `cv` (of the data), re-transformed by
    exponentiation. The generator is seeded, so that the samples are the same in
    every run.

    Args:
        cv: coefficient of variation.
        fac: mean of the activities.
        seed: seed of the generator.
        size: number of samples.

    Returns:
        The sampled activities.
    """
    rng = np.random.default_rng(seed)
    return np.exp(
        rng.normal(
            loc=np.log(fac) - 0.5 * np.log(cv**2 + 1),
            scale=np.sqrt(np.log(cv**2 + 1)),
            size=size,
        )
    )
