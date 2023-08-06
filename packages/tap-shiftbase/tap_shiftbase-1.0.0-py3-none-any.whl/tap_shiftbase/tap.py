"""shiftbase tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_shiftbase import streams


class Tapshiftbase(Tap):
    """shiftbase tap class."""

    name = "tap-shiftbase"
    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The api key to authenticate Shiftbase (prepend with API or USER)",
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://api.shiftbase.com/api",
            description="The url for the shiftbase api",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.shiftbaseStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.UsersStream(self),
            streams.AbsenteeOptionsStream(self),
            streams.AbsenteesStream(self),
            streams.ContractTypesStream(self),
            streams.CustomFieldsStream(self),
            streams.DepartmentsStream(self),
            streams.LocationsStream(self),
            streams.RostersStream(self),
            streams.ShiftsStream(self),
            streams.TeamsStream(self),
            streams.TimesheetsStream(self),
        ]


if __name__ == "__main__":
    Tapshiftbase.cli()
