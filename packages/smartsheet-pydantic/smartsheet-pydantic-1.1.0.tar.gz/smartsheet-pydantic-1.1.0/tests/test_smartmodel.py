from copy import deepcopy
from datetime import date, datetime
from pydantic import ValidationError
import pytest

from tests.factories.mock_smartmodel import \
    MockSmartModel, MockSmartModelWithNone
from tests.factories.mock_source import MockSource


detail_param = {
    "sheet_id": "8967363656738692",
    "description": "mock_integration_sheet",
    "smart_model": MockSmartModel,
    "source": MockSource,
}


class TestValidationDate:
    mock_nominal = {
        'test_field_1': "test",
        'test_field_2': 10,
        'test_field_3': 12.0,
        'test_field_4': "2014-01-01"
    }

    mock_nominal_2 = {
        'test_field_1': "test",
        'test_field_2': 10,
        'test_field_3': 12.0,
        'test_field_4': date(2014, 1, 1)
    }

    mock_nominal_3 = {
        'test_field_1': "test",
        'test_field_2': 10,
        'test_field_3': 12.0,
        'test_field_4': datetime(2014, 1, 1)
    }

    mock_date_none = {
        'test_field_1': "test",
        'test_field_2': 10,
        'test_field_3': 12.0,
        'test_field_4': None
    }

    mock_date_string_none = {
        'test_field_1': "test",
        'test_field_2': 10,
        'test_field_3': 12.0,
        'test_field_4': "none"
    }

    mock_date_ill_formed = {
        'test_field_1': "test",
        'test_field_2': 10,
        'test_field_3': 12.0,
        'test_field_4': "not a date"
    }

    def test_validation_date(self):
        """
        "validation_date" and "validation_date_or_none" custom validations
        accurately capture all possible type conversion and raises errors
        correctly.

        date type with no None values allowed.
        """

        # nominal situation
        mock = MockSmartModel.from_source(self.mock_nominal)
        assert mock.test_field_1 == "test"
        assert mock.test_field_2 == 10
        assert mock.test_field_3 == 12.0
        assert mock.test_field_4 == date(2014, 1, 1)

        mock = MockSmartModel.from_source(self.mock_nominal_2)
        assert mock.test_field_4 == date(2014, 1, 1)

        mock = MockSmartModel.from_source(self.mock_nominal_3)
        assert mock.test_field_4 == date(2014, 1, 1)

        # Empty Dates either as 'none' string or None
        with pytest.raises(ValueError) as excinfo:
            MockSmartModel.from_source(self.mock_date_none)
        assert "Value cannot be empty" in str(excinfo.value)

        with pytest.raises(ValueError) as excinfo:
            MockSmartModel.from_source(self.mock_date_string_none)
        assert "Value cannot be empty" in str(excinfo.value)

        # Ill-formed date strings
        with pytest.raises(ValueError) as excinfo:
            MockSmartModel.from_source(self.mock_date_ill_formed)
        assert "Must be string formatted date or datetime object: not a date" \
            in str(excinfo.value)

    def test_validation_date_or_none(self):
        """
        "validation_date" and "validation_date_or_none" custom validations
        accurately capture all possible type conversion and raises errors
        correctly.

        date type with None values allowed.
        """

        # nominal situation
        mock = MockSmartModelWithNone.from_source(self.mock_nominal)
        assert mock.test_field_1 == "test"
        assert mock.test_field_2 == 10
        assert mock.test_field_3 == 12.0
        assert mock.test_field_4 == date(2014, 1, 1)

        mock = MockSmartModelWithNone.from_source(self.mock_nominal_2)
        assert mock.test_field_4 == date(2014, 1, 1)

        mock = MockSmartModelWithNone.from_source(self.mock_nominal_3)
        assert mock.test_field_4 == date(2014, 1, 1)

        # Empty Dates either as 'none' string or None
        mock = MockSmartModelWithNone.from_source(self.mock_date_none)
        assert mock.test_field_4 is None

        mock = MockSmartModelWithNone.from_source(self.mock_date_string_none)
        assert mock.test_field_4 is None

        # Ill-formed date strings
        with pytest.raises(ValueError) as excinfo:
            MockSmartModelWithNone.from_source(self.mock_date_ill_formed)
        assert "Must be string formatted date or datetime object: not a date" \
            in str(excinfo.value)


