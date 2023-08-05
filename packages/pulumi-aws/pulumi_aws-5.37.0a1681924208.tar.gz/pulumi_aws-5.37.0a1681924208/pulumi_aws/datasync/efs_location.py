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
from ._inputs import *

__all__ = ['EfsLocationArgs', 'EfsLocation']

@pulumi.input_type
class EfsLocationArgs:
    def __init__(__self__, *,
                 ec2_config: pulumi.Input['EfsLocationEc2ConfigArgs'],
                 efs_file_system_arn: pulumi.Input[str],
                 access_point_arn: Optional[pulumi.Input[str]] = None,
                 file_system_access_role_arn: Optional[pulumi.Input[str]] = None,
                 in_transit_encryption: Optional[pulumi.Input[str]] = None,
                 subdirectory: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a EfsLocation resource.
        :param pulumi.Input['EfsLocationEc2ConfigArgs'] ec2_config: Configuration block containing EC2 configurations for connecting to the EFS File System.
        :param pulumi.Input[str] efs_file_system_arn: Amazon Resource Name (ARN) of EFS File System.
        :param pulumi.Input[str] access_point_arn: Specifies the Amazon Resource Name (ARN) of the access point that DataSync uses to access the Amazon EFS file system.
        :param pulumi.Input[str] file_system_access_role_arn: Specifies an Identity and Access Management (IAM) role that DataSync assumes when mounting the Amazon EFS file system.
        :param pulumi.Input[str] in_transit_encryption: Specifies whether you want DataSync to use TLS encryption when transferring data to or from your Amazon EFS file system. Valid values are `NONE` and `TLS1_2`.
        :param pulumi.Input[str] subdirectory: Subdirectory to perform actions as source or destination. Default `/`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value pairs of resource tags to assign to the DataSync Location. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        pulumi.set(__self__, "ec2_config", ec2_config)
        pulumi.set(__self__, "efs_file_system_arn", efs_file_system_arn)
        if access_point_arn is not None:
            pulumi.set(__self__, "access_point_arn", access_point_arn)
        if file_system_access_role_arn is not None:
            pulumi.set(__self__, "file_system_access_role_arn", file_system_access_role_arn)
        if in_transit_encryption is not None:
            pulumi.set(__self__, "in_transit_encryption", in_transit_encryption)
        if subdirectory is not None:
            pulumi.set(__self__, "subdirectory", subdirectory)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter(name="ec2Config")
    def ec2_config(self) -> pulumi.Input['EfsLocationEc2ConfigArgs']:
        """
        Configuration block containing EC2 configurations for connecting to the EFS File System.
        """
        return pulumi.get(self, "ec2_config")

    @ec2_config.setter
    def ec2_config(self, value: pulumi.Input['EfsLocationEc2ConfigArgs']):
        pulumi.set(self, "ec2_config", value)

    @property
    @pulumi.getter(name="efsFileSystemArn")
    def efs_file_system_arn(self) -> pulumi.Input[str]:
        """
        Amazon Resource Name (ARN) of EFS File System.
        """
        return pulumi.get(self, "efs_file_system_arn")

    @efs_file_system_arn.setter
    def efs_file_system_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "efs_file_system_arn", value)

    @property
    @pulumi.getter(name="accessPointArn")
    def access_point_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the Amazon Resource Name (ARN) of the access point that DataSync uses to access the Amazon EFS file system.
        """
        return pulumi.get(self, "access_point_arn")

    @access_point_arn.setter
    def access_point_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_point_arn", value)

    @property
    @pulumi.getter(name="fileSystemAccessRoleArn")
    def file_system_access_role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies an Identity and Access Management (IAM) role that DataSync assumes when mounting the Amazon EFS file system.
        """
        return pulumi.get(self, "file_system_access_role_arn")

    @file_system_access_role_arn.setter
    def file_system_access_role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "file_system_access_role_arn", value)

    @property
    @pulumi.getter(name="inTransitEncryption")
    def in_transit_encryption(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether you want DataSync to use TLS encryption when transferring data to or from your Amazon EFS file system. Valid values are `NONE` and `TLS1_2`.
        """
        return pulumi.get(self, "in_transit_encryption")

    @in_transit_encryption.setter
    def in_transit_encryption(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "in_transit_encryption", value)

    @property
    @pulumi.getter
    def subdirectory(self) -> Optional[pulumi.Input[str]]:
        """
        Subdirectory to perform actions as source or destination. Default `/`.
        """
        return pulumi.get(self, "subdirectory")

    @subdirectory.setter
    def subdirectory(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subdirectory", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value pairs of resource tags to assign to the DataSync Location. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)


@pulumi.input_type
class _EfsLocationState:
    def __init__(__self__, *,
                 access_point_arn: Optional[pulumi.Input[str]] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 ec2_config: Optional[pulumi.Input['EfsLocationEc2ConfigArgs']] = None,
                 efs_file_system_arn: Optional[pulumi.Input[str]] = None,
                 file_system_access_role_arn: Optional[pulumi.Input[str]] = None,
                 in_transit_encryption: Optional[pulumi.Input[str]] = None,
                 subdirectory: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 uri: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering EfsLocation resources.
        :param pulumi.Input[str] access_point_arn: Specifies the Amazon Resource Name (ARN) of the access point that DataSync uses to access the Amazon EFS file system.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the DataSync Location.
        :param pulumi.Input['EfsLocationEc2ConfigArgs'] ec2_config: Configuration block containing EC2 configurations for connecting to the EFS File System.
        :param pulumi.Input[str] efs_file_system_arn: Amazon Resource Name (ARN) of EFS File System.
        :param pulumi.Input[str] file_system_access_role_arn: Specifies an Identity and Access Management (IAM) role that DataSync assumes when mounting the Amazon EFS file system.
        :param pulumi.Input[str] in_transit_encryption: Specifies whether you want DataSync to use TLS encryption when transferring data to or from your Amazon EFS file system. Valid values are `NONE` and `TLS1_2`.
        :param pulumi.Input[str] subdirectory: Subdirectory to perform actions as source or destination. Default `/`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value pairs of resource tags to assign to the DataSync Location. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if access_point_arn is not None:
            pulumi.set(__self__, "access_point_arn", access_point_arn)
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if ec2_config is not None:
            pulumi.set(__self__, "ec2_config", ec2_config)
        if efs_file_system_arn is not None:
            pulumi.set(__self__, "efs_file_system_arn", efs_file_system_arn)
        if file_system_access_role_arn is not None:
            pulumi.set(__self__, "file_system_access_role_arn", file_system_access_role_arn)
        if in_transit_encryption is not None:
            pulumi.set(__self__, "in_transit_encryption", in_transit_encryption)
        if subdirectory is not None:
            pulumi.set(__self__, "subdirectory", subdirectory)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if uri is not None:
            pulumi.set(__self__, "uri", uri)

    @property
    @pulumi.getter(name="accessPointArn")
    def access_point_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the Amazon Resource Name (ARN) of the access point that DataSync uses to access the Amazon EFS file system.
        """
        return pulumi.get(self, "access_point_arn")

    @access_point_arn.setter
    def access_point_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_point_arn", value)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of the DataSync Location.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="ec2Config")
    def ec2_config(self) -> Optional[pulumi.Input['EfsLocationEc2ConfigArgs']]:
        """
        Configuration block containing EC2 configurations for connecting to the EFS File System.
        """
        return pulumi.get(self, "ec2_config")

    @ec2_config.setter
    def ec2_config(self, value: Optional[pulumi.Input['EfsLocationEc2ConfigArgs']]):
        pulumi.set(self, "ec2_config", value)

    @property
    @pulumi.getter(name="efsFileSystemArn")
    def efs_file_system_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of EFS File System.
        """
        return pulumi.get(self, "efs_file_system_arn")

    @efs_file_system_arn.setter
    def efs_file_system_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "efs_file_system_arn", value)

    @property
    @pulumi.getter(name="fileSystemAccessRoleArn")
    def file_system_access_role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies an Identity and Access Management (IAM) role that DataSync assumes when mounting the Amazon EFS file system.
        """
        return pulumi.get(self, "file_system_access_role_arn")

    @file_system_access_role_arn.setter
    def file_system_access_role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "file_system_access_role_arn", value)

    @property
    @pulumi.getter(name="inTransitEncryption")
    def in_transit_encryption(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether you want DataSync to use TLS encryption when transferring data to or from your Amazon EFS file system. Valid values are `NONE` and `TLS1_2`.
        """
        return pulumi.get(self, "in_transit_encryption")

    @in_transit_encryption.setter
    def in_transit_encryption(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "in_transit_encryption", value)

    @property
    @pulumi.getter
    def subdirectory(self) -> Optional[pulumi.Input[str]]:
        """
        Subdirectory to perform actions as source or destination. Default `/`.
        """
        return pulumi.get(self, "subdirectory")

    @subdirectory.setter
    def subdirectory(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subdirectory", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value pairs of resource tags to assign to the DataSync Location. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter
    def uri(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "uri")

    @uri.setter
    def uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "uri", value)


class EfsLocation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_point_arn: Optional[pulumi.Input[str]] = None,
                 ec2_config: Optional[pulumi.Input[pulumi.InputType['EfsLocationEc2ConfigArgs']]] = None,
                 efs_file_system_arn: Optional[pulumi.Input[str]] = None,
                 file_system_access_role_arn: Optional[pulumi.Input[str]] = None,
                 in_transit_encryption: Optional[pulumi.Input[str]] = None,
                 subdirectory: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages an AWS DataSync EFS Location.

        > **NOTE:** The EFS File System must have a mounted EFS Mount Target before creating this resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.datasync.EfsLocation("example",
            efs_file_system_arn=aws_efs_mount_target["example"]["file_system_arn"],
            ec2_config=aws.datasync.EfsLocationEc2ConfigArgs(
                security_group_arns=[aws_security_group["example"]["arn"]],
                subnet_arn=aws_subnet["example"]["arn"],
            ))
        ```

        ## Import

        `aws_datasync_location_efs` can be imported by using the DataSync Task Amazon Resource Name (ARN), e.g.,

        ```sh
         $ pulumi import aws:datasync/efsLocation:EfsLocation example arn:aws:datasync:us-east-1:123456789012:location/loc-12345678901234567
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_point_arn: Specifies the Amazon Resource Name (ARN) of the access point that DataSync uses to access the Amazon EFS file system.
        :param pulumi.Input[pulumi.InputType['EfsLocationEc2ConfigArgs']] ec2_config: Configuration block containing EC2 configurations for connecting to the EFS File System.
        :param pulumi.Input[str] efs_file_system_arn: Amazon Resource Name (ARN) of EFS File System.
        :param pulumi.Input[str] file_system_access_role_arn: Specifies an Identity and Access Management (IAM) role that DataSync assumes when mounting the Amazon EFS file system.
        :param pulumi.Input[str] in_transit_encryption: Specifies whether you want DataSync to use TLS encryption when transferring data to or from your Amazon EFS file system. Valid values are `NONE` and `TLS1_2`.
        :param pulumi.Input[str] subdirectory: Subdirectory to perform actions as source or destination. Default `/`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value pairs of resource tags to assign to the DataSync Location. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EfsLocationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an AWS DataSync EFS Location.

        > **NOTE:** The EFS File System must have a mounted EFS Mount Target before creating this resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.datasync.EfsLocation("example",
            efs_file_system_arn=aws_efs_mount_target["example"]["file_system_arn"],
            ec2_config=aws.datasync.EfsLocationEc2ConfigArgs(
                security_group_arns=[aws_security_group["example"]["arn"]],
                subnet_arn=aws_subnet["example"]["arn"],
            ))
        ```

        ## Import

        `aws_datasync_location_efs` can be imported by using the DataSync Task Amazon Resource Name (ARN), e.g.,

        ```sh
         $ pulumi import aws:datasync/efsLocation:EfsLocation example arn:aws:datasync:us-east-1:123456789012:location/loc-12345678901234567
        ```

        :param str resource_name: The name of the resource.
        :param EfsLocationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EfsLocationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_point_arn: Optional[pulumi.Input[str]] = None,
                 ec2_config: Optional[pulumi.Input[pulumi.InputType['EfsLocationEc2ConfigArgs']]] = None,
                 efs_file_system_arn: Optional[pulumi.Input[str]] = None,
                 file_system_access_role_arn: Optional[pulumi.Input[str]] = None,
                 in_transit_encryption: Optional[pulumi.Input[str]] = None,
                 subdirectory: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EfsLocationArgs.__new__(EfsLocationArgs)

            __props__.__dict__["access_point_arn"] = access_point_arn
            if ec2_config is None and not opts.urn:
                raise TypeError("Missing required property 'ec2_config'")
            __props__.__dict__["ec2_config"] = ec2_config
            if efs_file_system_arn is None and not opts.urn:
                raise TypeError("Missing required property 'efs_file_system_arn'")
            __props__.__dict__["efs_file_system_arn"] = efs_file_system_arn
            __props__.__dict__["file_system_access_role_arn"] = file_system_access_role_arn
            __props__.__dict__["in_transit_encryption"] = in_transit_encryption
            __props__.__dict__["subdirectory"] = subdirectory
            __props__.__dict__["tags"] = tags
            __props__.__dict__["tags_all"] = tags_all
            __props__.__dict__["arn"] = None
            __props__.__dict__["uri"] = None
        super(EfsLocation, __self__).__init__(
            'aws:datasync/efsLocation:EfsLocation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            access_point_arn: Optional[pulumi.Input[str]] = None,
            arn: Optional[pulumi.Input[str]] = None,
            ec2_config: Optional[pulumi.Input[pulumi.InputType['EfsLocationEc2ConfigArgs']]] = None,
            efs_file_system_arn: Optional[pulumi.Input[str]] = None,
            file_system_access_role_arn: Optional[pulumi.Input[str]] = None,
            in_transit_encryption: Optional[pulumi.Input[str]] = None,
            subdirectory: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            uri: Optional[pulumi.Input[str]] = None) -> 'EfsLocation':
        """
        Get an existing EfsLocation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_point_arn: Specifies the Amazon Resource Name (ARN) of the access point that DataSync uses to access the Amazon EFS file system.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the DataSync Location.
        :param pulumi.Input[pulumi.InputType['EfsLocationEc2ConfigArgs']] ec2_config: Configuration block containing EC2 configurations for connecting to the EFS File System.
        :param pulumi.Input[str] efs_file_system_arn: Amazon Resource Name (ARN) of EFS File System.
        :param pulumi.Input[str] file_system_access_role_arn: Specifies an Identity and Access Management (IAM) role that DataSync assumes when mounting the Amazon EFS file system.
        :param pulumi.Input[str] in_transit_encryption: Specifies whether you want DataSync to use TLS encryption when transferring data to or from your Amazon EFS file system. Valid values are `NONE` and `TLS1_2`.
        :param pulumi.Input[str] subdirectory: Subdirectory to perform actions as source or destination. Default `/`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value pairs of resource tags to assign to the DataSync Location. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EfsLocationState.__new__(_EfsLocationState)

        __props__.__dict__["access_point_arn"] = access_point_arn
        __props__.__dict__["arn"] = arn
        __props__.__dict__["ec2_config"] = ec2_config
        __props__.__dict__["efs_file_system_arn"] = efs_file_system_arn
        __props__.__dict__["file_system_access_role_arn"] = file_system_access_role_arn
        __props__.__dict__["in_transit_encryption"] = in_transit_encryption
        __props__.__dict__["subdirectory"] = subdirectory
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["uri"] = uri
        return EfsLocation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessPointArn")
    def access_point_arn(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the Amazon Resource Name (ARN) of the access point that DataSync uses to access the Amazon EFS file system.
        """
        return pulumi.get(self, "access_point_arn")

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of the DataSync Location.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="ec2Config")
    def ec2_config(self) -> pulumi.Output['outputs.EfsLocationEc2Config']:
        """
        Configuration block containing EC2 configurations for connecting to the EFS File System.
        """
        return pulumi.get(self, "ec2_config")

    @property
    @pulumi.getter(name="efsFileSystemArn")
    def efs_file_system_arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of EFS File System.
        """
        return pulumi.get(self, "efs_file_system_arn")

    @property
    @pulumi.getter(name="fileSystemAccessRoleArn")
    def file_system_access_role_arn(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies an Identity and Access Management (IAM) role that DataSync assumes when mounting the Amazon EFS file system.
        """
        return pulumi.get(self, "file_system_access_role_arn")

    @property
    @pulumi.getter(name="inTransitEncryption")
    def in_transit_encryption(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies whether you want DataSync to use TLS encryption when transferring data to or from your Amazon EFS file system. Valid values are `NONE` and `TLS1_2`.
        """
        return pulumi.get(self, "in_transit_encryption")

    @property
    @pulumi.getter
    def subdirectory(self) -> pulumi.Output[Optional[str]]:
        """
        Subdirectory to perform actions as source or destination. Default `/`.
        """
        return pulumi.get(self, "subdirectory")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value pairs of resource tags to assign to the DataSync Location. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter
    def uri(self) -> pulumi.Output[str]:
        return pulumi.get(self, "uri")

