from unittest.mock import patch, Mock
from smartsheet.models.row import Row

from src.smartsheet_pydantic.controller import \
    SheetDetail, SmartsheetControllerFactory, SmartsheetController
from tests.factories.mock_smartmodel import MockSmartModel
from tests.factories.mock_source import MockSource
from tests.factories.mock_sheet import MockSheet


detail_param = {
    "sheet_id": "0123456789",
    "description": "mock_sheet",
    "unique_columns": ["test_field_1"],
    "smart_model": MockSmartModel,
    "source": MockSource,
}


@patch('tests.test_controller.SmartsheetControllerFactory.return_client')
def setup_test_controller(client) -> SmartsheetController:
    client.return_value = Mock()
    sheet_detail = SheetDetail(**detail_param)

    return SmartsheetControllerFactory.get_controller(
        sheet_detail=sheet_detail,
    )


def test_smartsheet_controller_factory_initialization():
    test_controller = setup_test_controller()
    assert test_controller.sheet_id == detail_param['sheet_id']
    assert test_controller.description == detail_param['description']
    assert test_controller.unique_columns == detail_param['unique_columns']
    assert test_controller.smart_model == detail_param['smart_model']
    assert test_controller.source == detail_param['source']


@patch('tests.test_controller.SmartsheetControllerFactory.return_client')
@patch('src.smartsheet_pydantic.controller.SmartsheetController._set_sheet')
def test_smartsheet_controller_extract_as_smartmodels(set_sheet, client):
    client.return_value = Mock()
    data = MockSource().get()
    set_sheet.return_value = MockSheet(data)
    sheet_detail = SheetDetail(**detail_param)

    test_controller = SmartsheetControllerFactory.get_controller(
        sheet_detail=sheet_detail,
    )
    result: set[MockSmartModel] = test_controller.extract_as_smartmodels()
    expected = {
        MockSmartModel(**mock_data) for mock_data
        in MockSource().get()
    }
    assert result == expected


@patch('tests.test_controller.SmartsheetControllerFactory.return_client')
@patch('src.smartsheet_pydantic.controller.SmartsheetController._set_sheet')
def test_smartsheet_controller_get_row_ids(set_sheet, client):
    client.return_value = Mock()
    data = MockSource().get()
    mock_sheet = MockSheet(data)
    set_sheet.return_value = mock_sheet

    sheet_detail = SheetDetail(**detail_param)
    test_controller = SmartsheetControllerFactory.get_controller(
        sheet_detail=sheet_detail
    )
    actual_row_ids = test_controller._get_row_ids()
    expected_row_ids = [row.id for row in mock_sheet.rows]
    assert actual_row_ids == expected_row_ids


@patch('tests.test_controller.SmartsheetControllerFactory.return_client')
@patch('src.smartsheet_pydantic.controller.SmartsheetController._set_sheet')
def test_smartsheet_controller_query_database(set_sheet, client):
    client.return_value = Mock()
    data = MockSource().get()
    mock_sheet = MockSheet(data)
    set_sheet.return_value = mock_sheet

    sheet_detail = SheetDetail(**detail_param)
    test_controller = SmartsheetControllerFactory.get_controller(
        sheet_detail=sheet_detail
    )
    db_data = test_controller._query_database()
    assert db_data == data


@patch('tests.test_controller.SmartsheetControllerFactory.return_client')
@patch('src.smartsheet_pydantic.controller.SmartsheetController._set_sheet')
def test_smartsheet_controller_extract_row_objects(set_sheet, client):
    client.return_value = Mock()
    data = MockSource().get()
    mock_sheet = MockSheet(data)
    set_sheet.return_value = mock_sheet

    sheet_detail = SheetDetail(**detail_param)
    test_controller = SmartsheetControllerFactory.get_controller(
        sheet_detail=sheet_detail
    )
    actual_rows: list[Row] = test_controller.extract_row_objects()
    expected_rows: list[Row] = [row for row in mock_sheet.rows]
    assert actual_rows == expected_rows