class TestValidationInt:
    mock_nominal = {
        'test_field_1': 'test',
        'test_field_2': 1,
        'test_field_3': 1.0,
        'test_field_4': '2014-01-01'
    }

    mock_nominal_2 = {
        'test_field_1': 'test',
        'test_field_2': 1.0,
        'test_field_3': 1.0,
        'test_field_4': '2014-01-01'
    }

    mock_nominal_3 = {
        'test_field_1': 'test',
        'test_field_2': "1",
        'test_field_3': 1.0,
        'test_field_4': '2014-01-01'
    }

    mock_nominal_4 = {
        'test_field_1': 'test',
        'test_field_2': "1.0",
        'test_field_3': 1.0,
        'test_field_4': '2014-01-01'
    }

    mock_int_none = {
        'test_field_1': 'test',
        'test_field_2': None,
        'test_field_3': 1.0,
        'test_field_4': '2014-01-01'
    }

    mock_int_string_none = {
        'test_field_1': 'test',
        'test_field_2': "none",
        'test_field_3': 1.0,
        'test_field_4': '2014-01-01'
    }

    mock_int_ill_formed = {
        'test_field_1': 'test',
        'test_field_2': "not a number",
        'test_field_3': 1.0,
        'test_field_4': '2014-01-01'
    }

    def test_validation_int(self):
        """
        "validation_int" and "validation_int_or_none" custom validations
        accurately capture all possible type conversion and raises errors
        correctly.

        int type with None values not allowed.
        """

        # nominal situation
        mock = MockSmartModel.from_source(self.mock_nominal)
        assert mock.test_field_1 == 'test'
        assert mock.test_field_2 == 1
        assert mock.test_field_3 == 1.0
        assert mock.test_field_4 == date(2014, 1, 1)

        mock = MockSmartModel.from_source(self.mock_nominal_2)
        assert mock.test_field_2 == 1

        mock = MockSmartModel.from_source(self.mock_nominal_3)
        assert mock.test_field_2 == 1

        mock = MockSmartModel.from_source(self.mock_nominal_4)
        assert mock.test_field_2 == 1

        with pytest.raises(ValueError) as excinfo:
            MockSmartModel.from_source(self.mock_int_none)
        assert "Value cannot be empty" in str(excinfo.value)

        with pytest.raises(ValueError) as excinfo:
            MockSmartModel.from_source(self.mock_int_string_none)
        assert "Value cannot be empty" in str(excinfo.value)

        with pytest.raises(ValueError) as excinfo:
            MockSmartModel.from_source(self.mock_int_ill_formed)
        assert "Must be string formatted number: not a number" \
            in str(excinfo.value)

    def test_validation_int_or_none(self):
        """
        "validation_int" and "validation_int_or_none" custom validations
        accurately capture all possible type conversion and raises errors
        correctly.

        int type with None values allowed.
        """

        # nominal situation
        mock = MockSmartModelWithNone.from_source(self.mock_nominal)
        assert mock.test_field_1 == "test"
        assert mock.test_field_2 == 1
        assert mock.test_field_3 == 1.0
        assert mock.test_field_4 == date(2014, 1, 1)

        mock = MockSmartModelWithNone.from_source(self.mock_nominal_2)
        assert mock.test_field_2 == 1

        mock = MockSmartModelWithNone.from_source(self.mock_nominal_3)
        assert mock.test_field_2 == 1

        # Empty Dates either as 'none' string or None
        mock = MockSmartModelWithNone.from_source(self.mock_int_none)
        assert mock.test_field_2 is None

        mock = MockSmartModelWithNone.from_source(self.mock_int_string_none)
        assert mock.test_field_2 is None

        # Ill-formed date strings
        with pytest.raises(ValueError):
            MockSmartModelWithNone.from_source(self.mock_int_ill_formed)
            assert True


