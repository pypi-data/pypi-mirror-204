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

__all__ = [
    'GetInstanceTypeOfferingsResult',
    'AwaitableGetInstanceTypeOfferingsResult',
    'get_instance_type_offerings',
    'get_instance_type_offerings_output',
]

@pulumi.output_type
class GetInstanceTypeOfferingsResult:
    """
    A collection of values returned by getInstanceTypeOfferings.
    """
    def __init__(__self__, filters=None, id=None, instance_types=None, location_type=None, location_types=None, locations=None):
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance_types and not isinstance(instance_types, list):
            raise TypeError("Expected argument 'instance_types' to be a list")
        pulumi.set(__self__, "instance_types", instance_types)
        if location_type and not isinstance(location_type, str):
            raise TypeError("Expected argument 'location_type' to be a str")
        pulumi.set(__self__, "location_type", location_type)
        if location_types and not isinstance(location_types, list):
            raise TypeError("Expected argument 'location_types' to be a list")
        pulumi.set(__self__, "location_types", location_types)
        if locations and not isinstance(locations, list):
            raise TypeError("Expected argument 'locations' to be a list")
        pulumi.set(__self__, "locations", locations)

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetInstanceTypeOfferingsFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="instanceTypes")
    def instance_types(self) -> Sequence[str]:
        """
        List of EC2 Instance Types.
        """
        return pulumi.get(self, "instance_types")

    @property
    @pulumi.getter(name="locationType")
    def location_type(self) -> Optional[str]:
        return pulumi.get(self, "location_type")

    @property
    @pulumi.getter(name="locationTypes")
    def location_types(self) -> Sequence[str]:
        """
        List of location types.
        """
        return pulumi.get(self, "location_types")

    @property
    @pulumi.getter
    def locations(self) -> Sequence[str]:
        """
        List of locations.
        """
        return pulumi.get(self, "locations")


class AwaitableGetInstanceTypeOfferingsResult(GetInstanceTypeOfferingsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInstanceTypeOfferingsResult(
            filters=self.filters,
            id=self.id,
            instance_types=self.instance_types,
            location_type=self.location_type,
            location_types=self.location_types,
            locations=self.locations)


def get_instance_type_offerings(filters: Optional[Sequence[pulumi.InputType['GetInstanceTypeOfferingsFilterArgs']]] = None,
                                location_type: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInstanceTypeOfferingsResult:
    """
    Information about EC2 Instance Type Offerings.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2.get_instance_type_offerings(filters=[
            aws.ec2.GetInstanceTypeOfferingsFilterArgs(
                name="instance-type",
                values=[
                    "t2.micro",
                    "t3.micro",
                ],
            ),
            aws.ec2.GetInstanceTypeOfferingsFilterArgs(
                name="location",
                values=["usw2-az4"],
            ),
        ],
        location_type="availability-zone-id")
    ```


    :param Sequence[pulumi.InputType['GetInstanceTypeOfferingsFilterArgs']] filters: One or more configuration blocks containing name-values filters. See the [EC2 API Reference](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeInstanceTypeOfferings.html) for supported filters. Detailed below.
    :param str location_type: Location type. Defaults to `region`. Valid values: `availability-zone`, `availability-zone-id`, and `region`.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['locationType'] = location_type
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ec2/getInstanceTypeOfferings:getInstanceTypeOfferings', __args__, opts=opts, typ=GetInstanceTypeOfferingsResult).value

    return AwaitableGetInstanceTypeOfferingsResult(
        filters=__ret__.filters,
        id=__ret__.id,
        instance_types=__ret__.instance_types,
        location_type=__ret__.location_type,
        location_types=__ret__.location_types,
        locations=__ret__.locations)


@_utilities.lift_output_func(get_instance_type_offerings)
def get_instance_type_offerings_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetInstanceTypeOfferingsFilterArgs']]]]] = None,
                                       location_type: Optional[pulumi.Input[Optional[str]]] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetInstanceTypeOfferingsResult]:
    """
    Information about EC2 Instance Type Offerings.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2.get_instance_type_offerings(filters=[
            aws.ec2.GetInstanceTypeOfferingsFilterArgs(
                name="instance-type",
                values=[
                    "t2.micro",
                    "t3.micro",
                ],
            ),
            aws.ec2.GetInstanceTypeOfferingsFilterArgs(
                name="location",
                values=["usw2-az4"],
            ),
        ],
        location_type="availability-zone-id")
    ```


    :param Sequence[pulumi.InputType['GetInstanceTypeOfferingsFilterArgs']] filters: One or more configuration blocks containing name-values filters. See the [EC2 API Reference](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeInstanceTypeOfferings.html) for supported filters. Detailed below.
    :param str location_type: Location type. Defaults to `region`. Valid values: `availability-zone`, `availability-zone-id`, and `region`.
    """
    ...
