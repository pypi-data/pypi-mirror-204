# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetExternalLinkResult',
    'AwaitableGetExternalLinkResult',
    'get_external_link',
    'get_external_link_output',
]

@pulumi.output_type
class GetExternalLinkResult:
    """
    A collection of values returned by getExternalLink.
    """
    def __init__(__self__, created_epoch_millis=None, creator_id=None, description=None, id=None, is_log_integration=None, metric_filter_regex=None, name=None, point_tag_filter_regexes=None, source_filter_regex=None, template=None, updated_epoch_millis=None, updater_id=None):
        if created_epoch_millis and not isinstance(created_epoch_millis, int):
            raise TypeError("Expected argument 'created_epoch_millis' to be a int")
        pulumi.set(__self__, "created_epoch_millis", created_epoch_millis)
        if creator_id and not isinstance(creator_id, str):
            raise TypeError("Expected argument 'creator_id' to be a str")
        pulumi.set(__self__, "creator_id", creator_id)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_log_integration and not isinstance(is_log_integration, bool):
            raise TypeError("Expected argument 'is_log_integration' to be a bool")
        pulumi.set(__self__, "is_log_integration", is_log_integration)
        if metric_filter_regex and not isinstance(metric_filter_regex, str):
            raise TypeError("Expected argument 'metric_filter_regex' to be a str")
        pulumi.set(__self__, "metric_filter_regex", metric_filter_regex)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if point_tag_filter_regexes and not isinstance(point_tag_filter_regexes, dict):
            raise TypeError("Expected argument 'point_tag_filter_regexes' to be a dict")
        pulumi.set(__self__, "point_tag_filter_regexes", point_tag_filter_regexes)
        if source_filter_regex and not isinstance(source_filter_regex, str):
            raise TypeError("Expected argument 'source_filter_regex' to be a str")
        pulumi.set(__self__, "source_filter_regex", source_filter_regex)
        if template and not isinstance(template, str):
            raise TypeError("Expected argument 'template' to be a str")
        pulumi.set(__self__, "template", template)
        if updated_epoch_millis and not isinstance(updated_epoch_millis, int):
            raise TypeError("Expected argument 'updated_epoch_millis' to be a int")
        pulumi.set(__self__, "updated_epoch_millis", updated_epoch_millis)
        if updater_id and not isinstance(updater_id, str):
            raise TypeError("Expected argument 'updater_id' to be a str")
        pulumi.set(__self__, "updater_id", updater_id)

    @property
    @pulumi.getter(name="createdEpochMillis")
    def created_epoch_millis(self) -> int:
        """
        The timestamp in epoch milliseconds indicating when the external link is created.
        """
        return pulumi.get(self, "created_epoch_millis")

    @property
    @pulumi.getter(name="creatorId")
    def creator_id(self) -> str:
        """
        The ID of the user who created the external link.
        """
        return pulumi.get(self, "creator_id")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Human-readable description of this link.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the external link.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isLogIntegration")
    def is_log_integration(self) -> bool:
        """
        Whether this is a "Log Integration" subType of external link.
        """
        return pulumi.get(self, "is_log_integration")

    @property
    @pulumi.getter(name="metricFilterRegex")
    def metric_filter_regex(self) -> str:
        """
        Controls whether a link is displayed in the context menu of a highlighted series. If present, the metric name of the highlighted series must match this regular expression in order for the link to be displayed.
        """
        return pulumi.get(self, "metric_filter_regex")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the external link.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="pointTagFilterRegexes")
    def point_tag_filter_regexes(self) -> Mapping[str, str]:
        """
        (Optional) Controls whether a link is displayed in the context menu of a highlighted
        series. This is a map from string to regular expression. The highlighted series must contain point tags whose
        keys are present in the keys of this map and whose values match the regular expressions associated with those
        keys in order for the link to be displayed.
        """
        return pulumi.get(self, "point_tag_filter_regexes")

    @property
    @pulumi.getter(name="sourceFilterRegex")
    def source_filter_regex(self) -> str:
        """
        Controls whether a link is displayed in the context menu of a highlighted series. If present, the source name of the highlighted series must match this regular expression in order for the link to be displayed.
        """
        return pulumi.get(self, "source_filter_regex")

    @property
    @pulumi.getter
    def template(self) -> str:
        """
        The mustache template for the link. The template must expand to a full URL, including scheme, origin, etc.
        """
        return pulumi.get(self, "template")

    @property
    @pulumi.getter(name="updatedEpochMillis")
    def updated_epoch_millis(self) -> int:
        """
        The timestamp in epoch milliseconds indicating when the external link is updated.
        """
        return pulumi.get(self, "updated_epoch_millis")

    @property
    @pulumi.getter(name="updaterId")
    def updater_id(self) -> str:
        """
        The ID of the user who updated the external link.
        """
        return pulumi.get(self, "updater_id")


class AwaitableGetExternalLinkResult(GetExternalLinkResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetExternalLinkResult(
            created_epoch_millis=self.created_epoch_millis,
            creator_id=self.creator_id,
            description=self.description,
            id=self.id,
            is_log_integration=self.is_log_integration,
            metric_filter_regex=self.metric_filter_regex,
            name=self.name,
            point_tag_filter_regexes=self.point_tag_filter_regexes,
            source_filter_regex=self.source_filter_regex,
            template=self.template,
            updated_epoch_millis=self.updated_epoch_millis,
            updater_id=self.updater_id)


def get_external_link(id: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetExternalLinkResult:
    """
    Use this data source to get information about a Wavefront external link by its ID.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_wavefront as wavefront

    example = wavefront.get_external_link(id="sample-external-link-id")
    ```


    :param str id: The ID of the external link.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('wavefront:index/getExternalLink:getExternalLink', __args__, opts=opts, typ=GetExternalLinkResult).value

    return AwaitableGetExternalLinkResult(
        created_epoch_millis=__ret__.created_epoch_millis,
        creator_id=__ret__.creator_id,
        description=__ret__.description,
        id=__ret__.id,
        is_log_integration=__ret__.is_log_integration,
        metric_filter_regex=__ret__.metric_filter_regex,
        name=__ret__.name,
        point_tag_filter_regexes=__ret__.point_tag_filter_regexes,
        source_filter_regex=__ret__.source_filter_regex,
        template=__ret__.template,
        updated_epoch_millis=__ret__.updated_epoch_millis,
        updater_id=__ret__.updater_id)


@_utilities.lift_output_func(get_external_link)
def get_external_link_output(id: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetExternalLinkResult]:
    """
    Use this data source to get information about a Wavefront external link by its ID.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_wavefront as wavefront

    example = wavefront.get_external_link(id="sample-external-link-id")
    ```


    :param str id: The ID of the external link.
    """
    ...
