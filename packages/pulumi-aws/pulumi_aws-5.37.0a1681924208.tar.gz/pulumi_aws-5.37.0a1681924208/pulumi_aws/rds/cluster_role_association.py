# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ClusterRoleAssociationArgs', 'ClusterRoleAssociation']

@pulumi.input_type
class ClusterRoleAssociationArgs:
    def __init__(__self__, *,
                 db_cluster_identifier: pulumi.Input[str],
                 feature_name: pulumi.Input[str],
                 role_arn: pulumi.Input[str]):
        """
        The set of arguments for constructing a ClusterRoleAssociation resource.
        :param pulumi.Input[str] db_cluster_identifier: DB Cluster Identifier to associate with the IAM Role.
        :param pulumi.Input[str] feature_name: Name of the feature for association. This can be found in the AWS documentation relevant to the integration or a full list is available in the `SupportedFeatureNames` list returned by [AWS CLI rds describe-db-engine-versions](https://docs.aws.amazon.com/cli/latest/reference/rds/describe-db-engine-versions.html).
        :param pulumi.Input[str] role_arn: Amazon Resource Name (ARN) of the IAM Role to associate with the DB Cluster.
        """
        pulumi.set(__self__, "db_cluster_identifier", db_cluster_identifier)
        pulumi.set(__self__, "feature_name", feature_name)
        pulumi.set(__self__, "role_arn", role_arn)

    @property
    @pulumi.getter(name="dbClusterIdentifier")
    def db_cluster_identifier(self) -> pulumi.Input[str]:
        """
        DB Cluster Identifier to associate with the IAM Role.
        """
        return pulumi.get(self, "db_cluster_identifier")

    @db_cluster_identifier.setter
    def db_cluster_identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "db_cluster_identifier", value)

    @property
    @pulumi.getter(name="featureName")
    def feature_name(self) -> pulumi.Input[str]:
        """
        Name of the feature for association. This can be found in the AWS documentation relevant to the integration or a full list is available in the `SupportedFeatureNames` list returned by [AWS CLI rds describe-db-engine-versions](https://docs.aws.amazon.com/cli/latest/reference/rds/describe-db-engine-versions.html).
        """
        return pulumi.get(self, "feature_name")

    @feature_name.setter
    def feature_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "feature_name", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Input[str]:
        """
        Amazon Resource Name (ARN) of the IAM Role to associate with the DB Cluster.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_arn", value)


@pulumi.input_type
class _ClusterRoleAssociationState:
    def __init__(__self__, *,
                 db_cluster_identifier: Optional[pulumi.Input[str]] = None,
                 feature_name: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ClusterRoleAssociation resources.
        :param pulumi.Input[str] db_cluster_identifier: DB Cluster Identifier to associate with the IAM Role.
        :param pulumi.Input[str] feature_name: Name of the feature for association. This can be found in the AWS documentation relevant to the integration or a full list is available in the `SupportedFeatureNames` list returned by [AWS CLI rds describe-db-engine-versions](https://docs.aws.amazon.com/cli/latest/reference/rds/describe-db-engine-versions.html).
        :param pulumi.Input[str] role_arn: Amazon Resource Name (ARN) of the IAM Role to associate with the DB Cluster.
        """
        if db_cluster_identifier is not None:
            pulumi.set(__self__, "db_cluster_identifier", db_cluster_identifier)
        if feature_name is not None:
            pulumi.set(__self__, "feature_name", feature_name)
        if role_arn is not None:
            pulumi.set(__self__, "role_arn", role_arn)

    @property
    @pulumi.getter(name="dbClusterIdentifier")
    def db_cluster_identifier(self) -> Optional[pulumi.Input[str]]:
        """
        DB Cluster Identifier to associate with the IAM Role.
        """
        return pulumi.get(self, "db_cluster_identifier")

    @db_cluster_identifier.setter
    def db_cluster_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "db_cluster_identifier", value)

    @property
    @pulumi.getter(name="featureName")
    def feature_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the feature for association. This can be found in the AWS documentation relevant to the integration or a full list is available in the `SupportedFeatureNames` list returned by [AWS CLI rds describe-db-engine-versions](https://docs.aws.amazon.com/cli/latest/reference/rds/describe-db-engine-versions.html).
        """
        return pulumi.get(self, "feature_name")

    @feature_name.setter
    def feature_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "feature_name", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of the IAM Role to associate with the DB Cluster.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_arn", value)


class ClusterRoleAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 db_cluster_identifier: Optional[pulumi.Input[str]] = None,
                 feature_name: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a RDS DB Cluster association with an IAM Role. Example use cases:

        * [Creating an IAM Role to Allow Amazon Aurora to Access AWS Services](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Integrating.Authorizing.IAM.CreateRole.html)
        * [Importing Amazon S3 Data into an RDS PostgreSQL DB Cluster](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PostgreSQL.S3Import.html)

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.rds.ClusterRoleAssociation("example",
            db_cluster_identifier=aws_rds_cluster["example"]["id"],
            feature_name="S3_INTEGRATION",
            role_arn=aws_iam_role["example"]["arn"])
        ```

        ## Import

        `aws_rds_cluster_role_association` can be imported using the DB Cluster Identifier and IAM Role ARN separated by a comma (`,`), e.g.,

        ```sh
         $ pulumi import aws:rds/clusterRoleAssociation:ClusterRoleAssociation example my-db-cluster,arn:aws:iam::123456789012:role/my-role
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] db_cluster_identifier: DB Cluster Identifier to associate with the IAM Role.
        :param pulumi.Input[str] feature_name: Name of the feature for association. This can be found in the AWS documentation relevant to the integration or a full list is available in the `SupportedFeatureNames` list returned by [AWS CLI rds describe-db-engine-versions](https://docs.aws.amazon.com/cli/latest/reference/rds/describe-db-engine-versions.html).
        :param pulumi.Input[str] role_arn: Amazon Resource Name (ARN) of the IAM Role to associate with the DB Cluster.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ClusterRoleAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a RDS DB Cluster association with an IAM Role. Example use cases:

        * [Creating an IAM Role to Allow Amazon Aurora to Access AWS Services](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Integrating.Authorizing.IAM.CreateRole.html)
        * [Importing Amazon S3 Data into an RDS PostgreSQL DB Cluster](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PostgreSQL.S3Import.html)

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.rds.ClusterRoleAssociation("example",
            db_cluster_identifier=aws_rds_cluster["example"]["id"],
            feature_name="S3_INTEGRATION",
            role_arn=aws_iam_role["example"]["arn"])
        ```

        ## Import

        `aws_rds_cluster_role_association` can be imported using the DB Cluster Identifier and IAM Role ARN separated by a comma (`,`), e.g.,

        ```sh
         $ pulumi import aws:rds/clusterRoleAssociation:ClusterRoleAssociation example my-db-cluster,arn:aws:iam::123456789012:role/my-role
        ```

        :param str resource_name: The name of the resource.
        :param ClusterRoleAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ClusterRoleAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 db_cluster_identifier: Optional[pulumi.Input[str]] = None,
                 feature_name: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ClusterRoleAssociationArgs.__new__(ClusterRoleAssociationArgs)

            if db_cluster_identifier is None and not opts.urn:
                raise TypeError("Missing required property 'db_cluster_identifier'")
            __props__.__dict__["db_cluster_identifier"] = db_cluster_identifier
            if feature_name is None and not opts.urn:
                raise TypeError("Missing required property 'feature_name'")
            __props__.__dict__["feature_name"] = feature_name
            if role_arn is None and not opts.urn:
                raise TypeError("Missing required property 'role_arn'")
            __props__.__dict__["role_arn"] = role_arn
        super(ClusterRoleAssociation, __self__).__init__(
            'aws:rds/clusterRoleAssociation:ClusterRoleAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            db_cluster_identifier: Optional[pulumi.Input[str]] = None,
            feature_name: Optional[pulumi.Input[str]] = None,
            role_arn: Optional[pulumi.Input[str]] = None) -> 'ClusterRoleAssociation':
        """
        Get an existing ClusterRoleAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] db_cluster_identifier: DB Cluster Identifier to associate with the IAM Role.
        :param pulumi.Input[str] feature_name: Name of the feature for association. This can be found in the AWS documentation relevant to the integration or a full list is available in the `SupportedFeatureNames` list returned by [AWS CLI rds describe-db-engine-versions](https://docs.aws.amazon.com/cli/latest/reference/rds/describe-db-engine-versions.html).
        :param pulumi.Input[str] role_arn: Amazon Resource Name (ARN) of the IAM Role to associate with the DB Cluster.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ClusterRoleAssociationState.__new__(_ClusterRoleAssociationState)

        __props__.__dict__["db_cluster_identifier"] = db_cluster_identifier
        __props__.__dict__["feature_name"] = feature_name
        __props__.__dict__["role_arn"] = role_arn
        return ClusterRoleAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dbClusterIdentifier")
    def db_cluster_identifier(self) -> pulumi.Output[str]:
        """
        DB Cluster Identifier to associate with the IAM Role.
        """
        return pulumi.get(self, "db_cluster_identifier")

    @property
    @pulumi.getter(name="featureName")
    def feature_name(self) -> pulumi.Output[str]:
        """
        Name of the feature for association. This can be found in the AWS documentation relevant to the integration or a full list is available in the `SupportedFeatureNames` list returned by [AWS CLI rds describe-db-engine-versions](https://docs.aws.amazon.com/cli/latest/reference/rds/describe-db-engine-versions.html).
        """
        return pulumi.get(self, "feature_name")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of the IAM Role to associate with the DB Cluster.
        """
        return pulumi.get(self, "role_arn")

