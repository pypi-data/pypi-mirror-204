from copy import deepcopy
from smartsheet.models.row import Row
import logging

from lib.tests.factories.mock_smartmodel import MockSmartModel
from lib.tests.factories.mock_source import MockSource


detail_param = {
    "sheet_id": "8967363656738692",
    "description": "mock_integration_sheet",
    "smart_model": MockSmartModel,
    "source": MockSource,
}


def test_smartmodel_identify_incoming_differences():
    """
    Smartmodel._identify_incoming_differences takes two sets of
    SmartModels and returns the set of their differences.
    """
    db_data = MockSource().get()
    existing_models: list[MockSmartModel] = [
        MockSmartModel.from_source(data) for data
        in db_data
    ]
    addition = [MockSmartModel.from_source(
        {
            'test_field_1': 'unique_key_4',
            'test_field_2': 4,
            'test_field_3': 4.0,
            'test_field_4': '2014-10-04'
        }
    )]
    existing_models_with_new: list[MockSmartModel] = deepcopy(existing_models)
    existing_models_with_new.extend(addition)

    actual_difference = MockSmartModel.identify_incoming_differences(
        existing_data=set(existing_models),
        incoming_data=set(existing_models_with_new)
    )
    assert actual_difference == set(addition)


def test_smartmodel_split_existing_vs_new():
    """
    Smartmodel.split_existing_vs_new will take existing data and using unique
    key columns, distinguish what already exists vs what is new.
    """
    db_data = MockSource().get()
    existing_models: list[MockSmartModel] = [
        MockSmartModel.from_source(data) for data
        in db_data
    ]
    addition = [MockSmartModel.from_source(
        {
            'test_field_1': 'unique_key_4',
            'test_field_2': 4,
            'test_field_3': 4.0,
            'test_field_4': '2014-10-04'
        }
    )]
    existing_models_with_new: list[MockSmartModel] = deepcopy(existing_models)
    existing_models_with_new.extend(addition)

    existing_vs_new = MockSmartModel.split_existing_vs_new(
        existing_data=set(existing_models),
        incoming_data=set(existing_models_with_new)
    )
    existing = existing_vs_new['existing']
    new = existing_vs_new['new']
    assert existing == set(existing_models)
    assert new == set(addition)
