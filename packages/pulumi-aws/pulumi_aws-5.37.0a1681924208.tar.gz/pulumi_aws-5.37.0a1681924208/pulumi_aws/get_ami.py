# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'GetAmiResult',
    'AwaitableGetAmiResult',
    'get_ami',
    'get_ami_output',
]

warnings.warn("""aws.getAmi has been deprecated in favor of aws.ec2.getAmi""", DeprecationWarning)

@pulumi.output_type
class GetAmiResult:
    """
    A collection of values returned by getAmi.
    """
    def __init__(__self__, architecture=None, arn=None, block_device_mappings=None, boot_mode=None, creation_date=None, deprecation_time=None, description=None, ena_support=None, executable_users=None, filters=None, hypervisor=None, id=None, image_id=None, image_location=None, image_owner_alias=None, image_type=None, imds_support=None, include_deprecated=None, kernel_id=None, most_recent=None, name=None, name_regex=None, owner_id=None, owners=None, platform=None, platform_details=None, product_codes=None, public=None, ramdisk_id=None, root_device_name=None, root_device_type=None, root_snapshot_id=None, sriov_net_support=None, state=None, state_reason=None, tags=None, tpm_support=None, usage_operation=None, virtualization_type=None):
        if architecture and not isinstance(architecture, str):
            raise TypeError("Expected argument 'architecture' to be a str")
        pulumi.set(__self__, "architecture", architecture)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if block_device_mappings and not isinstance(block_device_mappings, list):
            raise TypeError("Expected argument 'block_device_mappings' to be a list")
        pulumi.set(__self__, "block_device_mappings", block_device_mappings)
        if boot_mode and not isinstance(boot_mode, str):
            raise TypeError("Expected argument 'boot_mode' to be a str")
        pulumi.set(__self__, "boot_mode", boot_mode)
        if creation_date and not isinstance(creation_date, str):
            raise TypeError("Expected argument 'creation_date' to be a str")
        pulumi.set(__self__, "creation_date", creation_date)
        if deprecation_time and not isinstance(deprecation_time, str):
            raise TypeError("Expected argument 'deprecation_time' to be a str")
        pulumi.set(__self__, "deprecation_time", deprecation_time)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if ena_support and not isinstance(ena_support, bool):
            raise TypeError("Expected argument 'ena_support' to be a bool")
        pulumi.set(__self__, "ena_support", ena_support)
        if executable_users and not isinstance(executable_users, list):
            raise TypeError("Expected argument 'executable_users' to be a list")
        pulumi.set(__self__, "executable_users", executable_users)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if hypervisor and not isinstance(hypervisor, str):
            raise TypeError("Expected argument 'hypervisor' to be a str")
        pulumi.set(__self__, "hypervisor", hypervisor)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if image_id and not isinstance(image_id, str):
            raise TypeError("Expected argument 'image_id' to be a str")
        pulumi.set(__self__, "image_id", image_id)
        if image_location and not isinstance(image_location, str):
            raise TypeError("Expected argument 'image_location' to be a str")
        pulumi.set(__self__, "image_location", image_location)
        if image_owner_alias and not isinstance(image_owner_alias, str):
            raise TypeError("Expected argument 'image_owner_alias' to be a str")
        pulumi.set(__self__, "image_owner_alias", image_owner_alias)
        if image_type and not isinstance(image_type, str):
            raise TypeError("Expected argument 'image_type' to be a str")
        pulumi.set(__self__, "image_type", image_type)
        if imds_support and not isinstance(imds_support, str):
            raise TypeError("Expected argument 'imds_support' to be a str")
        pulumi.set(__self__, "imds_support", imds_support)
        if include_deprecated and not isinstance(include_deprecated, bool):
            raise TypeError("Expected argument 'include_deprecated' to be a bool")
        pulumi.set(__self__, "include_deprecated", include_deprecated)
        if kernel_id and not isinstance(kernel_id, str):
            raise TypeError("Expected argument 'kernel_id' to be a str")
        pulumi.set(__self__, "kernel_id", kernel_id)
        if most_recent and not isinstance(most_recent, bool):
            raise TypeError("Expected argument 'most_recent' to be a bool")
        pulumi.set(__self__, "most_recent", most_recent)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if owner_id and not isinstance(owner_id, str):
            raise TypeError("Expected argument 'owner_id' to be a str")
        pulumi.set(__self__, "owner_id", owner_id)
        if owners and not isinstance(owners, list):
            raise TypeError("Expected argument 'owners' to be a list")
        pulumi.set(__self__, "owners", owners)
        if platform and not isinstance(platform, str):
            raise TypeError("Expected argument 'platform' to be a str")
        pulumi.set(__self__, "platform", platform)
        if platform_details and not isinstance(platform_details, str):
            raise TypeError("Expected argument 'platform_details' to be a str")
        pulumi.set(__self__, "platform_details", platform_details)
        if product_codes and not isinstance(product_codes, list):
            raise TypeError("Expected argument 'product_codes' to be a list")
        pulumi.set(__self__, "product_codes", product_codes)
        if public and not isinstance(public, bool):
            raise TypeError("Expected argument 'public' to be a bool")
        pulumi.set(__self__, "public", public)
        if ramdisk_id and not isinstance(ramdisk_id, str):
            raise TypeError("Expected argument 'ramdisk_id' to be a str")
        pulumi.set(__self__, "ramdisk_id", ramdisk_id)
        if root_device_name and not isinstance(root_device_name, str):
            raise TypeError("Expected argument 'root_device_name' to be a str")
        pulumi.set(__self__, "root_device_name", root_device_name)
        if root_device_type and not isinstance(root_device_type, str):
            raise TypeError("Expected argument 'root_device_type' to be a str")
        pulumi.set(__self__, "root_device_type", root_device_type)
        if root_snapshot_id and not isinstance(root_snapshot_id, str):
            raise TypeError("Expected argument 'root_snapshot_id' to be a str")
        pulumi.set(__self__, "root_snapshot_id", root_snapshot_id)
        if sriov_net_support and not isinstance(sriov_net_support, str):
            raise TypeError("Expected argument 'sriov_net_support' to be a str")
        pulumi.set(__self__, "sriov_net_support", sriov_net_support)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if state_reason and not isinstance(state_reason, dict):
            raise TypeError("Expected argument 'state_reason' to be a dict")
        pulumi.set(__self__, "state_reason", state_reason)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if tpm_support and not isinstance(tpm_support, str):
            raise TypeError("Expected argument 'tpm_support' to be a str")
        pulumi.set(__self__, "tpm_support", tpm_support)
        if usage_operation and not isinstance(usage_operation, str):
            raise TypeError("Expected argument 'usage_operation' to be a str")
        pulumi.set(__self__, "usage_operation", usage_operation)
        if virtualization_type and not isinstance(virtualization_type, str):
            raise TypeError("Expected argument 'virtualization_type' to be a str")
        pulumi.set(__self__, "virtualization_type", virtualization_type)

    @property
    @pulumi.getter
    def architecture(self) -> str:
        """
        OS architecture of the AMI (ie: `i386` or `x86_64`).
        """
        return pulumi.get(self, "architecture")

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the AMI.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="blockDeviceMappings")
    def block_device_mappings(self) -> Sequence['outputs.GetAmiBlockDeviceMappingResult']:
        """
        Set of objects with block device mappings of the AMI.
        """
        return pulumi.get(self, "block_device_mappings")

    @property
    @pulumi.getter(name="bootMode")
    def boot_mode(self) -> str:
        """
        Boot mode of the image.
        """
        return pulumi.get(self, "boot_mode")

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> str:
        """
        Date and time the image was created.
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter(name="deprecationTime")
    def deprecation_time(self) -> str:
        """
        Date and time when the image will be deprecated.
        """
        return pulumi.get(self, "deprecation_time")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the AMI that was provided during image
        creation.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="enaSupport")
    def ena_support(self) -> bool:
        """
        Whether enhanced networking with ENA is enabled.
        """
        return pulumi.get(self, "ena_support")

    @property
    @pulumi.getter(name="executableUsers")
    def executable_users(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "executable_users")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetAmiFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def hypervisor(self) -> str:
        """
        Hypervisor type of the image.
        """
        return pulumi.get(self, "hypervisor")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="imageId")
    def image_id(self) -> str:
        """
        ID of the AMI. Should be the same as the resource `id`.
        """
        return pulumi.get(self, "image_id")

    @property
    @pulumi.getter(name="imageLocation")
    def image_location(self) -> str:
        """
        Location of the AMI.
        """
        return pulumi.get(self, "image_location")

    @property
    @pulumi.getter(name="imageOwnerAlias")
    def image_owner_alias(self) -> str:
        """
        AWS account alias (for example, `amazon`, `self`) or
        the AWS account ID of the AMI owner.
        """
        return pulumi.get(self, "image_owner_alias")

    @property
    @pulumi.getter(name="imageType")
    def image_type(self) -> str:
        """
        Type of image.
        """
        return pulumi.get(self, "image_type")

    @property
    @pulumi.getter(name="imdsSupport")
    def imds_support(self) -> str:
        """
        Instance Metadata Service (IMDS) support mode for the image. Set to `v2.0` if instances ran from this image enforce IMDSv2.
        """
        return pulumi.get(self, "imds_support")

    @property
    @pulumi.getter(name="includeDeprecated")
    def include_deprecated(self) -> Optional[bool]:
        return pulumi.get(self, "include_deprecated")

    @property
    @pulumi.getter(name="kernelId")
    def kernel_id(self) -> str:
        """
        Kernel associated with the image, if any. Only applicable
        for machine images.
        """
        return pulumi.get(self, "kernel_id")

    @property
    @pulumi.getter(name="mostRecent")
    def most_recent(self) -> Optional[bool]:
        return pulumi.get(self, "most_recent")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the AMI that was provided during image creation.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> str:
        """
        AWS account ID of the image owner.
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter
    def owners(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "owners")

    @property
    @pulumi.getter
    def platform(self) -> str:
        """
        Value is Windows for `Windows` AMIs; otherwise blank.
        """
        return pulumi.get(self, "platform")

    @property
    @pulumi.getter(name="platformDetails")
    def platform_details(self) -> str:
        """
        Platform details associated with the billing code of the AMI.
        """
        return pulumi.get(self, "platform_details")

    @property
    @pulumi.getter(name="productCodes")
    def product_codes(self) -> Sequence['outputs.GetAmiProductCodeResult']:
        """
        Any product codes associated with the AMI.
        * `product_codes.#.product_code_id` - The product code.
        * `product_codes.#.product_code_type` - The type of product code.
        """
        return pulumi.get(self, "product_codes")

    @property
    @pulumi.getter
    def public(self) -> bool:
        """
        `true` if the image has public launch permissions.
        """
        return pulumi.get(self, "public")

    @property
    @pulumi.getter(name="ramdiskId")
    def ramdisk_id(self) -> str:
        """
        RAM disk associated with the image, if any. Only applicable
        for machine images.
        """
        return pulumi.get(self, "ramdisk_id")

    @property
    @pulumi.getter(name="rootDeviceName")
    def root_device_name(self) -> str:
        """
        Device name of the root device.
        """
        return pulumi.get(self, "root_device_name")

    @property
    @pulumi.getter(name="rootDeviceType")
    def root_device_type(self) -> str:
        """
        Type of root device (ie: `ebs` or `instance-store`).
        """
        return pulumi.get(self, "root_device_type")

    @property
    @pulumi.getter(name="rootSnapshotId")
    def root_snapshot_id(self) -> str:
        """
        Snapshot id associated with the root device, if any
        (only applies to `ebs` root devices).
        """
        return pulumi.get(self, "root_snapshot_id")

    @property
    @pulumi.getter(name="sriovNetSupport")
    def sriov_net_support(self) -> str:
        """
        Whether enhanced networking is enabled.
        """
        return pulumi.get(self, "sriov_net_support")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        Current state of the AMI. If the state is `available`, the image
        is successfully registered and can be used to launch an instance.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="stateReason")
    def state_reason(self) -> Mapping[str, str]:
        """
        Describes a state change. Fields are `UNSET` if not available.
        * `state_reason.code` - The reason code for the state change.
        * `state_reason.message` - The message for the state change.
        """
        return pulumi.get(self, "state_reason")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Any tags assigned to the image.
        * `tags.#.key` - Key name of the tag.
        * `tags.#.value` - Value of the tag.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tpmSupport")
    def tpm_support(self) -> str:
        """
        If the image is configured for NitroTPM support, the value is `v2.0`.
        """
        return pulumi.get(self, "tpm_support")

    @property
    @pulumi.getter(name="usageOperation")
    def usage_operation(self) -> str:
        """
        Operation of the Amazon EC2 instance and the billing code that is associated with the AMI.
        """
        return pulumi.get(self, "usage_operation")

    @property
    @pulumi.getter(name="virtualizationType")
    def virtualization_type(self) -> str:
        """
        Type of virtualization of the AMI (ie: `hvm` or
        `paravirtual`).
        """
        return pulumi.get(self, "virtualization_type")


