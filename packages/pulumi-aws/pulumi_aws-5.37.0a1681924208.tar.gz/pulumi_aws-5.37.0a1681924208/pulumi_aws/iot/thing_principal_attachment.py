# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ThingPrincipalAttachmentArgs', 'ThingPrincipalAttachment']

@pulumi.input_type
class ThingPrincipalAttachmentArgs:
    def __init__(__self__, *,
                 principal: pulumi.Input[str],
                 thing: pulumi.Input[str]):
        """
        The set of arguments for constructing a ThingPrincipalAttachment resource.
        :param pulumi.Input[str] principal: The AWS IoT Certificate ARN or Amazon Cognito Identity ID.
        :param pulumi.Input[str] thing: The name of the thing.
        """
        pulumi.set(__self__, "principal", principal)
        pulumi.set(__self__, "thing", thing)

    @property
    @pulumi.getter
    def principal(self) -> pulumi.Input[str]:
        """
        The AWS IoT Certificate ARN or Amazon Cognito Identity ID.
        """
        return pulumi.get(self, "principal")

    @principal.setter
    def principal(self, value: pulumi.Input[str]):
        pulumi.set(self, "principal", value)

    @property
    @pulumi.getter
    def thing(self) -> pulumi.Input[str]:
        """
        The name of the thing.
        """
        return pulumi.get(self, "thing")

    @thing.setter
    def thing(self, value: pulumi.Input[str]):
        pulumi.set(self, "thing", value)


@pulumi.input_type
class _ThingPrincipalAttachmentState:
    def __init__(__self__, *,
                 principal: Optional[pulumi.Input[str]] = None,
                 thing: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ThingPrincipalAttachment resources.
        :param pulumi.Input[str] principal: The AWS IoT Certificate ARN or Amazon Cognito Identity ID.
        :param pulumi.Input[str] thing: The name of the thing.
        """
        if principal is not None:
            pulumi.set(__self__, "principal", principal)
        if thing is not None:
            pulumi.set(__self__, "thing", thing)

    @property
    @pulumi.getter
    def principal(self) -> Optional[pulumi.Input[str]]:
        """
        The AWS IoT Certificate ARN or Amazon Cognito Identity ID.
        """
        return pulumi.get(self, "principal")

    @principal.setter
    def principal(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal", value)

    @property
    @pulumi.getter
    def thing(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the thing.
        """
        return pulumi.get(self, "thing")

    @thing.setter
    def thing(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "thing", value)


class ThingPrincipalAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 principal: Optional[pulumi.Input[str]] = None,
                 thing: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Attaches Principal to AWS IoT Thing.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.iot.Thing("example")
        cert = aws.iot.Certificate("cert",
            csr=(lambda path: open(path).read())("csr.pem"),
            active=True)
        att = aws.iot.ThingPrincipalAttachment("att",
            principal=cert.arn,
            thing=example.name)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] principal: The AWS IoT Certificate ARN or Amazon Cognito Identity ID.
        :param pulumi.Input[str] thing: The name of the thing.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ThingPrincipalAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Attaches Principal to AWS IoT Thing.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.iot.Thing("example")
        cert = aws.iot.Certificate("cert",
            csr=(lambda path: open(path).read())("csr.pem"),
            active=True)
        att = aws.iot.ThingPrincipalAttachment("att",
            principal=cert.arn,
            thing=example.name)
        ```

        :param str resource_name: The name of the resource.
        :param ThingPrincipalAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ThingPrincipalAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 principal: Optional[pulumi.Input[str]] = None,
                 thing: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ThingPrincipalAttachmentArgs.__new__(ThingPrincipalAttachmentArgs)

            if principal is None and not opts.urn:
                raise TypeError("Missing required property 'principal'")
            __props__.__dict__["principal"] = principal
            if thing is None and not opts.urn:
                raise TypeError("Missing required property 'thing'")
            __props__.__dict__["thing"] = thing
        super(ThingPrincipalAttachment, __self__).__init__(
            'aws:iot/thingPrincipalAttachment:ThingPrincipalAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            principal: Optional[pulumi.Input[str]] = None,
            thing: Optional[pulumi.Input[str]] = None) -> 'ThingPrincipalAttachment':
        """
        Get an existing ThingPrincipalAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] principal: The AWS IoT Certificate ARN or Amazon Cognito Identity ID.
        :param pulumi.Input[str] thing: The name of the thing.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ThingPrincipalAttachmentState.__new__(_ThingPrincipalAttachmentState)

        __props__.__dict__["principal"] = principal
        __props__.__dict__["thing"] = thing
        return ThingPrincipalAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def principal(self) -> pulumi.Output[str]:
        """
        The AWS IoT Certificate ARN or Amazon Cognito Identity ID.
        """
        return pulumi.get(self, "principal")

    @property
    @pulumi.getter
    def thing(self) -> pulumi.Output[str]:
        """
        The name of the thing.
        """
        return pulumi.get(self, "thing")

