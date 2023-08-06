"""Stream type classes for tap-shiftbase."""

from __future__ import annotations

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_shiftbase.client import shiftbaseStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class UsersStream(shiftbaseStream):
    name = "users"
    path = "/users"
    primary_keys = ["Users.id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "users.json"

class AbsenteeOptionsStream(shiftbaseStream):
    name = "absentee_options"
    path = "/absentee_options"
    # primary_keys = ["absenteeoption__id"]
    # replication_key = None
    schema_filepath = SCHEMAS_DIR / "absentee_options.json"

class AbsenteesStream(shiftbaseStream):
    name = "absentees"
    path = "/absentees"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "absentees.json"

class ContractTypesStream(shiftbaseStream):
    name = "contract_types"
    path = "/contract_types"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "contract_types.json"

class CustomFieldsStream(shiftbaseStream):
    name = "custom_fields"
    path = "/custom_fields"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "custom_fields.json"

class DepartmentsStream(shiftbaseStream):
    name = "departments"
    path = "/departments"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "departments.json"

class LocationsStream(shiftbaseStream):
    name = "locations"
    path = "/locations"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "locations.json"

class RostersStream(shiftbaseStream):
    name = "rosters"
    path = "/rosters"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "rosters.json"

class ShiftsStream(shiftbaseStream):
    name = "shifts"
    path = "/shifts"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "shifts.json"

class TeamsStream(shiftbaseStream):
    name = "teams"
    path = "/teams"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "teams.json"

class TimesheetsStream(shiftbaseStream):
    name = "timesheets"
    path = "/timesheets"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "timesheets.json"