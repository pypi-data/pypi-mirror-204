"""REST client handling, including NorwayCityBikeAPIStream base class."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Iterable

import requests
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class NorwayCityBikeAPIStream(RESTStream):
    """NorwayCityBikeAPI stream class."""

    @property
    def url_base(self) -> str:
        """_summary_
        Return the API URL root, configurable via tap settings.

        Returns:
            str: url_base
                Set dynamically based on `city_name`, which can either
                be `bergen`, `trondheim` or `oslo`.
        """
        city_name = self.config["city_name"].lower()
        return f"https://gbfs.urbansharing.com/{city_name}bysykkel.no"

    records_jsonpath = "$.data.*[*]"  # Or override `parse_response`.

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "client_identifier" in self.config:
            headers["Client-Identifier"] = self.config.get("client_identifier")
        return headers

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())