class AwaitableGetAmiResult(GetAmiResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAmiResult(
            architecture=self.architecture,
            arn=self.arn,
            block_device_mappings=self.block_device_mappings,
            boot_mode=self.boot_mode,
            creation_date=self.creation_date,
            deprecation_time=self.deprecation_time,
            description=self.description,
            ena_support=self.ena_support,
            executable_users=self.executable_users,
            filters=self.filters,
            hypervisor=self.hypervisor,
            id=self.id,
            image_id=self.image_id,
            image_location=self.image_location,
            image_owner_alias=self.image_owner_alias,
            image_type=self.image_type,
            imds_support=self.imds_support,
            include_deprecated=self.include_deprecated,
            kernel_id=self.kernel_id,
            most_recent=self.most_recent,
            name=self.name,
            name_regex=self.name_regex,
            owner_id=self.owner_id,
            owners=self.owners,
            platform=self.platform,
            platform_details=self.platform_details,
            product_codes=self.product_codes,
            public=self.public,
            ramdisk_id=self.ramdisk_id,
            root_device_name=self.root_device_name,
            root_device_type=self.root_device_type,
            root_snapshot_id=self.root_snapshot_id,
            sriov_net_support=self.sriov_net_support,
            state=self.state,
            state_reason=self.state_reason,
            tags=self.tags,
            tpm_support=self.tpm_support,
            usage_operation=self.usage_operation,
            virtualization_type=self.virtualization_type)


def get_ami(executable_users: Optional[Sequence[str]] = None,
            filters: Optional[Sequence[pulumi.InputType['GetAmiFilterArgs']]] = None,
            include_deprecated: Optional[bool] = None,
            most_recent: Optional[bool] = None,
            name_regex: Optional[str] = None,
            owners: Optional[Sequence[str]] = None,
            tags: Optional[Mapping[str, str]] = None,
            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAmiResult:
    """
    Use this data source to get the ID of a registered AMI for use in other
    resources.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2.get_ami(executable_users=["self"],
        filters=[
            aws.ec2.GetAmiFilterArgs(
                name="name",
                values=["myami-*"],
            ),
            aws.ec2.GetAmiFilterArgs(
                name="root-device-type",
                values=["ebs"],
            ),
            aws.ec2.GetAmiFilterArgs(
                name="virtualization-type",
                values=["hvm"],
            ),
        ],
        most_recent=True,
        name_regex="^myami-\\\\d{3}",
        owners=["self"])
    ```


    :param Sequence[str] executable_users: Limit search to users with *explicit* launch permission on
           the image. Valid items are the numeric account ID or `self`.
    :param Sequence[pulumi.InputType['GetAmiFilterArgs']] filters: One or more name/value pairs to filter off of. There are
           several valid keys, for a full reference, check out
           [describe-images in the AWS CLI reference][1].
    :param bool include_deprecated: If true, all deprecated AMIs are included in the response. If false, no deprecated AMIs are included in the response. If no value is specified, the default value is false.
    :param bool most_recent: If more than one result is returned, use the most
           recent AMI.
    :param str name_regex: Regex string to apply to the AMI list returned
           by AWS. This allows more advanced filtering not supported from the AWS API. This
           filtering is done locally on what AWS returns, and could have a performance
           impact if the result is large. Combine this with other
           options to narrow down the list AWS returns.
    :param Sequence[str] owners: List of AMI owners to limit search. Valid values: an AWS account ID, `self` (the current account), or an AWS owner alias (e.g., `amazon`, `aws-marketplace`, `microsoft`).
    :param Mapping[str, str] tags: Any tags assigned to the image.
           * `tags.#.key` - Key name of the tag.
           * `tags.#.value` - Value of the tag.
    """
    pulumi.log.warn("""get_ami is deprecated: aws.getAmi has been deprecated in favor of aws.ec2.getAmi""")
    __args__ = dict()
    __args__['executableUsers'] = executable_users
    __args__['filters'] = filters
    __args__['includeDeprecated'] = include_deprecated
    __args__['mostRecent'] = most_recent
    __args__['nameRegex'] = name_regex
    __args__['owners'] = owners
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:index/getAmi:getAmi', __args__, opts=opts, typ=GetAmiResult).value

    return AwaitableGetAmiResult(
        architecture=__ret__.architecture,
        arn=__ret__.arn,
        block_device_mappings=__ret__.block_device_mappings,
        boot_mode=__ret__.boot_mode,
        creation_date=__ret__.creation_date,
        deprecation_time=__ret__.deprecation_time,
        description=__ret__.description,
        ena_support=__ret__.ena_support,
        executable_users=__ret__.executable_users,
        filters=__ret__.filters,
        hypervisor=__ret__.hypervisor,
        id=__ret__.id,
        image_id=__ret__.image_id,
        image_location=__ret__.image_location,
        image_owner_alias=__ret__.image_owner_alias,
        image_type=__ret__.image_type,
        imds_support=__ret__.imds_support,
        include_deprecated=__ret__.include_deprecated,
        kernel_id=__ret__.kernel_id,
        most_recent=__ret__.most_recent,
        name=__ret__.name,
        name_regex=__ret__.name_regex,
        owner_id=__ret__.owner_id,
        owners=__ret__.owners,
        platform=__ret__.platform,
        platform_details=__ret__.platform_details,
        product_codes=__ret__.product_codes,
        public=__ret__.public,
        ramdisk_id=__ret__.ramdisk_id,
        root_device_name=__ret__.root_device_name,
        root_device_type=__ret__.root_device_type,
        root_snapshot_id=__ret__.root_snapshot_id,
        sriov_net_support=__ret__.sriov_net_support,
        state=__ret__.state,
        state_reason=__ret__.state_reason,
        tags=__ret__.tags,
        tpm_support=__ret__.tpm_support,
        usage_operation=__ret__.usage_operation,
        virtualization_type=__ret__.virtualization_type)


@_utilities.lift_output_func(get_ami)
def get_ami_output(executable_users: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                   filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetAmiFilterArgs']]]]] = None,
                   include_deprecated: Optional[pulumi.Input[Optional[bool]]] = None,
                   most_recent: Optional[pulumi.Input[Optional[bool]]] = None,
                   name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                   owners: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                   tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAmiResult]:
    """
    Use this data source to get the ID of a registered AMI for use in other
    resources.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2.get_ami(executable_users=["self"],
        filters=[
            aws.ec2.GetAmiFilterArgs(
                name="name",
                values=["myami-*"],
            ),
            aws.ec2.GetAmiFilterArgs(
                name="root-device-type",
                values=["ebs"],
            ),
            aws.ec2.GetAmiFilterArgs(
                name="virtualization-type",
                values=["hvm"],
            ),
        ],
        most_recent=True,
        name_regex="^myami-\\\\d{3}",
        owners=["self"])
    ```


    :param Sequence[str] executable_users: Limit search to users with *explicit* launch permission on
           the image. Valid items are the numeric account ID or `self`.
    :param Sequence[pulumi.InputType['GetAmiFilterArgs']] filters: One or more name/value pairs to filter off of. There are
           several valid keys, for a full reference, check out
           [describe-images in the AWS CLI reference][1].
    :param bool include_deprecated: If true, all deprecated AMIs are included in the response. If false, no deprecated AMIs are included in the response. If no value is specified, the default value is false.
    :param bool most_recent: If more than one result is returned, use the most
           recent AMI.
    :param str name_regex: Regex string to apply to the AMI list returned
           by AWS. This allows more advanced filtering not supported from the AWS API. This
           filtering is done locally on what AWS returns, and could have a performance
           impact if the result is large. Combine this with other
           options to narrow down the list AWS returns.
    :param Sequence[str] owners: List of AMI owners to limit search. Valid values: an AWS account ID, `self` (the current account), or an AWS owner alias (e.g., `amazon`, `aws-marketplace`, `microsoft`).
    :param Mapping[str, str] tags: Any tags assigned to the image.
           * `tags.#.key` - Key name of the tag.
           * `tags.#.value` - Value of the tag.
    """
    pulumi.log.warn("""get_ami is deprecated: aws.getAmi has been deprecated in favor of aws.ec2.getAmi""")
    ...
