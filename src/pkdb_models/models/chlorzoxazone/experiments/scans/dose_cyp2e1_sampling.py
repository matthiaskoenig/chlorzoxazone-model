"""Sampling CYP2E1 protein amount from distributions.

Using experimental in vitro CYP2E1 distributions to simulate variability in
chlorzoxazone pharmacokinetics.

Using various doses.
"""

from typing import Any, ClassVar, override

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure as FigureMPL
from pint import Unit
from pkpdsim.metadata import ApplicationForm
from sbmlsim import Q
from sbmlsim.result import ScanResult
from sbmlsim.simulation import Dimension, Scan, Simulation
from sbmlsim.units import Quantity

from pkdb_models.models.chlorzoxazone import MODEL
from pkdb_models.models.chlorzoxazone.chlorzoxazone_pk import scan_analysis
from pkdb_models.models.chlorzoxazone.cyp2e1_amounts.helper import load_cyp_amounts
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
    Sids,
)
from pkdb_models.models.chlorzoxazone.pk_params.pk_parameters import (
    Pkps,
    all_control,
    load_pk_params,
)

#: the parameters of the non-compartmental analysis of pkpdutils
pk_keys = ["cmax", "auc_inf_obs", "lambda_z", "cl_f"]

#: the parameters of the curated studies
pk_key_map = {
    "cmax": Pkps.cmax,
    "auc_inf_obs": Pkps.auc_inf,
    "lambda_z": Pkps.kel,
    "cl_f": Pkps.cl,
}

#: the curated parameters given as a mass, which are converted to an amount
pk_key_mr_map = {"cmax": True, "auc_inf_obs": True, "lambda_z": False, "cl_f": False}

pk_units = ["mM", "µmole/ml*hr", "1/min", "ml/min"]


def get_f_cyp2e1(obs_mean: float, std: float, seed: int) -> np.ndarray:
    """Sample CYP2E1 activities from the distribution of the CYP2E1 amounts.

    Sampling from a normal distribution with the mean and standard deviation of
    the logarithm of the curated CYP2E1 amounts, re-transforming by exponentiation
    and rescaling by the mean of the samples.

    Args:
        obs_mean: mean of the logarithm of the amounts.
        std: standard deviation of the logarithm of the amounts.
        seed: seed of the generator, so that the samples are the same in every run.

    Returns:
        200 CYP2E1 activities relative to their mean.
    """
    rng = np.random.default_rng(seed)
    sampled_log_normal = np.exp(rng.normal(loc=obs_mean, scale=std, size=200))
    return sampled_log_normal / np.mean(sampled_log_normal)


