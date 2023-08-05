# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['DeploymentArgs', 'Deployment']

@pulumi.input_type
class DeploymentArgs:
    def __init__(__self__, *,
                 rest_api: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 stage_description: Optional[pulumi.Input[str]] = None,
                 stage_name: Optional[pulumi.Input[str]] = None,
                 triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Deployment resource.
        :param pulumi.Input[str] rest_api: REST API identifier.
        :param pulumi.Input[str] description: Description of the deployment
        :param pulumi.Input[str] stage_description: Description to set on the stage managed by the `stage_name` argument.
        :param pulumi.Input[str] stage_name: Name of the stage to create with this deployment. If the specified stage already exists, it will be updated to point to the new deployment. We recommend using the `apigateway.Stage` resource instead to manage stages.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] triggers: Map of arbitrary keys and values that, when changed, will trigger a redeployment.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] variables: Map to set on the stage managed by the `stage_name` argument.
        """
        pulumi.set(__self__, "rest_api", rest_api)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if stage_description is not None:
            pulumi.set(__self__, "stage_description", stage_description)
        if stage_name is not None:
            pulumi.set(__self__, "stage_name", stage_name)
        if triggers is not None:
            pulumi.set(__self__, "triggers", triggers)
        if variables is not None:
            pulumi.set(__self__, "variables", variables)

    @property
    @pulumi.getter(name="restApi")
    def rest_api(self) -> pulumi.Input[str]:
        """
        REST API identifier.
        """
        return pulumi.get(self, "rest_api")

    @rest_api.setter
    def rest_api(self, value: pulumi.Input[str]):
        pulumi.set(self, "rest_api", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the deployment
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="stageDescription")
    def stage_description(self) -> Optional[pulumi.Input[str]]:
        """
        Description to set on the stage managed by the `stage_name` argument.
        """
        return pulumi.get(self, "stage_description")

    @stage_description.setter
    def stage_description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "stage_description", value)

    @property
    @pulumi.getter(name="stageName")
    def stage_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the stage to create with this deployment. If the specified stage already exists, it will be updated to point to the new deployment. We recommend using the `apigateway.Stage` resource instead to manage stages.
        """
        return pulumi.get(self, "stage_name")

    @stage_name.setter
    def stage_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "stage_name", value)

    @property
    @pulumi.getter
    def triggers(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of arbitrary keys and values that, when changed, will trigger a redeployment.
        """
        return pulumi.get(self, "triggers")

    @triggers.setter
    def triggers(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "triggers", value)

    @property
    @pulumi.getter
    def variables(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map to set on the stage managed by the `stage_name` argument.
        """
        return pulumi.get(self, "variables")

    @variables.setter
    def variables(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "variables", value)


@pulumi.input_type
class _DeploymentState:
    def __init__(__self__, *,
                 created_date: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 execution_arn: Optional[pulumi.Input[str]] = None,
                 invoke_url: Optional[pulumi.Input[str]] = None,
                 rest_api: Optional[pulumi.Input[str]] = None,
                 stage_description: Optional[pulumi.Input[str]] = None,
                 stage_name: Optional[pulumi.Input[str]] = None,
                 triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Deployment resources.
        :param pulumi.Input[str] created_date: Creation date of the deployment
        :param pulumi.Input[str] description: Description of the deployment
        :param pulumi.Input[str] execution_arn: Execution ARN to be used in `lambda_permission`'s `source_arn`
               when allowing API Gateway to invoke a Lambda function,
               e.g., `arn:aws:execute-api:eu-west-2:123456789012:z4675bid1j/prod`
        :param pulumi.Input[str] invoke_url: URL to invoke the API pointing to the stage,
               e.g., `https://z4675bid1j.execute-api.eu-west-2.amazonaws.com/prod`
        :param pulumi.Input[str] rest_api: REST API identifier.
        :param pulumi.Input[str] stage_description: Description to set on the stage managed by the `stage_name` argument.
        :param pulumi.Input[str] stage_name: Name of the stage to create with this deployment. If the specified stage already exists, it will be updated to point to the new deployment. We recommend using the `apigateway.Stage` resource instead to manage stages.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] triggers: Map of arbitrary keys and values that, when changed, will trigger a redeployment.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] variables: Map to set on the stage managed by the `stage_name` argument.
        """
        if created_date is not None:
            pulumi.set(__self__, "created_date", created_date)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if execution_arn is not None:
            pulumi.set(__self__, "execution_arn", execution_arn)
        if invoke_url is not None:
            pulumi.set(__self__, "invoke_url", invoke_url)
        if rest_api is not None:
            pulumi.set(__self__, "rest_api", rest_api)
        if stage_description is not None:
            pulumi.set(__self__, "stage_description", stage_description)
        if stage_name is not None:
            pulumi.set(__self__, "stage_name", stage_name)
        if triggers is not None:
            pulumi.set(__self__, "triggers", triggers)
        if variables is not None:
            pulumi.set(__self__, "variables", variables)

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> Optional[pulumi.Input[str]]:
        """
        Creation date of the deployment
        """
        return pulumi.get(self, "created_date")

    @created_date.setter
    def created_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_date", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the deployment
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="executionArn")
    def execution_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Execution ARN to be used in `lambda_permission`'s `source_arn`
        when allowing API Gateway to invoke a Lambda function,
        e.g., `arn:aws:execute-api:eu-west-2:123456789012:z4675bid1j/prod`
        """
        return pulumi.get(self, "execution_arn")

    @execution_arn.setter
    def execution_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "execution_arn", value)

    @property
    @pulumi.getter(name="invokeUrl")
    def invoke_url(self) -> Optional[pulumi.Input[str]]:
        """
        URL to invoke the API pointing to the stage,
        e.g., `https://z4675bid1j.execute-api.eu-west-2.amazonaws.com/prod`
        """
        return pulumi.get(self, "invoke_url")

    @invoke_url.setter
    def invoke_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "invoke_url", value)

    @property
    @pulumi.getter(name="restApi")
    def rest_api(self) -> Optional[pulumi.Input[str]]:
        """
        REST API identifier.
        """
        return pulumi.get(self, "rest_api")

    @rest_api.setter
    def rest_api(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rest_api", value)

    @property
    @pulumi.getter(name="stageDescription")
    def stage_description(self) -> Optional[pulumi.Input[str]]:
        """
        Description to set on the stage managed by the `stage_name` argument.
        """
        return pulumi.get(self, "stage_description")

    @stage_description.setter
    def stage_description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "stage_description", value)

    @property
    @pulumi.getter(name="stageName")
    def stage_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the stage to create with this deployment. If the specified stage already exists, it will be updated to point to the new deployment. We recommend using the `apigateway.Stage` resource instead to manage stages.
        """
        return pulumi.get(self, "stage_name")

    @stage_name.setter
    def stage_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "stage_name", value)

    @property
    @pulumi.getter
    def triggers(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of arbitrary keys and values that, when changed, will trigger a redeployment.
        """
        return pulumi.get(self, "triggers")

    @triggers.setter
    def triggers(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "triggers", value)

    @property
    @pulumi.getter
    def variables(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map to set on the stage managed by the `stage_name` argument.
        """
        return pulumi.get(self, "variables")

    @variables.setter
    def variables(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "variables", value)


class Deployment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 rest_api: Optional[pulumi.Input[str]] = None,
                 stage_description: Optional[pulumi.Input[str]] = None,
                 stage_name: Optional[pulumi.Input[str]] = None,
                 triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages an API Gateway REST Deployment. A deployment is a snapshot of the REST API configuration. The deployment can then be published to callable endpoints via the `apigateway.Stage` resource and optionally managed further with the `apigateway.BasePathMapping` resource, `apigateway.DomainName` resource, and `aws_api_method_settings` resource. For more information, see the [API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-deploy-api.html).

        To properly capture all REST API configuration in a deployment, this resource must have dependencies on all prior resources that manage resources/paths, methods, integrations, etc.

        * For REST APIs that are configured via OpenAPI specification (`apigateway.RestApi` resource `body` argument), no special dependency setup is needed beyond referencing the  `id` attribute of that resource unless additional resources have further customized the REST API.
        * When the REST API configuration involves other resources (`apigateway.Integration` resource), the dependency setup can be done with implicit resource references in the `triggers` argument or explicit resource references using the [resource `dependsOn` custom option](https://www.pulumi.com/docs/intro/concepts/resources/#dependson). The `triggers` argument should be preferred over `depends_on`, since `depends_on` can only capture dependency ordering and will not cause the resource to recreate (redeploy the REST API) with upstream configuration changes.

        !> **WARNING:** It is recommended to use the `apigateway.Stage` resource instead of managing an API Gateway Stage via the `stage_name` argument of this resource. When this resource is recreated (REST API redeployment) with the `stage_name` configured, the stage is deleted and recreated. This will cause a temporary service interruption, increase provide plan differences, and can require a second apply to recreate any downstream stage configuration such as associated `aws_api_method_settings` resources.

        ## Example Usage
        ### OpenAPI Specification

        ```python
        import pulumi
        import hashlib
        import json
        import pulumi_aws as aws

        example_rest_api = aws.apigateway.RestApi("exampleRestApi", body=json.dumps({
            "openapi": "3.0.1",
            "info": {
                "title": "example",
                "version": "1.0",
            },
            "paths": {
                "/path1": {
                    "get": {
                        "x-amazon-apigateway-integration": {
                            "httpMethod": "GET",
                            "payloadFormatVersion": "1.0",
                            "type": "HTTP_PROXY",
                            "uri": "https://ip-ranges.amazonaws.com/ip-ranges.json",
                        },
                    },
                },
            },
        }))
        example_deployment = aws.apigateway.Deployment("exampleDeployment",
            rest_api=example_rest_api.id,
            triggers={
                "redeployment": example_rest_api.body.apply(lambda body: json.dumps(body)).apply(lambda to_json: hashlib.sha1(to_json.encode()).hexdigest()),
            })
        example_stage = aws.apigateway.Stage("exampleStage",
            deployment=example_deployment.id,
            rest_api=example_rest_api.id,
            stage_name="example")
        ```
        ### Resources

        ```python
        import pulumi
        import hashlib
        import json
        import pulumi_aws as aws

        example_rest_api = aws.apigateway.RestApi("exampleRestApi")
        example_resource = aws.apigateway.Resource("exampleResource",
            parent_id=example_rest_api.root_resource_id,
            path_part="example",
            rest_api=example_rest_api.id)
        example_method = aws.apigateway.Method("exampleMethod",
            authorization="NONE",
            http_method="GET",
            resource_id=example_resource.id,
            rest_api=example_rest_api.id)
        example_integration = aws.apigateway.Integration("exampleIntegration",
            http_method=example_method.http_method,
            resource_id=example_resource.id,
            rest_api=example_rest_api.id,
            type="MOCK")
        example_deployment = aws.apigateway.Deployment("exampleDeployment",
            rest_api=example_rest_api.id,
            triggers={
                "redeployment": pulumi.Output.all(example_resource.id, example_method.id, example_integration.id).apply(lambda exampleResourceId, exampleMethodId, exampleIntegrationId: json.dumps([
                    example_resource_id,
                    example_method_id,
                    example_integration_id,
                ])).apply(lambda to_json: hashlib.sha1(to_json.encode()).hexdigest()),
            })
        example_stage = aws.apigateway.Stage("exampleStage",
            deployment=example_deployment.id,
            rest_api=example_rest_api.id,
            stage_name="example")
        ```

        ## Import

        `aws_api_gateway_deployment` can be imported using `REST-API-ID/DEPLOYMENT-ID`, e.g.,

        ```sh
         $ pulumi import aws:apigateway/deployment:Deployment example aabbccddee/1122334
        ```

         The `stage_name`, `stage_description`, and `variables` arguments cannot be imported. Use the `aws_api_gateway_stage` resource to import and manage stages. The `triggers` argument cannot be imported.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the deployment
        :param pulumi.Input[str] rest_api: REST API identifier.
        :param pulumi.Input[str] stage_description: Description to set on the stage managed by the `stage_name` argument.
        :param pulumi.Input[str] stage_name: Name of the stage to create with this deployment. If the specified stage already exists, it will be updated to point to the new deployment. We recommend using the `apigateway.Stage` resource instead to manage stages.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] triggers: Map of arbitrary keys and values that, when changed, will trigger a redeployment.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] variables: Map to set on the stage managed by the `stage_name` argument.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DeploymentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an API Gateway REST Deployment. A deployment is a snapshot of the REST API configuration. The deployment can then be published to callable endpoints via the `apigateway.Stage` resource and optionally managed further with the `apigateway.BasePathMapping` resource, `apigateway.DomainName` resource, and `aws_api_method_settings` resource. For more information, see the [API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-deploy-api.html).

        To properly capture all REST API configuration in a deployment, this resource must have dependencies on all prior resources that manage resources/paths, methods, integrations, etc.

        * For REST APIs that are configured via OpenAPI specification (`apigateway.RestApi` resource `body` argument), no special dependency setup is needed beyond referencing the  `id` attribute of that resource unless additional resources have further customized the REST API.
        * When the REST API configuration involves other resources (`apigateway.Integration` resource), the dependency setup can be done with implicit resource references in the `triggers` argument or explicit resource references using the [resource `dependsOn` custom option](https://www.pulumi.com/docs/intro/concepts/resources/#dependson). The `triggers` argument should be preferred over `depends_on`, since `depends_on` can only capture dependency ordering and will not cause the resource to recreate (redeploy the REST API) with upstream configuration changes.

        !> **WARNING:** It is recommended to use the `apigateway.Stage` resource instead of managing an API Gateway Stage via the `stage_name` argument of this resource. When this resource is recreated (REST API redeployment) with the `stage_name` configured, the stage is deleted and recreated. This will cause a temporary service interruption, increase provide plan differences, and can require a second apply to recreate any downstream stage configuration such as associated `aws_api_method_settings` resources.

        ## Example Usage
        ### OpenAPI Specification

        ```python
        import pulumi
        import hashlib
        import json
        import pulumi_aws as aws

        example_rest_api = aws.apigateway.RestApi("exampleRestApi", body=json.dumps({
            "openapi": "3.0.1",
            "info": {
                "title": "example",
                "version": "1.0",
            },
            "paths": {
                "/path1": {
                    "get": {
                        "x-amazon-apigateway-integration": {
                            "httpMethod": "GET",
                            "payloadFormatVersion": "1.0",
                            "type": "HTTP_PROXY",
                            "uri": "https://ip-ranges.amazonaws.com/ip-ranges.json",
                        },
                    },
                },
            },
        }))
        example_deployment = aws.apigateway.Deployment("exampleDeployment",
            rest_api=example_rest_api.id,
            triggers={
                "redeployment": example_rest_api.body.apply(lambda body: json.dumps(body)).apply(lambda to_json: hashlib.sha1(to_json.encode()).hexdigest()),
            })
        example_stage = aws.apigateway.Stage("exampleStage",
            deployment=example_deployment.id,
            rest_api=example_rest_api.id,
            stage_name="example")
        ```
        ### Resources

        ```python
        import pulumi
        import hashlib
        import json
        import pulumi_aws as aws

        example_rest_api = aws.apigateway.RestApi("exampleRestApi")
        example_resource = aws.apigateway.Resource("exampleResource",
            parent_id=example_rest_api.root_resource_id,
            path_part="example",
            rest_api=example_rest_api.id)
        example_method = aws.apigateway.Method("exampleMethod",
            authorization="NONE",
            http_method="GET",
            resource_id=example_resource.id,
            rest_api=example_rest_api.id)
        example_integration = aws.apigateway.Integration("exampleIntegration",
            http_method=example_method.http_method,
            resource_id=example_resource.id,
            rest_api=example_rest_api.id,
            type="MOCK")
        example_deployment = aws.apigateway.Deployment("exampleDeployment",
            rest_api=example_rest_api.id,
            triggers={
                "redeployment": pulumi.Output.all(example_resource.id, example_method.id, example_integration.id).apply(lambda exampleResourceId, exampleMethodId, exampleIntegrationId: json.dumps([
                    example_resource_id,
                    example_method_id,
                    example_integration_id,
                ])).apply(lambda to_json: hashlib.sha1(to_json.encode()).hexdigest()),
            })
        example_stage = aws.apigateway.Stage("exampleStage",
            deployment=example_deployment.id,
            rest_api=example_rest_api.id,
            stage_name="example")
        ```

        ## Import

        `aws_api_gateway_deployment` can be imported using `REST-API-ID/DEPLOYMENT-ID`, e.g.,

        ```sh
         $ pulumi import aws:apigateway/deployment:Deployment example aabbccddee/1122334
        ```

         The `stage_name`, `stage_description`, and `variables` arguments cannot be imported. Use the `aws_api_gateway_stage` resource to import and manage stages. The `triggers` argument cannot be imported.

        :param str resource_name: The name of the resource.
        :param DeploymentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DeploymentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 rest_api: Optional[pulumi.Input[str]] = None,
                 stage_description: Optional[pulumi.Input[str]] = None,
                 stage_name: Optional[pulumi.Input[str]] = None,
                 triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DeploymentArgs.__new__(DeploymentArgs)

            __props__.__dict__["description"] = description
            if rest_api is None and not opts.urn:
                raise TypeError("Missing required property 'rest_api'")
            __props__.__dict__["rest_api"] = rest_api
            __props__.__dict__["stage_description"] = stage_description
            __props__.__dict__["stage_name"] = stage_name
            __props__.__dict__["triggers"] = triggers
            __props__.__dict__["variables"] = variables
            __props__.__dict__["created_date"] = None
            __props__.__dict__["execution_arn"] = None
            __props__.__dict__["invoke_url"] = None
        super(Deployment, __self__).__init__(
            'aws:apigateway/deployment:Deployment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            created_date: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            execution_arn: Optional[pulumi.Input[str]] = None,
            invoke_url: Optional[pulumi.Input[str]] = None,
            rest_api: Optional[pulumi.Input[str]] = None,
            stage_description: Optional[pulumi.Input[str]] = None,
            stage_name: Optional[pulumi.Input[str]] = None,
            triggers: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Deployment':
        """
        Get an existing Deployment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] created_date: Creation date of the deployment
        :param pulumi.Input[str] description: Description of the deployment
        :param pulumi.Input[str] execution_arn: Execution ARN to be used in `lambda_permission`'s `source_arn`
               when allowing API Gateway to invoke a Lambda function,
               e.g., `arn:aws:execute-api:eu-west-2:123456789012:z4675bid1j/prod`
        :param pulumi.Input[str] invoke_url: URL to invoke the API pointing to the stage,
               e.g., `https://z4675bid1j.execute-api.eu-west-2.amazonaws.com/prod`
        :param pulumi.Input[str] rest_api: REST API identifier.
        :param pulumi.Input[str] stage_description: Description to set on the stage managed by the `stage_name` argument.
        :param pulumi.Input[str] stage_name: Name of the stage to create with this deployment. If the specified stage already exists, it will be updated to point to the new deployment. We recommend using the `apigateway.Stage` resource instead to manage stages.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] triggers: Map of arbitrary keys and values that, when changed, will trigger a redeployment.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] variables: Map to set on the stage managed by the `stage_name` argument.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DeploymentState.__new__(_DeploymentState)

        __props__.__dict__["created_date"] = created_date
        __props__.__dict__["description"] = description
        __props__.__dict__["execution_arn"] = execution_arn
        __props__.__dict__["invoke_url"] = invoke_url
        __props__.__dict__["rest_api"] = rest_api
        __props__.__dict__["stage_description"] = stage_description
        __props__.__dict__["stage_name"] = stage_name
        __props__.__dict__["triggers"] = triggers
        __props__.__dict__["variables"] = variables
        return Deployment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> pulumi.Output[str]:
        """
        Creation date of the deployment
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the deployment
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="executionArn")
    def execution_arn(self) -> pulumi.Output[str]:
        """
        Execution ARN to be used in `lambda_permission`'s `source_arn`
        when allowing API Gateway to invoke a Lambda function,
        e.g., `arn:aws:execute-api:eu-west-2:123456789012:z4675bid1j/prod`
        """
        return pulumi.get(self, "execution_arn")

    @property
    @pulumi.getter(name="invokeUrl")
    def invoke_url(self) -> pulumi.Output[str]:
        """
        URL to invoke the API pointing to the stage,
        e.g., `https://z4675bid1j.execute-api.eu-west-2.amazonaws.com/prod`
        """
        return pulumi.get(self, "invoke_url")

    @property
    @pulumi.getter(name="restApi")
    def rest_api(self) -> pulumi.Output[str]:
        """
        REST API identifier.
        """
        return pulumi.get(self, "rest_api")

    @property
    @pulumi.getter(name="stageDescription")
    def stage_description(self) -> pulumi.Output[Optional[str]]:
        """
        Description to set on the stage managed by the `stage_name` argument.
        """
        return pulumi.get(self, "stage_description")

    @property
    @pulumi.getter(name="stageName")
    def stage_name(self) -> pulumi.Output[Optional[str]]:
        """
        Name of the stage to create with this deployment. If the specified stage already exists, it will be updated to point to the new deployment. We recommend using the `apigateway.Stage` resource instead to manage stages.
        """
        return pulumi.get(self, "stage_name")

    @property
    @pulumi.getter
    def triggers(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Map of arbitrary keys and values that, when changed, will trigger a redeployment.
        """
        return pulumi.get(self, "triggers")

    @property
    @pulumi.getter
    def variables(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Map to set on the stage managed by the `stage_name` argument.
        """
        return pulumi.get(self, "variables")

