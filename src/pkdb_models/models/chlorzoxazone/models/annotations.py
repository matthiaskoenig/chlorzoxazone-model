"""Annotations of the chlorzoxazone models: the compartments and the species.

The compartments are the shared ones of `pkpdsim.annotations`.
"""

from pkpdsim.annotations import compartments
from sbmlutils.metadata import BQB

__all__ = ["compartments", "species"]

species = {
    "czx": [
        # chlorzoxazone
        (BQB.IS, "pubchem.compound/2733"),
        (BQB.IS, "chebi/CHEBI:3655"),
        (BQB.IS, "ncit/C28926"),
        (BQB.IS, "inchikey/TZFWDZFKRBELIQ-UHFFFAOYSA-N"),
    ],
    "czx6oh": [
        # 6-hydroxy-chlorzoxazone
        (BQB.IS, "chebi/CHEBI:184399"),
        (BQB.IS, "pubchem.compound/2734"),
        (BQB.IS, "inchikey/AGLXDWOTVQZHIQ-UHFFFAOYSA-N"),
    ],
    "czxoglu": [
        (BQB.IS, "inchikey/XZSZLTOSEPTADQ-LIJGXYGRSA-N"),
        (BQB.IS, "pubchem.compound/129522086"),
    ],
    "ethanol": [
        (BQB.IS, "chebi/CHEBI:16236"),
        (BQB.IS, "pubchem.compound/702"),
        (BQB.IS, "inchikey/LFQSCWFLJHTTHZ-UHFFFAOYSA-N"),
    ],
}
