# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['InstanceStateArgs', 'InstanceState']

@pulumi.input_type
class InstanceStateArgs:
    def __init__(__self__, *,
                 instance_id: pulumi.Input[str],
                 state: pulumi.Input[str],
                 force: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a InstanceState resource.
        :param pulumi.Input[str] instance_id: ID of the instance.
        :param pulumi.Input[str] state: State of the instance. Valid values are `stopped`, `running`.
        :param pulumi.Input[bool] force: Whether to request a forced stop when `state` is `stopped`. Otherwise (_i.e._, `state` is `running`), ignored. When an instance is forced to stop, it does not flush file system caches or file system metadata, and you must subsequently perform file system check and repair. Not recommended for Windows instances. Defaults to `false`.
        """
        pulumi.set(__self__, "instance_id", instance_id)
        pulumi.set(__self__, "state", state)
        if force is not None:
            pulumi.set(__self__, "force", force)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Input[str]:
        """
        ID of the instance.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter
    def state(self) -> pulumi.Input[str]:
        """
        State of the instance. Valid values are `stopped`, `running`.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: pulumi.Input[str]):
        pulumi.set(self, "state", value)

    @property
    @pulumi.getter
    def force(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to request a forced stop when `state` is `stopped`. Otherwise (_i.e._, `state` is `running`), ignored. When an instance is forced to stop, it does not flush file system caches or file system metadata, and you must subsequently perform file system check and repair. Not recommended for Windows instances. Defaults to `false`.
        """
        return pulumi.get(self, "force")

    @force.setter
    def force(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "force", value)


@pulumi.input_type
class _InstanceStateState:
    def __init__(__self__, *,
                 force: Optional[pulumi.Input[bool]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering InstanceState resources.
        :param pulumi.Input[bool] force: Whether to request a forced stop when `state` is `stopped`. Otherwise (_i.e._, `state` is `running`), ignored. When an instance is forced to stop, it does not flush file system caches or file system metadata, and you must subsequently perform file system check and repair. Not recommended for Windows instances. Defaults to `false`.
        :param pulumi.Input[str] instance_id: ID of the instance.
        :param pulumi.Input[str] state: State of the instance. Valid values are `stopped`, `running`.
        """
        if force is not None:
            pulumi.set(__self__, "force", force)
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)
        if state is not None:
            pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter
    def force(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to request a forced stop when `state` is `stopped`. Otherwise (_i.e._, `state` is `running`), ignored. When an instance is forced to stop, it does not flush file system caches or file system metadata, and you must subsequently perform file system check and repair. Not recommended for Windows instances. Defaults to `false`.
        """
        return pulumi.get(self, "force")

    @force.setter
    def force(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "force", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the instance.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        State of the instance. Valid values are `stopped`, `running`.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)


class InstanceState(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 force: Optional[pulumi.Input[bool]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an EC2 instance state resource. This allows managing an instance power state.

        > **NOTE on Instance State Management:** AWS does not currently have an EC2 API operation to determine an instance has finished processing user data. As a result, this resource can interfere with user data processing. For example, this resource may stop an instance while the user data script is in mid run.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        ubuntu = aws.ec2.get_ami(most_recent=True,
            filters=[
                aws.ec2.GetAmiFilterArgs(
                    name="name",
                    values=["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"],
                ),
                aws.ec2.GetAmiFilterArgs(
                    name="virtualization-type",
                    values=["hvm"],
                ),
            ],
            owners=["099720109477"])
        test_instance = aws.ec2.Instance("testInstance",
            ami=ubuntu.id,
            instance_type="t3.micro",
            tags={
                "Name": "HelloWorld",
            })
        test_instance_state = aws.ec2transitgateway.InstanceState("testInstanceState",
            instance_id=test_instance.id,
            state="stopped")
        ```

        ## Import

        `aws_ec2_instance_state` can be imported by using the `instance_id` attribute, e.g.,

        ```sh
         $ pulumi import aws:ec2transitgateway/instanceState:InstanceState test i-02cae6557dfcf2f96
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] force: Whether to request a forced stop when `state` is `stopped`. Otherwise (_i.e._, `state` is `running`), ignored. When an instance is forced to stop, it does not flush file system caches or file system metadata, and you must subsequently perform file system check and repair. Not recommended for Windows instances. Defaults to `false`.
        :param pulumi.Input[str] instance_id: ID of the instance.
        :param pulumi.Input[str] state: State of the instance. Valid values are `stopped`, `running`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: InstanceStateArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an EC2 instance state resource. This allows managing an instance power state.

        > **NOTE on Instance State Management:** AWS does not currently have an EC2 API operation to determine an instance has finished processing user data. As a result, this resource can interfere with user data processing. For example, this resource may stop an instance while the user data script is in mid run.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        ubuntu = aws.ec2.get_ami(most_recent=True,
            filters=[
                aws.ec2.GetAmiFilterArgs(
                    name="name",
                    values=["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"],
                ),
                aws.ec2.GetAmiFilterArgs(
                    name="virtualization-type",
                    values=["hvm"],
                ),
            ],
            owners=["099720109477"])
        test_instance = aws.ec2.Instance("testInstance",
            ami=ubuntu.id,
            instance_type="t3.micro",
            tags={
                "Name": "HelloWorld",
            })
        test_instance_state = aws.ec2transitgateway.InstanceState("testInstanceState",
            instance_id=test_instance.id,
            state="stopped")
        ```

        ## Import

        `aws_ec2_instance_state` can be imported by using the `instance_id` attribute, e.g.,

        ```sh
         $ pulumi import aws:ec2transitgateway/instanceState:InstanceState test i-02cae6557dfcf2f96
        ```

        :param str resource_name: The name of the resource.
        :param InstanceStateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InstanceStateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 force: Optional[pulumi.Input[bool]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = InstanceStateArgs.__new__(InstanceStateArgs)

            __props__.__dict__["force"] = force
            if instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'instance_id'")
            __props__.__dict__["instance_id"] = instance_id
            if state is None and not opts.urn:
                raise TypeError("Missing required property 'state'")
            __props__.__dict__["state"] = state
        super(InstanceState, __self__).__init__(
            'aws:ec2transitgateway/instanceState:InstanceState',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            force: Optional[pulumi.Input[bool]] = None,
            instance_id: Optional[pulumi.Input[str]] = None,
            state: Optional[pulumi.Input[str]] = None) -> 'InstanceState':
        """
        Get an existing InstanceState resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] force: Whether to request a forced stop when `state` is `stopped`. Otherwise (_i.e._, `state` is `running`), ignored. When an instance is forced to stop, it does not flush file system caches or file system metadata, and you must subsequently perform file system check and repair. Not recommended for Windows instances. Defaults to `false`.
        :param pulumi.Input[str] instance_id: ID of the instance.
        :param pulumi.Input[str] state: State of the instance. Valid values are `stopped`, `running`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _InstanceStateState.__new__(_InstanceStateState)

        __props__.__dict__["force"] = force
        __props__.__dict__["instance_id"] = instance_id
        __props__.__dict__["state"] = state
        return InstanceState(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def force(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to request a forced stop when `state` is `stopped`. Otherwise (_i.e._, `state` is `running`), ignored. When an instance is forced to stop, it does not flush file system caches or file system metadata, and you must subsequently perform file system check and repair. Not recommended for Windows instances. Defaults to `false`.
        """
        return pulumi.get(self, "force")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        ID of the instance.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        State of the instance. Valid values are `stopped`, `running`.
        """
        return pulumi.get(self, "state")