class TestValidationFloat:
    mock_nominal = {
        'test_field_1': 'test',
        'test_field_2': 1,
        'test_field_3': 1.0,
        'test_field_4': '2014-01-01',
    }
    mock_nominal_2 = {
        'test_field_1': 'test',
        'test_field_2': 2,
        'test_field_3': 2,
        'test_field_4': '2014-01-01',
    }
    mock_nominal_3 = {
        'test_field_1': 'test',
        'test_field_2': 3,
        'test_field_3': "3.0",
        'test_field_4': '2014-01-01',
    }
    mock_nominal_4 = {
        'test_field_1': 'test',
        'test_field_2': 4,
        'test_field_3': "4",
        'test_field_4': '2014-01-01',
    }
    mock_float_none = {
        'test_field_1': "test",
        'test_field_2': 10,
        'test_field_3': None,
        'test_field_4': '2014-01-01',
    }
    mock_float_string_none = {
        'test_field_1': "test",
        'test_field_2': 10,
        'test_field_3': 'none',
        'test_field_4': '2014-01-01'
    }

    mock_float_ill_formed = {
        'test_field_1': "test",
        'test_field_2': 10,
        'test_field_3': 'not a float',
        'test_field_4': "2014-01-01"
    }

    def test_validation_float(self):
        """
        "validation_date" and "validation_date_or_none" custom validations
        accurately capture all possible type conversion and raises errors
        correctly.

        date type with no None values allowed.
        """

        # nominal situation
        mock = MockSmartModel.from_source(self.mock_nominal)
        assert mock.test_field_1 == "test"
        assert mock.test_field_2 == 1
        assert mock.test_field_3 == 1.0
        assert mock.test_field_4 == date(2014, 1, 1)

        mock = MockSmartModel.from_source(self.mock_nominal_2)
        assert mock.test_field_3 == 2.0

        mock = MockSmartModel.from_source(self.mock_nominal_3)
        assert mock.test_field_3 == 3.0

        mock = MockSmartModel.from_source(self.mock_nominal_4)
        assert mock.test_field_3 == 4.0

        # Empty Dates either as 'none' string or None
        with pytest.raises(ValueError) as excinfo:
            MockSmartModel.from_source(self.mock_float_none)
        assert "Value cannot be empty" in str(excinfo.value)

        with pytest.raises(ValueError) as excinfo:
            MockSmartModel.from_source(self.mock_float_string_none)
        assert "Value cannot be empty" in str(excinfo.value)

        # Ill-formed date strings
        with pytest.raises(ValueError) as excinfo:
            MockSmartModel.from_source(self.mock_float_ill_formed)
            assert True

    def test_validation_float_with_none(self):
        """
        "validation_float" and "validation_float_or_none" custom validations
        accurately capture all possible type conversion and raises errors
        correctly.

        float type with None values allowed.
        """

        # nominal situation
        mock = MockSmartModelWithNone.from_source(self.mock_nominal)
        assert mock.test_field_1 == "test"
        assert mock.test_field_2 == 1
        assert mock.test_field_3 == 1.0
        assert mock.test_field_4 == date(2014, 1, 1)

        mock = MockSmartModelWithNone.from_source(self.mock_nominal_2)
        assert mock.test_field_3 == 2.0

        mock = MockSmartModelWithNone.from_source(self.mock_nominal_3)
        assert mock.test_field_3 == 3.0

        mock = MockSmartModelWithNone.from_source(self.mock_nominal_4)
        assert mock.test_field_3 == 4.0

        # Empty Dates either as 'none' string or None
        mock = MockSmartModelWithNone.from_source(self.mock_float_none)
        assert mock.test_field_3 is None

        mock = MockSmartModelWithNone.from_source(self.mock_float_string_none)
        assert mock.test_field_3 is None

        # Ill-formed date strings
        with pytest.raises(ValueError):
            MockSmartModelWithNone.from_source(self.mock_float_ill_formed)
            assert True


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
