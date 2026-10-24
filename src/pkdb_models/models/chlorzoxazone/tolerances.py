"""The tolerances of the integrator for the chlorzoxazone model."""

from sbmlsim.model.tolerances import AbsoluteTolerance


def absolute_tolerance(value: float, species: float) -> AbsoluteTolerance:
    """Get the absolute tolerance of the integrator for the chlorzoxazone model.

    Chlorzoxazone is dosed in mg, about 1 mmole (the microdoses of Hohmann2019
    and Witt2016 down to 1.5e-5 mmole): the amounts and concentrations of
    chlorzoxazone and its metabolites are far below the default tolerance of
    1e-10 at the microdoses, so the species get absolute tolerances of their own
    scale.

    Args:
        value: tolerance of every other state (the doses).
        species: tolerance of the amounts and concentrations of the species.

    Returns:
        The absolute tolerance per kind of state.
    """
    return AbsoluteTolerance(amount=species, concentration=species, other=value)


#: the absolute tolerance of the simulation experiments
ABSOLUTE_TOLERANCE = absolute_tolerance(1e-10, species=1e-14)
