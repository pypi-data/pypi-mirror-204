from abc import ABC, abstractmethod
from functools import reduce
import logging
from smartsheet.models.row import Row

from .filters import CustomFilter
from .sources import DataSource, SourceType
from .smartmodels import SmartModel


class Transformer(ABC):
    @abstractmethod
    def fit(self) -> set[SmartModel]:
        ...


class DatabaseTransformer(Transformer):
    def __init__(
                self,
                source: DataSource,
                model: SmartModel,
                custom_filter: CustomFilter
            ):
        self.source = source
        self.model = model
        self.filter = custom_filter()

    def fit(self, dataset) -> set[SmartModel]:
        initializer = dataset
        functions = [
            self._apply_custom_filter,
            self._smartmodel_fit,
        ]
        return reduce(lambda x, y: y(x), functions, initializer)

    def _apply_custom_filter(
                self,
                dataset: list[SourceType]
            ) -> list[SourceType]:
        """
        Each DataSource may require filters to be applied to limit the queries
        returned.
        """
        return self.filter.apply_filter(
            option=self.source().key, dataset=dataset
        )

    def _smartmodel_fit(
                self,
                dataset: list[SourceType]
            ) -> set[SmartModel]:
        return {self.model.from_source(data) for data in dataset}


class SmartsheetTransformer(Transformer):
    def __init__(
                self,
                model: SmartModel,
            ):
        self.model = model

    def fit(self, rows: list[Row]) -> set[SmartModel]:
        result = []
        model_fields: list[str] = self.model.__fields__.keys()
        logging.info(f"Smartmodel fields: {model_fields}")
        for row in rows:
            cell_values = [getattr(cell, 'value', None) for cell in row.cells]
            cell_values.insert(0, row.id)
            param = dict(zip(model_fields, cell_values))
            try:
                smart_model = self.model.from_smartsheet(param)
                result.append(smart_model)
            except Exception as e:
                logging.warning(f'Smartmodel validation failure: {e}')
        logging.info(f"Total rows transformed into Smartmodel: {len(result)}")
        return set(result)
