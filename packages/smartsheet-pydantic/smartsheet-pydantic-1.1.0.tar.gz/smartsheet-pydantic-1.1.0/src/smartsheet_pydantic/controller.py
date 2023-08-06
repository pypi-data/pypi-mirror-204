import logging
from smartsheet.models.row import Row
from smartsheet import Smartsheet
from typing import TypedDict

from .debug_logger import debug_logger
from .filters import CustomFilter
from .smartmodels import SmartModel
from .sources import DataSourceAPI, SourceType
from .transformer import DatabaseTransformer, SmartsheetTransformer


class SheetDetail(TypedDict):
    sheet_id: int
    description: str | None
    smart_model: SmartModel
    source: DataSourceAPI


class SmartsheetController():
    def __init__(self, client, **sheet_detail: SheetDetail):
        self.client = client
        self.sheet_id = sheet_detail['sheet_id']
        self.description = sheet_detail['description']
        self.smart_model = sheet_detail['smart_model']
        self.source = self.smart_model.Configuration.source
        self.unique_columns = self.smart_model.Configuration.unique_columns
        self.sheet = self._set_sheet(client, self.sheet_id)

        self.source_transformer = DatabaseTransformer(
            source=self.source,
            model=self.smart_model,
            custom_filter=CustomFilter
        )
        self.target_transformer = SmartsheetTransformer(
            model=self.smart_model
        )

    def _set_sheet(self, client, sheet_id):
        return client.Sheets.get_sheet(sheet_id)

    def _get_row_ids(self) -> list[int]:
        """
        If sheet has been declared, get a list of all row_ids from the sheet.
        """
        if self.sheet:
            return [row.id for row in self.sheet.rows]
        else:
            raise Exception("No sheet has been declared.")

    def create_or_update(self):
        try:
            db_data: list[SourceType] = self._query_database()
            smartmodel_source: set[SmartModel] = \
                self.source_transformer.fit(db_data)

            smartsheet_data: list[Row] = self.extract_row_objects()
            smartmodel_target: set[SmartModel] = \
                self.target_transformer.fit(smartsheet_data)

            difference = self.smart_model.identify_incoming_differences(
                existing_data=smartmodel_target,
                incoming_data=smartmodel_source,
            )
            existing_vs_new = self.smart_model.split_existing_vs_new(
                existing_data=smartmodel_target,
                incoming_data=difference,
            )
            existing = existing_vs_new['existing']
            new = existing_vs_new['new']
            self.add_rows(new)
            self.update_rows(existing)
        except Exception as e:
            logging.error(f"Data refresh failed: {e}")
            raise Exception(e)
        return None

    def _query_database(self) -> list[SourceType]:
        try:
            return self.source().get()
        except Exception as e:
            raise Exception(f"Database query failed: {e}")

    @debug_logger
    def extract_row_objects(self) -> list[Row]:
        """
        Extract the Smartsheet into Smartsheet Row objects, skipping any empty
        rows.
        """
        result: list[Row] = []
        debug_empty_row_count = 0

        def is_empty_row(row):
            """
            Check to see if the smartsheet row is blank.
            """
            if len([cell.value for cell in row.cells if cell.value]) == 0:
                return True
            return False

        # Create a dictionary of the Smartmodel fields as key, and sheet values
        # as the values. Pass along as kwarg arguments to the Smartmodel, and
        # return a full set of Smartmodels.
        for row in self.sheet.rows:
            if is_empty_row(row):
                debug_empty_row_count += 1
                continue
            result.append(row)
        logging.info(f"Total empty rows skipped: {debug_empty_row_count}")
        logging.info(f"Total Row objects extracted: {len(result)}")
        return list(result)

    @debug_logger
    def extract_as_smartmodels(self) -> set[SmartModel]:
        rows = self.extract_row_objects()
        return self.target_transformer.fit(rows)

    def add_rows(self, dataset: set[SmartModel]) -> dict[str: int]:
        """
        Append the given set of SmartModels into the smartsheet.
        """
        try:
            logging.info(f"{len(dataset)} SmartModels prepared for addition")
            rows = []
            for data in dataset:
                row = \
                    data.to_row(self.sheet)
                rows.append(row)
            response = self.sheet.add_rows(rows)
            if response.result_code != 0:
                raise Exception(f"Row addition failed {response.data}")
            return {"status_code": 201}
        except Exception as e:
            raise Exception(f"Row addition failed {e}")

    @debug_logger
    def update_rows(self, dataset: set[SmartModel]) -> dict[str: int]:
        """
        Update the existing data rows within smartsheet, using their unique
        row_ids to find the appropriate rows to update.
        """
        try:
            logging.info(f"{len(dataset)} SmartModels prepared for update")
            rows = []
            for data in dataset:
                row = \
                    data.to_row(self.sheet)
                rows.append(row)
            logging.info(f"Number of rows: {len(rows)}")
            unique_row_ids = {row.id for row in rows}
            logging.info(f"Number of unique row_ids: {len(unique_row_ids)}")
            response = self.client.Sheets.update_rows(
                self.sheet_id,
                rows
            )
            if response.result_code != 0:
                raise Exception(f"Row addition failed {response.data}")
            return {"status_code": 201}
        except Exception as e:
            raise Exception(f"Row update failed {e}")

    def delete_all_rows(
                self,
                chunk_interval=300
            ) -> bool:
        """
        Delete all existing rows in the declared sheet.
        """
        row_ids_to_delete: list[int] = self.get_row_ids()
        for i in range(0, len(row_ids_to_delete), chunk_interval):
            response = self.client.Sheets.delete_rows(
                self.sheet.id,
                row_ids_to_delete[i:i + chunk_interval]
            )
            if response.result_code != 0:
                raise Exception("Row deletion failed.")
        return True


class SmartsheetControllerFactory():
    @staticmethod
    def return_client():
        return Smartsheet()

    @staticmethod
    def get_controller(sheet_detail: SheetDetail):
        client = SmartsheetControllerFactory.return_client()
        client.errors_as_exceptions(True)
        return SmartsheetController(client, **sheet_detail)
