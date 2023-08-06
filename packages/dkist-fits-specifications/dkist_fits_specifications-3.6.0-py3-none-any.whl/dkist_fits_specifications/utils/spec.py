"""
Functions and variables common to all specifications.
"""
from typing import Any, Tuple, Iterable, Optional, cast
from pathlib import Path
from functools import cache
from dataclasses import dataclass

import yaml

from dkist_fits_specifications.utils.frozendict import frozendict

__all__ = [
    "load_raw_spec",
    "raw_schema_type_hint",
    "schema_type_hint",
    "ExpansionIndex",
    "expand_schema",
]

schema_type_hint = frozendict[str, frozendict[str, Any]]
"""
A type hint for a single validation schema.

As returned by `.load_spec122` and `.load_spec214`.
"""

# For some reason using tuple and not typing.Tuple here causes the doc build to fail
raw_schema_type_hint = Tuple[frozendict[str, Any], schema_type_hint]
"""
A Type hint for a single raw schema, as loaded directly from a yaml file.

This type is returned by the `.load_raw_spec122` and `.load_raw_spec214` methods.
"""


@dataclass
class ExpansionIndex:
    """
    A class for defining a FITS schema expansion.

    index: the string to be substituted, omitting the surrounding '<', '>'
    size: how many (zero-padded) characters to use for the substituted integer
    values: the iterable of integers to be used as substitution for the index

    Example:
        Using the expansion of:
        ExpansionIndex(index="a", size=3, values=range(1, 6))

        on the keyword 'KEY<a>' would produce the expanded set of keys:
        ['KEY001', 'KEY002', 'KEY003', 'KEY004', 'KEY005']

    """

    index: str
    values: Iterable
    size: int = None

    def __post_init__(self):
        if len(str(max(self.values))) > self.size:
            raise ValueError(
                f"The maximum expansion value ({max(self.values)}) does not fit within the prescribed size ({self.size})."
            )

    def _expanded_keys(self, key: str) -> list[str]:
        """Generate schema entries for expanded keys."""
        return [key.replace(f"<{self.index}>", str(i).zfill(self.size)) for i in self.values]

    def generate(self, keys: list[str]) -> list[str]:
        """Generate the new keys to be added."""
        return_keys = []
        for key in keys:
            if f"<{self.index}>" in key:
                return_keys.extend(self._expanded_keys(key=key))
        long_keys = [k for k in return_keys if len(k) > 8]
        if long_keys:
            raise ValueError(
                f"FITS keywords cannot be more than 8 characters in length. {long_keys} are too long."
            )
        return return_keys


def expand_schema(
    schema: schema_type_hint, expansions: list[ExpansionIndex]
) -> dict[str, frozendict[str, Any]]:
    """Perform a schema expansion given a schema and a list of ExpansionIndexes to apply."""
    expanded_schema = dict()
    for fits_keyword_name, spec_fields in schema.items():
        if "<" not in fits_keyword_name:
            expanded_schema.update({fits_keyword_name: spec_fields})
        else:
            expanded_fits_keywords = [fits_keyword_name]
            for expansion in expansions:
                expanded_fits_keywords.extend(expansion.generate(keys=expanded_fits_keywords))
            expanded_schema.update({k: spec_fields for k in expanded_fits_keywords if "<" not in k})
    return expanded_schema


@cache
def load_raw_spec(
    base_path: Path, glob: Optional[str] = None
) -> frozendict[str, raw_schema_type_hint]:
    """
    Load raw schemas from the yaml files in ``base_path``.

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
    if glob is None:
        glob = "*"

    files = Path(base_path).glob(f"{glob}.yml")

    raw_schemas = {}
    for fname in files:
        schema_name = fname.stem
        with open(fname) as fobj:
            raw_schema = tuple(yaml.load_all(fobj, Loader=yaml.SafeLoader))

            # Because this function is cached, we want to strongly discourage
            # modification of the return values. We do this by wrapping the
            # expected tree of dicts into frozendict objects which disallow
            # modification
            frozen_header = {}
            for key, head in raw_schema[0].items():
                frozen_header[key] = frozendict(head)
            frozen_key_schemas = {}
            for key, schema in raw_schema[1].items():
                frozen_key_schemas[key] = frozendict(schema)
            raw_schema = (frozendict(frozen_header), frozendict(frozen_key_schemas))

        # Apply a more specific type hint to the loaded schema
        raw_schemas[schema_name] = cast(raw_schema_type_hint, raw_schema)

    return frozendict(raw_schemas)
