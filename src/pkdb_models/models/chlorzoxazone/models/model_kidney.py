"""Chlorzoxazone kidney model.

The kidneys excrete 6-hydroxychlorzoxazone-O-glucuronide, the main metabolite
of chlorzoxazone in urine; chlorzoxazone itself is excreted unchanged below
1-2 % of the dose. The renal clearance is given relative to the glomerular
filtration rate (GFR) and scales with the renal function.
"""

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
from sbmlutils.metadata import BQB, SBO

from pkdb_models.models.chlorzoxazone.models import annotations, templates
from pkdb_models.models.chlorzoxazone.models.fits import FITS


class U(templates.U):
    """UnitDefinitions of the kidney model."""

    ml_per_min = UnitDefinition("ml_per_min", "ml/min")
    l_per_ml = UnitDefinition("l_per_ml", "l/ml")


_m = Model(
    "chlorzoxazone_kidney",
    name="Model for the renal excretion of 6-hydroxychlorzoxazone-O-glucuronide",
    notes="""
    # Model for the renal excretion of 6-hydroxychlorzoxazone-O-glucuronide

    Model for the renal excretion of 6-hydroxychlorzoxazone-O-glucuronide
    encoded in <a href="http://sbml.org">SBML</a> format.

    Import and secretion are not modeled explicitly but a lumped excretion
    reaction relative to the GFR is used to describe the urinary elimination
    of the glucuronide.

    - 58-64 % of a 250 mg dose are recovered as 6-hydroxychlorzoxazone (free
      and glucuronide) in the urine (Frye1998, Burckart1998, Vesell1995)
    - 71-74 % of a 750 mg dose (Desiraju1983, Kharasch1993)
    - the renal clearance of total 6-hydroxychlorzoxazone is 464-506 ml/min
      (Frye1998), above the GFR: a tubular secretion
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
        "Vki",
        1.5,
        name="kidney",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["ki"],
    ),
    Compartment(
        "Vurine",
        1.0,
        name="urine",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["urine"],
    ),
]

_m.species = [
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
        "czxoglu_urine",
        initialConcentration=0.0,
        name="6-hydroxychlorzoxazone-O-glucuronide (urine)",
        compartment="Vurine",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["czxoglu"],
        port=True,
        notes="""
        Urinary species are in amounts.
        """,
    ),
]

_m.parameters = [
    Parameter(
        "f_renal_function",
        name="renal function",
        value=1.0,
        unit=U.dimensionless,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""
        >1.0: increased kidney function
        1.0: normal kidney function (healthy control)
        <1.0: decreased kidney function

        Renal function relative to the healthy glomerular filtration rate
        GFR_base, which is 101 ml/min at 75 kg; a measured creatinine
        clearance of X ml/min is the renal function X/101.
        """,
    ),
    Parameter(
        "GFR_base",
        101,
        U.ml_per_min,
        name="glomerular filtration rate (healthy)",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        port=True,
    ),
    Parameter(
        "CZXOGLU_EX_f",
        **FITS.parameter("KI__CZXOGLU_EX_f", unit=U.dimensionless),
        name="renal clearance of the glucuronide relative to the GFR",
        sboTerm=SBO.KINETIC_CONSTANT,
        notes="""
        The renal clearance of 6-hydroxychlorzoxazone-O-glucuronide is
        CZXOGLU_EX_f times the GFR: above 1 a net secretion. The renal
        clearance of total 6-hydroxychlorzoxazone is 464-506 ml/min (Frye1998).
        """,
    ),
]

_m.rules = [
    AssignmentRule(
        "GFR",
        "f_renal_function * GFR_base",
        unit=U.ml_per_min,
        name="glomerular filtration rate",
    ),
]

_m.reactions = [
    Reaction(
        "CZXOGLU_EX",
        name="excretion 6-hydroxychlorzoxazone-O-glucuronide",
        equation="czxoglu_ext -> czxoglu_urine",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vki",
        # [ml/min] * [l/ml] * [-] * [mmole/l]
        formula=(
            "GFR * 0.001 l_per_ml * CZXOGLU_EX_f * czxoglu_ext",
            U.mmole_per_min,
        ),
        annotations=[(BQB.IS, "ncit/C75913")],  # renal clearance
    ),
]

model_kidney = _m

if __name__ == "__main__":
    from pkdb_models.models.chlorzoxazone import MODEL_BASE_PATH

    result: FactoryResult = create_model(
        model=model_kidney,
        filepath=MODEL_BASE_PATH / f"{model_kidney.sid}.xml",
        sbml_level=3,
        sbml_version=2,
    )
