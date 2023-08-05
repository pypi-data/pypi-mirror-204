# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['TrafficPolicyInstanceArgs', 'TrafficPolicyInstance']

@pulumi.input_type
class TrafficPolicyInstanceArgs:
    def __init__(__self__, *,
                 hosted_zone_id: pulumi.Input[str],
                 traffic_policy_id: pulumi.Input[str],
                 traffic_policy_version: pulumi.Input[int],
                 ttl: pulumi.Input[int],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a TrafficPolicyInstance resource.
        :param pulumi.Input[str] hosted_zone_id: ID of the hosted zone that you want Amazon Route 53 to create resource record sets in by using the configuration in a traffic policy.
        :param pulumi.Input[str] traffic_policy_id: ID of the traffic policy that you want to use to create resource record sets in the specified hosted zone.
        :param pulumi.Input[int] traffic_policy_version: Version of the traffic policy
        :param pulumi.Input[int] ttl: TTL that you want Amazon Route 53 to assign to all the resource record sets that it creates in the specified hosted zone.
        :param pulumi.Input[str] name: Domain name for which Amazon Route 53 responds to DNS queries by using the resource record sets that Route 53 creates for this traffic policy instance.
        """
        pulumi.set(__self__, "hosted_zone_id", hosted_zone_id)
        pulumi.set(__self__, "traffic_policy_id", traffic_policy_id)
        pulumi.set(__self__, "traffic_policy_version", traffic_policy_version)
        pulumi.set(__self__, "ttl", ttl)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="hostedZoneId")
    def hosted_zone_id(self) -> pulumi.Input[str]:
        """
        ID of the hosted zone that you want Amazon Route 53 to create resource record sets in by using the configuration in a traffic policy.
        """
        return pulumi.get(self, "hosted_zone_id")

    @hosted_zone_id.setter
    def hosted_zone_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "hosted_zone_id", value)

    @property
    @pulumi.getter(name="trafficPolicyId")
    def traffic_policy_id(self) -> pulumi.Input[str]:
        """
        ID of the traffic policy that you want to use to create resource record sets in the specified hosted zone.
        """
        return pulumi.get(self, "traffic_policy_id")

    @traffic_policy_id.setter
    def traffic_policy_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "traffic_policy_id", value)

    @property
    @pulumi.getter(name="trafficPolicyVersion")
    def traffic_policy_version(self) -> pulumi.Input[int]:
        """
        Version of the traffic policy
        """
        return pulumi.get(self, "traffic_policy_version")

    @traffic_policy_version.setter
    def traffic_policy_version(self, value: pulumi.Input[int]):
        pulumi.set(self, "traffic_policy_version", value)

    @property
    @pulumi.getter
    def ttl(self) -> pulumi.Input[int]:
        """
        TTL that you want Amazon Route 53 to assign to all the resource record sets that it creates in the specified hosted zone.
        """
        return pulumi.get(self, "ttl")

    @ttl.setter
    def ttl(self, value: pulumi.Input[int]):
        pulumi.set(self, "ttl", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Domain name for which Amazon Route 53 responds to DNS queries by using the resource record sets that Route 53 creates for this traffic policy instance.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _TrafficPolicyInstanceState:
    def __init__(__self__, *,
                 hosted_zone_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 traffic_policy_id: Optional[pulumi.Input[str]] = None,
                 traffic_policy_version: Optional[pulumi.Input[int]] = None,
                 ttl: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering TrafficPolicyInstance resources.
        :param pulumi.Input[str] hosted_zone_id: ID of the hosted zone that you want Amazon Route 53 to create resource record sets in by using the configuration in a traffic policy.
        :param pulumi.Input[str] name: Domain name for which Amazon Route 53 responds to DNS queries by using the resource record sets that Route 53 creates for this traffic policy instance.
        :param pulumi.Input[str] traffic_policy_id: ID of the traffic policy that you want to use to create resource record sets in the specified hosted zone.
        :param pulumi.Input[int] traffic_policy_version: Version of the traffic policy
        :param pulumi.Input[int] ttl: TTL that you want Amazon Route 53 to assign to all the resource record sets that it creates in the specified hosted zone.
        """
        if hosted_zone_id is not None:
            pulumi.set(__self__, "hosted_zone_id", hosted_zone_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if traffic_policy_id is not None:
            pulumi.set(__self__, "traffic_policy_id", traffic_policy_id)
        if traffic_policy_version is not None:
            pulumi.set(__self__, "traffic_policy_version", traffic_policy_version)
        if ttl is not None:
            pulumi.set(__self__, "ttl", ttl)

    @property
    @pulumi.getter(name="hostedZoneId")
    def hosted_zone_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the hosted zone that you want Amazon Route 53 to create resource record sets in by using the configuration in a traffic policy.
        """
        return pulumi.get(self, "hosted_zone_id")

    @hosted_zone_id.setter
    def hosted_zone_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "hosted_zone_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Domain name for which Amazon Route 53 responds to DNS queries by using the resource record sets that Route 53 creates for this traffic policy instance.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="trafficPolicyId")
    def traffic_policy_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the traffic policy that you want to use to create resource record sets in the specified hosted zone.
        """
        return pulumi.get(self, "traffic_policy_id")

    @traffic_policy_id.setter
    def traffic_policy_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "traffic_policy_id", value)

    @property
    @pulumi.getter(name="trafficPolicyVersion")
    def traffic_policy_version(self) -> Optional[pulumi.Input[int]]:
        """
        Version of the traffic policy
        """
        return pulumi.get(self, "traffic_policy_version")

    @traffic_policy_version.setter
    def traffic_policy_version(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "traffic_policy_version", value)

    @property
    @pulumi.getter
    def ttl(self) -> Optional[pulumi.Input[int]]:
        """
        TTL that you want Amazon Route 53 to assign to all the resource record sets that it creates in the specified hosted zone.
        """
        return pulumi.get(self, "ttl")

    @ttl.setter
    def ttl(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "ttl", value)


class TrafficPolicyInstance(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 hosted_zone_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 traffic_policy_id: Optional[pulumi.Input[str]] = None,
                 traffic_policy_version: Optional[pulumi.Input[int]] = None,
                 ttl: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Provides a Route53 traffic policy instance resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.route53.TrafficPolicyInstance("test",
            hosted_zone_id="Z033120931TAQO548OGJC",
            traffic_policy_id="b3gb108f-ea6f-45a5-baab-9d112d8b4037",
            traffic_policy_version=1,
            ttl=360)
        ```

        ## Import

        Route53 traffic policy instance can be imported using its id.

        ```sh
         $ pulumi import aws:route53/trafficPolicyInstance:TrafficPolicyInstance test df579d9a-6396-410e-ac22-e7ad60cf9e7e
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] hosted_zone_id: ID of the hosted zone that you want Amazon Route 53 to create resource record sets in by using the configuration in a traffic policy.
        :param pulumi.Input[str] name: Domain name for which Amazon Route 53 responds to DNS queries by using the resource record sets that Route 53 creates for this traffic policy instance.
        :param pulumi.Input[str] traffic_policy_id: ID of the traffic policy that you want to use to create resource record sets in the specified hosted zone.
        :param pulumi.Input[int] traffic_policy_version: Version of the traffic policy
        :param pulumi.Input[int] ttl: TTL that you want Amazon Route 53 to assign to all the resource record sets that it creates in the specified hosted zone.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TrafficPolicyInstanceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Route53 traffic policy instance resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.route53.TrafficPolicyInstance("test",
            hosted_zone_id="Z033120931TAQO548OGJC",
            traffic_policy_id="b3gb108f-ea6f-45a5-baab-9d112d8b4037",
            traffic_policy_version=1,
            ttl=360)
        ```

        ## Import

        Route53 traffic policy instance can be imported using its id.

        ```sh
         $ pulumi import aws:route53/trafficPolicyInstance:TrafficPolicyInstance test df579d9a-6396-410e-ac22-e7ad60cf9e7e
        ```

        :param str resource_name: The name of the resource.
        :param TrafficPolicyInstanceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TrafficPolicyInstanceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 hosted_zone_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 traffic_policy_id: Optional[pulumi.Input[str]] = None,
                 traffic_policy_version: Optional[pulumi.Input[int]] = None,
                 ttl: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TrafficPolicyInstanceArgs.__new__(TrafficPolicyInstanceArgs)

            if hosted_zone_id is None and not opts.urn:
                raise TypeError("Missing required property 'hosted_zone_id'")
            __props__.__dict__["hosted_zone_id"] = hosted_zone_id
            __props__.__dict__["name"] = name
            if traffic_policy_id is None and not opts.urn:
                raise TypeError("Missing required property 'traffic_policy_id'")
            __props__.__dict__["traffic_policy_id"] = traffic_policy_id
            if traffic_policy_version is None and not opts.urn:
                raise TypeError("Missing required property 'traffic_policy_version'")
            __props__.__dict__["traffic_policy_version"] = traffic_policy_version
            if ttl is None and not opts.urn:
                raise TypeError("Missing required property 'ttl'")
            __props__.__dict__["ttl"] = ttl
        super(TrafficPolicyInstance, __self__).__init__(
            'aws:route53/trafficPolicyInstance:TrafficPolicyInstance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            hosted_zone_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            traffic_policy_id: Optional[pulumi.Input[str]] = None,
            traffic_policy_version: Optional[pulumi.Input[int]] = None,
            ttl: Optional[pulumi.Input[int]] = None) -> 'TrafficPolicyInstance':
        """
        Get an existing TrafficPolicyInstance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] hosted_zone_id: ID of the hosted zone that you want Amazon Route 53 to create resource record sets in by using the configuration in a traffic policy.
        :param pulumi.Input[str] name: Domain name for which Amazon Route 53 responds to DNS queries by using the resource record sets that Route 53 creates for this traffic policy instance.
        :param pulumi.Input[str] traffic_policy_id: ID of the traffic policy that you want to use to create resource record sets in the specified hosted zone.
        :param pulumi.Input[int] traffic_policy_version: Version of the traffic policy
        :param pulumi.Input[int] ttl: TTL that you want Amazon Route 53 to assign to all the resource record sets that it creates in the specified hosted zone.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TrafficPolicyInstanceState.__new__(_TrafficPolicyInstanceState)

        __props__.__dict__["hosted_zone_id"] = hosted_zone_id
        __props__.__dict__["name"] = name
        __props__.__dict__["traffic_policy_id"] = traffic_policy_id
        __props__.__dict__["traffic_policy_version"] = traffic_policy_version
        __props__.__dict__["ttl"] = ttl
        return TrafficPolicyInstance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="hostedZoneId")
    def hosted_zone_id(self) -> pulumi.Output[str]:
        """
        ID of the hosted zone that you want Amazon Route 53 to create resource record sets in by using the configuration in a traffic policy.
        """
        return pulumi.get(self, "hosted_zone_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Domain name for which Amazon Route 53 responds to DNS queries by using the resource record sets that Route 53 creates for this traffic policy instance.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="trafficPolicyId")
    def traffic_policy_id(self) -> pulumi.Output[str]:
        """
        ID of the traffic policy that you want to use to create resource record sets in the specified hosted zone.
        """
        return pulumi.get(self, "traffic_policy_id")

    @property
    @pulumi.getter(name="trafficPolicyVersion")
    def traffic_policy_version(self) -> pulumi.Output[int]:
        """
        Version of the traffic policy
        """
        return pulumi.get(self, "traffic_policy_version")

    @property
    @pulumi.getter
    def ttl(self) -> pulumi.Output[int]:
        """
        TTL that you want Amazon Route 53 to assign to all the resource record sets that it creates in the specified hosted zone.
        """
        return pulumi.get(self, "ttl")

