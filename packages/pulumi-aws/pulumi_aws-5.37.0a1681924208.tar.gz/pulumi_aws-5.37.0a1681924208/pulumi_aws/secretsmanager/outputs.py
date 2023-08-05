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
    'SecretReplica',
    'SecretRotationRotationRules',
    'SecretRotationRules',
    'GetSecretRotationRotationRuleResult',
    'GetSecretRotationRuleResult',
    'GetSecretsFilterResult',
]

@pulumi.output_type
class SecretReplica(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "kmsKeyId":
            suggest = "kms_key_id"
        elif key == "lastAccessedDate":
            suggest = "last_accessed_date"
        elif key == "statusMessage":
            suggest = "status_message"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SecretReplica. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SecretReplica.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SecretReplica.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 region: str,
                 kms_key_id: Optional[str] = None,
                 last_accessed_date: Optional[str] = None,
                 status: Optional[str] = None,
                 status_message: Optional[str] = None):
        """
        :param str region: Region for replicating the secret.
        :param str kms_key_id: ARN, Key ID, or Alias of the AWS KMS key within the region secret is replicated to. If one is not specified, then Secrets Manager defaults to using the AWS account's default KMS key (`aws/secretsmanager`) in the region or creates one for use if non-existent.
        :param str last_accessed_date: Date that you last accessed the secret in the Region.
        :param str status: Status can be `InProgress`, `Failed`, or `InSync`.
        :param str status_message: Message such as `Replication succeeded` or `Secret with this name already exists in this region`.
        """
        pulumi.set(__self__, "region", region)
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)
        if last_accessed_date is not None:
            pulumi.set(__self__, "last_accessed_date", last_accessed_date)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if status_message is not None:
            pulumi.set(__self__, "status_message", status_message)

    @property
    @pulumi.getter
    def region(self) -> str:
        """
        Region for replicating the secret.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[str]:
        """
        ARN, Key ID, or Alias of the AWS KMS key within the region secret is replicated to. If one is not specified, then Secrets Manager defaults to using the AWS account's default KMS key (`aws/secretsmanager`) in the region or creates one for use if non-existent.
        """
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="lastAccessedDate")
    def last_accessed_date(self) -> Optional[str]:
        """
        Date that you last accessed the secret in the Region.
        """
        return pulumi.get(self, "last_accessed_date")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        Status can be `InProgress`, `Failed`, or `InSync`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="statusMessage")
    def status_message(self) -> Optional[str]:
        """
        Message such as `Replication succeeded` or `Secret with this name already exists in this region`.
        """
        return pulumi.get(self, "status_message")


@pulumi.output_type
class SecretRotationRotationRules(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "automaticallyAfterDays":
            suggest = "automatically_after_days"
        elif key == "scheduleExpression":
            suggest = "schedule_expression"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SecretRotationRotationRules. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SecretRotationRotationRules.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SecretRotationRotationRules.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 automatically_after_days: Optional[int] = None,
                 duration: Optional[str] = None,
                 schedule_expression: Optional[str] = None):
        """
        :param int automatically_after_days: Specifies the number of days between automatic scheduled rotations of the secret. Either `automatically_after_days` or `schedule_expression` must be specified.
        :param str duration: The length of the rotation window in hours. For example, `3h` for a three hour window.
        :param str schedule_expression: A `cron()` or `rate()` expression that defines the schedule for rotating your secret. Either `automatically_after_days` or `schedule_expression` must be specified.
        """
        if automatically_after_days is not None:
            pulumi.set(__self__, "automatically_after_days", automatically_after_days)
        if duration is not None:
            pulumi.set(__self__, "duration", duration)
        if schedule_expression is not None:
            pulumi.set(__self__, "schedule_expression", schedule_expression)

    @property
    @pulumi.getter(name="automaticallyAfterDays")
    def automatically_after_days(self) -> Optional[int]:
        """
        Specifies the number of days between automatic scheduled rotations of the secret. Either `automatically_after_days` or `schedule_expression` must be specified.
        """
        return pulumi.get(self, "automatically_after_days")

    @property
    @pulumi.getter
    def duration(self) -> Optional[str]:
        """
        The length of the rotation window in hours. For example, `3h` for a three hour window.
        """
        return pulumi.get(self, "duration")

    @property
    @pulumi.getter(name="scheduleExpression")
    def schedule_expression(self) -> Optional[str]:
        """
        A `cron()` or `rate()` expression that defines the schedule for rotating your secret. Either `automatically_after_days` or `schedule_expression` must be specified.
        """
        return pulumi.get(self, "schedule_expression")


@pulumi.output_type
class SecretRotationRules(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "automaticallyAfterDays":
            suggest = "automatically_after_days"
        elif key == "scheduleExpression":
            suggest = "schedule_expression"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SecretRotationRules. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SecretRotationRules.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SecretRotationRules.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 automatically_after_days: Optional[int] = None,
                 duration: Optional[str] = None,
                 schedule_expression: Optional[str] = None):
        """
        :param int automatically_after_days: Specifies the number of days between automatic scheduled rotations of the secret.
        """
        if automatically_after_days is not None:
            pulumi.set(__self__, "automatically_after_days", automatically_after_days)
        if duration is not None:
            pulumi.set(__self__, "duration", duration)
        if schedule_expression is not None:
            pulumi.set(__self__, "schedule_expression", schedule_expression)

    @property
    @pulumi.getter(name="automaticallyAfterDays")
    def automatically_after_days(self) -> Optional[int]:
        """
        Specifies the number of days between automatic scheduled rotations of the secret.
        """
        return pulumi.get(self, "automatically_after_days")

    @property
    @pulumi.getter
    def duration(self) -> Optional[str]:
        return pulumi.get(self, "duration")

    @property
    @pulumi.getter(name="scheduleExpression")
    def schedule_expression(self) -> Optional[str]:
        return pulumi.get(self, "schedule_expression")


@pulumi.output_type
class GetSecretRotationRotationRuleResult(dict):
    def __init__(__self__, *,
                 automatically_after_days: int,
                 duration: str,
                 schedule_expression: str):
        pulumi.set(__self__, "automatically_after_days", automatically_after_days)
        pulumi.set(__self__, "duration", duration)
        pulumi.set(__self__, "schedule_expression", schedule_expression)

    @property
    @pulumi.getter(name="automaticallyAfterDays")
    def automatically_after_days(self) -> int:
        return pulumi.get(self, "automatically_after_days")

    @property
    @pulumi.getter
    def duration(self) -> str:
        return pulumi.get(self, "duration")

    @property
    @pulumi.getter(name="scheduleExpression")
    def schedule_expression(self) -> str:
        return pulumi.get(self, "schedule_expression")


@pulumi.output_type
class GetSecretRotationRuleResult(dict):
    def __init__(__self__, *,
                 automatically_after_days: int,
                 duration: str,
                 schedule_expression: str):
        pulumi.set(__self__, "automatically_after_days", automatically_after_days)
        pulumi.set(__self__, "duration", duration)
        pulumi.set(__self__, "schedule_expression", schedule_expression)

    @property
    @pulumi.getter(name="automaticallyAfterDays")
    def automatically_after_days(self) -> int:
        return pulumi.get(self, "automatically_after_days")

    @property
    @pulumi.getter
    def duration(self) -> str:
        return pulumi.get(self, "duration")

    @property
    @pulumi.getter(name="scheduleExpression")
    def schedule_expression(self) -> str:
        return pulumi.get(self, "schedule_expression")


@pulumi.output_type
class GetSecretsFilterResult(dict):
    def __init__(__self__, *,
                 name: str,
                 values: Sequence[str]):
        """
        :param str name: Name of the filter field. Valid values can be found in the [Secrets Manager ListSecrets API Reference](https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_ListSecrets.html).
        :param Sequence[str] values: Set of values that are accepted for the given filter field. Results will be selected if any given value matches.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the filter field. Valid values can be found in the [Secrets Manager ListSecrets API Reference](https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_ListSecrets.html).
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def values(self) -> Sequence[str]:
        """
        Set of values that are accepted for the given filter field. Results will be selected if any given value matches.
        """
        return pulumi.get(self, "values")


