# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['PlaybackKeyPairArgs', 'PlaybackKeyPair']

@pulumi.input_type
class PlaybackKeyPairArgs:
    def __init__(__self__, *,
                 public_key: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a PlaybackKeyPair resource.
        :param pulumi.Input[str] public_key: Public portion of a customer-generated key pair. Must be an ECDSA public key in PEM format.
        :param pulumi.Input[str] name: Playback Key Pair name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "public_key", public_key)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="publicKey")
    def public_key(self) -> pulumi.Input[str]:
        """
        Public portion of a customer-generated key pair. Must be an ECDSA public key in PEM format.
        """
        return pulumi.get(self, "public_key")

    @public_key.setter
    def public_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "public_key", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Playback Key Pair name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _PlaybackKeyPairState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 fingerprint: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 public_key: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering PlaybackKeyPair resources.
        :param pulumi.Input[str] arn: ARN of the Playback Key Pair.
        :param pulumi.Input[str] fingerprint: Key-pair identifier.
        :param pulumi.Input[str] name: Playback Key Pair name.
        :param pulumi.Input[str] public_key: Public portion of a customer-generated key pair. Must be an ECDSA public key in PEM format.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if fingerprint is not None:
            pulumi.set(__self__, "fingerprint", fingerprint)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if public_key is not None:
            pulumi.set(__self__, "public_key", public_key)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the Playback Key Pair.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def fingerprint(self) -> Optional[pulumi.Input[str]]:
        """
        Key-pair identifier.
        """
        return pulumi.get(self, "fingerprint")

    @fingerprint.setter
    def fingerprint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "fingerprint", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Playback Key Pair name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="publicKey")
    def public_key(self) -> Optional[pulumi.Input[str]]:
        """
        Public portion of a customer-generated key pair. Must be an ECDSA public key in PEM format.
        """
        return pulumi.get(self, "public_key")

    @public_key.setter
    def public_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "public_key", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)


class PlaybackKeyPair(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 public_key: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Resource for managing an AWS IVS (Interactive Video) Playback Key Pair.

        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ivs.PlaybackKeyPair("example", public_key=(lambda path: open(path).read())("./public-key.pem"))
        ```

        ## Import

        IVS (Interactive Video) Playback Key Pair can be imported using the ARN, e.g.,

        ```sh
         $ pulumi import aws:ivs/playbackKeyPair:PlaybackKeyPair example arn:aws:ivs:us-west-2:326937407773:playback-key/KDJRJNQhiQzA
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Playback Key Pair name.
        :param pulumi.Input[str] public_key: Public portion of a customer-generated key pair. Must be an ECDSA public key in PEM format.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PlaybackKeyPairArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS IVS (Interactive Video) Playback Key Pair.

        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ivs.PlaybackKeyPair("example", public_key=(lambda path: open(path).read())("./public-key.pem"))
        ```

        ## Import

        IVS (Interactive Video) Playback Key Pair can be imported using the ARN, e.g.,

        ```sh
         $ pulumi import aws:ivs/playbackKeyPair:PlaybackKeyPair example arn:aws:ivs:us-west-2:326937407773:playback-key/KDJRJNQhiQzA
        ```

        :param str resource_name: The name of the resource.
        :param PlaybackKeyPairArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PlaybackKeyPairArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 public_key: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PlaybackKeyPairArgs.__new__(PlaybackKeyPairArgs)

            __props__.__dict__["name"] = name
            if public_key is None and not opts.urn:
                raise TypeError("Missing required property 'public_key'")
            __props__.__dict__["public_key"] = public_key
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["fingerprint"] = None
            __props__.__dict__["tags_all"] = None
        super(PlaybackKeyPair, __self__).__init__(
            'aws:ivs/playbackKeyPair:PlaybackKeyPair',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            fingerprint: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            public_key: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'PlaybackKeyPair':
        """
        Get an existing PlaybackKeyPair resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: ARN of the Playback Key Pair.
        :param pulumi.Input[str] fingerprint: Key-pair identifier.
        :param pulumi.Input[str] name: Playback Key Pair name.
        :param pulumi.Input[str] public_key: Public portion of a customer-generated key pair. Must be an ECDSA public key in PEM format.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PlaybackKeyPairState.__new__(_PlaybackKeyPairState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["fingerprint"] = fingerprint
        __props__.__dict__["name"] = name
        __props__.__dict__["public_key"] = public_key
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return PlaybackKeyPair(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN of the Playback Key Pair.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def fingerprint(self) -> pulumi.Output[str]:
        """
        Key-pair identifier.
        """
        return pulumi.get(self, "fingerprint")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Playback Key Pair name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="publicKey")
    def public_key(self) -> pulumi.Output[str]:
        """
        Public portion of a customer-generated key pair. Must be an ECDSA public key in PEM format.
        """
        return pulumi.get(self, "public_key")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

