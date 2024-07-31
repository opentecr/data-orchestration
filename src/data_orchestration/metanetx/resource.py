# Copyright (c) 2024 openTECR Community
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.


"""Provide MetaNetX resources."""

from hashlib import md5
from typing import Annotated

import httpx
from dagster import ConfigurableResource
from pydantic import Field
from upath import UPath
from zstandard import ZstdCompressor


class MetaNetXResource(ConfigurableResource):
    """Define a MetaNetX table resource."""

    base_url: Annotated[
        str,
        Field(
            default="https://www.metanetx.org/ftp",
            description="The MetaNetX base URL.",
        ),
    ]
    version: Annotated[
        str,
        Field(
            default="4.4",
            description="The MetaNetX release version.",
        ),
    ]
    base_path: Annotated[
        str,
        Field(
            default=".",
            description="The base path where to store table files.",
        ),
    ]

    def url(self, table: str) -> str:
        """Return the URL of the table file."""
        return f"{self.base_url}/{self.version}/{table}"

    def _md5_url(self, table: str) -> str:
        """Return the URL of the MD5 checksum file."""
        return f"{self.url(table)}.md5"

    def _fetch_md5(self, client: httpx.Client, table: str) -> str:
        """Fetch the MD5 checksum from the remote file."""
        response = client.get(self._md5_url(table))
        response.raise_for_status()

        # We expect a single line within the MD5 checksum file.
        checksum, filename = next(
            (line.split() for line in response.text.splitlines()),
            None,
        )

        if filename != table:
            msg = (
                f"Filename mismatch in MD5 checksum file: {filename} is not the "
                f"expected {table}."
            )
            raise ValueError(msg)

        return checksum

    def _fetch_table(self, client: httpx.Client, table: str, expected_md5: str) -> UPath:
        """Fetch the table file in a streaming fashion."""
        md5_hash = md5(usedforsecurity=False)
        zstd = ZstdCompressor(
            level=22,
            write_checksum=True,
            write_content_size=True,
        )
        total = 0

        result = UPath(self.base_path) / f"{table}.zst"
        with (
            client.stream("GET", self.url(table)) as response,
            result.open(mode="wb") as handle,
            zstd.stream_writer(writer=handle, closefd=False) as compressor,
        ):
            response.raise_for_status()
            for data in response.iter_bytes():
                total += len(data)
                md5_hash.update(data)
                compressor.write(data)

        # Check the content size.
        if (
            expected_size := int(response.headers.get("Content-Length", -1))
        ) >= 0 and total != expected_size:
            msg = (
                f"Content size mismatch in table file: {total} bytes is not the "
                f"expected {expected_size}."
            )
            raise ValueError(msg)

        # Check the MD5 checksum.
        if (actual := md5_hash.hexdigest()) != expected_md5:
            msg = (
                f"MD5 checksum mismatch in table file: {actual} is not the expected "
                f"{expected_md5}."
            )
            raise ValueError(msg)

        return result

    def fetch(self, table: str) -> UPath:
        """Fetch the configured table."""
        with httpx.Client() as client:
            expected_md5 = self._fetch_md5(client, table)
            return self._fetch_table(client, table, expected_md5)
