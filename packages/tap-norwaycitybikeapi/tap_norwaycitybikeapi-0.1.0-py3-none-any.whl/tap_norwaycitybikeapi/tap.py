"""NorwayCityBikeAPI tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_norwaycitybikeapi.streams import (
    AvailabilityStream,
    NorwayCityBikeAPIStream,
    StationsStream,
)


class TapNorwayCityBikeAPI(Tap):
    """NorwayCityBikeAPI tap class."""

    name = "tap-norwaycitybikeapi"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "client_identifier",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description=(
                "The value should contain your company/organization name, "
                "follwed by a dash and the application's name."
            ),
        ),
        th.Property(
            "city_name",
            th.StringType,
            default="oslo",
            required=True,
            description=(
                "Name of Norwegian city having City Bikes. "
                "Currently only available for Trondheim, Oslo and Bergen."
            ),
        ),
    ).to_dict()

    def discover_streams(self) -> list[NorwayCityBikeAPIStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            StationsStream(self),
            AvailabilityStream(self),
        ]


if __name__ == "__main__":
    TapNorwayCityBikeAPI.cli()
