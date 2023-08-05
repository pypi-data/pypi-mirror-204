# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetServiceQuotaResult',
    'AwaitableGetServiceQuotaResult',
    'get_service_quota',
    'get_service_quota_output',
]

@pulumi.output_type
class GetServiceQuotaResult:
    """
    A collection of values returned by getServiceQuota.
    """
    def __init__(__self__, adjustable=None, arn=None, default_value=None, global_quota=None, id=None, quota_code=None, quota_name=None, service_code=None, service_name=None, value=None):
        if adjustable and not isinstance(adjustable, bool):
            raise TypeError("Expected argument 'adjustable' to be a bool")
        pulumi.set(__self__, "adjustable", adjustable)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if default_value and not isinstance(default_value, float):
            raise TypeError("Expected argument 'default_value' to be a float")
        pulumi.set(__self__, "default_value", default_value)
        if global_quota and not isinstance(global_quota, bool):
            raise TypeError("Expected argument 'global_quota' to be a bool")
        pulumi.set(__self__, "global_quota", global_quota)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if quota_code and not isinstance(quota_code, str):
            raise TypeError("Expected argument 'quota_code' to be a str")
        pulumi.set(__self__, "quota_code", quota_code)
        if quota_name and not isinstance(quota_name, str):
            raise TypeError("Expected argument 'quota_name' to be a str")
        pulumi.set(__self__, "quota_name", quota_name)
        if service_code and not isinstance(service_code, str):
            raise TypeError("Expected argument 'service_code' to be a str")
        pulumi.set(__self__, "service_code", service_code)
        if service_name and not isinstance(service_name, str):
            raise TypeError("Expected argument 'service_name' to be a str")
        pulumi.set(__self__, "service_name", service_name)
        if value and not isinstance(value, float):
            raise TypeError("Expected argument 'value' to be a float")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def adjustable(self) -> bool:
        """
        Whether the service quota is adjustable.
        """
        return pulumi.get(self, "adjustable")

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the service quota.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="defaultValue")
    def default_value(self) -> float:
        """
        Default value of the service quota.
        """
        return pulumi.get(self, "default_value")

    @property
    @pulumi.getter(name="globalQuota")
    def global_quota(self) -> bool:
        """
        Whether the service quota is global for the AWS account.
        """
        return pulumi.get(self, "global_quota")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="quotaCode")
    def quota_code(self) -> str:
        return pulumi.get(self, "quota_code")

    @property
    @pulumi.getter(name="quotaName")
    def quota_name(self) -> str:
        return pulumi.get(self, "quota_name")

    @property
    @pulumi.getter(name="serviceCode")
    def service_code(self) -> str:
        return pulumi.get(self, "service_code")

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> str:
        """
        Name of the service.
        """
        return pulumi.get(self, "service_name")

    @property
    @pulumi.getter
    def value(self) -> float:
        """
        Current value of the service quota.
        """
        return pulumi.get(self, "value")


class AwaitableGetServiceQuotaResult(GetServiceQuotaResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServiceQuotaResult(
            adjustable=self.adjustable,
            arn=self.arn,
            default_value=self.default_value,
            global_quota=self.global_quota,
            id=self.id,
            quota_code=self.quota_code,
            quota_name=self.quota_name,
            service_code=self.service_code,
            service_name=self.service_name,
            value=self.value)


def get_service_quota(quota_code: Optional[str] = None,
                      quota_name: Optional[str] = None,
                      service_code: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServiceQuotaResult:
    """
    Retrieve information about a Service Quota.

    > **NOTE:** Global quotas apply to all AWS regions, but can only be accessed in `us-east-1` in the Commercial partition or `us-gov-west-1` in the GovCloud partition. In other regions, the AWS API will return the error `The request failed because the specified service does not exist.`

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    by_quota_code = aws.servicequotas.get_service_quota(quota_code="L-F678F1CE",
        service_code="vpc")
    by_quota_name = aws.servicequotas.get_service_quota(quota_name="VPCs per Region",
        service_code="vpc")
    ```


    :param str quota_code: Quota code within the service. When configured, the data source directly looks up the service quota. Available values can be found with the [AWS CLI service-quotas list-service-quotas command](https://docs.aws.amazon.com/cli/latest/reference/service-quotas/list-service-quotas.html). One of `quota_code` or `quota_name` must be specified.
    :param str quota_name: Quota name within the service. When configured, the data source searches through all service quotas to find the matching quota name. Available values can be found with the [AWS CLI service-quotas list-service-quotas command](https://docs.aws.amazon.com/cli/latest/reference/service-quotas/list-service-quotas.html). One of `quota_name` or `quota_code` must be specified.
    :param str service_code: Service code for the quota. Available values can be found with the `servicequotas_get_service` data source or [AWS CLI service-quotas list-services command](https://docs.aws.amazon.com/cli/latest/reference/service-quotas/list-services.html).
    """
    __args__ = dict()
    __args__['quotaCode'] = quota_code
    __args__['quotaName'] = quota_name
    __args__['serviceCode'] = service_code
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:servicequotas/getServiceQuota:getServiceQuota', __args__, opts=opts, typ=GetServiceQuotaResult).value

    return AwaitableGetServiceQuotaResult(
        adjustable=__ret__.adjustable,
        arn=__ret__.arn,
        default_value=__ret__.default_value,
        global_quota=__ret__.global_quota,
        id=__ret__.id,
        quota_code=__ret__.quota_code,
        quota_name=__ret__.quota_name,
        service_code=__ret__.service_code,
        service_name=__ret__.service_name,
        value=__ret__.value)


@_utilities.lift_output_func(get_service_quota)
def get_service_quota_output(quota_code: Optional[pulumi.Input[Optional[str]]] = None,
                             quota_name: Optional[pulumi.Input[Optional[str]]] = None,
                             service_code: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetServiceQuotaResult]:
    """
    Retrieve information about a Service Quota.

    > **NOTE:** Global quotas apply to all AWS regions, but can only be accessed in `us-east-1` in the Commercial partition or `us-gov-west-1` in the GovCloud partition. In other regions, the AWS API will return the error `The request failed because the specified service does not exist.`

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    by_quota_code = aws.servicequotas.get_service_quota(quota_code="L-F678F1CE",
        service_code="vpc")
    by_quota_name = aws.servicequotas.get_service_quota(quota_name="VPCs per Region",
        service_code="vpc")
    ```


    :param str quota_code: Quota code within the service. When configured, the data source directly looks up the service quota. Available values can be found with the [AWS CLI service-quotas list-service-quotas command](https://docs.aws.amazon.com/cli/latest/reference/service-quotas/list-service-quotas.html). One of `quota_code` or `quota_name` must be specified.
    :param str quota_name: Quota name within the service. When configured, the data source searches through all service quotas to find the matching quota name. Available values can be found with the [AWS CLI service-quotas list-service-quotas command](https://docs.aws.amazon.com/cli/latest/reference/service-quotas/list-service-quotas.html). One of `quota_name` or `quota_code` must be specified.
    :param str service_code: Service code for the quota. Available values can be found with the `servicequotas_get_service` data source or [AWS CLI service-quotas list-services command](https://docs.aws.amazon.com/cli/latest/reference/service-quotas/list-services.html).
    """
    ...
