from collections.abc import KeysView
from unittest.mock import patch

from lib import DataSource
from lib.sources import DataSourceDB
from sources import ReleaseSchedule, Summary
from tests.factories.sources import (
    MockSourceReleaseSchedule, MockSourceSummary
)


def test_process_heartbeat_db_release_schedule():
    """
    The "Release Schedule" aka "Fill Lot" mock dataset column values matches
    that of the typed dict model defined for use within the system.
    """
    database: DataSource = \
        MockSourceReleaseSchedule().get()
    mock_database_keys: KeysView = database[0].keys()
    expected_keys: KeysView = ReleaseSchedule.__annotations__.keys()
    assert mock_database_keys == expected_keys


def test_process_heartbeat_db_trackwise():
    """
    The "TrackWise" mock dataset column values matches that of the typed dict
    model defined for use within the system.
    """
    database: DataSource = MockSourceSummary().get()
    mock_database_keys: KeysView = database[0].keys()
    expected_keys: KeysView = Summary.__annotations__.keys()
    assert mock_database_keys == expected_keys


def test_db_source_tuple_to_dict_transformation():
    """
    Databases return results as tuples. Test that the tuples are properly
    transformed to a dictionary with the specified column keys.
    """
    class TestSource(DataSourceDB):
        columns = ['test_column_1', 'test_column_2', 'test_column_3']

        def _query(self):
            return [
                ('value_1', 'value_2', 'value_3'),
                ('value_4', 'value_5', 'value_6')
            ]

    result = TestSource().get()
    assert result == [
        {
            'test_column_1': 'value_1',
            'test_column_2': 'value_2',
            'test_column_3': 'value_3',
        },
        {
            'test_column_1': 'value_4',
            'test_column_2': 'value_5',
            'test_column_3': 'value_6',
        },
    ]
