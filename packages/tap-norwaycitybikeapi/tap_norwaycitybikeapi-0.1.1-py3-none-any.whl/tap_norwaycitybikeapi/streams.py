"""Stream type classes for tap-norwaycitybikeapi."""

from __future__ import annotations

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_norwaycitybikeapi.client import NorwayCityBikeAPIStream


class StationsStream(NorwayCityBikeAPIStream):
    """Stream for information about stations and their locations."""

    name = "stations"
    path = "/station_information.json"
    primary_keys = ["station_id"]
    # replication_key = "last_updated"
    schema = th.PropertiesList(
        th.Property(
            "station_id",
            th.StringType,
            description="Unique identifier of a station",
        ),
        th.Property(
            "name",
            th.StringType,
            description="Public name of the station",
        ),
        th.Property(
            "address",
            th.StringType,
            description="Valid street number and name where station is located",
        ),
        th.Property("lat", th.NumberType, description="The WGS 84 latitude of station"),
        th.Property(
            "lon", th.NumberType, description="The WGS 84 longitude of station"
        ),
        th.Property(
            "capacity",
            th.IntegerType,
            description=(
                "Number of total docking points installed at this station, both "
                "available and unavailable"
            ),
        ),
    ).to_dict()


class AvailabilityStream(NorwayCityBikeAPIStream):
    """Stream for the availability of stations."""

    name = "availability"
    path = "/station_status.json"
    primary_keys = ["station_id"]
    schema = th.PropertiesList(
        th.Property(
            "station_id",
            th.StringType,
            description="Unique identifier of a station",
        ),
        th.Property(
            "is_installed",
            th.BooleanType,
            description="1/0 boolean - is the station currently on the street",
        ),
        th.Property(
            "is_renting",
            th.BooleanType,
            description=(
                "1/0 boolean - is the station currently renting bikes (even if the "
                "station is empty, if it is set to allow rentals this value should "
                "be 1)"
            ),
        ),
        th.Property("num_bikes_available", th.NumberType),
        th.Property(
            "num_docks_available",
            th.NumberType,
            description=(
                "Number of empty but disabled dock points at the station. This value "
                "remains as part of the spec as it is possibly useful during "
                "development"
            ),
        ),
        th.Property("last_reported", th.IntegerType),
        th.Property(
            "is_returning",
            th.BooleanType,
            description=(
                "1/0 boolean - is the station accepting bike returns (if a station is "
                "full but would allow a return if it was not full then this value "
                "should be 1)"
            ),
        ),
    ).to_dict()
