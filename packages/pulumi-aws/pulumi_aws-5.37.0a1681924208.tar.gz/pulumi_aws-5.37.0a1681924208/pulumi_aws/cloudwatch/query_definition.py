# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['QueryDefinitionArgs', 'QueryDefinition']

@pulumi.input_type
class QueryDefinitionArgs:
    def __init__(__self__, *,
                 query_string: pulumi.Input[str],
                 log_group_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a QueryDefinition resource.
        :param pulumi.Input[str] query_string: The query to save. You can read more about CloudWatch Logs Query Syntax in the [documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html).
        :param pulumi.Input[Sequence[pulumi.Input[str]]] log_group_names: Specific log groups to use with the query.
        :param pulumi.Input[str] name: The name of the query.
        """
        pulumi.set(__self__, "query_string", query_string)
        if log_group_names is not None:
            pulumi.set(__self__, "log_group_names", log_group_names)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="queryString")
    def query_string(self) -> pulumi.Input[str]:
        """
        The query to save. You can read more about CloudWatch Logs Query Syntax in the [documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html).
        """
        return pulumi.get(self, "query_string")

    @query_string.setter
    def query_string(self, value: pulumi.Input[str]):
        pulumi.set(self, "query_string", value)

    @property
    @pulumi.getter(name="logGroupNames")
    def log_group_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specific log groups to use with the query.
        """
        return pulumi.get(self, "log_group_names")

    @log_group_names.setter
    def log_group_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "log_group_names", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the query.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _QueryDefinitionState:
    def __init__(__self__, *,
                 log_group_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 query_definition_id: Optional[pulumi.Input[str]] = None,
                 query_string: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering QueryDefinition resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] log_group_names: Specific log groups to use with the query.
        :param pulumi.Input[str] name: The name of the query.
        :param pulumi.Input[str] query_definition_id: The query definition ID.
        :param pulumi.Input[str] query_string: The query to save. You can read more about CloudWatch Logs Query Syntax in the [documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html).
        """
        if log_group_names is not None:
            pulumi.set(__self__, "log_group_names", log_group_names)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if query_definition_id is not None:
            pulumi.set(__self__, "query_definition_id", query_definition_id)
        if query_string is not None:
            pulumi.set(__self__, "query_string", query_string)

    @property
    @pulumi.getter(name="logGroupNames")
    def log_group_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specific log groups to use with the query.
        """
        return pulumi.get(self, "log_group_names")

    @log_group_names.setter
    def log_group_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "log_group_names", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the query.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="queryDefinitionId")
    def query_definition_id(self) -> Optional[pulumi.Input[str]]:
        """
        The query definition ID.
        """
        return pulumi.get(self, "query_definition_id")

    @query_definition_id.setter
    def query_definition_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "query_definition_id", value)

    @property
    @pulumi.getter(name="queryString")
    def query_string(self) -> Optional[pulumi.Input[str]]:
        """
        The query to save. You can read more about CloudWatch Logs Query Syntax in the [documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html).
        """
        return pulumi.get(self, "query_string")

    @query_string.setter
    def query_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "query_string", value)


class QueryDefinition(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 log_group_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 query_string: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a CloudWatch Logs query definition resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.cloudwatch.QueryDefinition("example",
            log_group_names=[
                "/aws/logGroup1",
                "/aws/logGroup2",
            ],
            query_string=\"\"\"fields @timestamp, @message
        | sort @timestamp desc
        | limit 25

        \"\"\")
        ```

        ## Import

        CloudWatch query definitions can be imported using the query definition ARN. The ARN can be found on the "Edit Query" page for the query in the AWS Console.

        ```sh
         $ pulumi import aws:cloudwatch/queryDefinition:QueryDefinition example arn:aws:logs:us-west-2:123456789012:query-definition:269951d7-6f75-496d-9d7b-6b7a5486bdbd
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] log_group_names: Specific log groups to use with the query.
        :param pulumi.Input[str] name: The name of the query.
        :param pulumi.Input[str] query_string: The query to save. You can read more about CloudWatch Logs Query Syntax in the [documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: QueryDefinitionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a CloudWatch Logs query definition resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.cloudwatch.QueryDefinition("example",
            log_group_names=[
                "/aws/logGroup1",
                "/aws/logGroup2",
            ],
            query_string=\"\"\"fields @timestamp, @message
        | sort @timestamp desc
        | limit 25

        \"\"\")
        ```

        ## Import

        CloudWatch query definitions can be imported using the query definition ARN. The ARN can be found on the "Edit Query" page for the query in the AWS Console.

        ```sh
         $ pulumi import aws:cloudwatch/queryDefinition:QueryDefinition example arn:aws:logs:us-west-2:123456789012:query-definition:269951d7-6f75-496d-9d7b-6b7a5486bdbd
        ```

        :param str resource_name: The name of the resource.
        :param QueryDefinitionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(QueryDefinitionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 log_group_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 query_string: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = QueryDefinitionArgs.__new__(QueryDefinitionArgs)

            __props__.__dict__["log_group_names"] = log_group_names
            __props__.__dict__["name"] = name
            if query_string is None and not opts.urn:
                raise TypeError("Missing required property 'query_string'")
            __props__.__dict__["query_string"] = query_string
            __props__.__dict__["query_definition_id"] = None
        super(QueryDefinition, __self__).__init__(
            'aws:cloudwatch/queryDefinition:QueryDefinition',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            log_group_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            query_definition_id: Optional[pulumi.Input[str]] = None,
            query_string: Optional[pulumi.Input[str]] = None) -> 'QueryDefinition':
        """
        Get an existing QueryDefinition resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] log_group_names: Specific log groups to use with the query.
        :param pulumi.Input[str] name: The name of the query.
        :param pulumi.Input[str] query_definition_id: The query definition ID.
        :param pulumi.Input[str] query_string: The query to save. You can read more about CloudWatch Logs Query Syntax in the [documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _QueryDefinitionState.__new__(_QueryDefinitionState)

        __props__.__dict__["log_group_names"] = log_group_names
        __props__.__dict__["name"] = name
        __props__.__dict__["query_definition_id"] = query_definition_id
        __props__.__dict__["query_string"] = query_string
        return QueryDefinition(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="logGroupNames")
    def log_group_names(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Specific log groups to use with the query.
        """
        return pulumi.get(self, "log_group_names")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the query.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="queryDefinitionId")
    def query_definition_id(self) -> pulumi.Output[str]:
        """
        The query definition ID.
        """
        return pulumi.get(self, "query_definition_id")

    @property
    @pulumi.getter(name="queryString")
    def query_string(self) -> pulumi.Output[str]:
        """
        The query to save. You can read more about CloudWatch Logs Query Syntax in the [documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html).
        """
        return pulumi.get(self, "query_string")

