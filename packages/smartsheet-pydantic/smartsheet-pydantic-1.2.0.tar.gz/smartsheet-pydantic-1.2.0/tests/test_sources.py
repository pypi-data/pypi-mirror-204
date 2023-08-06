import pytest

from src.smartsheet_pydantic.sources import DataSourcePostgres


class TestDataSourcePostgres:

    def test_missing_properties_raise_type_error(self):
        """
        DataSourcePostgres class requires pre-defined attributes for accessing
        the database. Missing attributes will raise TypeError.
        """
        with pytest.raises(TypeError) as excinfo:
            class TestSource(DataSourcePostgres):
                pass

            TestSource()

        assert "Can't instantiate abstract class TestSource" \
            in str(excinfo.value)

    def test_db_source_tuple_to_dict_transformation(self):
        """
        Databases return results as tuples. Test that the tuples are properly
        transformed to a dictionary with the specified column keys.
        """
        class TestSource(DataSourcePostgres):
            user = 'test user'
            password = 'test password'
            host = 'test host'
            database = 'test database'
            query = 'test query'
            columns = ['test_column_1', 'test_column_2', 'test_column_3']

            def _query(self):
                return [
                    ('value_1', 'value_2', 'value_3'),
                    ('value_4', 'value_5', 'value_6')
                ]

        test_source = TestSource()
        result = test_source.get()
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
