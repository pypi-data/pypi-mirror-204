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
    'GetTableItemResult',
    'AwaitableGetTableItemResult',
    'get_table_item',
    'get_table_item_output',
]

@pulumi.output_type
class GetTableItemResult:
    """
    A collection of values returned by getTableItem.
    """
    def __init__(__self__, expression_attribute_names=None, id=None, item=None, key=None, projection_expression=None, table_name=None):
        if expression_attribute_names and not isinstance(expression_attribute_names, dict):
            raise TypeError("Expected argument 'expression_attribute_names' to be a dict")
        pulumi.set(__self__, "expression_attribute_names", expression_attribute_names)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if item and not isinstance(item, str):
            raise TypeError("Expected argument 'item' to be a str")
        pulumi.set(__self__, "item", item)
        if key and not isinstance(key, str):
            raise TypeError("Expected argument 'key' to be a str")
        pulumi.set(__self__, "key", key)
        if projection_expression and not isinstance(projection_expression, str):
            raise TypeError("Expected argument 'projection_expression' to be a str")
        pulumi.set(__self__, "projection_expression", projection_expression)
        if table_name and not isinstance(table_name, str):
            raise TypeError("Expected argument 'table_name' to be a str")
        pulumi.set(__self__, "table_name", table_name)

    @property
    @pulumi.getter(name="expressionAttributeNames")
    def expression_attribute_names(self) -> Optional[Mapping[str, str]]:
        return pulumi.get(self, "expression_attribute_names")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def item(self) -> str:
        """
        A map of attribute names to [AttributeValue](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_AttributeValue.html) objects, as specified by ProjectionExpression.
        """
        return pulumi.get(self, "item")

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter(name="projectionExpression")
    def projection_expression(self) -> Optional[str]:
        return pulumi.get(self, "projection_expression")

    @property
    @pulumi.getter(name="tableName")
    def table_name(self) -> str:
        return pulumi.get(self, "table_name")


class AwaitableGetTableItemResult(GetTableItemResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTableItemResult(
            expression_attribute_names=self.expression_attribute_names,
            id=self.id,
            item=self.item,
            key=self.key,
            projection_expression=self.projection_expression,
            table_name=self.table_name)


def get_table_item(expression_attribute_names: Optional[Mapping[str, str]] = None,
                   key: Optional[str] = None,
                   projection_expression: Optional[str] = None,
                   table_name: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTableItemResult:
    """
    Data source for retrieving a value from an AWS DynamoDB table.

    ## Example Usage
    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.dynamodb.get_table_item(table_name=aws_dynamodb_table["example"]["name"],
        expression_attribute_names={
            "#P": "Percentile",
        },
        projection_expression="#P",
        key=\"\"\"{
    	"hashKey": {"S": "example"}
    }
    \"\"\")
    ```


    :param str key: A map of attribute names to AttributeValue objects, representing the primary key of the item to retrieve.
           For the primary key, you must provide all of the attributes. For example, with a simple primary key, you only need to provide a value for the partition key. For a composite primary key, you must provide values for both the partition key and the sort key.
    :param str projection_expression: A string that identifies one or more attributes to retrieve from the table. These attributes can include scalars, sets, or elements of a JSON document. The attributes in the expression must be separated by commas.
           If no attribute names are specified, then all attributes are returned. If any of the requested attributes are not found, they do not appear in the result.
    :param str table_name: The name of the table containing the requested item.
    """
    __args__ = dict()
    __args__['expressionAttributeNames'] = expression_attribute_names
    __args__['key'] = key
    __args__['projectionExpression'] = projection_expression
    __args__['tableName'] = table_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:dynamodb/getTableItem:getTableItem', __args__, opts=opts, typ=GetTableItemResult).value

    return AwaitableGetTableItemResult(
        expression_attribute_names=__ret__.expression_attribute_names,
        id=__ret__.id,
        item=__ret__.item,
        key=__ret__.key,
        projection_expression=__ret__.projection_expression,
        table_name=__ret__.table_name)


@_utilities.lift_output_func(get_table_item)
def get_table_item_output(expression_attribute_names: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                          key: Optional[pulumi.Input[str]] = None,
                          projection_expression: Optional[pulumi.Input[Optional[str]]] = None,
                          table_name: Optional[pulumi.Input[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTableItemResult]:
    """
    Data source for retrieving a value from an AWS DynamoDB table.

    ## Example Usage
    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.dynamodb.get_table_item(table_name=aws_dynamodb_table["example"]["name"],
        expression_attribute_names={
            "#P": "Percentile",
        },
        projection_expression="#P",
        key=\"\"\"{
    	"hashKey": {"S": "example"}
    }
    \"\"\")
    ```


    :param str key: A map of attribute names to AttributeValue objects, representing the primary key of the item to retrieve.
           For the primary key, you must provide all of the attributes. For example, with a simple primary key, you only need to provide a value for the partition key. For a composite primary key, you must provide values for both the partition key and the sort key.
    :param str projection_expression: A string that identifies one or more attributes to retrieve from the table. These attributes can include scalars, sets, or elements of a JSON document. The attributes in the expression must be separated by commas.
           If no attribute names are specified, then all attributes are returned. If any of the requested attributes are not found, they do not appear in the result.
    :param str table_name: The name of the table containing the requested item.
    """
    ...
