from _qwak_proto.qwak.logging.log_filter_pb2 import LogText, SearchFilter
from _qwak_proto.qwak.logging.log_reader_service_pb2 import (
    ReadLogsRequest,
    ReadLogsResponse,
)
from _qwak_proto.qwak.logging.log_reader_service_pb2_grpc import LogReaderServiceStub
from _qwak_proto.qwak.logging.log_source_pb2 import (
    InferenceExecutionSource,
    LogSource,
    ModelRuntimeSource,
    RemoteBuildSource,
)
from grpc import RpcError
from qwak.exceptions import QwakException
from qwak.inner.di_configuration.account import UserAccountConfiguration
from qwak.inner.tool.grpc.grpc_tools import create_grpc_channel


class LoggingClient:
    """
    Used for interacting with Logging endpoint
    """

    def __init__(self, endpoint_url=None, enable_ssl=True):
        if endpoint_url is None:
            endpoint_url = UserAccountConfiguration().get_rpc_api()

        self._channel = create_grpc_channel(url=endpoint_url, enable_ssl=enable_ssl)

        self._logging_service = LogReaderServiceStub(self._channel)

    def read_build_logs(
        self,
        build_id=None,
        before_offset=None,
        after_offset=None,
        max_number_of_results=None,
        log_text_filter=None,
    ):
        try:
            response = self.read_logs(
                source=LogSource(remote_build=RemoteBuildSource(build_id=build_id)),
                before_offset=before_offset,
                after_offset=after_offset,
                log_text_filter=log_text_filter,
                max_number_of_results=max_number_of_results,
            )

            return response
        except QwakException as e:
            raise QwakException(f"Failed to fetch build logs, error is [{e}]")

    def read_model_runtime_logs(
        self,
        build_id=None,
        deployment_id=None,
        before_offset=None,
        after_offset=None,
        max_number_of_results=None,
        log_text_filter=None,
    ) -> ReadLogsResponse:
        try:
            response = self.read_logs(
                source=LogSource(
                    model_runtime=ModelRuntimeSource(
                        build_id=build_id, deployment_id=deployment_id
                    )
                ),
                before_offset=before_offset,
                after_offset=after_offset,
                log_text_filter=log_text_filter,
                max_number_of_results=max_number_of_results,
            )

            return response
        except QwakException as e:
            raise QwakException(f"Failed to fetch runtime logs, error is [{e}]")

    def read_execution_models_logs(
        self,
        execution_id,
        before_offset=None,
        after_offset=None,
        max_number_of_results=None,
        log_text_filter=None,
    ) -> ReadLogsResponse:
        try:
            response = self.read_logs(
                source=LogSource(
                    inference_execution=InferenceExecutionSource(
                        inference_job_id=execution_id
                    )
                ),
                before_offset=before_offset,
                after_offset=after_offset,
                log_text_filter=log_text_filter,
                max_number_of_results=max_number_of_results,
            )

            return response
        except QwakException as e:
            raise QwakException(f"Failed to fetch execution logs, error is [{e}]")

    def read_logs(
        self,
        source,
        before_offset,
        after_offset,
        max_number_of_results,
        log_text_filter,
    ):
        try:
            response = self._logging_service.ReadLogs(
                ReadLogsRequest(
                    source=source,
                    before_offset=before_offset,
                    after_offset=after_offset,
                    search_filter=SearchFilter(
                        log_text_filter=LogText(contains=log_text_filter)
                    ),
                    max_number_of_results=max_number_of_results,
                )
            )
            return response
        except RpcError as e:
            raise QwakException(
                f"Failed grpc read logs request, grpc error is "
                f"[{e.details() if e.details() else e.code()}]"
            )
