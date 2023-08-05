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

__all__ = [
    'GetLaunchTemplateResult',
    'AwaitableGetLaunchTemplateResult',
    'get_launch_template',
    'get_launch_template_output',
]

@pulumi.output_type
class GetLaunchTemplateResult:
    """
    A collection of values returned by getLaunchTemplate.
    """
    def __init__(__self__, arn=None, block_device_mappings=None, capacity_reservation_specifications=None, cpu_options=None, credit_specifications=None, default_version=None, description=None, disable_api_stop=None, disable_api_termination=None, ebs_optimized=None, elastic_gpu_specifications=None, elastic_inference_accelerators=None, enclave_options=None, filters=None, hibernation_options=None, iam_instance_profiles=None, id=None, image_id=None, instance_initiated_shutdown_behavior=None, instance_market_options=None, instance_requirements=None, instance_type=None, kernel_id=None, key_name=None, latest_version=None, license_specifications=None, maintenance_options=None, metadata_options=None, monitorings=None, name=None, network_interfaces=None, placements=None, private_dns_name_options=None, ram_disk_id=None, security_group_names=None, tag_specifications=None, tags=None, user_data=None, vpc_security_group_ids=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if block_device_mappings and not isinstance(block_device_mappings, list):
            raise TypeError("Expected argument 'block_device_mappings' to be a list")
        pulumi.set(__self__, "block_device_mappings", block_device_mappings)
        if capacity_reservation_specifications and not isinstance(capacity_reservation_specifications, list):
            raise TypeError("Expected argument 'capacity_reservation_specifications' to be a list")
        pulumi.set(__self__, "capacity_reservation_specifications", capacity_reservation_specifications)
        if cpu_options and not isinstance(cpu_options, list):
            raise TypeError("Expected argument 'cpu_options' to be a list")
        pulumi.set(__self__, "cpu_options", cpu_options)
        if credit_specifications and not isinstance(credit_specifications, list):
            raise TypeError("Expected argument 'credit_specifications' to be a list")
        pulumi.set(__self__, "credit_specifications", credit_specifications)
        if default_version and not isinstance(default_version, int):
            raise TypeError("Expected argument 'default_version' to be a int")
        pulumi.set(__self__, "default_version", default_version)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if disable_api_stop and not isinstance(disable_api_stop, bool):
            raise TypeError("Expected argument 'disable_api_stop' to be a bool")
        pulumi.set(__self__, "disable_api_stop", disable_api_stop)
        if disable_api_termination and not isinstance(disable_api_termination, bool):
            raise TypeError("Expected argument 'disable_api_termination' to be a bool")
        pulumi.set(__self__, "disable_api_termination", disable_api_termination)
        if ebs_optimized and not isinstance(ebs_optimized, str):
            raise TypeError("Expected argument 'ebs_optimized' to be a str")
        pulumi.set(__self__, "ebs_optimized", ebs_optimized)
        if elastic_gpu_specifications and not isinstance(elastic_gpu_specifications, list):
            raise TypeError("Expected argument 'elastic_gpu_specifications' to be a list")
        pulumi.set(__self__, "elastic_gpu_specifications", elastic_gpu_specifications)
        if elastic_inference_accelerators and not isinstance(elastic_inference_accelerators, list):
            raise TypeError("Expected argument 'elastic_inference_accelerators' to be a list")
        pulumi.set(__self__, "elastic_inference_accelerators", elastic_inference_accelerators)
        if enclave_options and not isinstance(enclave_options, list):
            raise TypeError("Expected argument 'enclave_options' to be a list")
        pulumi.set(__self__, "enclave_options", enclave_options)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if hibernation_options and not isinstance(hibernation_options, list):
            raise TypeError("Expected argument 'hibernation_options' to be a list")
        pulumi.set(__self__, "hibernation_options", hibernation_options)
        if iam_instance_profiles and not isinstance(iam_instance_profiles, list):
            raise TypeError("Expected argument 'iam_instance_profiles' to be a list")
        pulumi.set(__self__, "iam_instance_profiles", iam_instance_profiles)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if image_id and not isinstance(image_id, str):
            raise TypeError("Expected argument 'image_id' to be a str")
        pulumi.set(__self__, "image_id", image_id)
        if instance_initiated_shutdown_behavior and not isinstance(instance_initiated_shutdown_behavior, str):
            raise TypeError("Expected argument 'instance_initiated_shutdown_behavior' to be a str")
        pulumi.set(__self__, "instance_initiated_shutdown_behavior", instance_initiated_shutdown_behavior)
        if instance_market_options and not isinstance(instance_market_options, list):
            raise TypeError("Expected argument 'instance_market_options' to be a list")
        pulumi.set(__self__, "instance_market_options", instance_market_options)
        if instance_requirements and not isinstance(instance_requirements, list):
            raise TypeError("Expected argument 'instance_requirements' to be a list")
        pulumi.set(__self__, "instance_requirements", instance_requirements)
        if instance_type and not isinstance(instance_type, str):
            raise TypeError("Expected argument 'instance_type' to be a str")
        pulumi.set(__self__, "instance_type", instance_type)
        if kernel_id and not isinstance(kernel_id, str):
            raise TypeError("Expected argument 'kernel_id' to be a str")
        pulumi.set(__self__, "kernel_id", kernel_id)
        if key_name and not isinstance(key_name, str):
            raise TypeError("Expected argument 'key_name' to be a str")
        pulumi.set(__self__, "key_name", key_name)
        if latest_version and not isinstance(latest_version, int):
            raise TypeError("Expected argument 'latest_version' to be a int")
        pulumi.set(__self__, "latest_version", latest_version)
        if license_specifications and not isinstance(license_specifications, list):
            raise TypeError("Expected argument 'license_specifications' to be a list")
        pulumi.set(__self__, "license_specifications", license_specifications)
        if maintenance_options and not isinstance(maintenance_options, list):
            raise TypeError("Expected argument 'maintenance_options' to be a list")
        pulumi.set(__self__, "maintenance_options", maintenance_options)
        if metadata_options and not isinstance(metadata_options, list):
            raise TypeError("Expected argument 'metadata_options' to be a list")
        pulumi.set(__self__, "metadata_options", metadata_options)
        if monitorings and not isinstance(monitorings, list):
            raise TypeError("Expected argument 'monitorings' to be a list")
        pulumi.set(__self__, "monitorings", monitorings)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_interfaces and not isinstance(network_interfaces, list):
            raise TypeError("Expected argument 'network_interfaces' to be a list")
        pulumi.set(__self__, "network_interfaces", network_interfaces)
        if placements and not isinstance(placements, list):
            raise TypeError("Expected argument 'placements' to be a list")
        pulumi.set(__self__, "placements", placements)
        if private_dns_name_options and not isinstance(private_dns_name_options, list):
            raise TypeError("Expected argument 'private_dns_name_options' to be a list")
        pulumi.set(__self__, "private_dns_name_options", private_dns_name_options)
        if ram_disk_id and not isinstance(ram_disk_id, str):
            raise TypeError("Expected argument 'ram_disk_id' to be a str")
        pulumi.set(__self__, "ram_disk_id", ram_disk_id)
        if security_group_names and not isinstance(security_group_names, list):
            raise TypeError("Expected argument 'security_group_names' to be a list")
        pulumi.set(__self__, "security_group_names", security_group_names)
        if tag_specifications and not isinstance(tag_specifications, list):
            raise TypeError("Expected argument 'tag_specifications' to be a list")
        pulumi.set(__self__, "tag_specifications", tag_specifications)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if user_data and not isinstance(user_data, str):
            raise TypeError("Expected argument 'user_data' to be a str")
        pulumi.set(__self__, "user_data", user_data)
        if vpc_security_group_ids and not isinstance(vpc_security_group_ids, list):
            raise TypeError("Expected argument 'vpc_security_group_ids' to be a list")
        pulumi.set(__self__, "vpc_security_group_ids", vpc_security_group_ids)

    @property
    @pulumi.getter
    def arn(self) -> str:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="blockDeviceMappings")
    def block_device_mappings(self) -> Sequence['outputs.GetLaunchTemplateBlockDeviceMappingResult']:
        return pulumi.get(self, "block_device_mappings")

    @property
    @pulumi.getter(name="capacityReservationSpecifications")
    def capacity_reservation_specifications(self) -> Sequence['outputs.GetLaunchTemplateCapacityReservationSpecificationResult']:
        return pulumi.get(self, "capacity_reservation_specifications")

    @property
    @pulumi.getter(name="cpuOptions")
    def cpu_options(self) -> Sequence['outputs.GetLaunchTemplateCpuOptionResult']:
        return pulumi.get(self, "cpu_options")

    @property
    @pulumi.getter(name="creditSpecifications")
    def credit_specifications(self) -> Sequence['outputs.GetLaunchTemplateCreditSpecificationResult']:
        return pulumi.get(self, "credit_specifications")

    @property
    @pulumi.getter(name="defaultVersion")
    def default_version(self) -> int:
        return pulumi.get(self, "default_version")

    @property
    @pulumi.getter
    def description(self) -> str:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="disableApiStop")
    def disable_api_stop(self) -> bool:
        return pulumi.get(self, "disable_api_stop")

    @property
    @pulumi.getter(name="disableApiTermination")
    def disable_api_termination(self) -> bool:
        return pulumi.get(self, "disable_api_termination")

    @property
    @pulumi.getter(name="ebsOptimized")
    def ebs_optimized(self) -> str:
        return pulumi.get(self, "ebs_optimized")

    @property
    @pulumi.getter(name="elasticGpuSpecifications")
    def elastic_gpu_specifications(self) -> Sequence['outputs.GetLaunchTemplateElasticGpuSpecificationResult']:
        return pulumi.get(self, "elastic_gpu_specifications")

    @property
    @pulumi.getter(name="elasticInferenceAccelerators")
    def elastic_inference_accelerators(self) -> Sequence['outputs.GetLaunchTemplateElasticInferenceAcceleratorResult']:
        return pulumi.get(self, "elastic_inference_accelerators")

    @property
    @pulumi.getter(name="enclaveOptions")
    def enclave_options(self) -> Sequence['outputs.GetLaunchTemplateEnclaveOptionResult']:
        return pulumi.get(self, "enclave_options")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetLaunchTemplateFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter(name="hibernationOptions")
    def hibernation_options(self) -> Sequence['outputs.GetLaunchTemplateHibernationOptionResult']:
        return pulumi.get(self, "hibernation_options")

    @property
    @pulumi.getter(name="iamInstanceProfiles")
    def iam_instance_profiles(self) -> Sequence['outputs.GetLaunchTemplateIamInstanceProfileResult']:
        return pulumi.get(self, "iam_instance_profiles")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        ID of the launch template.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="imageId")
    def image_id(self) -> str:
        return pulumi.get(self, "image_id")

    @property
    @pulumi.getter(name="instanceInitiatedShutdownBehavior")
    def instance_initiated_shutdown_behavior(self) -> str:
        return pulumi.get(self, "instance_initiated_shutdown_behavior")

    @property
    @pulumi.getter(name="instanceMarketOptions")
    def instance_market_options(self) -> Sequence['outputs.GetLaunchTemplateInstanceMarketOptionResult']:
        return pulumi.get(self, "instance_market_options")

    @property
    @pulumi.getter(name="instanceRequirements")
    def instance_requirements(self) -> Sequence['outputs.GetLaunchTemplateInstanceRequirementResult']:
        return pulumi.get(self, "instance_requirements")

    @property
    @pulumi.getter(name="instanceType")
    def instance_type(self) -> str:
        return pulumi.get(self, "instance_type")

    @property
    @pulumi.getter(name="kernelId")
    def kernel_id(self) -> str:
        return pulumi.get(self, "kernel_id")

    @property
    @pulumi.getter(name="keyName")
    def key_name(self) -> str:
        return pulumi.get(self, "key_name")

    @property
    @pulumi.getter(name="latestVersion")
    def latest_version(self) -> int:
        return pulumi.get(self, "latest_version")

    @property
    @pulumi.getter(name="licenseSpecifications")
    def license_specifications(self) -> Sequence['outputs.GetLaunchTemplateLicenseSpecificationResult']:
        return pulumi.get(self, "license_specifications")

    @property
    @pulumi.getter(name="maintenanceOptions")
    def maintenance_options(self) -> Sequence['outputs.GetLaunchTemplateMaintenanceOptionResult']:
        return pulumi.get(self, "maintenance_options")

    @property
    @pulumi.getter(name="metadataOptions")
    def metadata_options(self) -> Sequence['outputs.GetLaunchTemplateMetadataOptionResult']:
        return pulumi.get(self, "metadata_options")

    @property
    @pulumi.getter
    def monitorings(self) -> Sequence['outputs.GetLaunchTemplateMonitoringResult']:
        return pulumi.get(self, "monitorings")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkInterfaces")
    def network_interfaces(self) -> Sequence['outputs.GetLaunchTemplateNetworkInterfaceResult']:
        return pulumi.get(self, "network_interfaces")

    @property
    @pulumi.getter
    def placements(self) -> Sequence['outputs.GetLaunchTemplatePlacementResult']:
        return pulumi.get(self, "placements")

    @property
    @pulumi.getter(name="privateDnsNameOptions")
    def private_dns_name_options(self) -> Sequence['outputs.GetLaunchTemplatePrivateDnsNameOptionResult']:
        return pulumi.get(self, "private_dns_name_options")

    @property
    @pulumi.getter(name="ramDiskId")
    def ram_disk_id(self) -> str:
        return pulumi.get(self, "ram_disk_id")

    @property
    @pulumi.getter(name="securityGroupNames")
    def security_group_names(self) -> Sequence[str]:
        return pulumi.get(self, "security_group_names")

    @property
    @pulumi.getter(name="tagSpecifications")
    def tag_specifications(self) -> Sequence['outputs.GetLaunchTemplateTagSpecificationResult']:
        return pulumi.get(self, "tag_specifications")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="userData")
    def user_data(self) -> str:
        return pulumi.get(self, "user_data")

    @property
    @pulumi.getter(name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> Sequence[str]:
        return pulumi.get(self, "vpc_security_group_ids")


class AwaitableGetLaunchTemplateResult(GetLaunchTemplateResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLaunchTemplateResult(
            arn=self.arn,
            block_device_mappings=self.block_device_mappings,
            capacity_reservation_specifications=self.capacity_reservation_specifications,
            cpu_options=self.cpu_options,
            credit_specifications=self.credit_specifications,
            default_version=self.default_version,
            description=self.description,
            disable_api_stop=self.disable_api_stop,
            disable_api_termination=self.disable_api_termination,
            ebs_optimized=self.ebs_optimized,
            elastic_gpu_specifications=self.elastic_gpu_specifications,
            elastic_inference_accelerators=self.elastic_inference_accelerators,
            enclave_options=self.enclave_options,
            filters=self.filters,
            hibernation_options=self.hibernation_options,
            iam_instance_profiles=self.iam_instance_profiles,
            id=self.id,
            image_id=self.image_id,
            instance_initiated_shutdown_behavior=self.instance_initiated_shutdown_behavior,
            instance_market_options=self.instance_market_options,
            instance_requirements=self.instance_requirements,
            instance_type=self.instance_type,
            kernel_id=self.kernel_id,
            key_name=self.key_name,
            latest_version=self.latest_version,
            license_specifications=self.license_specifications,
            maintenance_options=self.maintenance_options,
            metadata_options=self.metadata_options,
            monitorings=self.monitorings,
            name=self.name,
            network_interfaces=self.network_interfaces,
            placements=self.placements,
            private_dns_name_options=self.private_dns_name_options,
            ram_disk_id=self.ram_disk_id,
            security_group_names=self.security_group_names,
            tag_specifications=self.tag_specifications,
            tags=self.tags,
            user_data=self.user_data,
            vpc_security_group_ids=self.vpc_security_group_ids)


def get_launch_template(filters: Optional[Sequence[pulumi.InputType['GetLaunchTemplateFilterArgs']]] = None,
                        id: Optional[str] = None,
                        name: Optional[str] = None,
                        tags: Optional[Mapping[str, str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLaunchTemplateResult:
    """
    Provides information about a Launch Template.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    default = aws.ec2.get_launch_template(name="my-launch-template")
    ```
    ### Filter

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.ec2.get_launch_template(filters=[aws.ec2.GetLaunchTemplateFilterArgs(
        name="launch-template-name",
        values=["some-template"],
    )])
    ```


    :param Sequence[pulumi.InputType['GetLaunchTemplateFilterArgs']] filters: Configuration block(s) for filtering. Detailed below.
    :param str id: ID of the specific launch template to retrieve.
    :param str name: Name of the launch template.
    :param Mapping[str, str] tags: Map of tags, each pair of which must exactly match a pair on the desired Launch Template.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['id'] = id
    __args__['name'] = name
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ec2/getLaunchTemplate:getLaunchTemplate', __args__, opts=opts, typ=GetLaunchTemplateResult).value

    return AwaitableGetLaunchTemplateResult(
        arn=__ret__.arn,
        block_device_mappings=__ret__.block_device_mappings,
        capacity_reservation_specifications=__ret__.capacity_reservation_specifications,
        cpu_options=__ret__.cpu_options,
        credit_specifications=__ret__.credit_specifications,
        default_version=__ret__.default_version,
        description=__ret__.description,
        disable_api_stop=__ret__.disable_api_stop,
        disable_api_termination=__ret__.disable_api_termination,
        ebs_optimized=__ret__.ebs_optimized,
        elastic_gpu_specifications=__ret__.elastic_gpu_specifications,
        elastic_inference_accelerators=__ret__.elastic_inference_accelerators,
        enclave_options=__ret__.enclave_options,
        filters=__ret__.filters,
        hibernation_options=__ret__.hibernation_options,
        iam_instance_profiles=__ret__.iam_instance_profiles,
        id=__ret__.id,
        image_id=__ret__.image_id,
        instance_initiated_shutdown_behavior=__ret__.instance_initiated_shutdown_behavior,
        instance_market_options=__ret__.instance_market_options,
        instance_requirements=__ret__.instance_requirements,
        instance_type=__ret__.instance_type,
        kernel_id=__ret__.kernel_id,
        key_name=__ret__.key_name,
        latest_version=__ret__.latest_version,
        license_specifications=__ret__.license_specifications,
        maintenance_options=__ret__.maintenance_options,
        metadata_options=__ret__.metadata_options,
        monitorings=__ret__.monitorings,
        name=__ret__.name,
        network_interfaces=__ret__.network_interfaces,
        placements=__ret__.placements,
        private_dns_name_options=__ret__.private_dns_name_options,
        ram_disk_id=__ret__.ram_disk_id,
        security_group_names=__ret__.security_group_names,
        tag_specifications=__ret__.tag_specifications,
        tags=__ret__.tags,
        user_data=__ret__.user_data,
        vpc_security_group_ids=__ret__.vpc_security_group_ids)


@_utilities.lift_output_func(get_launch_template)
def get_launch_template_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetLaunchTemplateFilterArgs']]]]] = None,
                               id: Optional[pulumi.Input[Optional[str]]] = None,
                               name: Optional[pulumi.Input[Optional[str]]] = None,
                               tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLaunchTemplateResult]:
    """
    Provides information about a Launch Template.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    default = aws.ec2.get_launch_template(name="my-launch-template")
    ```
    ### Filter

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.ec2.get_launch_template(filters=[aws.ec2.GetLaunchTemplateFilterArgs(
        name="launch-template-name",
        values=["some-template"],
    )])
    ```


    :param Sequence[pulumi.InputType['GetLaunchTemplateFilterArgs']] filters: Configuration block(s) for filtering. Detailed below.
    :param str id: ID of the specific launch template to retrieve.
    :param str name: Name of the launch template.
    :param Mapping[str, str] tags: Map of tags, each pair of which must exactly match a pair on the desired Launch Template.
    """
    ...
