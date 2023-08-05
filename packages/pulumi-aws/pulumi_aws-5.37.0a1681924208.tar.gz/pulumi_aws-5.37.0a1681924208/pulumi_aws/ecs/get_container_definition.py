# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetContainerDefinitionResult',
    'AwaitableGetContainerDefinitionResult',
    'get_container_definition',
    'get_container_definition_output',
]

@pulumi.output_type
class GetContainerDefinitionResult:
    """
    A collection of values returned by getContainerDefinition.
    """
    def __init__(__self__, container_name=None, cpu=None, disable_networking=None, docker_labels=None, environment=None, id=None, image=None, image_digest=None, memory=None, memory_reservation=None, task_definition=None):
        if container_name and not isinstance(container_name, str):
            raise TypeError("Expected argument 'container_name' to be a str")
        pulumi.set(__self__, "container_name", container_name)
        if cpu and not isinstance(cpu, int):
            raise TypeError("Expected argument 'cpu' to be a int")
        pulumi.set(__self__, "cpu", cpu)
        if disable_networking and not isinstance(disable_networking, bool):
            raise TypeError("Expected argument 'disable_networking' to be a bool")
        pulumi.set(__self__, "disable_networking", disable_networking)
        if docker_labels and not isinstance(docker_labels, dict):
            raise TypeError("Expected argument 'docker_labels' to be a dict")
        pulumi.set(__self__, "docker_labels", docker_labels)
        if environment and not isinstance(environment, dict):
            raise TypeError("Expected argument 'environment' to be a dict")
        pulumi.set(__self__, "environment", environment)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if image and not isinstance(image, str):
            raise TypeError("Expected argument 'image' to be a str")
        pulumi.set(__self__, "image", image)
        if image_digest and not isinstance(image_digest, str):
            raise TypeError("Expected argument 'image_digest' to be a str")
        pulumi.set(__self__, "image_digest", image_digest)
        if memory and not isinstance(memory, int):
            raise TypeError("Expected argument 'memory' to be a int")
        pulumi.set(__self__, "memory", memory)
        if memory_reservation and not isinstance(memory_reservation, int):
            raise TypeError("Expected argument 'memory_reservation' to be a int")
        pulumi.set(__self__, "memory_reservation", memory_reservation)
        if task_definition and not isinstance(task_definition, str):
            raise TypeError("Expected argument 'task_definition' to be a str")
        pulumi.set(__self__, "task_definition", task_definition)

    @property
    @pulumi.getter(name="containerName")
    def container_name(self) -> str:
        return pulumi.get(self, "container_name")

    @property
    @pulumi.getter
    def cpu(self) -> int:
        """
        CPU limit for this container definition
        """
        return pulumi.get(self, "cpu")

    @property
    @pulumi.getter(name="disableNetworking")
    def disable_networking(self) -> bool:
        """
        Indicator if networking is disabled
        """
        return pulumi.get(self, "disable_networking")

    @property
    @pulumi.getter(name="dockerLabels")
    def docker_labels(self) -> Mapping[str, str]:
        """
        Set docker labels
        """
        return pulumi.get(self, "docker_labels")

    @property
    @pulumi.getter
    def environment(self) -> Mapping[str, str]:
        """
        Environment in use
        """
        return pulumi.get(self, "environment")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def image(self) -> str:
        """
        Docker image in use, including the digest
        """
        return pulumi.get(self, "image")

    @property
    @pulumi.getter(name="imageDigest")
    def image_digest(self) -> str:
        """
        Digest of the docker image in use
        """
        return pulumi.get(self, "image_digest")

    @property
    @pulumi.getter
    def memory(self) -> int:
        """
        Memory limit for this container definition
        """
        return pulumi.get(self, "memory")

    @property
    @pulumi.getter(name="memoryReservation")
    def memory_reservation(self) -> int:
        """
        Soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory to this soft limit
        """
        return pulumi.get(self, "memory_reservation")

    @property
    @pulumi.getter(name="taskDefinition")
    def task_definition(self) -> str:
        return pulumi.get(self, "task_definition")


class AwaitableGetContainerDefinitionResult(GetContainerDefinitionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetContainerDefinitionResult(
            container_name=self.container_name,
            cpu=self.cpu,
            disable_networking=self.disable_networking,
            docker_labels=self.docker_labels,
            environment=self.environment,
            id=self.id,
            image=self.image,
            image_digest=self.image_digest,
            memory=self.memory,
            memory_reservation=self.memory_reservation,
            task_definition=self.task_definition)


def get_container_definition(container_name: Optional[str] = None,
                             task_definition: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetContainerDefinitionResult:
    """
    The ECS container definition data source allows access to details of
    a specific container within an AWS ECS service.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    ecs_mongo = aws.ecs.get_container_definition(task_definition=aws_ecs_task_definition["mongo"]["id"],
        container_name="mongodb")
    ```


    :param str container_name: Name of the container definition
    :param str task_definition: ARN of the task definition which contains the container
    """
    __args__ = dict()
    __args__['containerName'] = container_name
    __args__['taskDefinition'] = task_definition
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ecs/getContainerDefinition:getContainerDefinition', __args__, opts=opts, typ=GetContainerDefinitionResult).value

    return AwaitableGetContainerDefinitionResult(
        container_name=__ret__.container_name,
        cpu=__ret__.cpu,
        disable_networking=__ret__.disable_networking,
        docker_labels=__ret__.docker_labels,
        environment=__ret__.environment,
        id=__ret__.id,
        image=__ret__.image,
        image_digest=__ret__.image_digest,
        memory=__ret__.memory,
        memory_reservation=__ret__.memory_reservation,
        task_definition=__ret__.task_definition)


@_utilities.lift_output_func(get_container_definition)
def get_container_definition_output(container_name: Optional[pulumi.Input[str]] = None,
                                    task_definition: Optional[pulumi.Input[str]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetContainerDefinitionResult]:
    """
    The ECS container definition data source allows access to details of
    a specific container within an AWS ECS service.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    ecs_mongo = aws.ecs.get_container_definition(task_definition=aws_ecs_task_definition["mongo"]["id"],
        container_name="mongodb")
    ```


    :param str container_name: Name of the container definition
    :param str task_definition: ARN of the task definition which contains the container
    """
    ...
