import pandas as pd
from qiime2 import Metadata

from qupid.casematch import CaseMatchOneToMany
from qupid import match_by_multiple


def match_one_to_many(
    sample_metadata: Metadata,
    case_control_column: str,
    categories: list,
    case_identifier: str,
    tolerances: list = None,
    on_failure: str = "raise",
) -> CaseMatchOneToMany:
    sample_metadata = sample_metadata.to_dataframe()
    focus = sample_metadata[sample_metadata[case_control_column] == case_identifier]
    background = sample_metadata[
        sample_metadata[case_control_column] != case_identifier
    ]

    if tolerances is None:
        tolerance_map = None
    else:
        tolerance_map = {}
        for token in tolerances:
            parts = token.split("+-")
            if len(parts) != 2:
                raise ValueError(
                    f"Malformed tolerance token: {token!r}. "
                    "Expected format 'category+-value'."
                )
            cat, val_str = parts
            try:
                val = float(val_str)
            except ValueError:
                raise ValueError(
                    f"Cannot parse tolerance value {val_str!r} in token {token!r}."
                )
            tolerance_map[cat] = val

    cm_one_to_many = match_by_multiple(
        focus=focus,
        background=background,
        categories=categories,
        tolerance_map=tolerance_map,
        on_failure=on_failure,
    )
    return cm_one_to_many


def match_one_to_one(
    case_match_one_to_many: CaseMatchOneToMany,
    iterations: int = 10,
    strict: bool = True,
    seed: int = None,
    n_jobs: int = 1,
) -> pd.DataFrame:
    res = case_match_one_to_many.create_matched_pairs(
        iterations=iterations,
        strict=strict,
        n_jobs=n_jobs,
        seed=seed,
    )
    return res.to_dataframe()
