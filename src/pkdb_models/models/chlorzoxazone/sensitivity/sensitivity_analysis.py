"""Sensitivity analysis of the chlorzoxazone model.

The outputs are the pharmacokinetic parameters of chlorzoxazone in plasma and of
the total 6-hydroxychlorzoxazone (free and glucuronide) in plasma after a single
oral dose of 250 mg chlorzoxazone as a tablet (the non-compartmental analysis of
`pkpdutils`) and the urinary recovery of 6-hydroxychlorzoxazone, the measure of
the CYP2E1 6-hydroxylation. The parameters are the parameters of the model with
bounds of +-15 % around their value. The analyses are run as a script, the
local analysis by default:

    python -m pkdb_models.models.chlorzoxazone.sensitivity.sensitivity_analysis
    python -m pkdb_models.models.chlorzoxazone.sensitivity.sensitivity_analysis local sampling

The analyses run on `pkpdsim.sensitivity.SensitivityRunner`, which writes the
table of the parameters into `results/sensitivity` of the model and the tables
and figures of an analysis into `results/sensitivity/<analysis>`.
An analysis does not vary a parameter which one of its groups sets
(`pkpdsim.sensitivity.free_parameters`): `sampling`, over the groups, leaves out
`f_cirrhosis`. The environment variable `PKPDSIM_SENSITIVITY_N` replaces the
numbers of samples of the global analyses for a quick run, see
`pkpdsim.sensitivity.sample_size`.

The model without chlorzoxazone is stationary, so the simulation of a group
starts with the dose. The dose is followed for `END_HR` hours, long enough for
the terminal phase of chlorzoxazone (a half-life of about 1 hr, longer in
cirrhosis) and the excretion of the glucuronide. The parameters of ethanol and
of the induction of CYP2E1 by ethanol are left out: the analysis has no
ethanol.
"""

from collections.abc import Callable, Mapping

import numpy as np
from pkpdsim.sensitivity import (
    FastAnalysis,
    LocalAnalysis,
    ParameterType,
    SamplingAnalysis,
    SensitivityGroup,
    SensitivityOutput,
    SensitivityParameter,
    SensitivityRunner,
    SobolAnalysis,
    parameters_from_sbml,
    set_bounds,
    set_relative_bounds,
)
from pkpdutils import NCAOptions
from sbmlsim import Q
from sbmlsim.simulation import PK, Custom, Formula, Simulation

from pkdb_models.models.chlorzoxazone import MODEL, MODEL_PATH
from pkdb_models.models.chlorzoxazone.experiments.base_experiment import (
    ChlorzoxazoneSimulationExperiment,
)
from pkdb_models.models.chlorzoxazone.fitting.parameters import (
    parameters_pk as fit_parameters,
)

#: oral dose of chlorzoxazone of the analysis, a tablet [mg]
DOSE_CZX = 250
#: the hours after the dose
END_HR = 48
#: the limit of quantification of the non-compartmental analysis [mM], about
#: 1e-6 of the maximal plasma concentrations of chlorzoxazone and of the total
#: 6-hydroxychlorzoxazone after 250 mg (2e-2 mM), so that the noise of the
#: integrator is not the terminal phase
LLOQ = 2e-8
#: fraction of the bounds of a parameter relative to its value
BOUNDS_FRACTION = 0.15

#: outputs of the non-compartmental analysis of chlorzoxazone -> unit of the output
PK_OUTPUTS_CZX: dict[str, str] = {
    "auc_inf_obs": "mM*min",
    "cmax": "mM",
    "tmax": "min",
    "thalf": "min",
    "vz_f": "l",
    "cl_f": "ml/min",
}
#: outputs of the non-compartmental analysis of the total
#: 6-hydroxychlorzoxazone, the metabolite of the dose: no clearance or volume
#: -> unit of the output
PK_OUTPUTS_CZX6OH: dict[str, str] = {
    "auc_inf_obs": "mM*min",
    "cmax": "mM",
    "tmax": "min",
}
#: the outputs whose unit has the amount of the dose: the dose is a mass
#: (`PODOSE_czx` in mg), so they are divided by the molecular weight (its value
#: at the start, a value per simulation like the parameter of the analysis)
PK_PER_DOSE_MASS: frozenset[str] = frozenset({"vz_f", "cl_f"})


