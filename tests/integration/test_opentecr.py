from pathlib import Path

import pytest

from data_orchestration.opentecr.resource import GoogleSheetsResource


# from data_orchestration.opentecr.op import fetch_sheet


@pytest.mark.parametrize("gid", ["81596307"])
def test_table_fetch(gid: str, tmp_path: Path):
    """Test fetching a Google sheet as Excel."""
    resource = GoogleSheetsResource(base_path=str(tmp_path))
    result = resource.fetch(gid=gid)

    assert result.is_file()
