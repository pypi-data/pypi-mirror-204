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
    'GetResourceResult',
    'AwaitableGetResourceResult',
    'get_resource',
    'get_resource_output',
]

@pulumi.output_type
class GetResourceResult:
    """
    A collection of values returned by getResource.
    """
    def __init__(__self__, id=None, identifier=None, properties=None, role_arn=None, type_name=None, type_version_id=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identifier and not isinstance(identifier, str):
            raise TypeError("Expected argument 'identifier' to be a str")
        pulumi.set(__self__, "identifier", identifier)
        if properties and not isinstance(properties, str):
            raise TypeError("Expected argument 'properties' to be a str")
        pulumi.set(__self__, "properties", properties)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)
        if type_name and not isinstance(type_name, str):
            raise TypeError("Expected argument 'type_name' to be a str")
        pulumi.set(__self__, "type_name", type_name)
        if type_version_id and not isinstance(type_version_id, str):
            raise TypeError("Expected argument 'type_version_id' to be a str")
        pulumi.set(__self__, "type_version_id", type_version_id)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identifier(self) -> str:
        return pulumi.get(self, "identifier")

    @property
    @pulumi.getter
    def properties(self) -> str:
        """
        JSON string matching the CloudFormation resource type schema with current configuration.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[str]:
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="typeName")
    def type_name(self) -> str:
        return pulumi.get(self, "type_name")

    @property
    @pulumi.getter(name="typeVersionId")
    def type_version_id(self) -> Optional[str]:
        return pulumi.get(self, "type_version_id")


class AwaitableGetResourceResult(GetResourceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetResourceResult(
            id=self.id,
            identifier=self.identifier,
            properties=self.properties,
            role_arn=self.role_arn,
            type_name=self.type_name,
            type_version_id=self.type_version_id)


def get_resource(identifier: Optional[str] = None,
                 role_arn: Optional[str] = None,
                 type_name: Optional[str] = None,
                 type_version_id: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetResourceResult:
    """
    Provides details for a Cloud Control API Resource. The reading of these resources is proxied through Cloud Control API handlers to the backend service.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.cloudcontrol.get_resource(identifier="example",
        type_name="AWS::ECS::Cluster")
    ```


    :param str identifier: Identifier of the CloudFormation resource type. For example, `vpc-12345678`.
    :param str role_arn: ARN of the IAM Role to assume for operations.
    :param str type_name: CloudFormation resource type name. For example, `AWS::EC2::VPC`.
    :param str type_version_id: Identifier of the CloudFormation resource type version.
    """
    __args__ = dict()
    __args__['identifier'] = identifier
    __args__['roleArn'] = role_arn
    __args__['typeName'] = type_name
    __args__['typeVersionId'] = type_version_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:cloudcontrol/getResource:getResource', __args__, opts=opts, typ=GetResourceResult).value

    return AwaitableGetResourceResult(
        id=__ret__.id,
        identifier=__ret__.identifier,
        properties=__ret__.properties,
        role_arn=__ret__.role_arn,
        type_name=__ret__.type_name,
        type_version_id=__ret__.type_version_id)


@_utilities.lift_output_func(get_resource)
def get_resource_output(identifier: Optional[pulumi.Input[str]] = None,
                        role_arn: Optional[pulumi.Input[Optional[str]]] = None,
                        type_name: Optional[pulumi.Input[str]] = None,
                        type_version_id: Optional[pulumi.Input[Optional[str]]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetResourceResult]:
    """
    Provides details for a Cloud Control API Resource. The reading of these resources is proxied through Cloud Control API handlers to the backend service.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.cloudcontrol.get_resource(identifier="example",
        type_name="AWS::ECS::Cluster")
    ```


    :param str identifier: Identifier of the CloudFormation resource type. For example, `vpc-12345678`.
    :param str role_arn: ARN of the IAM Role to assume for operations.
    :param str type_name: CloudFormation resource type name. For example, `AWS::EC2::VPC`.
    :param str type_version_id: Identifier of the CloudFormation resource type version.
    """
    ...
