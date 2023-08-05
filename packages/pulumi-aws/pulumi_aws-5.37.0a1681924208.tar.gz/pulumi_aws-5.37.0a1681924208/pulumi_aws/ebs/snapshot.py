# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SnapshotArgs', 'Snapshot']

@pulumi.input_type
class SnapshotArgs:
    def __init__(__self__, *,
                 volume_id: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 outpost_arn: Optional[pulumi.Input[str]] = None,
                 permanent_restore: Optional[pulumi.Input[bool]] = None,
                 storage_tier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 temporary_restore_days: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a Snapshot resource.
        :param pulumi.Input[str] volume_id: The Volume ID of which to make a snapshot.
        :param pulumi.Input[str] description: A description of what the snapshot is.
        :param pulumi.Input[str] outpost_arn: The Amazon Resource Name (ARN) of the Outpost on which to create a local snapshot.
        :param pulumi.Input[bool] permanent_restore: Indicates whether to permanently restore an archived snapshot.
        :param pulumi.Input[str] storage_tier: The name of the storage tier. Valid values are `archive` and `standard`. Default value is `standard`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the snapshot. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[int] temporary_restore_days: Specifies the number of days for which to temporarily restore an archived snapshot. Required for temporary restores only. The snapshot will be automatically re-archived after this period.
        """
        pulumi.set(__self__, "volume_id", volume_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if outpost_arn is not None:
            pulumi.set(__self__, "outpost_arn", outpost_arn)
        if permanent_restore is not None:
            pulumi.set(__self__, "permanent_restore", permanent_restore)
        if storage_tier is not None:
            pulumi.set(__self__, "storage_tier", storage_tier)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if temporary_restore_days is not None:
            pulumi.set(__self__, "temporary_restore_days", temporary_restore_days)

    @property
    @pulumi.getter(name="volumeId")
    def volume_id(self) -> pulumi.Input[str]:
        """
        The Volume ID of which to make a snapshot.
        """
        return pulumi.get(self, "volume_id")

    @volume_id.setter
    def volume_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "volume_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of what the snapshot is.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="outpostArn")
    def outpost_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the Outpost on which to create a local snapshot.
        """
        return pulumi.get(self, "outpost_arn")

    @outpost_arn.setter
    def outpost_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "outpost_arn", value)

    @property
    @pulumi.getter(name="permanentRestore")
    def permanent_restore(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether to permanently restore an archived snapshot.
        """
        return pulumi.get(self, "permanent_restore")

    @permanent_restore.setter
    def permanent_restore(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "permanent_restore", value)

    @property
    @pulumi.getter(name="storageTier")
    def storage_tier(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the storage tier. Valid values are `archive` and `standard`. Default value is `standard`.
        """
        return pulumi.get(self, "storage_tier")

    @storage_tier.setter
    def storage_tier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_tier", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the snapshot. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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
    @pulumi.getter(name="temporaryRestoreDays")
    def temporary_restore_days(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the number of days for which to temporarily restore an archived snapshot. Required for temporary restores only. The snapshot will be automatically re-archived after this period.
        """
        return pulumi.get(self, "temporary_restore_days")

    @temporary_restore_days.setter
    def temporary_restore_days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "temporary_restore_days", value)


@pulumi.input_type
class _SnapshotState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 data_encryption_key_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 encrypted: Optional[pulumi.Input[bool]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 outpost_arn: Optional[pulumi.Input[str]] = None,
                 owner_alias: Optional[pulumi.Input[str]] = None,
                 owner_id: Optional[pulumi.Input[str]] = None,
                 permanent_restore: Optional[pulumi.Input[bool]] = None,
                 storage_tier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 temporary_restore_days: Optional[pulumi.Input[int]] = None,
                 volume_id: Optional[pulumi.Input[str]] = None,
                 volume_size: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering Snapshot resources.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the EBS Snapshot.
        :param pulumi.Input[str] data_encryption_key_id: The data encryption key identifier for the snapshot.
        :param pulumi.Input[str] description: A description of what the snapshot is.
        :param pulumi.Input[bool] encrypted: Whether the snapshot is encrypted.
        :param pulumi.Input[str] kms_key_id: The ARN for the KMS encryption key.
        :param pulumi.Input[str] outpost_arn: The Amazon Resource Name (ARN) of the Outpost on which to create a local snapshot.
        :param pulumi.Input[str] owner_alias: Value from an Amazon-maintained list (`amazon`, `aws-marketplace`, `microsoft`) of snapshot owners.
        :param pulumi.Input[str] owner_id: The AWS account ID of the EBS snapshot owner.
        :param pulumi.Input[bool] permanent_restore: Indicates whether to permanently restore an archived snapshot.
        :param pulumi.Input[str] storage_tier: The name of the storage tier. Valid values are `archive` and `standard`. Default value is `standard`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the snapshot. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[int] temporary_restore_days: Specifies the number of days for which to temporarily restore an archived snapshot. Required for temporary restores only. The snapshot will be automatically re-archived after this period.
        :param pulumi.Input[str] volume_id: The Volume ID of which to make a snapshot.
        :param pulumi.Input[int] volume_size: The size of the drive in GiBs.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if data_encryption_key_id is not None:
            pulumi.set(__self__, "data_encryption_key_id", data_encryption_key_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if encrypted is not None:
            pulumi.set(__self__, "encrypted", encrypted)
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)
        if outpost_arn is not None:
            pulumi.set(__self__, "outpost_arn", outpost_arn)
        if owner_alias is not None:
            pulumi.set(__self__, "owner_alias", owner_alias)
        if owner_id is not None:
            pulumi.set(__self__, "owner_id", owner_id)
        if permanent_restore is not None:
            pulumi.set(__self__, "permanent_restore", permanent_restore)
        if storage_tier is not None:
            pulumi.set(__self__, "storage_tier", storage_tier)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if temporary_restore_days is not None:
            pulumi.set(__self__, "temporary_restore_days", temporary_restore_days)
        if volume_id is not None:
            pulumi.set(__self__, "volume_id", volume_id)
        if volume_size is not None:
            pulumi.set(__self__, "volume_size", volume_size)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of the EBS Snapshot.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="dataEncryptionKeyId")
    def data_encryption_key_id(self) -> Optional[pulumi.Input[str]]:
        """
        The data encryption key identifier for the snapshot.
        """
        return pulumi.get(self, "data_encryption_key_id")

    @data_encryption_key_id.setter
    def data_encryption_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_encryption_key_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of what the snapshot is.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def encrypted(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the snapshot is encrypted.
        """
        return pulumi.get(self, "encrypted")

    @encrypted.setter
    def encrypted(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "encrypted", value)

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN for the KMS encryption key.
        """
        return pulumi.get(self, "kms_key_id")

    @kms_key_id.setter
    def kms_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_id", value)

    @property
    @pulumi.getter(name="outpostArn")
    def outpost_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the Outpost on which to create a local snapshot.
        """
        return pulumi.get(self, "outpost_arn")

    @outpost_arn.setter
    def outpost_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "outpost_arn", value)

    @property
    @pulumi.getter(name="ownerAlias")
    def owner_alias(self) -> Optional[pulumi.Input[str]]:
        """
        Value from an Amazon-maintained list (`amazon`, `aws-marketplace`, `microsoft`) of snapshot owners.
        """
        return pulumi.get(self, "owner_alias")

    @owner_alias.setter
    def owner_alias(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner_alias", value)

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> Optional[pulumi.Input[str]]:
        """
        The AWS account ID of the EBS snapshot owner.
        """
        return pulumi.get(self, "owner_id")

    @owner_id.setter
    def owner_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner_id", value)

    @property
    @pulumi.getter(name="permanentRestore")
    def permanent_restore(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether to permanently restore an archived snapshot.
        """
        return pulumi.get(self, "permanent_restore")

    @permanent_restore.setter
    def permanent_restore(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "permanent_restore", value)

    @property
    @pulumi.getter(name="storageTier")
    def storage_tier(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the storage tier. Valid values are `archive` and `standard`. Default value is `standard`.
        """
        return pulumi.get(self, "storage_tier")

    @storage_tier.setter
    def storage_tier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_tier", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the snapshot. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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
    @pulumi.getter(name="temporaryRestoreDays")
    def temporary_restore_days(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the number of days for which to temporarily restore an archived snapshot. Required for temporary restores only. The snapshot will be automatically re-archived after this period.
        """
        return pulumi.get(self, "temporary_restore_days")

    @temporary_restore_days.setter
    def temporary_restore_days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "temporary_restore_days", value)

    @property
    @pulumi.getter(name="volumeId")
    def volume_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Volume ID of which to make a snapshot.
        """
        return pulumi.get(self, "volume_id")

    @volume_id.setter
    def volume_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "volume_id", value)

    @property
    @pulumi.getter(name="volumeSize")
    def volume_size(self) -> Optional[pulumi.Input[int]]:
        """
        The size of the drive in GiBs.
        """
        return pulumi.get(self, "volume_size")

    @volume_size.setter
    def volume_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "volume_size", value)


class Snapshot(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 outpost_arn: Optional[pulumi.Input[str]] = None,
                 permanent_restore: Optional[pulumi.Input[bool]] = None,
                 storage_tier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 temporary_restore_days: Optional[pulumi.Input[int]] = None,
                 volume_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates a Snapshot of an EBS Volume.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ebs.Volume("example",
            availability_zone="us-west-2a",
            size=40,
            tags={
                "Name": "HelloWorld",
            })
        example_snapshot = aws.ebs.Snapshot("exampleSnapshot",
            volume_id=example.id,
            tags={
                "Name": "HelloWorld_snap",
            })
        ```

        ## Import

        EBS Snapshot can be imported using the `id`, e.g.,

        ```sh
         $ pulumi import aws:ebs/snapshot:Snapshot id snap-049df61146c4d7901
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A description of what the snapshot is.
        :param pulumi.Input[str] outpost_arn: The Amazon Resource Name (ARN) of the Outpost on which to create a local snapshot.
        :param pulumi.Input[bool] permanent_restore: Indicates whether to permanently restore an archived snapshot.
        :param pulumi.Input[str] storage_tier: The name of the storage tier. Valid values are `archive` and `standard`. Default value is `standard`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the snapshot. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[int] temporary_restore_days: Specifies the number of days for which to temporarily restore an archived snapshot. Required for temporary restores only. The snapshot will be automatically re-archived after this period.
        :param pulumi.Input[str] volume_id: The Volume ID of which to make a snapshot.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SnapshotArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a Snapshot of an EBS Volume.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ebs.Volume("example",
            availability_zone="us-west-2a",
            size=40,
            tags={
                "Name": "HelloWorld",
            })
        example_snapshot = aws.ebs.Snapshot("exampleSnapshot",
            volume_id=example.id,
            tags={
                "Name": "HelloWorld_snap",
            })
        ```

        ## Import

        EBS Snapshot can be imported using the `id`, e.g.,

        ```sh
         $ pulumi import aws:ebs/snapshot:Snapshot id snap-049df61146c4d7901
        ```

        :param str resource_name: The name of the resource.
        :param SnapshotArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SnapshotArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 outpost_arn: Optional[pulumi.Input[str]] = None,
                 permanent_restore: Optional[pulumi.Input[bool]] = None,
                 storage_tier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 temporary_restore_days: Optional[pulumi.Input[int]] = None,
                 volume_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SnapshotArgs.__new__(SnapshotArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["outpost_arn"] = outpost_arn
            __props__.__dict__["permanent_restore"] = permanent_restore
            __props__.__dict__["storage_tier"] = storage_tier
            __props__.__dict__["tags"] = tags
            __props__.__dict__["tags_all"] = tags_all
            __props__.__dict__["temporary_restore_days"] = temporary_restore_days
            if volume_id is None and not opts.urn:
                raise TypeError("Missing required property 'volume_id'")
            __props__.__dict__["volume_id"] = volume_id
            __props__.__dict__["arn"] = None
            __props__.__dict__["data_encryption_key_id"] = None
            __props__.__dict__["encrypted"] = None
            __props__.__dict__["kms_key_id"] = None
            __props__.__dict__["owner_alias"] = None
            __props__.__dict__["owner_id"] = None
            __props__.__dict__["volume_size"] = None
        super(Snapshot, __self__).__init__(
            'aws:ebs/snapshot:Snapshot',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            data_encryption_key_id: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            encrypted: Optional[pulumi.Input[bool]] = None,
            kms_key_id: Optional[pulumi.Input[str]] = None,
            outpost_arn: Optional[pulumi.Input[str]] = None,
            owner_alias: Optional[pulumi.Input[str]] = None,
            owner_id: Optional[pulumi.Input[str]] = None,
            permanent_restore: Optional[pulumi.Input[bool]] = None,
            storage_tier: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            temporary_restore_days: Optional[pulumi.Input[int]] = None,
            volume_id: Optional[pulumi.Input[str]] = None,
            volume_size: Optional[pulumi.Input[int]] = None) -> 'Snapshot':
        """
        Get an existing Snapshot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the EBS Snapshot.
        :param pulumi.Input[str] data_encryption_key_id: The data encryption key identifier for the snapshot.
        :param pulumi.Input[str] description: A description of what the snapshot is.
        :param pulumi.Input[bool] encrypted: Whether the snapshot is encrypted.
        :param pulumi.Input[str] kms_key_id: The ARN for the KMS encryption key.
        :param pulumi.Input[str] outpost_arn: The Amazon Resource Name (ARN) of the Outpost on which to create a local snapshot.
        :param pulumi.Input[str] owner_alias: Value from an Amazon-maintained list (`amazon`, `aws-marketplace`, `microsoft`) of snapshot owners.
        :param pulumi.Input[str] owner_id: The AWS account ID of the EBS snapshot owner.
        :param pulumi.Input[bool] permanent_restore: Indicates whether to permanently restore an archived snapshot.
        :param pulumi.Input[str] storage_tier: The name of the storage tier. Valid values are `archive` and `standard`. Default value is `standard`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the snapshot. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[int] temporary_restore_days: Specifies the number of days for which to temporarily restore an archived snapshot. Required for temporary restores only. The snapshot will be automatically re-archived after this period.
        :param pulumi.Input[str] volume_id: The Volume ID of which to make a snapshot.
        :param pulumi.Input[int] volume_size: The size of the drive in GiBs.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SnapshotState.__new__(_SnapshotState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["data_encryption_key_id"] = data_encryption_key_id
        __props__.__dict__["description"] = description
        __props__.__dict__["encrypted"] = encrypted
        __props__.__dict__["kms_key_id"] = kms_key_id
        __props__.__dict__["outpost_arn"] = outpost_arn
        __props__.__dict__["owner_alias"] = owner_alias
        __props__.__dict__["owner_id"] = owner_id
        __props__.__dict__["permanent_restore"] = permanent_restore
        __props__.__dict__["storage_tier"] = storage_tier
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["temporary_restore_days"] = temporary_restore_days
        __props__.__dict__["volume_id"] = volume_id
        __props__.__dict__["volume_size"] = volume_size
        return Snapshot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of the EBS Snapshot.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="dataEncryptionKeyId")
    def data_encryption_key_id(self) -> pulumi.Output[str]:
        """
        The data encryption key identifier for the snapshot.
        """
        return pulumi.get(self, "data_encryption_key_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description of what the snapshot is.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def encrypted(self) -> pulumi.Output[bool]:
        """
        Whether the snapshot is encrypted.
        """
        return pulumi.get(self, "encrypted")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> pulumi.Output[str]:
        """
        The ARN for the KMS encryption key.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="outpostArn")
    def outpost_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The Amazon Resource Name (ARN) of the Outpost on which to create a local snapshot.
        """
        return pulumi.get(self, "outpost_arn")

    @property
    @pulumi.getter(name="ownerAlias")
    def owner_alias(self) -> pulumi.Output[str]:
        """
        Value from an Amazon-maintained list (`amazon`, `aws-marketplace`, `microsoft`) of snapshot owners.
        """
        return pulumi.get(self, "owner_alias")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> pulumi.Output[str]:
        """
        The AWS account ID of the EBS snapshot owner.
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter(name="permanentRestore")
    def permanent_restore(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether to permanently restore an archived snapshot.
        """
        return pulumi.get(self, "permanent_restore")

    @property
    @pulumi.getter(name="storageTier")
    def storage_tier(self) -> pulumi.Output[str]:
        """
        The name of the storage tier. Valid values are `archive` and `standard`. Default value is `standard`.
        """
        return pulumi.get(self, "storage_tier")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the snapshot. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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
    @pulumi.getter(name="temporaryRestoreDays")
    def temporary_restore_days(self) -> pulumi.Output[Optional[int]]:
        """
        Specifies the number of days for which to temporarily restore an archived snapshot. Required for temporary restores only. The snapshot will be automatically re-archived after this period.
        """
        return pulumi.get(self, "temporary_restore_days")

    @property
    @pulumi.getter(name="volumeId")
    def volume_id(self) -> pulumi.Output[str]:
        """
        The Volume ID of which to make a snapshot.
        """
        return pulumi.get(self, "volume_id")

    @property
    @pulumi.getter(name="volumeSize")
    def volume_size(self) -> pulumi.Output[int]:
        """
        The size of the drive in GiBs.
        """
        return pulumi.get(self, "volume_size")

