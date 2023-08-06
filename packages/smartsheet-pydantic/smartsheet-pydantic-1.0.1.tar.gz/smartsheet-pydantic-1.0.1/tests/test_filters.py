from copy import copy
from datetime import datetime, timedelta

from src.smartsheet_pydantic.filters import CustomFilter


def test_custom_filter_no_option_returns_default():
    custom_filter = CustomFilter()
    option = None
    data = [{
        "test_column": "test_data"
    }]
    result = custom_filter.apply_filter(option=option, dataset=data)
    assert result == data


def test_custom_filter_keep_only_thousand_oaks_location():
    """
    CustomFilter class can filter and keep just thousand oaks records.
    """
    mock_dataset = [
        {
            "test_column": "abc",
            "location": "Thousand Oaks Plant, CA - United States"
        },
        {
            "test_column": "def",
            "location": "Not Thousand Oaks"
        },
        {
            "test_column": "ghi",
            "location": None
        }
    ]
    custom_filter = CustomFilter()
    result = custom_filter.apply_filter(
        option="summary",
        dataset=mock_dataset
    )
    assert len(result) == 1


def test_custom_filter_keep_only_prs_opened_within_a_year():
    mock_dataset = [
        {
            'test_column': 'abc',
            'opened_date': None,
            'proj_name': None,
            'lot_names': 'keep',
        },
        {
            'test_column': 'def',
            'opened_date': str(datetime.now() - timedelta(days=1000)),
            'proj_name': 'keep',
            'lot_names': 'keep'
        },
        {
            'test_column': 'ghi',
            'opened_date': str(datetime.now() - timedelta(days=100)),
            'proj_name': 'keep',
            'lot_names': 'keep',
        }
    ]
    custom_filter = CustomFilter()
    result = custom_filter.apply_filter(
        option='trackwise_v2',
        dataset=mock_dataset
    )
    assert len(result) == 1


def test_custom_filter_remove_trackwise_records_by_type():
    template_dataset = {
        'test_column': 'test',
        'opened_date': str(datetime.now()),
        'proj_name': '',
        'lot_names': 'test_lots',
    }
    record_types_to_remove = [
        "Invest.- CAPA Record",
        "Investigation Task",
        "Change Control Record",
        "Change Control Task",
        "Change Record",
        "Corrective and Preventive Action",
        "Corrective and Preventive Action Task",
        "Lab Investigation",
        "Phase 1 Task",
        "SME Assessment",
        None
    ]
    dataset = []
    for record in record_types_to_remove:
        new_data = copy(template_dataset)
        new_data['proj_name'] = record
        dataset.append(new_data)
    print(dataset)
    custom_filter = CustomFilter()
    result = custom_filter.apply_filter(
        option='trackwise_v2',
        dataset=dataset
    )
    assert len(result) == 0


def test_custom_filter_remove_prs_without_lot_impact():
    mock_dataset = [
        {
            'test_column': 'abc',
            'opened_date': str(datetime.now()),
            'proj_name': 'keep',
            'lot_names': None,
        },
        {
            'test_column': 'def',
            'opened_date': str(datetime.now()),
            'proj_name': 'keep',
            'lot_names': None
        },
        {
            'test_column': 'ghi',
            'opened_date': str(datetime.now()),
            'proj_name': 'keep',
            'lot_names': 'keep',
        }
    ]
    custom_filter = CustomFilter()
    result = custom_filter.apply_filter(
        option="trackwise_v2",
        dataset=mock_dataset
    )
    assert len(result) == 1
