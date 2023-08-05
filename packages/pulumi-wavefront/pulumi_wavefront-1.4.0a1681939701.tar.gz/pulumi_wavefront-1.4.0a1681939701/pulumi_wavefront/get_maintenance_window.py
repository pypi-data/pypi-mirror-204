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
    'GetMaintenanceWindowResult',
    'AwaitableGetMaintenanceWindowResult',
    'get_maintenance_window',
    'get_maintenance_window_output',
]

@pulumi.output_type
class GetMaintenanceWindowResult:
    """
    A collection of values returned by getMaintenanceWindow.
    """
    def __init__(__self__, created_epoch_millis=None, creator_id=None, customer_id=None, end_time_in_seconds=None, event_name=None, host_tag_group_host_names_group_anded=None, id=None, reason=None, relevant_customer_tags=None, relevant_host_names=None, relevant_host_tags=None, relevant_host_tags_anded=None, running_state=None, sort_attr=None, start_time_in_seconds=None, title=None, updated_epoch_millis=None, updater_id=None):
        if created_epoch_millis and not isinstance(created_epoch_millis, int):
            raise TypeError("Expected argument 'created_epoch_millis' to be a int")
        pulumi.set(__self__, "created_epoch_millis", created_epoch_millis)
        if creator_id and not isinstance(creator_id, str):
            raise TypeError("Expected argument 'creator_id' to be a str")
        pulumi.set(__self__, "creator_id", creator_id)
        if customer_id and not isinstance(customer_id, str):
            raise TypeError("Expected argument 'customer_id' to be a str")
        pulumi.set(__self__, "customer_id", customer_id)
        if end_time_in_seconds and not isinstance(end_time_in_seconds, int):
            raise TypeError("Expected argument 'end_time_in_seconds' to be a int")
        pulumi.set(__self__, "end_time_in_seconds", end_time_in_seconds)
        if event_name and not isinstance(event_name, str):
            raise TypeError("Expected argument 'event_name' to be a str")
        pulumi.set(__self__, "event_name", event_name)
        if host_tag_group_host_names_group_anded and not isinstance(host_tag_group_host_names_group_anded, bool):
            raise TypeError("Expected argument 'host_tag_group_host_names_group_anded' to be a bool")
        pulumi.set(__self__, "host_tag_group_host_names_group_anded", host_tag_group_host_names_group_anded)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if reason and not isinstance(reason, str):
            raise TypeError("Expected argument 'reason' to be a str")
        pulumi.set(__self__, "reason", reason)
        if relevant_customer_tags and not isinstance(relevant_customer_tags, list):
            raise TypeError("Expected argument 'relevant_customer_tags' to be a list")
        pulumi.set(__self__, "relevant_customer_tags", relevant_customer_tags)
        if relevant_host_names and not isinstance(relevant_host_names, list):
            raise TypeError("Expected argument 'relevant_host_names' to be a list")
        pulumi.set(__self__, "relevant_host_names", relevant_host_names)
        if relevant_host_tags and not isinstance(relevant_host_tags, list):
            raise TypeError("Expected argument 'relevant_host_tags' to be a list")
        pulumi.set(__self__, "relevant_host_tags", relevant_host_tags)
        if relevant_host_tags_anded and not isinstance(relevant_host_tags_anded, bool):
            raise TypeError("Expected argument 'relevant_host_tags_anded' to be a bool")
        pulumi.set(__self__, "relevant_host_tags_anded", relevant_host_tags_anded)
        if running_state and not isinstance(running_state, str):
            raise TypeError("Expected argument 'running_state' to be a str")
        pulumi.set(__self__, "running_state", running_state)
        if sort_attr and not isinstance(sort_attr, int):
            raise TypeError("Expected argument 'sort_attr' to be a int")
        pulumi.set(__self__, "sort_attr", sort_attr)
        if start_time_in_seconds and not isinstance(start_time_in_seconds, int):
            raise TypeError("Expected argument 'start_time_in_seconds' to be a int")
        pulumi.set(__self__, "start_time_in_seconds", start_time_in_seconds)
        if title and not isinstance(title, str):
            raise TypeError("Expected argument 'title' to be a str")
        pulumi.set(__self__, "title", title)
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
        The timestamp in epoch milliseconds indicating when the maintenance window is created.
        """
        return pulumi.get(self, "created_epoch_millis")

    @property
    @pulumi.getter(name="creatorId")
    def creator_id(self) -> str:
        """
        The ID of the user who created the maintenance window.
        """
        return pulumi.get(self, "creator_id")

    @property
    @pulumi.getter(name="customerId")
    def customer_id(self) -> str:
        """
        The ID of the customer in Wavefront.
        """
        return pulumi.get(self, "customer_id")

    @property
    @pulumi.getter(name="endTimeInSeconds")
    def end_time_in_seconds(self) -> int:
        """
        The end time in seconds after 1 Jan 1970 GMT.
        """
        return pulumi.get(self, "end_time_in_seconds")

    @property
    @pulumi.getter(name="eventName")
    def event_name(self) -> str:
        """
        The event name of the maintenance window.
        """
        return pulumi.get(self, "event_name")

    @property
    @pulumi.getter(name="hostTagGroupHostNamesGroupAnded")
    def host_tag_group_host_names_group_anded(self) -> bool:
        """
        If set to `true`, the source or host must be in `relevant_host_names` and must have tags matching the specification formed by `relevant_host_tags` and `relevant_host_tags_anded` in for this maintenance window to apply. 
        If set to false, the source or host must either be in `relevant_host_names` or match `relevant_host_tags` and `relevant_host_tags_anded`. Default value is `false`.
        """
        return pulumi.get(self, "host_tag_group_host_names_group_anded")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the maintenance window.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def reason(self) -> str:
        """
        The reason for the maintenance window.
        """
        return pulumi.get(self, "reason")

    @property
    @pulumi.getter(name="relevantCustomerTags")
    def relevant_customer_tags(self) -> Sequence[str]:
        """
        The list of alert tags whose matching alerts will be put into maintenance because
        of this maintenance window. At least one of `relevant_customer_tags`, `relevant_host_tags`, or `relevant_host_names`
        is required.
        """
        return pulumi.get(self, "relevant_customer_tags")

    @property
    @pulumi.getter(name="relevantHostNames")
    def relevant_host_names(self) -> Sequence[str]:
        """
        The list of source or host names that will be put into maintenance because of this
        maintenance window. At least one of `relevant_customer_tags`, `relevant_host_tags`, or `relevant_host_names`
        is required.
        """
        return pulumi.get(self, "relevant_host_names")

    @property
    @pulumi.getter(name="relevantHostTags")
    def relevant_host_tags(self) -> Sequence[str]:
        """
        The list of source or host tags whose matching sources or hosts will be put into maintenance
        because of this maintenance window. At least one of `relevant_customer_tags`, `relevant_host_tags`, or
        `relevant_host_names` is required.
        """
        return pulumi.get(self, "relevant_host_tags")

    @property
    @pulumi.getter(name="relevantHostTagsAnded")
    def relevant_host_tags_anded(self) -> bool:
        """
        Whether to AND source or host tags listed in `relevant_host_tags`.
        If set to `true`, the source or host must contain all tags for the maintenance window to apply. If set to `false`,
        the tags are OR'ed, and the source or host must contain one of the tags. Default value is `false`.
        """
        return pulumi.get(self, "relevant_host_tags_anded")

    @property
    @pulumi.getter(name="runningState")
    def running_state(self) -> str:
        """
        The running state of the maintenance window.
        """
        return pulumi.get(self, "running_state")

    @property
    @pulumi.getter(name="sortAttr")
    def sort_attr(self) -> int:
        return pulumi.get(self, "sort_attr")

    @property
    @pulumi.getter(name="startTimeInSeconds")
    def start_time_in_seconds(self) -> int:
        """
        The start time in seconds after 1 Jan 1970 GMT.
        """
        return pulumi.get(self, "start_time_in_seconds")

    @property
    @pulumi.getter
    def title(self) -> str:
        """
        The title of the maintenance window.
        """
        return pulumi.get(self, "title")

    @property
    @pulumi.getter(name="updatedEpochMillis")
    def updated_epoch_millis(self) -> int:
        """
        The timestamp in epoch milliseconds indicating when the maintenance window is updated.
        """
        return pulumi.get(self, "updated_epoch_millis")

    @property
    @pulumi.getter(name="updaterId")
    def updater_id(self) -> str:
        """
        The ID of the user who updated the maintenance window.
        """
        return pulumi.get(self, "updater_id")


class AwaitableGetMaintenanceWindowResult(GetMaintenanceWindowResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMaintenanceWindowResult(
            created_epoch_millis=self.created_epoch_millis,
            creator_id=self.creator_id,
            customer_id=self.customer_id,
            end_time_in_seconds=self.end_time_in_seconds,
            event_name=self.event_name,
            host_tag_group_host_names_group_anded=self.host_tag_group_host_names_group_anded,
            id=self.id,
            reason=self.reason,
            relevant_customer_tags=self.relevant_customer_tags,
            relevant_host_names=self.relevant_host_names,
            relevant_host_tags=self.relevant_host_tags,
            relevant_host_tags_anded=self.relevant_host_tags_anded,
            running_state=self.running_state,
            sort_attr=self.sort_attr,
            start_time_in_seconds=self.start_time_in_seconds,
            title=self.title,
            updated_epoch_millis=self.updated_epoch_millis,
            updater_id=self.updater_id)


def get_maintenance_window(id: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMaintenanceWindowResult:
    """
    Use this data source to get information about a Wavefront maintenance window by its ID.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_wavefront as wavefront

    example = wavefront.get_maintenance_window(id="sample-maintenance-window-id")
    ```


    :param str id: The ID of the maintenance window.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('wavefront:index/getMaintenanceWindow:getMaintenanceWindow', __args__, opts=opts, typ=GetMaintenanceWindowResult).value

    return AwaitableGetMaintenanceWindowResult(
        created_epoch_millis=__ret__.created_epoch_millis,
        creator_id=__ret__.creator_id,
        customer_id=__ret__.customer_id,
        end_time_in_seconds=__ret__.end_time_in_seconds,
        event_name=__ret__.event_name,
        host_tag_group_host_names_group_anded=__ret__.host_tag_group_host_names_group_anded,
        id=__ret__.id,
        reason=__ret__.reason,
        relevant_customer_tags=__ret__.relevant_customer_tags,
        relevant_host_names=__ret__.relevant_host_names,
        relevant_host_tags=__ret__.relevant_host_tags,
        relevant_host_tags_anded=__ret__.relevant_host_tags_anded,
        running_state=__ret__.running_state,
        sort_attr=__ret__.sort_attr,
        start_time_in_seconds=__ret__.start_time_in_seconds,
        title=__ret__.title,
        updated_epoch_millis=__ret__.updated_epoch_millis,
        updater_id=__ret__.updater_id)


@_utilities.lift_output_func(get_maintenance_window)
def get_maintenance_window_output(id: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetMaintenanceWindowResult]:
    """
    Use this data source to get information about a Wavefront maintenance window by its ID.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_wavefront as wavefront

    example = wavefront.get_maintenance_window(id="sample-maintenance-window-id")
    ```


    :param str id: The ID of the maintenance window.
    """
    ...
