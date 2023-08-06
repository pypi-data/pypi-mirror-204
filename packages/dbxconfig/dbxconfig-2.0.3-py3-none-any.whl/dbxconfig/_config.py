import yaml
import os
from .dataset import DataSet
from ._timeslice import Timeslice
from ._tables import Tables, _INDEX_WILDCARD
from ._stage_type import StageType
from .dataset import dataset_factory
from ._utils import abs_config_path


class Config:
    _CONFIG_PATH = "./Config/"
    _ENCODING = "utf-8"
    _TABLES = "tables"
    _SOURCE_TABLE = "source_table"

    def __init__(self, pattern: str, config_path: str = None):
        self.config = self._load_config(pattern, config_path)
        self.tables = self._load_tables()

    def _load_config(self, pattern: str, config_path: str):
        config_path = self._get_config_path(config_path)
        config_file = f"{pattern}.yaml"

        config_file_path = os.path.join(config_path, config_file)

        with open(config_file_path, "r", encoding=self._ENCODING) as f:
            config = yaml.safe_load(f)

        # add the configuration path into the confif dictionart
        # so that it gets passed to table config when created
        config["config_path"] = config_path
        return config

    def _load_tables(self):
        tables_path = self.config["tables"]
        tables_path = abs_config_path(self.config["config_path"], self.config["tables"])

        with open(tables_path, "r", encoding=self._ENCODING) as f:
            self.config["tables"] = yaml.safe_load(f)

        tables = Tables(
            table_data=self.config["tables"], config_path=self.config["config_path"]
        )

        return tables

    def _get_config_path(self, config_path: str):
        if not config_path:
            config_path = self._CONFIG_PATH
        config_path = os.path.abspath(config_path)
        return config_path

    def get_table_mapping(
        self,
        timeslice: Timeslice,
        stage: StageType,
        table: str = _INDEX_WILDCARD,
        database: str = _INDEX_WILDCARD,
        index: str = None,
    ):
        table_mapping = self.tables.get_table_mapping(
            stage=stage, table=table, database=database, index=index
        )

        table_mapping.source = dataset_factory.get_data_set(
            self.config, table_mapping.source, timeslice
        )
        table_mapping.destination = dataset_factory.get_data_set(
            self.config, table_mapping.destination, timeslice
        )

        return table_mapping

    def set_checkpoint(
        self,
        source: DataSet,
        destination: DataSet,
        checkpoint_name: str = None,
    ):
        if not checkpoint_name:
            checkpoint_name = f"{source.database}.{source.table}-{destination.database}.{destination.table}"

        source.checkpoint = checkpoint_name
        source._render()
        destination.checkpoint = checkpoint_name
        destination.options["checkpointLocation"] = "{{ checkpoint }}"
        destination._render()
