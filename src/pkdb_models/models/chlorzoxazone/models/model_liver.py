"""Chlorzoxazone liver model.

Chlorzoxazone is 6-hydroxylated by CYP2E1 (`CZXOX`, Michaelis-Menten) and
eliminated by a second, CYP2E1 independent pathway to unidentified metabolites
(`CZXOTHER`, first order). 6-hydroxychlorzoxazone is glucuronidated
(`CZXOGLU`, first order) and the glucuronide leaves the liver into the plasma,
from where the kidneys excrete it. The model contains the elimination of
ethanol and the stabilization of CYP2E1 by ethanol (the induction of CYP2E1 by
drinking).
"""

import numpy as np
from pkpdsim.templates import terms_of_use
from sbmlutils.factory import (
    AssignmentRule,
    Compartment,
    FactoryResult,
    Model,
    Parameter,
    Reaction,
    Species,
    UnitDefinition,
    create_model,
)
from sbmlutils.metadata import SBO

from pkdb_models.models.chlorzoxazone.models import annotations, templates
from pkdb_models.models.chlorzoxazone.models.fits import FITS


class U(templates.U):
    """UnitDefinitions of the liver model."""

    kg = UnitDefinition("kg", "kg")
    per_mmole = UnitDefinition("per_mmole", "1/mmole")
    mmole_l_per_min = UnitDefinition("mmole_l_per_min", "mmole*l/min")


_m = Model(
    "chlorzoxazone_liver",
    name="Model for chlorzoxazone elimination in the liver",
    # the trailing whitespace of the notes is part of the SBML
    notes="""
    # Model for chlorzoxazone elimination in the liver

    Model for the hepatic metabolism of chlorzoxazone via CYP2E1 and a second,
    CYP2E1 independent pathway, the glucuronidation of 6-hydroxychlorzoxazone,
    the elimination of ethanol and the turnover of CYP2E1 encoded in
    <a href="http://sbml.org">SBML</a> format.
    """
    + terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
)

