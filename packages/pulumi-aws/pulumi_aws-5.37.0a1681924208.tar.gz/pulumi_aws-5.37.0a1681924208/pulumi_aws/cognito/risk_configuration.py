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

__all__ = ['RiskConfigurationArgs', 'RiskConfiguration']

@pulumi.input_type
class RiskConfigurationArgs:
    def __init__(__self__, *,
                 user_pool_id: pulumi.Input[str],
                 account_takeover_risk_configuration: Optional[pulumi.Input['RiskConfigurationAccountTakeoverRiskConfigurationArgs']] = None,
                 client_id: Optional[pulumi.Input[str]] = None,
                 compromised_credentials_risk_configuration: Optional[pulumi.Input['RiskConfigurationCompromisedCredentialsRiskConfigurationArgs']] = None,
                 risk_exception_configuration: Optional[pulumi.Input['RiskConfigurationRiskExceptionConfigurationArgs']] = None):
        """
        The set of arguments for constructing a RiskConfiguration resource.
        :param pulumi.Input[str] user_pool_id: The user pool ID.
        :param pulumi.Input['RiskConfigurationAccountTakeoverRiskConfigurationArgs'] account_takeover_risk_configuration: The account takeover risk configuration. See details below.
        :param pulumi.Input[str] client_id: The app client ID. When the client ID is not provided, the same risk configuration is applied to all the clients in the User Pool.
        :param pulumi.Input['RiskConfigurationCompromisedCredentialsRiskConfigurationArgs'] compromised_credentials_risk_configuration: The compromised credentials risk configuration. See details below.
        :param pulumi.Input['RiskConfigurationRiskExceptionConfigurationArgs'] risk_exception_configuration: The configuration to override the risk decision. See details below.
        """
        pulumi.set(__self__, "user_pool_id", user_pool_id)
        if account_takeover_risk_configuration is not None:
            pulumi.set(__self__, "account_takeover_risk_configuration", account_takeover_risk_configuration)
        if client_id is not None:
            pulumi.set(__self__, "client_id", client_id)
        if compromised_credentials_risk_configuration is not None:
            pulumi.set(__self__, "compromised_credentials_risk_configuration", compromised_credentials_risk_configuration)
        if risk_exception_configuration is not None:
            pulumi.set(__self__, "risk_exception_configuration", risk_exception_configuration)

    @property
    @pulumi.getter(name="userPoolId")
    def user_pool_id(self) -> pulumi.Input[str]:
        """
        The user pool ID.
        """
        return pulumi.get(self, "user_pool_id")

    @user_pool_id.setter
    def user_pool_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_pool_id", value)

    @property
    @pulumi.getter(name="accountTakeoverRiskConfiguration")
    def account_takeover_risk_configuration(self) -> Optional[pulumi.Input['RiskConfigurationAccountTakeoverRiskConfigurationArgs']]:
        """
        The account takeover risk configuration. See details below.
        """
        return pulumi.get(self, "account_takeover_risk_configuration")

    @account_takeover_risk_configuration.setter
    def account_takeover_risk_configuration(self, value: Optional[pulumi.Input['RiskConfigurationAccountTakeoverRiskConfigurationArgs']]):
        pulumi.set(self, "account_takeover_risk_configuration", value)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> Optional[pulumi.Input[str]]:
        """
        The app client ID. When the client ID is not provided, the same risk configuration is applied to all the clients in the User Pool.
        """
        return pulumi.get(self, "client_id")

    @client_id.setter
    def client_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_id", value)

    @property
    @pulumi.getter(name="compromisedCredentialsRiskConfiguration")
    def compromised_credentials_risk_configuration(self) -> Optional[pulumi.Input['RiskConfigurationCompromisedCredentialsRiskConfigurationArgs']]:
        """
        The compromised credentials risk configuration. See details below.
        """
        return pulumi.get(self, "compromised_credentials_risk_configuration")

    @compromised_credentials_risk_configuration.setter
    def compromised_credentials_risk_configuration(self, value: Optional[pulumi.Input['RiskConfigurationCompromisedCredentialsRiskConfigurationArgs']]):
        pulumi.set(self, "compromised_credentials_risk_configuration", value)

    @property
    @pulumi.getter(name="riskExceptionConfiguration")
    def risk_exception_configuration(self) -> Optional[pulumi.Input['RiskConfigurationRiskExceptionConfigurationArgs']]:
        """
        The configuration to override the risk decision. See details below.
        """
        return pulumi.get(self, "risk_exception_configuration")

    @risk_exception_configuration.setter
    def risk_exception_configuration(self, value: Optional[pulumi.Input['RiskConfigurationRiskExceptionConfigurationArgs']]):
        pulumi.set(self, "risk_exception_configuration", value)


