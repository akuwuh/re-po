from __future__ import annotations

import pytest

from repo.features.bio.core.parsing import parse_rows_json


def test_parse_rows_json_rejects_malformed_json() -> None:
    with pytest.raises(ValueError, match="valid JSON"):
        parse_rows_json("[{bad json]")


def test_parse_rows_json_rejects_missing_fields() -> None:
    with pytest.raises(ValueError, match="missing required field: label"):
        parse_rows_json('[{"value":"22"}]')

    with pytest.raises(ValueError, match="missing required field: value"):
        parse_rows_json('[{"label":"age"}]')


def test_parse_rows_json_rejects_invalid_align() -> None:
    with pytest.raises(ValueError, match="align must be 'left' or 'right'"):
        parse_rows_json('[{"label":"age","value":"22","align":"center"}]')


def test_parse_rows_json_rejects_invalid_pad() -> None:
    with pytest.raises(ValueError, match="pad must be between 0 and 8"):
        parse_rows_json('[{"label":"age","value":"22","pad":-1}]')

    with pytest.raises(ValueError, match="pad must be between 0 and 8"):
        parse_rows_json('[{"label":"age","value":"22","pad":9}]')


def test_parse_rows_json_preserves_order() -> None:
    rows = parse_rows_json(
        '[{"label":"a","value":"1"},{"label":"b","value":"2"},{"label":"c","value":"3"}]'
    )
    assert [row.label for row in rows] == ["a", "b", "c"]