def urinary_recovery(time: np.ndarray, values: dict[str, np.ndarray]) -> float:
    """Get the 6-hydroxychlorzoxazone in the urine at the end as a fraction of the dose.

    The urine has the glucuronide [mmole], the dose is a mass [mg] of molecular
    weight `Mr_czx` [g/mole].
    """
    del time
    dose = values["PODOSE_czx"][0] / values["Mr_czx"][0]
    return float(values["Aurine_czxoglu"][-1] / dose)


#: the further outputs: id -> function, selections, unit
CUSTOM_OUTPUTS: dict[
    str,
    tuple[Callable[[np.ndarray, dict[str, np.ndarray]], float], list[str], str],
] = {
    "fe_czx6oh": (
        urinary_recovery,
        ["Aurine_czxoglu", "PODOSE_czx", "Mr_czx"],
        "dimensionless",
    ),
}

#: the outputs with their ids and names
OUTPUTS: list[SensitivityOutput] = [
    SensitivityOutput("czx_auc_inf_obs", "chlorzoxazone AUC∞"),
    SensitivityOutput("czx_cmax", "chlorzoxazone Cmax"),
    SensitivityOutput("czx_tmax", "chlorzoxazone tmax"),
    SensitivityOutput("czx_thalf", "chlorzoxazone Half-life"),
    SensitivityOutput("czx_vz_f", "chlorzoxazone Vz/F"),
    SensitivityOutput("czx_cl_f", "chlorzoxazone CL/F"),
    SensitivityOutput("czx6oh_auc_inf_obs", "6-OH-CZX (total) AUC∞"),
    SensitivityOutput("czx6oh_cmax", "6-OH-CZX (total) Cmax"),
    SensitivityOutput("czx6oh_tmax", "6-OH-CZX (total) tmax"),
    SensitivityOutput("fe_czx6oh", "6-OH-CZX urinary recovery"),
]


def _pk_observables(sid: str, expression: str, outputs: Mapping[str, str]) -> list:
    """Get the non-compartmental analysis of a substance in plasma and its outputs."""
    pk_id = f"pk_{sid}"
    return [
        PK(
            pk_id,
            expression,
            dose="PODOSE_czx",
            route="oral",
            options=NCAOptions(lloq=LLOQ),
            parameters=list(outputs),
        ),
        *(
            Formula(
                f"{sid}_{key}",
                f"{pk_id}.{key} / at(Mr_czx, 0)"
                if key in PK_PER_DOSE_MASS
                else f"{pk_id}.{key}",
                unit=unit,
            )
            for key, unit in outputs.items()
        ),
    ]


#: the observables of a simulation, the outputs with their units; the ids of
#: the analyses (`pk_czx`, `pk_czx6oh`) are no species of the model
OBSERVABLES = [
    *_pk_observables("czx", "[Cveplasma_czx]", PK_OUTPUTS_CZX),
    *_pk_observables("czx6oh", "Cve_czx6oh_all", PK_OUTPUTS_CZX6OH),
    *(
        Custom(key, function, unit, symbols=selections)
        for key, (function, selections, unit) in CUSTOM_OUTPUTS.items()
    ),
]

#: the output times [hr]: every 0.01 hr in the first 12 hr after the dose
#: (absorption, maximum and terminal phase), every 0.1 hr after them
TIMES_HR: tuple[float, ...] = tuple(
    np.unique(
        np.concatenate(
            [
                np.linspace(0, 12, 1201),
                np.linspace(12, END_HR, 10 * (END_HR - 12) + 1),
            ]
        )
    ).tolist()
)


def sensitivity_simulation(changes: Mapping[str, float]) -> Simulation:
    """Get the simulation of a group: a single oral tablet of chlorzoxazone at time 0."""
    return Simulation(
        start=0,
        end=END_HR,
        times=TIMES_HR,
        time_unit="hr",
        preinit_changes={
            **changes,
            "application_form": Q(0, "dimensionless"),
            "PODOSE_czx": Q(DOSE_CZX, "mg"),
        },
    )


