"""Templates of the chlorzoxazone models: the unit definitions and the creators."""

from pkpdsim.templates import creators as creators_generic
from sbmlutils.factory import Creator, ModelUnits, UnitDefinition, Units


class U(Units):
    """UnitDefinitions shared by the chlorzoxazone models."""

    mmole = UnitDefinition("mmole")
    min = UnitDefinition("min")
    mg = UnitDefinition("mg")
    per_min = UnitDefinition("per_min", "1/min")
    per_min_l = UnitDefinition("per_min_l", "1/min/liter")
    m2 = UnitDefinition("m2", "meter^2")
    mM = UnitDefinition("mM", "mmole/liter")
    mmole_per_min = UnitDefinition("mmole_per_min", "mmole/min")
    mmole_per_min_l = UnitDefinition("mmole_per_min_l", "mmole/min/liter")
    g_per_mole = UnitDefinition("g_per_mole", "g/mole")
    l_per_min = UnitDefinition("l_per_min", "l/min")
    l_per_min_mmole = UnitDefinition("l_per_min_mmole", "l/min/mmole")
    mmole_per_l = UnitDefinition("mmole_per_l", "mmole/liter")
    mmole_per_min_kg = UnitDefinition("mmole_per_min_kg", "mmole/min/kg")


model_units = ModelUnits(
    time=U.min,
    extent=U.mmole,
    substance=U.mmole,
    length=U.meter,
    area=U.m2,
    volume=U.liter,
)

creators = [
    Creator(
        familyName="Küttner",
        givenName="Jonas",
        email="jonas.kuettner98@gmail.com",
        organization="Humboldt-University Berlin, Institute for Theoretical Biology",
    ),
    *creators_generic,
]
