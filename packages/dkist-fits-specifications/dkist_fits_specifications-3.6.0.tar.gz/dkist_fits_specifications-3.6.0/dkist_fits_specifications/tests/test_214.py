from dkist_fits_specifications.spec214 import (
    define_214_schema_expansions,
    load_expanded_spec214,
    load_full_spec214,
    load_spec214,
)
from dkist_fits_specifications.utils.frozendict import frozendict


def test_load_full_214():
    spec = load_full_spec214()
    visp = spec["visp"]
    assert "VSPNUMST" not in visp
    assert "VSPSTNUM" not in visp
    assert "IPTASK" not in spec["dkist-op"]
    assert isinstance(spec, frozendict)
    assert isinstance(spec["fits"], frozendict)
    assert isinstance(spec["fits"]["NAXIS"], frozendict)

    # No sections should be empty
    for key in spec:
        assert spec[key], f"The {key} section is empty"


def test_load_214():
    spec = load_spec214()
    assert isinstance(spec, frozendict)
    assert isinstance(spec["fits"], frozendict)
    assert isinstance(spec["fits"]["NAXIS"], frozendict)


def test_expanded_schema():
    schemas = load_expanded_spec214(
        DAAXES=2,
        DEAXES=1,
        NAXIS=3,
        DNAXIS=5,
        ZIMAGE=True,
        ZVAL1=1,
        ZVAL2=2,
        ZVAL3=3,
        TFIELDS=5,
        NPROPOS=2,
        NEXPERS=5,
        INSTRUME="notthedkist",
    )
    assert "DINDEX3" in schemas["dataset"]
    assert "NAXIS1" in schemas["fits"]
    assert "DTYPE5" in schemas["dataset"]
    assert "EXPRID05" in schemas["dkist-id"]
    assert "PROPID02" in schemas["dkist-id"]
    for percentile in [1, 10, 25, 75, 90, 95, 98, 99]:
        assert f"DATAP{str(percentile).zfill(2)}" in schemas["stats"]
    assert "ZNAME3" in schemas["compression"]
    assert "TFORM4" in schemas["compression"]
    assert "CRPIX3" in schemas["telescope"]
    assert "CRPIX3A" in schemas["telescope"]
    assert "NBIN3" in schemas["camera"]
    for i in range(1, 4):
        for j in range(1, 4):
            assert f"PC{i}_{j}" in schemas["telescope"]


def test_define_214_schema_expansion_duplication():
    """
    Given: the list of requested spec 214 expansions
    When: checking the indices for each expansion
    Then: None of them match (all expansions are unique)
    """
    expansions = define_214_schema_expansions(
        DAAXES=2,
        DEAXES=1,
        NAXIS=3,
        DNAXIS=5,
        ZIMAGE=True,
        ZVAL1=1,
        ZVAL2=2,
        ZVAL3=3,
        TFIELDS=5,
        NPROPOS=2,
        NEXPERS=5,
        INSTRUME="notthedkist",
    )
    expansion_indices = [e.index for e in expansions]
    assert len(expansion_indices) == len(set(expansion_indices))


"""def test_spec_122_section():
    schemas = load_expanded_spec214(DAAXES=2, DEAXES=1, NAXIS=2, DNAXIS=5, INSTRUME="notthedkist")
    assert 'copy122' in schemas
    assert 'DATE-OBS' in schemas['copy122']"""
