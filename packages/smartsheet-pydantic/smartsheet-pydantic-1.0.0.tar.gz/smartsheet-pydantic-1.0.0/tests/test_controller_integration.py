from datetime import date
from lib.controller import \
    SheetDetail, SmartsheetController, SmartsheetControllerFactory
from lib.tests.factories.mock_smartmodel import MockSmartModel, MockSmartModel2


detail_param = {
    "sheet_id": "8967363656738692",
    "description": "mock_integration_sheet",
    "smart_model": MockSmartModel,
}


def setup_test_controller() -> SmartsheetController:
    sheet_detail = SheetDetail(**detail_param)

    return SmartsheetControllerFactory.get_controller(
        sheet_detail=sheet_detail,
    )


def test_smartsheet_controller_create_or_update():
    controller = setup_test_controller()
    controller.create_or_update()


def test_check_for_duplicate_entries():
    controller = setup_test_controller()
    controller.create_or_update()

    detail_param = {
        "sheet_id": "8967363656738692",
        "description": "mock_integration_sheet",
        "smart_model": MockSmartModel2,
    }
    
    sheet_detail = SheetDetail(**detail_param)
    controller = SmartsheetControllerFactory.get_controller(
        sheet_detail=sheet_detail,
    )
    controller.create_or_update()

    sheet_detail = SheetDetail(**detail_param)
    controller = SmartsheetControllerFactory.get_controller(
        sheet_detail=sheet_detail,
    )
    data = controller.extract_as_smartmodels()
    unique_key_3 = [i for i in data if i.test_field_1 == 'unique_key_3'][0]
    assert unique_key_3.test_field_2 == 4
    assert unique_key_3.test_field_3 == 4.0
    assert unique_key_3.test_field_4 == date(2022, 1, 1)
    assert len(data) == 3
