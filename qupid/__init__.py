from .casematch import CaseMatchCollection, CaseMatchOneToMany, CaseMatchOneToOne
from .qupid import match_by_multiple, match_by_single, shuffle
from .stats import compute_covariate_balance

__version__ = "0.1.0"

__all__ = [
    "CaseMatchOneToMany",
    "CaseMatchOneToOne",
    "CaseMatchCollection",
    "match_by_single",
    "match_by_multiple",
    "shuffle",
    "compute_covariate_balance",
]
