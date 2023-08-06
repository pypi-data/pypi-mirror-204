from dkist_fits_specifications.spec122 import (
    define_122_schema_expansions,
    load_raw_spec122,
    load_spec122,
)
from dkist_fits_specifications.utils.frozendict import frozendict


def test_load_122():
    spec = load_spec122()
    assert isinstance(spec, frozendict)
    assert isinstance(spec["fits"], frozendict)
    assert isinstance(spec["fits"]["NAXIS"], frozendict)


def test_load_raw_122():
    spec = load_raw_spec122()
    assert isinstance(spec, frozendict)
    assert isinstance(spec["fits"], tuple)
    header, spec = spec["fits"]
    assert isinstance(header, frozendict)
    assert isinstance(spec["NAXIS"], frozendict)


def test_define_122_schema_expansion_duplication():
    """
    Given: the list of requested spec 122 expansions
    When: checking the indices for each expansion
    Then: None of them match (all expansions are unique)
    """
    expansions = define_122_schema_expansions()
    expansion_indices = [e.index for e in expansions]
    assert len(expansion_indices) == len(set(expansion_indices))