#: the groups the analyses are run for: the control and the stages of
#: cirrhosis of the simulation experiments
SENSITIVITY_GROUPS: list[SensitivityGroup] = [
    SensitivityGroup("control", "Control", sensitivity_simulation({}), "dimgrey"),
    *(
        SensitivityGroup(
            uid,
            name,
            sensitivity_simulation(
                {"f_cirrhosis": ChlorzoxazoneSimulationExperiment.cirrhosis_map[name]}
            ),
            ChlorzoxazoneSimulationExperiment.cirrhosis_colors[name],
        )
        for uid, name in [
            ("mildCirrhosis", "Mild cirrhosis"),
            ("moderateCirrhosis", "Moderate cirrhosis"),
            ("severeCirrhosis", "Severe cirrhosis"),
        ]
    ),
]


def sensitivity_parameters() -> list[SensitivityParameter]:
    """Get the parameters of the analyses with their bounds and references."""
    parameters = parameters_from_sbml(
        MODEL_PATH,
        exclude_ids={
            # molecular weights
            "Mr_czx",
            "Mr_czx6oh",
            "Mr_czxoglu",
            "Mr_ethanol",
            # reference values
            "BW_ref",
            # unchangeable values
            "FQlu",
            "FVhv",
            "FVpo",
            "LI__cf_units_per_mmole",
            # dosing parameters
            "PODOSE_czx",
            "IVDOSE_czx",
            "ti_czx",
            "application_form",
            # the dissolution of solutions, the analysis doses a tablet
            "Ka_dis_solution_czx",
            # unused volumes
            "Vurine",
            "Vfeces",
            "Vstomach",
            # the fast equilibria of the liver
            "LI__CZX_k_IM",
            "LI__CZX6OH_k_EX",
            "LI__CZXOGLU_k_EX",
            "LI__ETH_k_IM",
            # ethanol and the induction of CYP2E1 by ethanol
            "ftissue_ethanol",
            "Kp_ethanol",
            "GU__Ka_abs_eth",
            "LI__ETHEL_VMAX",
            "LI__ETHEL_KM",
            "LI__Ki_cyp2e1_deg_ethanol",
            "LI__cyp2e1_thalf",
        },
        exclude_na=True,
        exclude_zero=True,
    )

    # the fitted parameters, their bounds are set relative to the value below
    set_bounds(
        parameters,
        [(fp.pid, np.nan, np.nan, ParameterType.FIT) for fp in fit_parameters],
    )
    # the scaling factors of the organ functions and of the enzymes
    set_bounds(
        parameters,
        [
            (uid, 1 - BOUNDS_FRACTION, 1 + BOUNDS_FRACTION, ParameterType.SCALING)
            for uid in [
                "KI__f_renal_function",
                "LI__f_cyp2e1",
                "LI__f_cyp2e1_Km",
                "LI__f_czxother",
                "LI__f_GLU",
                "GU__f_Ka_czx",
            ]
        ],
    )

    # the references of the values from the literature
    references = {
        "BW": r"\cite{Ogden2004, Jones2013, Thompson2009, Brown1997}",
        "FQgu": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FQh": r"\cite{Jones2013, Wynne1989, Thompson2009, Brown1997}",
        "FQki": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVar": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVgu": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVki": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVli": r"\cite{Jones2013, Wynne1989, Thompson2009, Brown1997}",
        "FVlu": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVve": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "COBW": r"\cite{Cattermole2017, Patel2021, Collis2001}",
        "BP_czx": r"\cite{DeVries1994}",
        "KI__f_renal_function": r"\cite{Stevens2024}",
    }
    by_uid = {p.uid: p for p in parameters}
    for uid, reference in references.items():
        p = by_uid[uid]
        p.reference = reference
        if p.type == ParameterType.NA:
            p.type = ParameterType.DATA

    # every parameter without bounds varies around its value
    set_relative_bounds(parameters, BOUNDS_FRACTION)
    return parameters


#: the analyses of the script, with their groups and numbers of samples
SENSITIVITY = SensitivityRunner(
    model=MODEL,
    parameters=sensitivity_parameters,
    outputs=OUTPUTS,
    observables=OBSERVABLES,
    analyses={
        "local": LocalAnalysis(groups=SENSITIVITY_GROUPS[:1], delta=0.01),
        "sampling": SamplingAnalysis(groups=SENSITIVITY_GROUPS, n=1000),
        "fast": FastAnalysis(groups=SENSITIVITY_GROUPS[:1], n=1000),
        "sobol": SobolAnalysis(groups=SENSITIVITY_GROUPS[:1], n=4096),
    },
    default=("local",),
)


if __name__ == "__main__":
    SENSITIVITY.main()
