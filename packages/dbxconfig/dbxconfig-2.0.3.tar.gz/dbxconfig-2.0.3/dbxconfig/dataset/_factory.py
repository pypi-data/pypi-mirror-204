from enum import Enum
from ._deltalake import DeltaLake
from ._read import Read
from ._write import Write
from ._dataset import DataSet
import logging
from .._stage_type import StageType
from .._table import Table
from .._timeslice import Timeslice
from typing import Union


class IOType(Enum):
    READ = "read"
    DELTALAKE = "deltalake"
    WRITE = "write"


class _DatasetFactory:
    _TIMESLICE = "timeslice"
    _TABLE = "destination_table"
    _TABLE_PROPERTIES = "table_properties"
    _STAGE = "stage"
    _DATABASE = "database"
    _CONFIG_PATH = "config_path"

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)
        self._dataset = {}

    def register_dataset_type(self, io_type: StageType, dataset_type: type):
        self._logger.debug(f"Register dataset type {dataset_type} as {type}")
        self._dataset[io_type] = dataset_type

    def _get_dataset_type(
        self,
        stage: StageType,
        dataset_config: dict,
    ) -> DataSet:
        type: IOType = IOType(stage.value.lower())

        self._logger.debug(f"Get {type.name} from factory dataset")
        dataset_class = self._dataset.get(type)

        if not dataset_class:
            self._logger.debug(
                f"IOType {type.name} not registered in the dataset factory dataset"
            )
            raise ValueError(type)

        return dataset_class(
            **dataset_config,
        )

    def get_data_set(
        self, config: dict, dataset: Union[Table, dict], timeslice: Timeslice
    ):
        if isinstance(dataset, dict):
            for name, table_obj in dataset.items():
                stage_config = self._get_stage_table_config(
                    config, table_obj, timeslice
                )
                dataset[name] = self._get_dataset_type(table_obj.stage, stage_config)

        elif isinstance(dataset, Table):
            stage_config = self._get_stage_table_config(config, dataset, timeslice)
            dataset = self._get_dataset_type(dataset.stage, stage_config)

        return dataset

    def _get_stage_table_config(self, config: dict, table: Table, timeslice: Timeslice):
        stage_config = config[table.stage.name]
        stage_config[self._TIMESLICE] = timeslice
        stage_config[self._TABLE] = table.name
        stage_config[self._TABLE_PROPERTIES] = table.table_properties
        stage_config[self._STAGE] = table.stage
        stage_config[self._DATABASE] = table.database
        stage_config[self._CONFIG_PATH] = config[self._CONFIG_PATH]

        return stage_config


factory = _DatasetFactory()
factory.register_dataset_type(IOType.READ, Read)
factory.register_dataset_type(IOType.DELTALAKE, DeltaLake)
factory.register_dataset_type(IOType.WRITE, Write)
