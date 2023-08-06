from dataclasses import dataclass
from typing import Optional

from _qwak_proto.qwak.feature_store.sources.batch_pb2 import (
    BatchSource as ProtoBatchSource,
)
from _qwak_proto.qwak.feature_store.sources.batch_pb2 import (
    ParquetSource as ProtoParquetSource,
)
from _qwak_proto.qwak.feature_store.sources.data_source_pb2 import (
    DataSourceSpec as ProtoDataSourceSpec,
)
from qwak.feature_store.data_sources.batch_sources._batch import BaseBatchSource
from qwak.feature_store.data_sources.batch_sources.filesystem_config import (
    FileSystemConfiguration,
    _filesystem_configuration_data_source_from_proto,
    _filesystem_configuration_data_source_to_proto,
)


@dataclass
class ParquetSource(BaseBatchSource):
    path: str
    filesystem_configuration: Optional[FileSystemConfiguration] = None

    @classmethod
    def _from_proto(cls, proto):
        parquet: ProtoParquetSource = proto.parquetSource
        fs_conf = _filesystem_configuration_data_source_from_proto(
            parquet.filesystem_configuration
        )

        return cls(
            name=proto.name,
            date_created_column=proto.date_created_column,
            description=proto.description,
            path=parquet.path,
            **fs_conf,
        )

    def _to_proto(self):
        fs_conf = _filesystem_configuration_data_source_to_proto(
            self.filesystem_configuration
        )

        return ProtoDataSourceSpec(
            batch_source=ProtoBatchSource(
                name=self.name,
                description=self.description,
                date_created_column=self.date_created_column,
                parquetSource=ProtoParquetSource(path=self.path, **fs_conf),
            )
        )
