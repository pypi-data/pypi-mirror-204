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
    'GetFirehoseDeliveryStreamResult',
    'AwaitableGetFirehoseDeliveryStreamResult',
    'get_firehose_delivery_stream',
    'get_firehose_delivery_stream_output',
]

@pulumi.output_type
class GetFirehoseDeliveryStreamResult:
    """
    A collection of values returned by getFirehoseDeliveryStream.
    """
    def __init__(__self__, arn=None, id=None, name=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the Kinesis Stream (same as id).
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")


class AwaitableGetFirehoseDeliveryStreamResult(GetFirehoseDeliveryStreamResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFirehoseDeliveryStreamResult(
            arn=self.arn,
            id=self.id,
            name=self.name)


def get_firehose_delivery_stream(name: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFirehoseDeliveryStreamResult:
    """
    Use this data source to get information about a Kinesis Firehose Delivery Stream for use in other resources.

    For more details, see the [Amazon Kinesis Firehose Documentation](https://aws.amazon.com/documentation/firehose/).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    stream = aws.kinesis.get_firehose_delivery_stream(name="stream-name")
    ```


    :param str name: Name of the Kinesis Stream.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:kinesis/getFirehoseDeliveryStream:getFirehoseDeliveryStream', __args__, opts=opts, typ=GetFirehoseDeliveryStreamResult).value

    return AwaitableGetFirehoseDeliveryStreamResult(
        arn=__ret__.arn,
        id=__ret__.id,
        name=__ret__.name)


@_utilities.lift_output_func(get_firehose_delivery_stream)
def get_firehose_delivery_stream_output(name: Optional[pulumi.Input[str]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFirehoseDeliveryStreamResult]:
    """
    Use this data source to get information about a Kinesis Firehose Delivery Stream for use in other resources.

    For more details, see the [Amazon Kinesis Firehose Documentation](https://aws.amazon.com/documentation/firehose/).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    stream = aws.kinesis.get_firehose_delivery_stream(name="stream-name")
    ```


    :param str name: Name of the Kinesis Stream.
    """
    ...
