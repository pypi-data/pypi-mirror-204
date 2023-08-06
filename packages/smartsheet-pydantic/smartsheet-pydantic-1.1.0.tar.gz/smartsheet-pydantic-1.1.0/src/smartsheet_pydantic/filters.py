from dateutil.parser import parse
from datetime import datetime, timedelta
import logging

from .sources import SourceType


class CustomFilter():
    def apply_filter(
                self,
                option: str,
                dataset: SourceType
            ) -> list[SourceType]:
        match option:
            case "summary":
                return self._keep_only_thousand_oaks_location(dataset)
            case "trackwise_v2":
                _ = self._keep_only_prs_opened_within_a_year(dataset)
                _ = self._remove_trackwise_records_by_type(_)
                result = self._remove_prs_without_lot_impact(_)
                return result
            case _:
                return dataset

    def _keep_only_thousand_oaks_location(
                self,
                dataset: SourceType
            ) -> list[SourceType]:
        db_result: list[SourceType] = []
        for result in dataset:
            if not result['location']:
                continue
            if result['location'] == "Thousand Oaks Plant, CA - United States":
                db_result.append(result)
        logging.info(f"db_result trimmed: {len(db_result)}")
        return db_result

    def _keep_only_prs_opened_within_a_year(
                self,
                dataset: SourceType
            ) -> list[SourceType]:
        db_result: list[SourceType] = []
        for result in dataset:
            if not result['opened_date']:
                continue
            opened_date = parse(result['opened_date'])
            a_year_ago = datetime.today() - timedelta(days=365)
            if opened_date > a_year_ago:
                db_result.append(result)
        return db_result

    def _remove_trackwise_records_by_type(
                self,
                dataset: SourceType
            ):
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
        ]
        db_result: list[SourceType] = []
        for result in dataset:
            if not result['proj_name']:
                continue
            if not result['proj_name'] in record_types_to_remove:
                db_result.append(result)
        return db_result

    def _remove_prs_without_lot_impact(self, dataset: SourceType):
        db_result: list[SourceType] = []
        for result in dataset:
            if not result['lot_names']:
                continue
            if len(result['lot_names']) > 0:
                db_result.append(result)
        return db_result
