"""
Functions and schemas relating to specification 122, the level 0 FITS files.

The 122 schemas have a singular variant, they are all NAXIS=3.
However, the yaml files still are written with the indices corresponding to NAXIS (``n, i, j``).
These indices are expanded by the loading function so the returned schema always has ``NAXIS = 3``.

The yamls are written with the indices, to reduce duplication and to make it
easier for 214 to use the raw (unprocessed) schemas.
"""
import copy
from typing import Optional
from pathlib import Path
from functools import cache

import yamale  # type: ignore

from dkist_fits_specifications import validation_schema
from dkist_fits_specifications.utils import (
    ExpansionIndex,
    expand_schema,
    frozendict,
    load_raw_spec,
    raw_schema_type_hint,
    schema_type_hint,
)

__all__ = ["load_raw_spec122", "load_spec122"]


base_path = Path(__file__).parent / "schemas"


def define_122_schema_expansions() -> list[ExpansionIndex]:
    # 122 always has 3 axes, but we encode the yamls independent of the number,
    # to match 214 which might have a variable number of axes.
    n_expansion = ExpansionIndex(index="n", size=1, values=range(1, 4))
    i_expansion = ExpansionIndex(index="i", size=1, values=range(1, 4))
    j_expansion = ExpansionIndex(index="j", size=1, values=range(1, 4))
    return [n_expansion, i_expansion, j_expansion]


def preprocess_schema(schema: schema_type_hint) -> schema_type_hint:
    """
    Convert the loaded raw schemas to the 122 schema.

    Parameters
    ----------
    raw_schema
        The loaded version of a single yaml file.

    Returns
    -------
    schema
        The body of a schema, updated as needed from the yaml files.
    """
    header, raw_schemas = schema
    header = dict(copy.deepcopy(header)["spec122"])
    header.pop("section")

    schema = {
        k: v
        for k, v in expand_schema(
            schema=raw_schemas, expansions=define_122_schema_expansions()
        ).items()
    }
    for key, key_schema in schema.items():
        updated_schema = {key: {**header, **key_schema}}
        # Rather than put expected in all the files, default it to required
        updated_schema[key]["expected"] = key_schema.get("expected", key_schema["required"])
        updated_schema[key] = frozendict(updated_schema[key])
        schema.update(updated_schema)
    return frozendict(schema)


# No cache here as load_raw_spec is cached
def load_raw_spec122(glob: Optional[str] = None) -> frozendict[str, raw_schema_type_hint]:
    """
    Load the raw 122 schemas from the yaml files.

    Parameters
    ----------
    glob
        A pattern to use to match a file, without the ``.yml`` file extension.
        Can be a section name like ``'wcs'``.

    Returns
    -------
    raw_schemas
        The schemas as loaded from the yaml files.
    """
    return load_raw_spec(base_path, glob)


@cache
def load_spec122(glob: Optional[str] = None) -> frozendict[str, schema_type_hint]:
    """
    Return the loaded schemas for DKIST Specification 122

    Parameters
    ----------
    glob
        A pattern to use to match a file, without the ``.yml`` file extension.
        Can be a section name like ``'wcs'``.
    """

    raw_schemas = load_raw_spec122(glob=glob)
    schemas = {}
    for schema_name, raw_schema in raw_schemas.items():
        # 122 only uses the second document
        schema = preprocess_schema(raw_schema)
        yamale.validate(validation_schema, [(schema, None)])
        schemas[schema_name] = schema

    return frozendict(schemas)
