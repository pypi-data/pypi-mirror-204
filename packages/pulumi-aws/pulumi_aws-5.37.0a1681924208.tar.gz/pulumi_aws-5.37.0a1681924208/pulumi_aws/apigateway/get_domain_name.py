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

__all__ = [
    'GetDomainNameResult',
    'AwaitableGetDomainNameResult',
    'get_domain_name',
    'get_domain_name_output',
]

@pulumi.output_type
class GetDomainNameResult:
    """
    A collection of values returned by getDomainName.
    """
    def __init__(__self__, arn=None, certificate_arn=None, certificate_name=None, certificate_upload_date=None, cloudfront_domain_name=None, cloudfront_zone_id=None, domain_name=None, endpoint_configurations=None, id=None, regional_certificate_arn=None, regional_certificate_name=None, regional_domain_name=None, regional_zone_id=None, security_policy=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if certificate_arn and not isinstance(certificate_arn, str):
            raise TypeError("Expected argument 'certificate_arn' to be a str")
        pulumi.set(__self__, "certificate_arn", certificate_arn)
        if certificate_name and not isinstance(certificate_name, str):
            raise TypeError("Expected argument 'certificate_name' to be a str")
        pulumi.set(__self__, "certificate_name", certificate_name)
        if certificate_upload_date and not isinstance(certificate_upload_date, str):
            raise TypeError("Expected argument 'certificate_upload_date' to be a str")
        pulumi.set(__self__, "certificate_upload_date", certificate_upload_date)
        if cloudfront_domain_name and not isinstance(cloudfront_domain_name, str):
            raise TypeError("Expected argument 'cloudfront_domain_name' to be a str")
        pulumi.set(__self__, "cloudfront_domain_name", cloudfront_domain_name)
        if cloudfront_zone_id and not isinstance(cloudfront_zone_id, str):
            raise TypeError("Expected argument 'cloudfront_zone_id' to be a str")
        pulumi.set(__self__, "cloudfront_zone_id", cloudfront_zone_id)
        if domain_name and not isinstance(domain_name, str):
            raise TypeError("Expected argument 'domain_name' to be a str")
        pulumi.set(__self__, "domain_name", domain_name)
        if endpoint_configurations and not isinstance(endpoint_configurations, list):
            raise TypeError("Expected argument 'endpoint_configurations' to be a list")
        pulumi.set(__self__, "endpoint_configurations", endpoint_configurations)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if regional_certificate_arn and not isinstance(regional_certificate_arn, str):
            raise TypeError("Expected argument 'regional_certificate_arn' to be a str")
        pulumi.set(__self__, "regional_certificate_arn", regional_certificate_arn)
        if regional_certificate_name and not isinstance(regional_certificate_name, str):
            raise TypeError("Expected argument 'regional_certificate_name' to be a str")
        pulumi.set(__self__, "regional_certificate_name", regional_certificate_name)
        if regional_domain_name and not isinstance(regional_domain_name, str):
            raise TypeError("Expected argument 'regional_domain_name' to be a str")
        pulumi.set(__self__, "regional_domain_name", regional_domain_name)
        if regional_zone_id and not isinstance(regional_zone_id, str):
            raise TypeError("Expected argument 'regional_zone_id' to be a str")
        pulumi.set(__self__, "regional_zone_id", regional_zone_id)
        if security_policy and not isinstance(security_policy, str):
            raise TypeError("Expected argument 'security_policy' to be a str")
        pulumi.set(__self__, "security_policy", security_policy)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the found custom domain name.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="certificateArn")
    def certificate_arn(self) -> str:
        """
        ARN for an AWS-managed certificate that is used by edge-optimized endpoint for this domain name.
        """
        return pulumi.get(self, "certificate_arn")

    @property
    @pulumi.getter(name="certificateName")
    def certificate_name(self) -> str:
        """
        Name of the certificate that is used by edge-optimized endpoint for this domain name.
        """
        return pulumi.get(self, "certificate_name")

    @property
    @pulumi.getter(name="certificateUploadDate")
    def certificate_upload_date(self) -> str:
        """
        Upload date associated with the domain certificate.
        """
        return pulumi.get(self, "certificate_upload_date")

    @property
    @pulumi.getter(name="cloudfrontDomainName")
    def cloudfront_domain_name(self) -> str:
        """
        Hostname created by Cloudfront to represent the distribution that implements this domain name mapping.
        """
        return pulumi.get(self, "cloudfront_domain_name")

    @property
    @pulumi.getter(name="cloudfrontZoneId")
    def cloudfront_zone_id(self) -> str:
        """
        For convenience, the hosted zone ID (`Z2FDTNDATAQYW2`) that can be used to create a Route53 alias record for the distribution.
        """
        return pulumi.get(self, "cloudfront_zone_id")

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> str:
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter(name="endpointConfigurations")
    def endpoint_configurations(self) -> Sequence['outputs.GetDomainNameEndpointConfigurationResult']:
        """
        List of objects with the endpoint configuration of this domain name.
        """
        return pulumi.get(self, "endpoint_configurations")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="regionalCertificateArn")
    def regional_certificate_arn(self) -> str:
        """
        ARN for an AWS-managed certificate that is used for validating the regional domain name.
        """
        return pulumi.get(self, "regional_certificate_arn")

    @property
    @pulumi.getter(name="regionalCertificateName")
    def regional_certificate_name(self) -> str:
        """
        User-friendly name of the certificate that is used by regional endpoint for this domain name.
        """
        return pulumi.get(self, "regional_certificate_name")

    @property
    @pulumi.getter(name="regionalDomainName")
    def regional_domain_name(self) -> str:
        """
        Hostname for the custom domain's regional endpoint.
        """
        return pulumi.get(self, "regional_domain_name")

    @property
    @pulumi.getter(name="regionalZoneId")
    def regional_zone_id(self) -> str:
        """
        Hosted zone ID that can be used to create a Route53 alias record for the regional endpoint.
        """
        return pulumi.get(self, "regional_zone_id")

    @property
    @pulumi.getter(name="securityPolicy")
    def security_policy(self) -> str:
        """
        Security policy for the domain name.
        """
        return pulumi.get(self, "security_policy")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Key-value map of tags for the resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetDomainNameResult(GetDomainNameResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDomainNameResult(
            arn=self.arn,
            certificate_arn=self.certificate_arn,
            certificate_name=self.certificate_name,
            certificate_upload_date=self.certificate_upload_date,
            cloudfront_domain_name=self.cloudfront_domain_name,
            cloudfront_zone_id=self.cloudfront_zone_id,
            domain_name=self.domain_name,
            endpoint_configurations=self.endpoint_configurations,
            id=self.id,
            regional_certificate_arn=self.regional_certificate_arn,
            regional_certificate_name=self.regional_certificate_name,
            regional_domain_name=self.regional_domain_name,
            regional_zone_id=self.regional_zone_id,
            security_policy=self.security_policy,
            tags=self.tags)


def get_domain_name(domain_name: Optional[str] = None,
                    tags: Optional[Mapping[str, str]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDomainNameResult:
    """
    Use this data source to get the custom domain name for use with AWS API Gateway.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.apigateway.get_domain_name(domain_name="api.example.com")
    ```


    :param str domain_name: Fully-qualified domain name to look up. If no domain name is found, an error will be returned.
    :param Mapping[str, str] tags: Key-value map of tags for the resource.
    """
    __args__ = dict()
    __args__['domainName'] = domain_name
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:apigateway/getDomainName:getDomainName', __args__, opts=opts, typ=GetDomainNameResult).value

    return AwaitableGetDomainNameResult(
        arn=__ret__.arn,
        certificate_arn=__ret__.certificate_arn,
        certificate_name=__ret__.certificate_name,
        certificate_upload_date=__ret__.certificate_upload_date,
        cloudfront_domain_name=__ret__.cloudfront_domain_name,
        cloudfront_zone_id=__ret__.cloudfront_zone_id,
        domain_name=__ret__.domain_name,
        endpoint_configurations=__ret__.endpoint_configurations,
        id=__ret__.id,
        regional_certificate_arn=__ret__.regional_certificate_arn,
        regional_certificate_name=__ret__.regional_certificate_name,
        regional_domain_name=__ret__.regional_domain_name,
        regional_zone_id=__ret__.regional_zone_id,
        security_policy=__ret__.security_policy,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_domain_name)
def get_domain_name_output(domain_name: Optional[pulumi.Input[str]] = None,
                           tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDomainNameResult]:
    """
    Use this data source to get the custom domain name for use with AWS API Gateway.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.apigateway.get_domain_name(domain_name="api.example.com")
    ```


    :param str domain_name: Fully-qualified domain name to look up. If no domain name is found, an error will be returned.
    :param Mapping[str, str] tags: Key-value map of tags for the resource.
    """
    ...
