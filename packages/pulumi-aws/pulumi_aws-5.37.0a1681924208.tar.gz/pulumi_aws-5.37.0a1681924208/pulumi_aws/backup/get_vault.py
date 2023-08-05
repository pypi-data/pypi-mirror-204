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
    'GetVaultResult',
    'AwaitableGetVaultResult',
    'get_vault',
    'get_vault_output',
]

@pulumi.output_type
class GetVaultResult:
    """
    A collection of values returned by getVault.
    """
    def __init__(__self__, arn=None, id=None, kms_key_arn=None, name=None, recovery_points=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kms_key_arn and not isinstance(kms_key_arn, str):
            raise TypeError("Expected argument 'kms_key_arn' to be a str")
        pulumi.set(__self__, "kms_key_arn", kms_key_arn)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if recovery_points and not isinstance(recovery_points, int):
            raise TypeError("Expected argument 'recovery_points' to be a int")
        pulumi.set(__self__, "recovery_points", recovery_points)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the vault.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="kmsKeyArn")
    def kms_key_arn(self) -> str:
        """
        Server-side encryption key that is used to protect your backups.
        """
        return pulumi.get(self, "kms_key_arn")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="recoveryPoints")
    def recovery_points(self) -> int:
        """
        Number of recovery points that are stored in a backup vault.
        """
        return pulumi.get(self, "recovery_points")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Metadata that you can assign to help organize the resources that you create.
        """
        return pulumi.get(self, "tags")


class AwaitableGetVaultResult(GetVaultResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVaultResult(
            arn=self.arn,
            id=self.id,
            kms_key_arn=self.kms_key_arn,
            name=self.name,
            recovery_points=self.recovery_points,
            tags=self.tags)


def get_vault(name: Optional[str] = None,
              tags: Optional[Mapping[str, str]] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVaultResult:
    """
    Use this data source to get information on an existing backup vault.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.backup.get_vault(name="example_backup_vault")
    ```


    :param str name: Name of the backup vault.
    :param Mapping[str, str] tags: Metadata that you can assign to help organize the resources that you create.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:backup/getVault:getVault', __args__, opts=opts, typ=GetVaultResult).value

    return AwaitableGetVaultResult(
        arn=__ret__.arn,
        id=__ret__.id,
        kms_key_arn=__ret__.kms_key_arn,
        name=__ret__.name,
        recovery_points=__ret__.recovery_points,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_vault)
def get_vault_output(name: Optional[pulumi.Input[str]] = None,
                     tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVaultResult]:
    """
    Use this data source to get information on an existing backup vault.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.backup.get_vault(name="example_backup_vault")
    ```


    :param str name: Name of the backup vault.
    :param Mapping[str, str] tags: Metadata that you can assign to help organize the resources that you create.
    """
    ...
