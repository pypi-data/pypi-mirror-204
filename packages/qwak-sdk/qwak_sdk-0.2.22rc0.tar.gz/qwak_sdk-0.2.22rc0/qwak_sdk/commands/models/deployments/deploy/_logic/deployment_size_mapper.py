from __future__ import annotations

from _qwak_proto.qwak.deployment.deployment_pb2 import DeploymentSize, MemoryUnit
from _qwak_proto.qwak.user_application.common.v0.resources_pb2 import GpuResources

from qwak_sdk.commands.models.deployments.deploy._logic.deploy_config import (
    DeployConfig,
)


def deployment_size_from_deploy_config(deploy_config: DeployConfig) -> DeploymentSize:
    return DeploymentSize(
        number_of_pods=deploy_config.resources.pods,
        cpu=deploy_config.resources.cpus,
        memory_amount=deploy_config.resources.memory,
        memory_units=MemoryUnit.MIB,
        gpu_resources=GpuResources(
            gpu_type=deploy_config.resources.gpu_type,
            gpu_amount=deploy_config.resources.gpu_amount,
        ),
    )
