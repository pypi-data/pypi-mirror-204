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
    'LoggingConfigurationDestinationConfiguration',
    'LoggingConfigurationDestinationConfigurationCloudwatchLogs',
    'LoggingConfigurationDestinationConfigurationFirehose',
    'LoggingConfigurationDestinationConfigurationS3',
    'RoomMessageReviewHandler',
]

@pulumi.output_type
class LoggingConfigurationDestinationConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cloudwatchLogs":
            suggest = "cloudwatch_logs"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LoggingConfigurationDestinationConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LoggingConfigurationDestinationConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LoggingConfigurationDestinationConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cloudwatch_logs: Optional['outputs.LoggingConfigurationDestinationConfigurationCloudwatchLogs'] = None,
                 firehose: Optional['outputs.LoggingConfigurationDestinationConfigurationFirehose'] = None,
                 s3: Optional['outputs.LoggingConfigurationDestinationConfigurationS3'] = None):
        """
        :param 'LoggingConfigurationDestinationConfigurationCloudwatchLogsArgs' cloudwatch_logs: An Amazon CloudWatch Logs destination configuration where chat activity will be logged.
        :param 'LoggingConfigurationDestinationConfigurationFirehoseArgs' firehose: An Amazon Kinesis Data Firehose destination configuration where chat activity will be logged.
        :param 'LoggingConfigurationDestinationConfigurationS3Args' s3: An Amazon S3 destination configuration where chat activity will be logged.
        """
        if cloudwatch_logs is not None:
            pulumi.set(__self__, "cloudwatch_logs", cloudwatch_logs)
        if firehose is not None:
            pulumi.set(__self__, "firehose", firehose)
        if s3 is not None:
            pulumi.set(__self__, "s3", s3)

    @property
    @pulumi.getter(name="cloudwatchLogs")
    def cloudwatch_logs(self) -> Optional['outputs.LoggingConfigurationDestinationConfigurationCloudwatchLogs']:
        """
        An Amazon CloudWatch Logs destination configuration where chat activity will be logged.
        """
        return pulumi.get(self, "cloudwatch_logs")

    @property
    @pulumi.getter
    def firehose(self) -> Optional['outputs.LoggingConfigurationDestinationConfigurationFirehose']:
        """
        An Amazon Kinesis Data Firehose destination configuration where chat activity will be logged.
        """
        return pulumi.get(self, "firehose")

    @property
    @pulumi.getter
    def s3(self) -> Optional['outputs.LoggingConfigurationDestinationConfigurationS3']:
        """
        An Amazon S3 destination configuration where chat activity will be logged.
        """
        return pulumi.get(self, "s3")


@pulumi.output_type
class LoggingConfigurationDestinationConfigurationCloudwatchLogs(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "logGroupName":
            suggest = "log_group_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LoggingConfigurationDestinationConfigurationCloudwatchLogs. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LoggingConfigurationDestinationConfigurationCloudwatchLogs.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LoggingConfigurationDestinationConfigurationCloudwatchLogs.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 log_group_name: str):
        """
        :param str log_group_name: Name of the Amazon Cloudwatch Logs destination where chat activity will be logged.
        """
        pulumi.set(__self__, "log_group_name", log_group_name)

    @property
    @pulumi.getter(name="logGroupName")
    def log_group_name(self) -> str:
        """
        Name of the Amazon Cloudwatch Logs destination where chat activity will be logged.
        """
        return pulumi.get(self, "log_group_name")


@pulumi.output_type
class LoggingConfigurationDestinationConfigurationFirehose(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "deliveryStreamName":
            suggest = "delivery_stream_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LoggingConfigurationDestinationConfigurationFirehose. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LoggingConfigurationDestinationConfigurationFirehose.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LoggingConfigurationDestinationConfigurationFirehose.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 delivery_stream_name: str):
        """
        :param str delivery_stream_name: Name of the Amazon Kinesis Firehose delivery stream where chat activity will be logged.
        """
        pulumi.set(__self__, "delivery_stream_name", delivery_stream_name)

    @property
    @pulumi.getter(name="deliveryStreamName")
    def delivery_stream_name(self) -> str:
        """
        Name of the Amazon Kinesis Firehose delivery stream where chat activity will be logged.
        """
        return pulumi.get(self, "delivery_stream_name")


@pulumi.output_type
class LoggingConfigurationDestinationConfigurationS3(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "bucketName":
            suggest = "bucket_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LoggingConfigurationDestinationConfigurationS3. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LoggingConfigurationDestinationConfigurationS3.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LoggingConfigurationDestinationConfigurationS3.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 bucket_name: str):
        """
        :param str bucket_name: Name of the Amazon S3 bucket where chat activity will be logged.
        """
        pulumi.set(__self__, "bucket_name", bucket_name)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> str:
        """
        Name of the Amazon S3 bucket where chat activity will be logged.
        """
        return pulumi.get(self, "bucket_name")


@pulumi.output_type
class RoomMessageReviewHandler(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "fallbackResult":
            suggest = "fallback_result"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RoomMessageReviewHandler. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RoomMessageReviewHandler.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RoomMessageReviewHandler.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 fallback_result: Optional[str] = None,
                 uri: Optional[str] = None):
        """
        :param str fallback_result: The fallback behavior (whether the message
               is allowed or denied) if the handler does not return a valid response,
               encounters an error, or times out. Valid values: `ALLOW`, `DENY`.
        :param str uri: ARN of the lambda message review handler function.
        """
        if fallback_result is not None:
            pulumi.set(__self__, "fallback_result", fallback_result)
        if uri is not None:
            pulumi.set(__self__, "uri", uri)

    @property
    @pulumi.getter(name="fallbackResult")
    def fallback_result(self) -> Optional[str]:
        """
        The fallback behavior (whether the message
        is allowed or denied) if the handler does not return a valid response,
        encounters an error, or times out. Valid values: `ALLOW`, `DENY`.
        """
        return pulumi.get(self, "fallback_result")

    @property
    @pulumi.getter
    def uri(self) -> Optional[str]:
        """
        ARN of the lambda message review handler function.
        """
        return pulumi.get(self, "uri")


