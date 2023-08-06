from __future__ import annotations
from abc import ABC, abstractmethod
from copy import deepcopy
from datetime import date, datetime
from dateutil.parser import parse, ParserError
from collections.abc import KeysView
from pydantic import BaseModel, create_model, root_validator, validator
from smartsheet import models
from smartsheet.models.sheet import Sheet


def validation_conform_to_date_format(cls, v):
    match True:
        case True if type(v) is date:
            return v
        case True if type(v) is datetime:
            return v.date()
        case True if type(v) is str:
            try:
                if v.lower() == "none":
                    return None
                return parse(v).date()
            except ParserError:
                raise ValueError(f"""
                    Must be string formatted date or datetime object: {v}
                """)
        case True if v is None:
            return None
        case _:
            return v


def validation_conform_to_string_int_or_float_into_int(cls, v):
    match True:
        case True if type(v) is int:
            return v
        case True if type(v) is str:
            if v.lower() == "none":
                return 0
            try:
                return int(float(v))
            except ValueError:
                raise ValueError(f"""
                    Must be string formatted number or None: {v}
                """)
        case True if type(v) is float:
            return int(v)
        case True if v is None:
            return 0
        case _:
            raise ValueError(f"""
                Must be string formatted number or None: {v}
            """)


class SmartModel(ABC, BaseModel):
    row_id: int | None

    def get_smart_sheet_column_ids(self, sheet: Sheet) -> list[int]:
        return [column.id for column in sheet.columns]

    def to_row(self, sheet: Sheet):
        """
        convert the smartmodel into a smartsheet Row object using the sheet
        parameters given.
        """
        column_ids: list[int] = self.get_smart_sheet_column_ids(sheet)
        new_row = models.Row()
        new_row.to_top = True
        fields = list(self.__fields__.keys())[1:]
        column_id_and_field_pair = zip(column_ids, fields)
        for column_id, field_name in column_id_and_field_pair:
            if getattr(self, field_name):
                params = {
                    'column_id': column_id,
                    'value': str(getattr(self, field_name, None)),
                    'strict': False
                }
                new_row.cells.append(params)
        if self.row_id:
            new_row.id_ = self.row_id
        return new_row

    def unique_columns(self, columns: list[str]) -> str:
        collection = []
        for i in columns:
            collection.append(str(getattr(self, i, None)))
        return "-".join(collection)

    @root_validator(pre=True, allow_reuse=True)
    def no_empty_strings(cls, values):
        for key, value in values.items():
            if value == '' or value == 'none':
                values[key] = None
        return values

    @classmethod
    def from_source(cls, data):
        validators = {}
        if cls.Configuration.conform_to_date:
            validators["conform_to_date"] = (
                validator(
                    *cls.Configuration.conform_to_date,
                    pre=True,
                    allow_reuse=True
                )
                (validation_conform_to_date_format)
            )
        if cls.Configuration.conform_to_int:
            validators["conform_to_int"] = (
                validator(
                    *cls.Configuration.conform_to_int,
                    pre=True,
                    allow_reuse=True
                )
                (validation_conform_to_string_int_or_float_into_int)
            )
        if cls.Configuration.key_mapping:
            new_data = {}
            for key, value in data.items():
                try:
                    new_data[cls.Configuration.key_mapping[key]] = value
                except KeyError:
                    continue
            data = new_data
        model = create_model(
            f"{cls.__class__.__name__}",
            __base__=cls,
            __validators__=validators
        )
        return model(**data)

    @classmethod
    def from_smartsheet(cls, data):
        validators = {}
        if cls.Configuration.conform_to_date:
            validators["conform_to_date"] = (
                validator(
                    *cls.Configuration.conform_to_date,
                    pre=True,
                    allow_reuse=True
                )
                (validation_conform_to_date_format)
            )
        if cls.Configuration.conform_to_int:
            validators["conform_to_int"] = (
                validator(
                    *cls.Configuration.conform_to_int,
                    pre=True,
                    allow_reuse=True
                )
                (validation_conform_to_string_int_or_float_into_int)
            )
        model = create_model(
            f"{cls.__class__.__name__}",
            __base__=cls,
            __validators__=validators
        )
        return model(**data)

    @abstractmethod
    def __lt__(self, other):
        pass

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        """
        Utilize all fields except the row_id to create a unique hash for the
        object to be used for equality checks. row_id may or may not be present
        depending upon the whether the object is created from reading
        Smartsheet data (with row_id), or from the database (no row_id).
        """
        full_key: KeysView = self.__fields__.keys()
        trimmed_key: list[str] = [key for key in full_key if key != 'row_id']
        values: list[str] = [
            str(getattr(self, field_name))
            for field_name in trimmed_key
        ]
        values.sort()  # values may come back in various orders from Smartsheet
        return hash("".join(values))

    @classmethod
    def identify_incoming_differences(
                cls,
                existing_data: set[SmartModel],
                incoming_data: set[SmartModel]
            ) -> set[SmartModel]:
        """
        Use the python set's builtin method 'difference_update' to remove from
        a given set, objects that are contained in the incoming set.
        This effectively isolates brand new data that is incoming, as well as
        existing data that has been modified and has a new hash key due to the
        change.
        """
        difference = deepcopy(incoming_data)
        difference.difference_update(existing_data)
        return difference

    @classmethod
    def split_existing_vs_new(
                cls,
                existing_data: set[SmartModel],
                incoming_data: set[SmartModel]
            ):
        """
        Using the user specified unique key, separate based on whether or
        not the key exists in the current Smartsheet or not.
        """
        def get_unique_columns_mapping():
            unique_columns_mapping = {}
            for model in existing_data:
                unique_columns_collection = []
                for key in cls.Configuration.unique_columns:
                    unique_columns_collection.append(
                        str(getattr(model, key, None))
                    )
                unique_columns = "-".join(unique_columns_collection)
                unique_columns_mapping[unique_columns] = model
            return unique_columns_mapping

        unique_columns_mapping = get_unique_columns_mapping()

        existing: set[SmartModel] = set()
        new: set[SmartModel] = set()

        for data in incoming_data:
            unique_column = data.unique_columns(cls.Configuration.unique_columns)
            if unique_column in unique_columns_mapping:
                smartsheet_model = unique_columns_mapping[unique_column]
                data.row_id = smartsheet_model.row_id
                existing.add(data)
            else:
                new.add(data)
        return {"existing": existing, "new": new}

    class Configuration:
        conform_to_date: list[str] | list[None] = []
        conform_to_int: list[str] | list[None] = []
        key_mapping: dict | None = None
        unique_columns: list[str] = []
