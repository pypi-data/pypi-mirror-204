from src.smartsheet_pydantic.sources import DataSourceDB


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
