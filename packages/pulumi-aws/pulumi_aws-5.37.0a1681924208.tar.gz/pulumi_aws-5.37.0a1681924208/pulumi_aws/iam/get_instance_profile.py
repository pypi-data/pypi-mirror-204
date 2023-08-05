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
    'GetInstanceProfileResult',
    'AwaitableGetInstanceProfileResult',
    'get_instance_profile',
    'get_instance_profile_output',
]

@pulumi.output_type
class GetInstanceProfileResult:
    """
    A collection of values returned by getInstanceProfile.
    """
    def __init__(__self__, arn=None, create_date=None, id=None, name=None, path=None, role_arn=None, role_id=None, role_name=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if create_date and not isinstance(create_date, str):
            raise TypeError("Expected argument 'create_date' to be a str")
        pulumi.set(__self__, "create_date", create_date)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if path and not isinstance(path, str):
            raise TypeError("Expected argument 'path' to be a str")
        pulumi.set(__self__, "path", path)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)
        if role_id and not isinstance(role_id, str):
            raise TypeError("Expected argument 'role_id' to be a str")
        pulumi.set(__self__, "role_id", role_id)
        if role_name and not isinstance(role_name, str):
            raise TypeError("Expected argument 'role_name' to be a str")
        pulumi.set(__self__, "role_name", role_name)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createDate")
    def create_date(self) -> str:
        """
        String representation of the date the instance profile was created.
        """
        return pulumi.get(self, "create_date")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def path(self) -> str:
        """
        Path to the instance profile.
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> str:
        """
        Role ARN associated with this instance profile.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="roleId")
    def role_id(self) -> str:
        """
        Role ID associated with this instance profile.
        """
        return pulumi.get(self, "role_id")

    @property
    @pulumi.getter(name="roleName")
    def role_name(self) -> str:
        """
        Role name associated with this instance profile.
        """
        return pulumi.get(self, "role_name")


class AwaitableGetInstanceProfileResult(GetInstanceProfileResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInstanceProfileResult(
            arn=self.arn,
            create_date=self.create_date,
            id=self.id,
            name=self.name,
            path=self.path,
            role_arn=self.role_arn,
            role_id=self.role_id,
            role_name=self.role_name)


def get_instance_profile(name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInstanceProfileResult:
    """
    This data source can be used to fetch information about a specific
    IAM instance profile. By using this data source, you can reference IAM
    instance profile properties without having to hard code ARNs as input.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.iam.get_instance_profile(name="an_example_instance_profile_name")
    ```


    :param str name: Friendly IAM instance profile name to match.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:iam/getInstanceProfile:getInstanceProfile', __args__, opts=opts, typ=GetInstanceProfileResult).value

    return AwaitableGetInstanceProfileResult(
        arn=__ret__.arn,
        create_date=__ret__.create_date,
        id=__ret__.id,
        name=__ret__.name,
        path=__ret__.path,
        role_arn=__ret__.role_arn,
        role_id=__ret__.role_id,
        role_name=__ret__.role_name)


@_utilities.lift_output_func(get_instance_profile)
def get_instance_profile_output(name: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetInstanceProfileResult]:
    """
    This data source can be used to fetch information about a specific
    IAM instance profile. By using this data source, you can reference IAM
    instance profile properties without having to hard code ARNs as input.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.iam.get_instance_profile(name="an_example_instance_profile_name")
    ```


    :param str name: Friendly IAM instance profile name to match.
    """
    ...
