from typing import Tuple

from qwak.clients.batch_job_management import BatchJobManagerClient
from qwak.clients.batch_job_management.executions_config import ExecutionConfig
from qwak.clients.batch_job_management.results import StartExecutionResult


def execute_start_execution(config: ExecutionConfig) -> Tuple[str, bool, str]:
    batch_job_start_response: StartExecutionResult = (
        BatchJobManagerClient().start_execution(config)
    )
    return (
        batch_job_start_response.execution_id,
        batch_job_start_response.success,
        batch_job_start_response.failure_message,
    )
