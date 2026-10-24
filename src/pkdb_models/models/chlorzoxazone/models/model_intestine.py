"""Chlorzoxazone intestine model."""

from pkpdsim.templates import terms_of_use
from sbmlutils.factory import (
    AssignmentRule,
    Compartment,
    FactoryResult,
    Model,
    Parameter,
    RateRule,
    Reaction,
    Species,
    UnitDefinition,
    create_model,
)
from sbmlutils.metadata import SBO

from pkdb_models.models.chlorzoxazone.models import annotations, templates
from pkdb_models.models.chlorzoxazone.models.fits import FITS


class U(templates.U):
    """UnitDefinitions of the intestine model."""

    per_hr = UnitDefinition("per_hr", "1/hr")
    min_per_hr = UnitDefinition("min_per_hr", "min/hr")
    mg_per_min = UnitDefinition("mg_per_min", "mg/min")


_m = Model(
    "chlorzoxazone_intestine",
    name="Model for chlorzoxazone absorption in the small intestine",
    notes="""
    # Model for chlorzoxazone absorption in the small intestine

    Absorption of chlorzoxazone from the intestinal lumen into the portal
    plasma and absorption of oral ethanol. Chlorzoxazone is not metabolized in
    the intestine: CYP2E1 is low in the enterocytes, the first pass is the
    saturable hepatic CYP2E1.
    """
    + terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
)

_m.compartments = [
    Compartment(
        "Vext",
        1.0,
        name="plasma",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["plasma"],
    ),
    Compartment(
        "Vgu",
        1.2825,  # 0.0171 [l/kg] * 75 kg
        name="intestine",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["gu"],
    ),
    Compartment(
        "Vlumen",
        1.2825 * 0.9,  # 0.0171 [l/kg] * 75 kg * 0.9, replaced by the body model
        name="intestinal lumen (inner part of intestine)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        constant=False,
        port=True,
        annotations=annotations.compartments["gu_lumen"],
    ),
    Compartment(
        "Vfeces",
        metaId="meta_Vfeces",
        value=1,
        unit=U.liter,
        constant=True,
        name="feces",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        port=True,
        annotations=annotations.compartments["feces"],
    ),
]

_m.species = [
    Species(
        "czx_lumen",
        initialConcentration=0.0,
        name="chlorzoxazone (intestinal volume)",
        compartment="Vlumen",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["czx"],
        port=True,
    ),
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
        "czx_feces",
        initialConcentration=0.0,
        name="chlorzoxazone (feces)",
        compartment="Vfeces",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["czx"],
        port=True,
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
]

_m.parameters = [
    Parameter(
        "PODOSE_ethanol",
        0,
        U.mg,
        constant=False,
        name="oral ethanol dose [mg]",
    ),
    Parameter(
        "F_czx_abs",
        1.0,
        U.dimensionless,
        constant=True,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        name="fraction absorbed chlorzoxazone",
        notes="""
        Fraction of the chlorzoxazone in the intestinal lumen which is absorbed,
        `(1 - F_czx_abs)` is excreted in the feces. Chlorzoxazone is absorbed
        completely: 71-74 % of an oral dose are recovered as
        6-hydroxychlorzoxazone in the urine (Desiraju1983, Kharasch1993), the
        rest is a second, unidentified elimination of chlorzoxazone (see
        `CZXOTHER` of the liver), not a fecal loss.
        """,
    ),
    Parameter(
        "Ka_abs_czx",
        **FITS.parameter("GU__Ka_abs_czx", unit=U.per_hr),
        constant=True,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        name="absorption rate chlorzoxazone",
        notes="""
        Rate of absorption from the intestinal lumen. Solutions peak at about
        0.5 hr (Hohmann2019, Witt2016), Desiraju1983 report an absorption rate
        of 2.28 1/hr after 750 mg in solution, Leclercq1998 2.0 1/hr after a
        capsule.
        """,
    ),
    Parameter(
        "f_Ka_czx",
        1,
        U.dimensionless,
        constant=True,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        name="scaling factor of the absorption rate of chlorzoxazone",
        notes="""
        Scales the rate of absorption, not the fraction absorbed.
        """,
    ),
    Parameter(
        "Ka_abs_eth",
        **FITS.parameter("GU__Ka_abs_eth", unit=U.per_hr),
        constant=True,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        name="absorption rate ethanol",
    ),
    Parameter(
        "Mr_ethanol",
        46.07,
        U.g_per_mole,
        constant=True,
        name="Molecular weight ethanol [g/mole]",
        sboTerm=SBO.MOLECULAR_MASS,
        port=True,
    ),
]

_m.rules.append(
    AssignmentRule(
        "absorption",
        value="f_Ka_czx * Ka_abs_czx/60 min_per_hr * Vgu * czx_lumen",
        unit=U.mmole_per_min,
        name="transport of chlorzoxazone out of the lumen",
        notes="""
        The flux out of the intestinal lumen, which is absorbed (`F_czx_abs`)
        or excreted in the feces (`1 - F_czx_abs`): the absorption rate
        `f_Ka_czx` does not change the fraction absorbed.
        """,
    )
)

_m.reactions = [
    Reaction(
        "CZXABS",
        name="absorption chlorzoxazone",
        equation="czx_lumen -> czx_ext",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vgu",
        formula=("F_czx_abs * absorption", U.mmole_per_min),
    ),
    Reaction(
        "ETHABS",
        name="absorption ethanol",
        equation=" -> ethanol_ext",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vgu",
        formula=(
            "Ka_abs_eth/60 min_per_hr * PODOSE_ethanol / Mr_ethanol",
            U.mmole_per_min,
        ),
    ),
]

_m.reactions.append(
    Reaction(
        sid="CZXEXC",
        name="excretion chlorzoxazone (feces)",
        compartment="Vlumen",
        equation="czx_lumen -> czx_feces",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=(
            "(1 dimensionless - F_czx_abs) * absorption",
            U.mmole_per_min,
        ),
        notes="""
            Fraction of the chlorzoxazone in the lumen which is not absorbed.
            """,
    ),
)

_m.rate_rules.append(RateRule("PODOSE_ethanol", "-ETHABS * Mr_ethanol", U.mg_per_min))

model_intestine = _m

if __name__ == "__main__":
    from pkdb_models.models.chlorzoxazone import MODEL_BASE_PATH

    result: FactoryResult = create_model(
        model=model_intestine,
        filepath=MODEL_BASE_PATH / f"{model_intestine.sid}.xml",
        sbml_level=3,
        sbml_version=2,
    )
