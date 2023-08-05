# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['RoleArgs', 'Role']

@pulumi.input_type
class RoleArgs:
    def __init__(__self__, *,
                 assignees: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 permissions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Role resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] assignees: A list of user groups or accounts to assign to this role.
        :param pulumi.Input[str] description: A short description of the role.
        :param pulumi.Input[str] name: The name of the role.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] permissions: A list of permissions to assign to this role. Valid options are 
               `agent_management`, `alerts_management`, `dashboard_management`, `embedded_charts`, `events_management`, `external_links_management`,
               `host_tag_management`, `metrics_management`, and `user_management`.
        """
        if assignees is not None:
            pulumi.set(__self__, "assignees", assignees)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if permissions is not None:
            pulumi.set(__self__, "permissions", permissions)

    @property
    @pulumi.getter
    def assignees(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of user groups or accounts to assign to this role.
        """
        return pulumi.get(self, "assignees")

    @assignees.setter
    def assignees(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "assignees", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A short description of the role.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the role.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def permissions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of permissions to assign to this role. Valid options are 
        `agent_management`, `alerts_management`, `dashboard_management`, `embedded_charts`, `events_management`, `external_links_management`,
        `host_tag_management`, `metrics_management`, and `user_management`.
        """
        return pulumi.get(self, "permissions")

    @permissions.setter
    def permissions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "permissions", value)


@pulumi.input_type
class _RoleState:
    def __init__(__self__, *,
                 assignees: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 permissions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Role resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] assignees: A list of user groups or accounts to assign to this role.
        :param pulumi.Input[str] description: A short description of the role.
        :param pulumi.Input[str] name: The name of the role.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] permissions: A list of permissions to assign to this role. Valid options are 
               `agent_management`, `alerts_management`, `dashboard_management`, `embedded_charts`, `events_management`, `external_links_management`,
               `host_tag_management`, `metrics_management`, and `user_management`.
        """
        if assignees is not None:
            pulumi.set(__self__, "assignees", assignees)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if permissions is not None:
            pulumi.set(__self__, "permissions", permissions)

    @property
    @pulumi.getter
    def assignees(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of user groups or accounts to assign to this role.
        """
        return pulumi.get(self, "assignees")

    @assignees.setter
    def assignees(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "assignees", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A short description of the role.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the role.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def permissions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of permissions to assign to this role. Valid options are 
        `agent_management`, `alerts_management`, `dashboard_management`, `embedded_charts`, `events_management`, `external_links_management`,
        `host_tag_management`, `metrics_management`, and `user_management`.
        """
        return pulumi.get(self, "permissions")

    @permissions.setter
    def permissions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "permissions", value)


class Role(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 assignees: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 permissions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a Wavefront Role Resource. This allows roles to be created, updated, and deleted.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_wavefront as wavefront

        role = wavefront.Role("role")
        ```

        ## Import

        Roles can be imported by using the `id`, e.g.

        ```sh
         $ pulumi import wavefront:index/role:Role some_role a411c16b-3cf7-4f03-bf11-8ca05aab898d
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] assignees: A list of user groups or accounts to assign to this role.
        :param pulumi.Input[str] description: A short description of the role.
        :param pulumi.Input[str] name: The name of the role.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] permissions: A list of permissions to assign to this role. Valid options are 
               `agent_management`, `alerts_management`, `dashboard_management`, `embedded_charts`, `events_management`, `external_links_management`,
               `host_tag_management`, `metrics_management`, and `user_management`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[RoleArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Wavefront Role Resource. This allows roles to be created, updated, and deleted.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_wavefront as wavefront

        role = wavefront.Role("role")
        ```

        ## Import

        Roles can be imported by using the `id`, e.g.

        ```sh
         $ pulumi import wavefront:index/role:Role some_role a411c16b-3cf7-4f03-bf11-8ca05aab898d
        ```

        :param str resource_name: The name of the resource.
        :param RoleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RoleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 assignees: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 permissions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RoleArgs.__new__(RoleArgs)

            __props__.__dict__["assignees"] = assignees
            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            __props__.__dict__["permissions"] = permissions
        super(Role, __self__).__init__(
            'wavefront:index/role:Role',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            assignees: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            permissions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'Role':
        """
        Get an existing Role resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] assignees: A list of user groups or accounts to assign to this role.
        :param pulumi.Input[str] description: A short description of the role.
        :param pulumi.Input[str] name: The name of the role.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] permissions: A list of permissions to assign to this role. Valid options are 
               `agent_management`, `alerts_management`, `dashboard_management`, `embedded_charts`, `events_management`, `external_links_management`,
               `host_tag_management`, `metrics_management`, and `user_management`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RoleState.__new__(_RoleState)

        __props__.__dict__["assignees"] = assignees
        __props__.__dict__["description"] = description
        __props__.__dict__["name"] = name
        __props__.__dict__["permissions"] = permissions
        return Role(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def assignees(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of user groups or accounts to assign to this role.
        """
        return pulumi.get(self, "assignees")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A short description of the role.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the role.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def permissions(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of permissions to assign to this role. Valid options are 
        `agent_management`, `alerts_management`, `dashboard_management`, `embedded_charts`, `events_management`, `external_links_management`,
        `host_tag_management`, `metrics_management`, and `user_management`.
        """
        return pulumi.get(self, "permissions")

