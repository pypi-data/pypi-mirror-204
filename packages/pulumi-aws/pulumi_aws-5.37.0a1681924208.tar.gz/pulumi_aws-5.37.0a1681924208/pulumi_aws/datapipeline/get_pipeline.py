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
    'GetPipelineResult',
    'AwaitableGetPipelineResult',
    'get_pipeline',
    'get_pipeline_output',
]

@pulumi.output_type
class GetPipelineResult:
    """
    A collection of values returned by getPipeline.
    """
    def __init__(__self__, description=None, id=None, name=None, pipeline_id=None, tags=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if pipeline_id and not isinstance(pipeline_id, str):
            raise TypeError("Expected argument 'pipeline_id' to be a str")
        pulumi.set(__self__, "pipeline_id", pipeline_id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of Pipeline.
        """
        return pulumi.get(self, "description")

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
        """
        Name of Pipeline.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="pipelineId")
    def pipeline_id(self) -> str:
        return pulumi.get(self, "pipeline_id")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Map of tags assigned to the resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetPipelineResult(GetPipelineResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPipelineResult(
            description=self.description,
            id=self.id,
            name=self.name,
            pipeline_id=self.pipeline_id,
            tags=self.tags)


def get_pipeline(pipeline_id: Optional[str] = None,
                 tags: Optional[Mapping[str, str]] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPipelineResult:
    """
    Provides details about a specific DataPipeline Pipeline.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.datapipeline.get_pipeline(pipeline_id="pipelineID")
    ```


    :param str pipeline_id: ID of the pipeline.
    :param Mapping[str, str] tags: Map of tags assigned to the resource.
    """
    __args__ = dict()
    __args__['pipelineId'] = pipeline_id
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:datapipeline/getPipeline:getPipeline', __args__, opts=opts, typ=GetPipelineResult).value

    return AwaitableGetPipelineResult(
        description=__ret__.description,
        id=__ret__.id,
        name=__ret__.name,
        pipeline_id=__ret__.pipeline_id,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_pipeline)
def get_pipeline_output(pipeline_id: Optional[pulumi.Input[str]] = None,
                        tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPipelineResult]:
    """
    Provides details about a specific DataPipeline Pipeline.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.datapipeline.get_pipeline(pipeline_id="pipelineID")
    ```


    :param str pipeline_id: ID of the pipeline.
    :param Mapping[str, str] tags: Map of tags assigned to the resource.
    """
    ...
