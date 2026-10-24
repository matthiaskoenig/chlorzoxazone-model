"""Chlorzoxazone parameter fitting.

The fit problems of the chlorzoxazone model: which fit mapping collections
enter a fit and which parameters are adjusted, see `FIT_DEFINITIONS`. The
commands `run_fit`, `run_report` and `run_identifiability` of pkpdsim run them
with the package of the model:

    run_fit pkdb_models.models.chlorzoxazone --subset=PK --runs=3 --cores=3 --seed=1234 --method=DE

A fit is not followed by the identifiability analysis of its parameters unless
`--identifiability` is given. The results, figures and the HTML report are
written into the fit folder of the model (`MODEL.fit_dir`), unless
`--output_dir` is given. The report of parameters which were fitted earlier is
created with the `run_report` command, their identifiability is analysed
without fitting again with the `run_identifiability` command:

    run_report pkdb_models.models.chlorzoxazone --subset=PK results/fit/PK_<fit id>/parameters.json
    run_identifiability pkdb_models.models.chlorzoxazone --subset=PK --cores=3 results/fit/PK_<fit id>/parameters.json
"""

from collections.abc import Callable

from pkpdsim.fit import default_fit_settings
from sbmlsim.fit import FitMappingCollection, FitParameter
from sbmlsim.fit.cli import FitDefinition

from pkdb_models.models.chlorzoxazone import (
    CHLORZOXAZONE_PATH,
    DATA_PATHS,
)
from pkdb_models.models.chlorzoxazone.fitting.mapping_collections import COLLECTIONS
from pkdb_models.models.chlorzoxazone.fitting.parameters import (
    parameters_alcohol,
    parameters_pk,
)
from pkdb_models.models.chlorzoxazone.tolerances import absolute_tolerance

#: settings of the fits, stored with the result and read back by the report;
#: the species get tolerances of their own scale (the microdoses of 2.5 µg give
#: plasma concentrations of about 1e-5 mM), see `tolerances`
FIT_SETTINGS = default_fit_settings(
    absolute_tolerance=absolute_tolerance(1e-6, species=1e-12)
)


def _definition(
    mapping_collections: Callable[[], dict[str, list[FitMappingCollection]]],
    parameters: list[FitParameter],
) -> FitDefinition:
    """Get a fit problem of the chlorzoxazone model with the settings of the model."""
    return FitDefinition(
        mapping_collections=mapping_collections,
        parameters=parameters,
        base_path=CHLORZOXAZONE_PATH,
        data_path=DATA_PATHS,
        settings=FIT_SETTINGS,
    )


#: the fit problems of the chlorzoxazone model, the keys are the `--subset`
#: argument, see `mapping_collections`
FIT_DEFINITIONS: dict[str, FitDefinition] = {
    # the pharmacokinetics of chlorzoxazone and its metabolites
    "PK": _definition(COLLECTIONS["PK"], parameters_pk),
    # ethanol
    "ALCOHOL": _definition(COLLECTIONS["ALCOHOL"], parameters_alcohol),
}