@pulumi.input_type
class _RiskConfigurationState:
    def __init__(__self__, *,
                 account_takeover_risk_configuration: Optional[pulumi.Input['RiskConfigurationAccountTakeoverRiskConfigurationArgs']] = None,
                 client_id: Optional[pulumi.Input[str]] = None,
                 compromised_credentials_risk_configuration: Optional[pulumi.Input['RiskConfigurationCompromisedCredentialsRiskConfigurationArgs']] = None,
                 risk_exception_configuration: Optional[pulumi.Input['RiskConfigurationRiskExceptionConfigurationArgs']] = None,
                 user_pool_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering RiskConfiguration resources.
        :param pulumi.Input['RiskConfigurationAccountTakeoverRiskConfigurationArgs'] account_takeover_risk_configuration: The account takeover risk configuration. See details below.
        :param pulumi.Input[str] client_id: The app client ID. When the client ID is not provided, the same risk configuration is applied to all the clients in the User Pool.
        :param pulumi.Input['RiskConfigurationCompromisedCredentialsRiskConfigurationArgs'] compromised_credentials_risk_configuration: The compromised credentials risk configuration. See details below.
        :param pulumi.Input['RiskConfigurationRiskExceptionConfigurationArgs'] risk_exception_configuration: The configuration to override the risk decision. See details below.
        :param pulumi.Input[str] user_pool_id: The user pool ID.
        """
        if account_takeover_risk_configuration is not None:
            pulumi.set(__self__, "account_takeover_risk_configuration", account_takeover_risk_configuration)
        if client_id is not None:
            pulumi.set(__self__, "client_id", client_id)
        if compromised_credentials_risk_configuration is not None:
            pulumi.set(__self__, "compromised_credentials_risk_configuration", compromised_credentials_risk_configuration)
        if risk_exception_configuration is not None:
            pulumi.set(__self__, "risk_exception_configuration", risk_exception_configuration)
        if user_pool_id is not None:
            pulumi.set(__self__, "user_pool_id", user_pool_id)

    @property
    @pulumi.getter(name="accountTakeoverRiskConfiguration")
    def account_takeover_risk_configuration(self) -> Optional[pulumi.Input['RiskConfigurationAccountTakeoverRiskConfigurationArgs']]:
        """
        The account takeover risk configuration. See details below.
        """
        return pulumi.get(self, "account_takeover_risk_configuration")

    @account_takeover_risk_configuration.setter
    def account_takeover_risk_configuration(self, value: Optional[pulumi.Input['RiskConfigurationAccountTakeoverRiskConfigurationArgs']]):
        pulumi.set(self, "account_takeover_risk_configuration", value)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> Optional[pulumi.Input[str]]:
        """
        The app client ID. When the client ID is not provided, the same risk configuration is applied to all the clients in the User Pool.
        """
        return pulumi.get(self, "client_id")

    @client_id.setter
    def client_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_id", value)

    @property
    @pulumi.getter(name="compromisedCredentialsRiskConfiguration")
    def compromised_credentials_risk_configuration(self) -> Optional[pulumi.Input['RiskConfigurationCompromisedCredentialsRiskConfigurationArgs']]:
        """
        The compromised credentials risk configuration. See details below.
        """
        return pulumi.get(self, "compromised_credentials_risk_configuration")

    @compromised_credentials_risk_configuration.setter
    def compromised_credentials_risk_configuration(self, value: Optional[pulumi.Input['RiskConfigurationCompromisedCredentialsRiskConfigurationArgs']]):
        pulumi.set(self, "compromised_credentials_risk_configuration", value)

    @property
    @pulumi.getter(name="riskExceptionConfiguration")
    def risk_exception_configuration(self) -> Optional[pulumi.Input['RiskConfigurationRiskExceptionConfigurationArgs']]:
        """
        The configuration to override the risk decision. See details below.
        """
        return pulumi.get(self, "risk_exception_configuration")

    @risk_exception_configuration.setter
    def risk_exception_configuration(self, value: Optional[pulumi.Input['RiskConfigurationRiskExceptionConfigurationArgs']]):
        pulumi.set(self, "risk_exception_configuration", value)

    @property
    @pulumi.getter(name="userPoolId")
    def user_pool_id(self) -> Optional[pulumi.Input[str]]:
        """
        The user pool ID.
        """
        return pulumi.get(self, "user_pool_id")

    @user_pool_id.setter
    def user_pool_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_pool_id", value)


class RiskConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_takeover_risk_configuration: Optional[pulumi.Input[pulumi.InputType['RiskConfigurationAccountTakeoverRiskConfigurationArgs']]] = None,
                 client_id: Optional[pulumi.Input[str]] = None,
                 compromised_credentials_risk_configuration: Optional[pulumi.Input[pulumi.InputType['RiskConfigurationCompromisedCredentialsRiskConfigurationArgs']]] = None,
                 risk_exception_configuration: Optional[pulumi.Input[pulumi.InputType['RiskConfigurationRiskExceptionConfigurationArgs']]] = None,
                 user_pool_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Cognito Risk Configuration resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.cognito.RiskConfiguration("example",
            user_pool_id=aws_cognito_user_pool["example"]["id"],
            risk_exception_configuration=aws.cognito.RiskConfigurationRiskExceptionConfigurationArgs(
                blocked_ip_range_lists=["10.10.10.10/32"],
            ))
        ```

        ## Import

        Cognito Risk Configurations can be imported using the `id`, e.g.,

        ```sh
         $ pulumi import aws:cognito/riskConfiguration:RiskConfiguration main example
        ```

        ```sh
         $ pulumi import aws:cognito/riskConfiguration:RiskConfiguration main example:example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['RiskConfigurationAccountTakeoverRiskConfigurationArgs']] account_takeover_risk_configuration: The account takeover risk configuration. See details below.
        :param pulumi.Input[str] client_id: The app client ID. When the client ID is not provided, the same risk configuration is applied to all the clients in the User Pool.
        :param pulumi.Input[pulumi.InputType['RiskConfigurationCompromisedCredentialsRiskConfigurationArgs']] compromised_credentials_risk_configuration: The compromised credentials risk configuration. See details below.
        :param pulumi.Input[pulumi.InputType['RiskConfigurationRiskExceptionConfigurationArgs']] risk_exception_configuration: The configuration to override the risk decision. See details below.
        :param pulumi.Input[str] user_pool_id: The user pool ID.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RiskConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Cognito Risk Configuration resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.cognito.RiskConfiguration("example",
            user_pool_id=aws_cognito_user_pool["example"]["id"],
            risk_exception_configuration=aws.cognito.RiskConfigurationRiskExceptionConfigurationArgs(
                blocked_ip_range_lists=["10.10.10.10/32"],
            ))
        ```

        ## Import

        Cognito Risk Configurations can be imported using the `id`, e.g.,

        ```sh
         $ pulumi import aws:cognito/riskConfiguration:RiskConfiguration main example
        ```

        ```sh
         $ pulumi import aws:cognito/riskConfiguration:RiskConfiguration main example:example
        ```

        :param str resource_name: The name of the resource.
        :param RiskConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RiskConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_takeover_risk_configuration: Optional[pulumi.Input[pulumi.InputType['RiskConfigurationAccountTakeoverRiskConfigurationArgs']]] = None,
                 client_id: Optional[pulumi.Input[str]] = None,
                 compromised_credentials_risk_configuration: Optional[pulumi.Input[pulumi.InputType['RiskConfigurationCompromisedCredentialsRiskConfigurationArgs']]] = None,
                 risk_exception_configuration: Optional[pulumi.Input[pulumi.InputType['RiskConfigurationRiskExceptionConfigurationArgs']]] = None,
                 user_pool_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RiskConfigurationArgs.__new__(RiskConfigurationArgs)

            __props__.__dict__["account_takeover_risk_configuration"] = account_takeover_risk_configuration
            __props__.__dict__["client_id"] = client_id
            __props__.__dict__["compromised_credentials_risk_configuration"] = compromised_credentials_risk_configuration
            __props__.__dict__["risk_exception_configuration"] = risk_exception_configuration
            if user_pool_id is None and not opts.urn:
                raise TypeError("Missing required property 'user_pool_id'")
            __props__.__dict__["user_pool_id"] = user_pool_id
        super(RiskConfiguration, __self__).__init__(
            'aws:cognito/riskConfiguration:RiskConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            account_takeover_risk_configuration: Optional[pulumi.Input[pulumi.InputType['RiskConfigurationAccountTakeoverRiskConfigurationArgs']]] = None,
            client_id: Optional[pulumi.Input[str]] = None,
            compromised_credentials_risk_configuration: Optional[pulumi.Input[pulumi.InputType['RiskConfigurationCompromisedCredentialsRiskConfigurationArgs']]] = None,
            risk_exception_configuration: Optional[pulumi.Input[pulumi.InputType['RiskConfigurationRiskExceptionConfigurationArgs']]] = None,
            user_pool_id: Optional[pulumi.Input[str]] = None) -> 'RiskConfiguration':
        """
        Get an existing RiskConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['RiskConfigurationAccountTakeoverRiskConfigurationArgs']] account_takeover_risk_configuration: The account takeover risk configuration. See details below.
        :param pulumi.Input[str] client_id: The app client ID. When the client ID is not provided, the same risk configuration is applied to all the clients in the User Pool.
        :param pulumi.Input[pulumi.InputType['RiskConfigurationCompromisedCredentialsRiskConfigurationArgs']] compromised_credentials_risk_configuration: The compromised credentials risk configuration. See details below.
        :param pulumi.Input[pulumi.InputType['RiskConfigurationRiskExceptionConfigurationArgs']] risk_exception_configuration: The configuration to override the risk decision. See details below.
        :param pulumi.Input[str] user_pool_id: The user pool ID.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RiskConfigurationState.__new__(_RiskConfigurationState)

        __props__.__dict__["account_takeover_risk_configuration"] = account_takeover_risk_configuration
        __props__.__dict__["client_id"] = client_id
        __props__.__dict__["compromised_credentials_risk_configuration"] = compromised_credentials_risk_configuration
        __props__.__dict__["risk_exception_configuration"] = risk_exception_configuration
        __props__.__dict__["user_pool_id"] = user_pool_id
        return RiskConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountTakeoverRiskConfiguration")
    def account_takeover_risk_configuration(self) -> pulumi.Output[Optional['outputs.RiskConfigurationAccountTakeoverRiskConfiguration']]:
        """
        The account takeover risk configuration. See details below.
        """
        return pulumi.get(self, "account_takeover_risk_configuration")

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> pulumi.Output[Optional[str]]:
        """
        The app client ID. When the client ID is not provided, the same risk configuration is applied to all the clients in the User Pool.
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="compromisedCredentialsRiskConfiguration")
    def compromised_credentials_risk_configuration(self) -> pulumi.Output[Optional['outputs.RiskConfigurationCompromisedCredentialsRiskConfiguration']]:
        """
        The compromised credentials risk configuration. See details below.
        """
        return pulumi.get(self, "compromised_credentials_risk_configuration")

    @property
    @pulumi.getter(name="riskExceptionConfiguration")
    def risk_exception_configuration(self) -> pulumi.Output[Optional['outputs.RiskConfigurationRiskExceptionConfiguration']]:
        """
        The configuration to override the risk decision. See details below.
        """
        return pulumi.get(self, "risk_exception_configuration")

    @property
    @pulumi.getter(name="userPoolId")
    def user_pool_id(self) -> pulumi.Output[str]:
        """
        The user pool ID.
        """
        return pulumi.get(self, "user_pool_id")

