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

__all__ = ['LoggingConfigurationArgs', 'LoggingConfiguration']

@pulumi.input_type
class LoggingConfigurationArgs:
    def __init__(__self__, *,
                 destination_configuration: Optional[pulumi.Input['LoggingConfigurationDestinationConfigurationArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a LoggingConfiguration resource.
        :param pulumi.Input['LoggingConfigurationDestinationConfigurationArgs'] destination_configuration: Object containing destination configuration for where chat activity will be logged. This object must contain exactly one of the following children arguments:
        :param pulumi.Input[str] name: Logging Configuration name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        if destination_configuration is not None:
            pulumi.set(__self__, "destination_configuration", destination_configuration)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="destinationConfiguration")
    def destination_configuration(self) -> Optional[pulumi.Input['LoggingConfigurationDestinationConfigurationArgs']]:
        """
        Object containing destination configuration for where chat activity will be logged. This object must contain exactly one of the following children arguments:
        """
        return pulumi.get(self, "destination_configuration")

    @destination_configuration.setter
    def destination_configuration(self, value: Optional[pulumi.Input['LoggingConfigurationDestinationConfigurationArgs']]):
        pulumi.set(self, "destination_configuration", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Logging Configuration name.
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
class _LoggingConfigurationState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 destination_configuration: Optional[pulumi.Input['LoggingConfigurationDestinationConfigurationArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering LoggingConfiguration resources.
        :param pulumi.Input[str] arn: ARN of the Logging Configuration.
        :param pulumi.Input['LoggingConfigurationDestinationConfigurationArgs'] destination_configuration: Object containing destination configuration for where chat activity will be logged. This object must contain exactly one of the following children arguments:
        :param pulumi.Input[str] name: Logging Configuration name.
        :param pulumi.Input[str] state: State of the Logging Configuration.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if destination_configuration is not None:
            pulumi.set(__self__, "destination_configuration", destination_configuration)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if state is not None:
            pulumi.set(__self__, "state", state)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the Logging Configuration.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="destinationConfiguration")
    def destination_configuration(self) -> Optional[pulumi.Input['LoggingConfigurationDestinationConfigurationArgs']]:
        """
        Object containing destination configuration for where chat activity will be logged. This object must contain exactly one of the following children arguments:
        """
        return pulumi.get(self, "destination_configuration")

    @destination_configuration.setter
    def destination_configuration(self, value: Optional[pulumi.Input['LoggingConfigurationDestinationConfigurationArgs']]):
        pulumi.set(self, "destination_configuration", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Logging Configuration name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        State of the Logging Configuration.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)

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


class LoggingConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 destination_configuration: Optional[pulumi.Input[pulumi.InputType['LoggingConfigurationDestinationConfigurationArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Resource for managing an AWS IVS (Interactive Video) Chat Logging Configuration.

        ## Example Usage
        ### Basic Usage - Logging to CloudWatch

        ```python
        import pulumi
        import pulumi_aws as aws

        example_log_group = aws.cloudwatch.LogGroup("exampleLogGroup")
        example_logging_configuration = aws.ivschat.LoggingConfiguration("exampleLoggingConfiguration", destination_configuration=aws.ivschat.LoggingConfigurationDestinationConfigurationArgs(
            cloudwatch_logs=aws.ivschat.LoggingConfigurationDestinationConfigurationCloudwatchLogsArgs(
                log_group_name=example_log_group.name,
            ),
        ))
        ```
        ### Basic Usage - Logging to Kinesis Firehose with Extended S3

        ```python
        import pulumi
        import pulumi_aws as aws

        example_bucket_v2 = aws.s3.BucketV2("exampleBucketV2", bucket_prefix="tf-ivschat-logging-bucket")
        assume_role = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                type="Service",
                identifiers=["firehose.amazonaws.com"],
            )],
            actions=["sts:AssumeRole"],
        )])
        example_role = aws.iam.Role("exampleRole", assume_role_policy=assume_role.json)
        example_firehose_delivery_stream = aws.kinesis.FirehoseDeliveryStream("exampleFirehoseDeliveryStream",
            destination="extended_s3",
            extended_s3_configuration=aws.kinesis.FirehoseDeliveryStreamExtendedS3ConfigurationArgs(
                role_arn=example_role.arn,
                bucket_arn=example_bucket_v2.arn,
            ),
            tags={
                "LogDeliveryEnabled": "true",
            })
        example_bucket_acl_v2 = aws.s3.BucketAclV2("exampleBucketAclV2",
            bucket=example_bucket_v2.id,
            acl="private")
        example_logging_configuration = aws.ivschat.LoggingConfiguration("exampleLoggingConfiguration", destination_configuration=aws.ivschat.LoggingConfigurationDestinationConfigurationArgs(
            firehose=aws.ivschat.LoggingConfigurationDestinationConfigurationFirehoseArgs(
                delivery_stream_name=example_firehose_delivery_stream.name,
            ),
        ))
        ```

        ## Import

        IVS (Interactive Video) Chat Logging Configuration can be imported using the ARN, e.g.,

        ```sh
         $ pulumi import aws:ivschat/loggingConfiguration:LoggingConfiguration example arn:aws:ivschat:us-west-2:326937407773:logging-configuration/MMUQc8wcqZmC
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['LoggingConfigurationDestinationConfigurationArgs']] destination_configuration: Object containing destination configuration for where chat activity will be logged. This object must contain exactly one of the following children arguments:
        :param pulumi.Input[str] name: Logging Configuration name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[LoggingConfigurationArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS IVS (Interactive Video) Chat Logging Configuration.

        ## Example Usage
        ### Basic Usage - Logging to CloudWatch

        ```python
        import pulumi
        import pulumi_aws as aws

        example_log_group = aws.cloudwatch.LogGroup("exampleLogGroup")
        example_logging_configuration = aws.ivschat.LoggingConfiguration("exampleLoggingConfiguration", destination_configuration=aws.ivschat.LoggingConfigurationDestinationConfigurationArgs(
            cloudwatch_logs=aws.ivschat.LoggingConfigurationDestinationConfigurationCloudwatchLogsArgs(
                log_group_name=example_log_group.name,
            ),
        ))
        ```
        ### Basic Usage - Logging to Kinesis Firehose with Extended S3

        ```python
        import pulumi
        import pulumi_aws as aws

        example_bucket_v2 = aws.s3.BucketV2("exampleBucketV2", bucket_prefix="tf-ivschat-logging-bucket")
        assume_role = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                type="Service",
                identifiers=["firehose.amazonaws.com"],
            )],
            actions=["sts:AssumeRole"],
        )])
        example_role = aws.iam.Role("exampleRole", assume_role_policy=assume_role.json)
        example_firehose_delivery_stream = aws.kinesis.FirehoseDeliveryStream("exampleFirehoseDeliveryStream",
            destination="extended_s3",
            extended_s3_configuration=aws.kinesis.FirehoseDeliveryStreamExtendedS3ConfigurationArgs(
                role_arn=example_role.arn,
                bucket_arn=example_bucket_v2.arn,
            ),
            tags={
                "LogDeliveryEnabled": "true",
            })
        example_bucket_acl_v2 = aws.s3.BucketAclV2("exampleBucketAclV2",
            bucket=example_bucket_v2.id,
            acl="private")
        example_logging_configuration = aws.ivschat.LoggingConfiguration("exampleLoggingConfiguration", destination_configuration=aws.ivschat.LoggingConfigurationDestinationConfigurationArgs(
            firehose=aws.ivschat.LoggingConfigurationDestinationConfigurationFirehoseArgs(
                delivery_stream_name=example_firehose_delivery_stream.name,
            ),
        ))
        ```

        ## Import

        IVS (Interactive Video) Chat Logging Configuration can be imported using the ARN, e.g.,

        ```sh
         $ pulumi import aws:ivschat/loggingConfiguration:LoggingConfiguration example arn:aws:ivschat:us-west-2:326937407773:logging-configuration/MMUQc8wcqZmC
        ```

        :param str resource_name: The name of the resource.
        :param LoggingConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LoggingConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 destination_configuration: Optional[pulumi.Input[pulumi.InputType['LoggingConfigurationDestinationConfigurationArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LoggingConfigurationArgs.__new__(LoggingConfigurationArgs)

            __props__.__dict__["destination_configuration"] = destination_configuration
            __props__.__dict__["name"] = name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["tags_all"] = None
        super(LoggingConfiguration, __self__).__init__(
            'aws:ivschat/loggingConfiguration:LoggingConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            destination_configuration: Optional[pulumi.Input[pulumi.InputType['LoggingConfigurationDestinationConfigurationArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            state: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'LoggingConfiguration':
        """
        Get an existing LoggingConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: ARN of the Logging Configuration.
        :param pulumi.Input[pulumi.InputType['LoggingConfigurationDestinationConfigurationArgs']] destination_configuration: Object containing destination configuration for where chat activity will be logged. This object must contain exactly one of the following children arguments:
        :param pulumi.Input[str] name: Logging Configuration name.
        :param pulumi.Input[str] state: State of the Logging Configuration.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _LoggingConfigurationState.__new__(_LoggingConfigurationState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["destination_configuration"] = destination_configuration
        __props__.__dict__["name"] = name
        __props__.__dict__["state"] = state
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return LoggingConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN of the Logging Configuration.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="destinationConfiguration")
    def destination_configuration(self) -> pulumi.Output[Optional['outputs.LoggingConfigurationDestinationConfiguration']]:
        """
        Object containing destination configuration for where chat activity will be logged. This object must contain exactly one of the following children arguments:
        """
        return pulumi.get(self, "destination_configuration")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Logging Configuration name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        State of the Logging Configuration.
        """
        return pulumi.get(self, "state")

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

