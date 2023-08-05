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
    'GetVpcPeeringConnectionsResult',
    'AwaitableGetVpcPeeringConnectionsResult',
    'get_vpc_peering_connections',
    'get_vpc_peering_connections_output',
]

@pulumi.output_type
class GetVpcPeeringConnectionsResult:
    """
    A collection of values returned by getVpcPeeringConnections.
    """
    def __init__(__self__, filters=None, id=None, ids=None, tags=None):
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetVpcPeeringConnectionsFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ids(self) -> Sequence[str]:
        """
        IDs of the VPC Peering Connections.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")


class AwaitableGetVpcPeeringConnectionsResult(GetVpcPeeringConnectionsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVpcPeeringConnectionsResult(
            filters=self.filters,
            id=self.id,
            ids=self.ids,
            tags=self.tags)


def get_vpc_peering_connections(filters: Optional[Sequence[pulumi.InputType['GetVpcPeeringConnectionsFilterArgs']]] = None,
                                tags: Optional[Mapping[str, str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVpcPeeringConnectionsResult:
    """
    Use this data source to get IDs of Amazon VPC peering connections
    To get more details on each connection, use the data resource ec2.VpcPeeringConnection

    Note: To use this data source in a count, the resources should exist before trying to access
    the data source.


    :param Sequence[pulumi.InputType['GetVpcPeeringConnectionsFilterArgs']] filters: Custom filter block as described below.
    :param Mapping[str, str] tags: Mapping of tags, each pair of which must exactly match
           a pair on the desired VPC Peering Connection.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ec2/getVpcPeeringConnections:getVpcPeeringConnections', __args__, opts=opts, typ=GetVpcPeeringConnectionsResult).value

    return AwaitableGetVpcPeeringConnectionsResult(
        filters=__ret__.filters,
        id=__ret__.id,
        ids=__ret__.ids,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_vpc_peering_connections)
def get_vpc_peering_connections_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetVpcPeeringConnectionsFilterArgs']]]]] = None,
                                       tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVpcPeeringConnectionsResult]:
    """
    Use this data source to get IDs of Amazon VPC peering connections
    To get more details on each connection, use the data resource ec2.VpcPeeringConnection

    Note: To use this data source in a count, the resources should exist before trying to access
    the data source.


    :param Sequence[pulumi.InputType['GetVpcPeeringConnectionsFilterArgs']] filters: Custom filter block as described below.
    :param Mapping[str, str] tags: Mapping of tags, each pair of which must exactly match
           a pair on the desired VPC Peering Connection.
    """
    ...
