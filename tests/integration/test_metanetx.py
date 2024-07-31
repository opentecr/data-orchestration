from pathlib import Path

import pytest

from data_orchestration.metanetx.resource import MetaNetXResource


@pytest.mark.parametrize("table_name", ["comp_prop.tsv"])
def test_table_fetch(table_name: str, tmp_path: Path):
    """Test fetching a MetaNetX table."""
    resource = MetaNetXResource(
        base_path=str(tmp_path),
    )
    result = resource.fetch(table=table_name)

    assert result.is_file()
