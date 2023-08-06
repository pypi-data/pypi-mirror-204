# Taken from: https://github.com/apache/superset/blob/master/superset/db_engine_specs/gsheets.py  # noqa: E501
from superset.db_engine_specs.sqlite import SqliteEngineSpec


class SystemDataEngineSpec(SqliteEngineSpec):
    """Engine for GraphQL API tables"""

    engine = "system"
    engine_name = "system"
    allows_joins = True
    allows_subqueries = True

    default_driver = "apsw"
    sqlalchemy_uri_placeholder = "system://"

    # TODO(cancan101): figure out what other spec items make sense here
    # See: https://preset.io/blog/building-database-connector/