_m.compartments = [
    Compartment(
        "Vext",
        4,
        name="plasma",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["plasma"],
    ),
    Compartment(
        "Vli",
        1.5,
        name="liver",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["li"],
    ),
]
_m.parameters = [
    Parameter(
        "BW",
        75,
        U.kg,
        constant=True,
        name="body weight [kg]",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        port=True,
    ),
    Parameter(
        sid="cf_units_per_mmole",
        value=1.0,
        unit=U.per_mmole,
        name="conversion factor for dimensionless species",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
]

_m.species = [
    Species(
        "czx_ext",
        initialConcentration=0.0,
        name="chlorzoxazone (plasma)",
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["czx"],
        port=True,
    ),
    Species(
        "czx",
        initialConcentration=0.0,
        name="chlorzoxazone (liver)",
        compartment="Vli",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["czx"],
    ),
    Species(
        "czx6oh",
        initialConcentration=0.0,
        name="6-hydroxychlorzoxazone (liver)",
        compartment="Vli",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["czx6oh"],
    ),
    Species(
        "czx6oh_ext",
        initialConcentration=0.0,
        name="6-hydroxychlorzoxazone (plasma)",
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["czx6oh"],
        port=True,
    ),
    Species(
        "czxoglu",
        initialConcentration=0.0,
        name="6-hydroxychlorzoxazone-O-glucuronide (liver)",
        compartment="Vli",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["czxoglu"],
    ),
    Species(
        "czxoglu_ext",
        initialConcentration=0.0,
        name="6-hydroxychlorzoxazone-O-glucuronide (plasma)",
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["czxoglu"],
        port=True,
    ),
    Species(
        "ethanol",
        initialConcentration=0.0,
        name="ethanol (liver)",
        compartment="Vli",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["ethanol"],
    ),
    Species(
        "ethanol_ext",
        initialConcentration=0.0,
        name="ethanol (plasma)",
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["ethanol"],
        port=True,
    ),
    Species(
        "cyp2e1",
        initialAmount=1.0,
        name="CYP2E1",
        compartment="Vli",
        substanceUnit=U.dimensionless,
        hasOnlySubstanceUnits=True,
        conversionFactor="cf_units_per_mmole",
        sboTerm=SBO.SIMPLE_CHEMICAL,
        port=False,
    ),
]

_m.reactions = [
    Reaction(
        "CZXIM",
        name="chlorzoxazone import",
        equation="czx_ext <-> czx",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vli",
        pars=[
            Parameter(
                "CZX_k_IM",
                100,
                unit=U.per_min,
                name="rate constant for chlorzoxazone import into the liver",
                sboTerm=SBO.KINETIC_CONSTANT,
            ),
            Parameter(
                "CZX_F_EX",
                1.59,
                unit=U.dimensionless,
                name="liver partition of chlorzoxazone (inverse)",
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                notes="""
                The liver concentration at equilibrium is the concentration of
                the hepatic plasma over `CZX_F_EX`, a liver to plasma ratio of
                1/1.59 = 0.627 (0.627 +- 0.062 in rats, Kim2002). The
                parameter is equivalent to the Km of the CYP2E1 and to the rate
                of the second pathway, which are fitted, and stays fixed.
                """,
            ),
        ],
        formula=(
            "CZX_k_IM * Vli * (czx_ext - CZX_F_EX * czx)",
            U.mmole_per_min,
        ),
    ),
    Reaction(
        "CZX6OHEX",
        name="6-hydroxychlorzoxazone export",
        equation="czx6oh <-> czx6oh_ext",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vli",
        pars=[
            Parameter(
                "CZX6OH_k_EX",
                100,
                unit=U.per_min,
                name="rate constant for 6-hydroxychlorzoxazone export",
                sboTerm=SBO.KINETIC_CONSTANT,
            ),
            Parameter(
                "CZX6OH_F_IM",
                0.221,
                unit=U.dimensionless,
                name="liver to plasma ratio of 6-hydroxychlorzoxazone",
                notes="""
                The liver to plasma ratio at equilibrium, 0.221 +- 0.009 in rats
                (Kim2002).
                """,
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            ),
        ],
        formula=(
            "CZX6OH_k_EX * Vli *  (czx6oh - CZX6OH_F_IM * czx6oh_ext)",
            U.mmole_per_min,
        ),
    ),
    Reaction(
        "CZXOGLU_EX",
        name="6-hydroxychlorzoxazone-O-glucuronide export",
        equation="czxoglu <-> czxoglu_ext",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vli",
        pars=[
            Parameter(
                "CZXOGLU_k_EX",
                100,
                unit=U.per_min,
                name="rate constant for 6-hydroxychlorzoxazone-O-glucuronide export",
                sboTerm=SBO.KINETIC_CONSTANT,
            ),
            Parameter(
                "CZXOGLU_F_IM",
                1,
                unit=U.dimensionless,
                name="liver to plasma ratio of 6-hydroxychlorzoxazone-O-glucuronide",
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            ),
        ],
        formula=(
            "CZXOGLU_k_EX * Vli *  (czxoglu - CZXOGLU_F_IM * czxoglu_ext)",
            U.mmole_per_min,
        ),
    ),
    Reaction(
        "CZXOX",
        name="chlorzoxazone 6-hydroxylation (CYP2E1)",
        equation="czx -> czx6oh [cyp2e1]",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        compartment="Vli",
        pars=[
            Parameter(
                "f_cyp2e1",
                1,
                unit=U.dimensionless,
                name="CYP2E1 activity",
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                notes="""
                Activity of CYP2E1 relative to healthy subjects (1), e.g. the
                inhibition by a coadministered drug; set by the experiments,
                not fitted.
                """,
            ),
            Parameter(
                "f_cyp2e1_Km",
                1,
                unit=U.dimensionless,
                name="factor of the Km of CYP2E1",
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            ),
            Parameter(
                "CZXOX_Vmax",
                **FITS.parameter("LI__CZXOX_Vmax", unit=U.mmole_per_min_l),
                name="Vmax of the chlorzoxazone 6-hydroxylation",
                sboTerm=SBO.MAXIMAL_VELOCITY,
            ),
            Parameter(
                "CZXOX_Km",
                **FITS.parameter("LI__CZXOX_Km", unit=U.mM),
                name="Km of the chlorzoxazone 6-hydroxylation",
                sboTerm=SBO.MICHAELIS_CONSTANT,
                # the trailing whitespace of the notes is part of the SBML
                notes="""
                14.4 µM (median) Yang2012
                110±10 µM (Km CYP2E1 chlorzoxazone, human liver microsomes) {Emoto2005}
                22-64.2 µM (Km CYP2E1 chlorzoxazone, human liver microsomes) {Emoto2003}

                The Km in vivo refers to the total concentration in the liver
                (fu 0.04, DeVries1994): the dose dependence of the clearance
                (CL/F 612-805 ml/min after microdoses, 250-400 ml/min after
                250-750 mg, Hohmann2019, Frye1998) sets it.
                """,
            ),
        ],
        formula=(
            "f_cyp2e1 * cyp2e1 * CZXOX_Vmax * Vli * czx/(czx + CZXOX_Km * f_cyp2e1_Km)",
            U.mmole_per_min,
        ),
        notes="""cyp2e1 is normalized to 1""",
    ),
    Reaction(
        "CZXOTHER",
        name="chlorzoxazone elimination (CYP2E1 independent)",
        equation="czx -> ",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        compartment="Vli",
        pars=[
            Parameter(
                "f_czxother",
                1,
                unit=U.dimensionless,
                name="activity of the CYP2E1 independent elimination",
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                notes="""
                Activity of the second pathway relative to healthy subjects
                (1); set by the experiments, not fitted.
                """,
            ),
            Parameter(
                "CZXOTHER_k",
                **FITS.parameter("LI__CZXOTHER_k", unit=U.per_min),
                name="rate constant of the CYP2E1 independent elimination",
                sboTerm=SBO.KINETIC_CONSTANT,
            ),
        ],
        formula=(
            "f_czxother * CZXOTHER_k * Vli * czx",
            U.mmole_per_min,
        ),
        notes="""
        The elimination of chlorzoxazone which is not the 6-hydroxylation:
        only 71-74 % of an oral dose are recovered as 6-hydroxychlorzoxazone in
        the urine (Desiraju1983, Kharasch1993), the formation clearance of
        6-hydroxychlorzoxazone is 70 % of the clearance (Kharasch1993), the
        remaining clearance is 158-191 ml/min (Frye1998). Under disulfiram,
        which inactivates CYP2E1, Kharasch1993 found a "metabolic switching to
        an as-yet unidentified metabolite". The products are not modeled.
        """,
    ),
    Reaction(
        "CZXOGLU",
        name="6-hydroxychlorzoxazone glucuronidation (UGT)",
        equation="czx6oh -> czxoglu",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        compartment="Vli",
        pars=[
            Parameter(
                "CZXOGLU_k",
                **FITS.parameter("LI__CZXOGLU_k", unit=U.per_min),
                name="rate constant of the glucuronidation of 6-hydroxychlorzoxazone",
                sboTerm=SBO.KINETIC_CONSTANT,
                notes="""
                First order: the glucuronidation by UGT1A1, UGT1A6 and UGT1A9
                is not saturated at the concentrations of 6-hydroxychlorzoxazone
                in vivo. The free 6-hydroxychlorzoxazone in plasma is 1.4-3.3 %
                of chlorzoxazone 0.5 hr after a microdose (Witt2016,
                Hohmann2019), the glucuronide is the main form in plasma and
                urine.
                """,
            ),
            Parameter(
                "f_GLU",
                1,
                unit=U.dimensionless,
                name="UGT activity (6-hydroxychlorzoxazone glucuronidation)",
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            ),
        ],
        formula=(
            "f_GLU * CZXOGLU_k * Vli * czx6oh",
            U.mmole_per_min,
        ),
        notes="""
        Catalyzed by UGT enzymes.
        """,
    ),
    Reaction(
        "ETHIM",
        name="ethanol import",
        equation="ethanol_ext <-> ethanol",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vli",
        pars=[
            Parameter(
                "ETH_k_IM",
                100,
                unit=U.per_min,
                name="rate constant for ethanol import into the liver",
                sboTerm=SBO.KINETIC_CONSTANT,
            ),
        ],
        formula=(
            "ETH_k_IM * Vli * (ethanol_ext - ethanol)",
            U.mmole_per_min,
        ),
    ),
    Reaction(
        "ETH_ELIMINATION",
        name="ethanol elimination (ALD)",
        equation="ethanol -> ",
        sboTerm=SBO.BIOCHEMICAL_REACTION,
        compartment="Vli",
        pars=[
            Parameter(
                "ETHEL_VMAX",
                **FITS.parameter("LI__ETHEL_VMAX", unit=U.mmole_per_min_kg),
                name="rate of ethanol elimination",
                sboTerm=SBO.MAXIMAL_VELOCITY,
                # the trailing whitespace of the notes is part of the SBML
                notes="""
                Rates of alcohol elimination
                8.5 g/hr/70kg (Holford1987) 
                0.121 g/hr/kg           | :46.07 g/mole
                2.626e-3 mole/hr/kg     | 1hr = 60 min
                4.376e-5 mole/min/kg    | 1 mole = 1000 mmole
                4.376e-2 mmole/min/kg
                """,  # noqa: W291
            ),
            Parameter(
                "ETHEL_KM",
                2.17,
                unit=U.mM,
                name="Km of the ethanol elimination",
                sboTerm=SBO.MICHAELIS_CONSTANT,
                notes="""
                The alcohol dehydrogenase has a Km of about 0.1 g/l (2.17 mM)
                in vivo (Holford1987). Not fitted: the blood ethanol of
                Wilkinson1977 does not identify it (flat profile likelihood
                from 0.05 to 5 mM).
                """,
            ),
        ],
        formula=(
            "ETHEL_VMAX * BW * ethanol/(ethanol + ETHEL_KM)",
            U.mmole_per_min,
        ),
        notes="""
        Ethanol elimination via alcohol dehydrogenase in the liver.
        Due to saturation of enzyme (`ethanol > ETHEL_KM`) constant rate of ethanol elimination.
        """,
    ),
]

_m.parameters.extend(
    [
        Parameter(
            sid="cyp2e1_thalf",
            value=1.8 * 24 * 60,  # 1.8 days
            unit=U.min,
            name="CYP2E1 half life",
            notes="""
            Half-life of CYP2E1 without ethanol: about 7 hr for the
            unstabilized and about 37 hr for the ethanol stabilized protein in
            rats (Roberts1995); the activity of drinkers normalizes within about
            one week of withdrawal (Oneta2002, Lucas1995).
            """,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
    ]
)

_m.rules.extend(
    [
        AssignmentRule(
            "k_cyp2e1_deg",
            "1 mmole * 0.693 dimensionless / cyp2e1_thalf / Vli",
            unit=U.mmole_per_min_l,
            notes="""
        degradation rate = ln(2)/thalf
        """,
        ),
        AssignmentRule(
            "k_cyp2e1_prod",
            "k_cyp2e1_deg",
            unit=U.mmole_per_min_l,
            notes="""
        `production rate = degradation rate` at baseline resulting in cyp2e1 = 1.0 dimensionless
        """,
        ),
    ]
)

_m.reactions.extend(
    [
        # CYP2E1 - alcohol model
        Reaction(
            "CYP2E1_PROD",
            name="CYP2E1 production",
            equation=" -> cyp2e1",
            sboTerm=SBO.BIOCHEMICAL_REACTION,
            compartment="Vli",
            pars=[
                Parameter(
                    "k_cyp2e1_prod",
                    np.nan,
                    unit=U.mmole_per_min_l,
                    name="rate constant for CYP2E1 production",
                    sboTerm=SBO.KINETIC_CONSTANT,
                    constant=False,
                    notes="""
                """,
                ),
            ],
            formula=(
                "Vli * k_cyp2e1_prod",
                U.mmole_per_min,
            ),
        ),
        Reaction(
            "CYP2E1_DEG",
            name="CYP2E1 degradation",
            equation="cyp2e1 -> [ethanol]",
            sboTerm=SBO.BIOCHEMICAL_REACTION,
            compartment="Vli",
            rules=[
                AssignmentRule(
                    "kd_cyp2e1",
                    "k_cyp2e1_deg/(1 dimensionless + ethanol/Ki_cyp2e1_deg_ethanol)",
                    unit=U.mmole_per_min_l,
                )
            ],
            pars=[
                Parameter(
                    "k_cyp2e1_deg",
                    np.nan,
                    unit=U.mmole_per_min_l,
                    name="rate constant for CYP2E1 degradation",
                    sboTerm=SBO.KINETIC_CONSTANT,
                    constant=False,
                    notes="Calculated from the half-life `cyp2e1_thalf`, kd = ln(2)/t_half.",
                ),
                Parameter(
                    "Ki_cyp2e1_deg_ethanol",
                    1e-5,
                    unit=U.mM,
                    name="stabilization constant (inhibition degradation)",
                    sboTerm=SBO.INHIBITORY_CONSTANT,
                    constant=True,
                    notes="""
                    Ethanol stabilizes CYP2E1 against its degradation. With a
                    constant far below the hepatic ethanol of drinking the
                    stabilization is a switch: the induction is the fraction of
                    the day with ethanol in the liver, about 1.9-fold after
                    weeks of 50 g ethanol a day, back to 1 within a week of
                    abstinence (the about twofold activity of drinkers). A
                    constant of 1 mM gives an induction of 1.3-fold only. The
                    value is not identified by the data.
                    """,
                ),
            ],
            formula=(
                "Vli * kd_cyp2e1 * cyp2e1",
                U.mmole_per_min,
            ),
            notes="""
        Ethanol stabilizes CYP2E1, i.e., the degradation rate is reduced.
        """,
        ),
    ]
)

model_liver = _m

if __name__ == "__main__":
    from pkdb_models.models.chlorzoxazone import MODEL_BASE_PATH

    result: FactoryResult = create_model(
        model=model_liver,
        filepath=MODEL_BASE_PATH / f"{model_liver.sid}.xml",
        sbml_level=3,
        sbml_version=2,
    )
