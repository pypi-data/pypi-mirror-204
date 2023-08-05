# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetQuickConnectResult',
    'AwaitableGetQuickConnectResult',
    'get_quick_connect',
    'get_quick_connect_output',
]

@pulumi.output_type
class GetQuickConnectResult:
    """
    A collection of values returned by getQuickConnect.
    """
    def __init__(__self__, arn=None, description=None, id=None, instance_id=None, name=None, quick_connect_configs=None, quick_connect_id=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance_id and not isinstance(instance_id, str):
            raise TypeError("Expected argument 'instance_id' to be a str")
        pulumi.set(__self__, "instance_id", instance_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if quick_connect_configs and not isinstance(quick_connect_configs, list):
            raise TypeError("Expected argument 'quick_connect_configs' to be a list")
        pulumi.set(__self__, "quick_connect_configs", quick_connect_configs)
        if quick_connect_id and not isinstance(quick_connect_id, str):
            raise TypeError("Expected argument 'quick_connect_id' to be a str")
        pulumi.set(__self__, "quick_connect_id", quick_connect_id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the Quick Connect.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the Quick Connect.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> str:
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="quickConnectConfigs")
    def quick_connect_configs(self) -> Sequence['outputs.GetQuickConnectQuickConnectConfigResult']:
        """
        A block that defines the configuration information for the Quick Connect: `quick_connect_type` and one of `phone_config`, `queue_config`, `user_config` . The Quick Connect Config block is documented below.
        """
        return pulumi.get(self, "quick_connect_configs")

    @property
    @pulumi.getter(name="quickConnectId")
    def quick_connect_id(self) -> str:
        """
        Identifier for the Quick Connect.
        """
        return pulumi.get(self, "quick_connect_id")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Map of tags to assign to the Quick Connect.
        """
        return pulumi.get(self, "tags")


class AwaitableGetQuickConnectResult(GetQuickConnectResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetQuickConnectResult(
            arn=self.arn,
            description=self.description,
            id=self.id,
            instance_id=self.instance_id,
            name=self.name,
            quick_connect_configs=self.quick_connect_configs,
            quick_connect_id=self.quick_connect_id,
            tags=self.tags)


def get_quick_connect(instance_id: Optional[str] = None,
                      name: Optional[str] = None,
                      quick_connect_id: Optional[str] = None,
                      tags: Optional[Mapping[str, str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetQuickConnectResult:
    """
    Provides details about a specific Amazon Connect Quick Connect.

    ## Example Usage

    By `name`

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.connect.get_quick_connect(instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111",
        name="Example")
    ```

    By `quick_connect_id`

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.connect.get_quick_connect(instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111",
        quick_connect_id="cccccccc-bbbb-cccc-dddd-111111111111")
    ```


    :param str instance_id: Reference to the hosting Amazon Connect Instance
    :param str name: Returns information on a specific Quick Connect by name
    :param str quick_connect_id: Returns information on a specific Quick Connect by Quick Connect id
    :param Mapping[str, str] tags: Map of tags to assign to the Quick Connect.
    """
    __args__ = dict()
    __args__['instanceId'] = instance_id
    __args__['name'] = name
    __args__['quickConnectId'] = quick_connect_id
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:connect/getQuickConnect:getQuickConnect', __args__, opts=opts, typ=GetQuickConnectResult).value

    return AwaitableGetQuickConnectResult(
        arn=__ret__.arn,
        description=__ret__.description,
        id=__ret__.id,
        instance_id=__ret__.instance_id,
        name=__ret__.name,
        quick_connect_configs=__ret__.quick_connect_configs,
        quick_connect_id=__ret__.quick_connect_id,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_quick_connect)
def get_quick_connect_output(instance_id: Optional[pulumi.Input[str]] = None,
                             name: Optional[pulumi.Input[Optional[str]]] = None,
                             quick_connect_id: Optional[pulumi.Input[Optional[str]]] = None,
                             tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetQuickConnectResult]:
    """
    Provides details about a specific Amazon Connect Quick Connect.

    ## Example Usage

    By `name`

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.connect.get_quick_connect(instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111",
        name="Example")
    ```

    By `quick_connect_id`

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.connect.get_quick_connect(instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111",
        quick_connect_id="cccccccc-bbbb-cccc-dddd-111111111111")
    ```


    :param str instance_id: Reference to the hosting Amazon Connect Instance
    :param str name: Returns information on a specific Quick Connect by name
    :param str quick_connect_id: Returns information on a specific Quick Connect by Quick Connect id
    :param Mapping[str, str] tags: Map of tags to assign to the Quick Connect.
    """
    ...