class CZXDoseCyp2e1ActivityScan(ChlorzoxazoneSimulationExperiment):
    """Sampling of the CYP2E1 activity for three oral doses.

    The CYP2E1 activities are sampled from the distribution of the protein amounts
    observed in human liver microsomes (caucasian): the distributions of the
    pharmacokinetic parameters of every dose.
    """

    doses: ClassVar[list[int]] = [250, 500, 750]
    cyp2e1_amounts: ClassVar[dict[str, Any]] = load_cyp_amounts(identifier="caucasian")
    obs_mean: ClassVar[float] = cyp2e1_amounts["mu"]
    std: ClassVar[float] = cyp2e1_amounts["sigma"]
    cyp2e1: ClassVar[np.ndarray] = get_f_cyp2e1(obs_mean=obs_mean, std=std, seed=8)

    @override
    def simulations(self) -> dict[str, Scan]:
        tcscans = {}
        for i, dose in enumerate(self.doses):
            tcscans[f"scan_f_cyp2e1_{i}"] = Scan(
                simulation=Simulation(
                    time_unit="min",
                    end=20 * 60,
                    preinit_changes={
                        **self.default_changes(ApplicationForm.TABLET),
                        "PODOSE_czx": Q(dose, "mg"),
                    },
                ),
                dimensions=[
                    Dimension(
                        "dim_cyp2e1",
                        values={
                            "LI__f_cyp2e1": Q(
                                self.population(self.cyp2e1, size=20), "dimensionless"
                            )
                        },
                    ),
                ],
            )

        return tcscans

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return {"fig_cyp2e1_sampling_pkp": self.fig_pk_distributions()}

    def fig_pk_distributions(self) -> FigureMPL:
        """Distributions of the pharmacokinetic parameters of every dose.

        Returns:
            The figure with the distributions and the curated data of the studies.
        """
        pk_results = self.calc_dose_pk_distributions()
        f, axes = plt.subplots(2, 2, dpi=300)
        axes = axes.flatten()

        for i, pk_key in enumerate(pk_keys):
            # vectors for a pharmacokinetic parameter for each dose
            vectors = [
                pk_results[task_id][pk_key]
                .to(self.ureg(pk_units[i]), "chemistry", mw=self.Mr.czx)
                .magnitude
                for task_id in pk_results
            ]

            axes[i].violinplot(vectors, showmeans=True)
            axes[i].set_ylabel(f"{pk_key} ({self.ureg(pk_units[i]).units:~P})")

        pk_params = load_pk_params("all_control")
        groupby = pk_params.groupby(["measurement", "intervention"])
        # the position of a dose (mg) on the x-axis
        dose_index: dict[float, int] = {
            dose: i + 1 for i, dose in enumerate(self.doses)
        }
        for sm in all_control:
            # the groups of the scanned doses
            if sm.dose not in dose_index:
                continue
            for i, pk_key in enumerate(pk_keys):
                try:
                    df = groupby.get_group((pk_key_map[pk_key].value, sm.intervention))
                except KeyError:
                    continue
                for _, row in df.iterrows():
                    # skip clearances that are normalized to body weight
                    if pk_key == "cl_f" and not Unit(row["unit"]).is_compatible_with(
                        "ml/min"
                    ):
                        continue
                    if row["mean"]:
                        q = Q(row["mean"], row["unit"])
                        # converting mass to mole
                        if pk_key_mr_map[pk_key]:
                            q = q / self.Mr.czx
                        transformed = q.to(pk_units[i])
                        axes[i].plot(
                            dose_index[sm.dose],
                            transformed.magnitude,
                            marker="o",
                            color="black",
                        )

        for ax in axes:
            ax.set_xticks(range(1, len(self.doses) + 1))
            ax.set_xticklabels(self.doses)
            ax.set_xlabel("dose (mg)")

        return f

    def calc_dose_pk_distributions(self) -> dict[str, dict[str, Quantity]]:
        """Get the pharmacokinetic parameters of every simulation of every dose.

        Returns:
            The parameters of every simulation by simulation key and parameter.
        """
        return {
            f"scan_f_cyp2e1_{i}": self.calculate_pk_dist_for_dose(
                self.results[f"task_scan_f_cyp2e1_{i}"], dose
            )
            for i, dose in enumerate(self.doses)
        }

    def calculate_pk_dist_for_dose(
        self, xres: ScanResult, dose: float
    ) -> dict[str, Quantity]:
        """Get the pharmacokinetic parameters of chlorzoxazone of a scan.

        Args:
            xres: the result of the scan of a dose.
            dose: the oral dose of chlorzoxazone in mg.

        Returns:
            The parameters of every simulation of the scan by parameter.
        """
        result = scan_analysis(xres, Sids.cpl_czx, dose=Q(dose, "mg") / self.Mr.czx)
        # every individual with every draw in a run over the draws
        return {
            pk_key: Q(
                self.draw_values(
                    result.ds[pk_key].transpose("dim_cyp2e1", ...)
                ).ravel(),
                result.units(pk_key),
            )
            for pk_key in pk_keys
        }


if __name__ == "__main__":
    MODEL.run_experiments(CZXDoseCyp2e1ActivityScan, output_dir="test")
