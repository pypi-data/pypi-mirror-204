# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = ['DashboardArgs', 'Dashboard']

@pulumi.input_type
class DashboardArgs:
    def __init__(__self__, *,
                 layout_type: pulumi.Input[str],
                 title: pulumi.Input[str],
                 dashboard_lists: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 is_read_only: Optional[pulumi.Input[bool]] = None,
                 notify_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 reflow_type: Optional[pulumi.Input[str]] = None,
                 restricted_roles: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 template_variable_presets: Optional[pulumi.Input[Sequence[pulumi.Input['DashboardTemplateVariablePresetArgs']]]] = None,
                 template_variables: Optional[pulumi.Input[Sequence[pulumi.Input['DashboardTemplateVariableArgs']]]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 widgets: Optional[pulumi.Input[Sequence[pulumi.Input['DashboardWidgetArgs']]]] = None):
        """
        The set of arguments for constructing a Dashboard resource.
        :param pulumi.Input[str] layout_type: The layout type of the dashboard. Valid values are `ordered`, `free`.
        :param pulumi.Input[str] title: The title of the dashboard.
        :param pulumi.Input[Sequence[pulumi.Input[int]]] dashboard_lists: A list of dashboard lists this dashboard belongs to.
        :param pulumi.Input[str] description: The description of the dashboard.
        :param pulumi.Input[bool] is_read_only: Whether this dashboard is read-only. **Deprecated.** Prefer using `restricted_roles` to define which roles are required to edit the dashboard.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] notify_lists: The list of handles for the users to notify when changes are made to this dashboard.
        :param pulumi.Input[str] reflow_type: The reflow type of a new dashboard layout. Set this only when layout type is `ordered`. If set to `fixed`, the dashboard expects all widgets to have a layout, and if it's set to `auto`, widgets should not have layouts. Valid values are `auto`, `fixed`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] restricted_roles: UUIDs of roles whose associated users are authorized to edit the dashboard.
        :param pulumi.Input[Sequence[pulumi.Input['DashboardTemplateVariablePresetArgs']]] template_variable_presets: The list of selectable template variable presets for this dashboard.
        :param pulumi.Input[Sequence[pulumi.Input['DashboardTemplateVariableArgs']]] template_variables: The list of template variables for this dashboard.
        :param pulumi.Input[str] url: The URL of the dashboard.
        :param pulumi.Input[Sequence[pulumi.Input['DashboardWidgetArgs']]] widgets: The list of widgets to display on the dashboard.
        """
        pulumi.set(__self__, "layout_type", layout_type)
        pulumi.set(__self__, "title", title)
        if dashboard_lists is not None:
            pulumi.set(__self__, "dashboard_lists", dashboard_lists)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if is_read_only is not None:
            warnings.warn("""Prefer using `restricted_roles` to define which roles are required to edit the dashboard.""", DeprecationWarning)
            pulumi.log.warn("""is_read_only is deprecated: Prefer using `restricted_roles` to define which roles are required to edit the dashboard.""")
        if is_read_only is not None:
            pulumi.set(__self__, "is_read_only", is_read_only)
        if notify_lists is not None:
            pulumi.set(__self__, "notify_lists", notify_lists)
        if reflow_type is not None:
            pulumi.set(__self__, "reflow_type", reflow_type)
        if restricted_roles is not None:
            pulumi.set(__self__, "restricted_roles", restricted_roles)
        if template_variable_presets is not None:
            pulumi.set(__self__, "template_variable_presets", template_variable_presets)
        if template_variables is not None:
            pulumi.set(__self__, "template_variables", template_variables)
        if url is not None:
            pulumi.set(__self__, "url", url)
        if widgets is not None:
            pulumi.set(__self__, "widgets", widgets)

    @property
    @pulumi.getter(name="layoutType")
    def layout_type(self) -> pulumi.Input[str]:
        """
        The layout type of the dashboard. Valid values are `ordered`, `free`.
        """
        return pulumi.get(self, "layout_type")

    @layout_type.setter
    def layout_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "layout_type", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        """
        The title of the dashboard.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter(name="dashboardLists")
    def dashboard_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]:
        """
        A list of dashboard lists this dashboard belongs to.
        """
        return pulumi.get(self, "dashboard_lists")

    @dashboard_lists.setter
    def dashboard_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]):
        pulumi.set(self, "dashboard_lists", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the dashboard.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="isReadOnly")
    def is_read_only(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether this dashboard is read-only. **Deprecated.** Prefer using `restricted_roles` to define which roles are required to edit the dashboard.
        """
        return pulumi.get(self, "is_read_only")

    @is_read_only.setter
    def is_read_only(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_read_only", value)

    @property
    @pulumi.getter(name="notifyLists")
    def notify_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The list of handles for the users to notify when changes are made to this dashboard.
        """
        return pulumi.get(self, "notify_lists")

    @notify_lists.setter
    def notify_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "notify_lists", value)

    @property
    @pulumi.getter(name="reflowType")
    def reflow_type(self) -> Optional[pulumi.Input[str]]:
        """
        The reflow type of a new dashboard layout. Set this only when layout type is `ordered`. If set to `fixed`, the dashboard expects all widgets to have a layout, and if it's set to `auto`, widgets should not have layouts. Valid values are `auto`, `fixed`.
        """
        return pulumi.get(self, "reflow_type")

    @reflow_type.setter
    def reflow_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "reflow_type", value)

    @property
    @pulumi.getter(name="restrictedRoles")
    def restricted_roles(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        UUIDs of roles whose associated users are authorized to edit the dashboard.
        """
        return pulumi.get(self, "restricted_roles")

    @restricted_roles.setter
    def restricted_roles(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "restricted_roles", value)

    @property
    @pulumi.getter(name="templateVariablePresets")
    def template_variable_presets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DashboardTemplateVariablePresetArgs']]]]:
        """
        The list of selectable template variable presets for this dashboard.
        """
        return pulumi.get(self, "template_variable_presets")

    @template_variable_presets.setter
    def template_variable_presets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DashboardTemplateVariablePresetArgs']]]]):
        pulumi.set(self, "template_variable_presets", value)

    @property
    @pulumi.getter(name="templateVariables")
    def template_variables(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DashboardTemplateVariableArgs']]]]:
        """
        The list of template variables for this dashboard.
        """
        return pulumi.get(self, "template_variables")

    @template_variables.setter
    def template_variables(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DashboardTemplateVariableArgs']]]]):
        pulumi.set(self, "template_variables", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        """
        The URL of the dashboard.
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)

    @property
    @pulumi.getter
    def widgets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DashboardWidgetArgs']]]]:
        """
        The list of widgets to display on the dashboard.
        """
        return pulumi.get(self, "widgets")

    @widgets.setter
    def widgets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DashboardWidgetArgs']]]]):
        pulumi.set(self, "widgets", value)


@pulumi.input_type
class _DashboardState:
    def __init__(__self__, *,
                 dashboard_lists: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 dashboard_lists_removeds: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 is_read_only: Optional[pulumi.Input[bool]] = None,
                 layout_type: Optional[pulumi.Input[str]] = None,
                 notify_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 reflow_type: Optional[pulumi.Input[str]] = None,
                 restricted_roles: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 template_variable_presets: Optional[pulumi.Input[Sequence[pulumi.Input['DashboardTemplateVariablePresetArgs']]]] = None,
                 template_variables: Optional[pulumi.Input[Sequence[pulumi.Input['DashboardTemplateVariableArgs']]]] = None,
                 title: Optional[pulumi.Input[str]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 widgets: Optional[pulumi.Input[Sequence[pulumi.Input['DashboardWidgetArgs']]]] = None):
        """
        Input properties used for looking up and filtering Dashboard resources.
        :param pulumi.Input[Sequence[pulumi.Input[int]]] dashboard_lists: A list of dashboard lists this dashboard belongs to.
        :param pulumi.Input[Sequence[pulumi.Input[int]]] dashboard_lists_removeds: A list of dashboard lists this dashboard should be removed from. Internal only.
        :param pulumi.Input[str] description: The description of the dashboard.
        :param pulumi.Input[bool] is_read_only: Whether this dashboard is read-only. **Deprecated.** Prefer using `restricted_roles` to define which roles are required to edit the dashboard.
        :param pulumi.Input[str] layout_type: The layout type of the dashboard. Valid values are `ordered`, `free`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] notify_lists: The list of handles for the users to notify when changes are made to this dashboard.
        :param pulumi.Input[str] reflow_type: The reflow type of a new dashboard layout. Set this only when layout type is `ordered`. If set to `fixed`, the dashboard expects all widgets to have a layout, and if it's set to `auto`, widgets should not have layouts. Valid values are `auto`, `fixed`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] restricted_roles: UUIDs of roles whose associated users are authorized to edit the dashboard.
        :param pulumi.Input[Sequence[pulumi.Input['DashboardTemplateVariablePresetArgs']]] template_variable_presets: The list of selectable template variable presets for this dashboard.
        :param pulumi.Input[Sequence[pulumi.Input['DashboardTemplateVariableArgs']]] template_variables: The list of template variables for this dashboard.
        :param pulumi.Input[str] title: The title of the dashboard.
        :param pulumi.Input[str] url: The URL of the dashboard.
        :param pulumi.Input[Sequence[pulumi.Input['DashboardWidgetArgs']]] widgets: The list of widgets to display on the dashboard.
        """
        if dashboard_lists is not None:
            pulumi.set(__self__, "dashboard_lists", dashboard_lists)
        if dashboard_lists_removeds is not None:
            pulumi.set(__self__, "dashboard_lists_removeds", dashboard_lists_removeds)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if is_read_only is not None:
            warnings.warn("""Prefer using `restricted_roles` to define which roles are required to edit the dashboard.""", DeprecationWarning)
            pulumi.log.warn("""is_read_only is deprecated: Prefer using `restricted_roles` to define which roles are required to edit the dashboard.""")
        if is_read_only is not None:
            pulumi.set(__self__, "is_read_only", is_read_only)
        if layout_type is not None:
            pulumi.set(__self__, "layout_type", layout_type)
        if notify_lists is not None:
            pulumi.set(__self__, "notify_lists", notify_lists)
        if reflow_type is not None:
            pulumi.set(__self__, "reflow_type", reflow_type)
        if restricted_roles is not None:
            pulumi.set(__self__, "restricted_roles", restricted_roles)
        if template_variable_presets is not None:
            pulumi.set(__self__, "template_variable_presets", template_variable_presets)
        if template_variables is not None:
            pulumi.set(__self__, "template_variables", template_variables)
        if title is not None:
            pulumi.set(__self__, "title", title)
        if url is not None:
            pulumi.set(__self__, "url", url)
        if widgets is not None:
            pulumi.set(__self__, "widgets", widgets)

    @property
    @pulumi.getter(name="dashboardLists")
    def dashboard_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]:
        """
        A list of dashboard lists this dashboard belongs to.
        """
        return pulumi.get(self, "dashboard_lists")

    @dashboard_lists.setter
    def dashboard_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]):
        pulumi.set(self, "dashboard_lists", value)

    @property
    @pulumi.getter(name="dashboardListsRemoveds")
    def dashboard_lists_removeds(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]:
        """
        A list of dashboard lists this dashboard should be removed from. Internal only.
        """
        return pulumi.get(self, "dashboard_lists_removeds")

    @dashboard_lists_removeds.setter
    def dashboard_lists_removeds(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]]):
        pulumi.set(self, "dashboard_lists_removeds", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the dashboard.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="isReadOnly")
    def is_read_only(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether this dashboard is read-only. **Deprecated.** Prefer using `restricted_roles` to define which roles are required to edit the dashboard.
        """
        return pulumi.get(self, "is_read_only")

    @is_read_only.setter
    def is_read_only(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_read_only", value)

    @property
    @pulumi.getter(name="layoutType")
    def layout_type(self) -> Optional[pulumi.Input[str]]:
        """
        The layout type of the dashboard. Valid values are `ordered`, `free`.
        """
        return pulumi.get(self, "layout_type")

    @layout_type.setter
    def layout_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "layout_type", value)

    @property
    @pulumi.getter(name="notifyLists")
    def notify_lists(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The list of handles for the users to notify when changes are made to this dashboard.
        """
        return pulumi.get(self, "notify_lists")

    @notify_lists.setter
    def notify_lists(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "notify_lists", value)

    @property
    @pulumi.getter(name="reflowType")
    def reflow_type(self) -> Optional[pulumi.Input[str]]:
        """
        The reflow type of a new dashboard layout. Set this only when layout type is `ordered`. If set to `fixed`, the dashboard expects all widgets to have a layout, and if it's set to `auto`, widgets should not have layouts. Valid values are `auto`, `fixed`.
        """
        return pulumi.get(self, "reflow_type")

    @reflow_type.setter
    def reflow_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "reflow_type", value)

    @property
    @pulumi.getter(name="restrictedRoles")
    def restricted_roles(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        UUIDs of roles whose associated users are authorized to edit the dashboard.
        """
        return pulumi.get(self, "restricted_roles")

    @restricted_roles.setter
    def restricted_roles(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "restricted_roles", value)

    @property
    @pulumi.getter(name="templateVariablePresets")
    def template_variable_presets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DashboardTemplateVariablePresetArgs']]]]:
        """
        The list of selectable template variable presets for this dashboard.
        """
        return pulumi.get(self, "template_variable_presets")

    @template_variable_presets.setter
    def template_variable_presets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DashboardTemplateVariablePresetArgs']]]]):
        pulumi.set(self, "template_variable_presets", value)

    @property
    @pulumi.getter(name="templateVariables")
    def template_variables(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DashboardTemplateVariableArgs']]]]:
        """
        The list of template variables for this dashboard.
        """
        return pulumi.get(self, "template_variables")

    @template_variables.setter
    def template_variables(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DashboardTemplateVariableArgs']]]]):
        pulumi.set(self, "template_variables", value)

    @property
    @pulumi.getter
    def title(self) -> Optional[pulumi.Input[str]]:
        """
        The title of the dashboard.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        """
        The URL of the dashboard.
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)

    @property
    @pulumi.getter
    def widgets(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DashboardWidgetArgs']]]]:
        """
        The list of widgets to display on the dashboard.
        """
        return pulumi.get(self, "widgets")

    @widgets.setter
    def widgets(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DashboardWidgetArgs']]]]):
        pulumi.set(self, "widgets", value)


class Dashboard(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dashboard_lists: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 is_read_only: Optional[pulumi.Input[bool]] = None,
                 layout_type: Optional[pulumi.Input[str]] = None,
                 notify_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 reflow_type: Optional[pulumi.Input[str]] = None,
                 restricted_roles: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 template_variable_presets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DashboardTemplateVariablePresetArgs']]]]] = None,
                 template_variables: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DashboardTemplateVariableArgs']]]]] = None,
                 title: Optional[pulumi.Input[str]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 widgets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DashboardWidgetArgs']]]]] = None,
                 __props__=None):
        """
        Provides a Datadog dashboard resource. This can be used to create and manage Datadog dashboards.

        ## Import

        ```sh
         $ pulumi import datadog:index/dashboard:Dashboard my_service_dashboard sv7-gyh-kas
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[int]]] dashboard_lists: A list of dashboard lists this dashboard belongs to.
        :param pulumi.Input[str] description: The description of the dashboard.
        :param pulumi.Input[bool] is_read_only: Whether this dashboard is read-only. **Deprecated.** Prefer using `restricted_roles` to define which roles are required to edit the dashboard.
        :param pulumi.Input[str] layout_type: The layout type of the dashboard. Valid values are `ordered`, `free`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] notify_lists: The list of handles for the users to notify when changes are made to this dashboard.
        :param pulumi.Input[str] reflow_type: The reflow type of a new dashboard layout. Set this only when layout type is `ordered`. If set to `fixed`, the dashboard expects all widgets to have a layout, and if it's set to `auto`, widgets should not have layouts. Valid values are `auto`, `fixed`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] restricted_roles: UUIDs of roles whose associated users are authorized to edit the dashboard.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DashboardTemplateVariablePresetArgs']]]] template_variable_presets: The list of selectable template variable presets for this dashboard.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DashboardTemplateVariableArgs']]]] template_variables: The list of template variables for this dashboard.
        :param pulumi.Input[str] title: The title of the dashboard.
        :param pulumi.Input[str] url: The URL of the dashboard.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DashboardWidgetArgs']]]] widgets: The list of widgets to display on the dashboard.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DashboardArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Datadog dashboard resource. This can be used to create and manage Datadog dashboards.

        ## Import

        ```sh
         $ pulumi import datadog:index/dashboard:Dashboard my_service_dashboard sv7-gyh-kas
        ```

        :param str resource_name: The name of the resource.
        :param DashboardArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DashboardArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dashboard_lists: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 is_read_only: Optional[pulumi.Input[bool]] = None,
                 layout_type: Optional[pulumi.Input[str]] = None,
                 notify_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 reflow_type: Optional[pulumi.Input[str]] = None,
                 restricted_roles: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 template_variable_presets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DashboardTemplateVariablePresetArgs']]]]] = None,
                 template_variables: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DashboardTemplateVariableArgs']]]]] = None,
                 title: Optional[pulumi.Input[str]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 widgets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DashboardWidgetArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DashboardArgs.__new__(DashboardArgs)

            __props__.__dict__["dashboard_lists"] = dashboard_lists
            __props__.__dict__["description"] = description
            if is_read_only is not None and not opts.urn:
                warnings.warn("""Prefer using `restricted_roles` to define which roles are required to edit the dashboard.""", DeprecationWarning)
                pulumi.log.warn("""is_read_only is deprecated: Prefer using `restricted_roles` to define which roles are required to edit the dashboard.""")
            __props__.__dict__["is_read_only"] = is_read_only
            if layout_type is None and not opts.urn:
                raise TypeError("Missing required property 'layout_type'")
            __props__.__dict__["layout_type"] = layout_type
            __props__.__dict__["notify_lists"] = notify_lists
            __props__.__dict__["reflow_type"] = reflow_type
            __props__.__dict__["restricted_roles"] = restricted_roles
            __props__.__dict__["template_variable_presets"] = template_variable_presets
            __props__.__dict__["template_variables"] = template_variables
            if title is None and not opts.urn:
                raise TypeError("Missing required property 'title'")
            __props__.__dict__["title"] = title
            __props__.__dict__["url"] = url
            __props__.__dict__["widgets"] = widgets
            __props__.__dict__["dashboard_lists_removeds"] = None
        super(Dashboard, __self__).__init__(
            'datadog:index/dashboard:Dashboard',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            dashboard_lists: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
            dashboard_lists_removeds: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
            description: Optional[pulumi.Input[str]] = None,
            is_read_only: Optional[pulumi.Input[bool]] = None,
            layout_type: Optional[pulumi.Input[str]] = None,
            notify_lists: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            reflow_type: Optional[pulumi.Input[str]] = None,
            restricted_roles: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            template_variable_presets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DashboardTemplateVariablePresetArgs']]]]] = None,
            template_variables: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DashboardTemplateVariableArgs']]]]] = None,
            title: Optional[pulumi.Input[str]] = None,
            url: Optional[pulumi.Input[str]] = None,
            widgets: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DashboardWidgetArgs']]]]] = None) -> 'Dashboard':
        """
        Get an existing Dashboard resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[int]]] dashboard_lists: A list of dashboard lists this dashboard belongs to.
        :param pulumi.Input[Sequence[pulumi.Input[int]]] dashboard_lists_removeds: A list of dashboard lists this dashboard should be removed from. Internal only.
        :param pulumi.Input[str] description: The description of the dashboard.
        :param pulumi.Input[bool] is_read_only: Whether this dashboard is read-only. **Deprecated.** Prefer using `restricted_roles` to define which roles are required to edit the dashboard.
        :param pulumi.Input[str] layout_type: The layout type of the dashboard. Valid values are `ordered`, `free`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] notify_lists: The list of handles for the users to notify when changes are made to this dashboard.
        :param pulumi.Input[str] reflow_type: The reflow type of a new dashboard layout. Set this only when layout type is `ordered`. If set to `fixed`, the dashboard expects all widgets to have a layout, and if it's set to `auto`, widgets should not have layouts. Valid values are `auto`, `fixed`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] restricted_roles: UUIDs of roles whose associated users are authorized to edit the dashboard.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DashboardTemplateVariablePresetArgs']]]] template_variable_presets: The list of selectable template variable presets for this dashboard.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DashboardTemplateVariableArgs']]]] template_variables: The list of template variables for this dashboard.
        :param pulumi.Input[str] title: The title of the dashboard.
        :param pulumi.Input[str] url: The URL of the dashboard.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DashboardWidgetArgs']]]] widgets: The list of widgets to display on the dashboard.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DashboardState.__new__(_DashboardState)

        __props__.__dict__["dashboard_lists"] = dashboard_lists
        __props__.__dict__["dashboard_lists_removeds"] = dashboard_lists_removeds
        __props__.__dict__["description"] = description
        __props__.__dict__["is_read_only"] = is_read_only
        __props__.__dict__["layout_type"] = layout_type
        __props__.__dict__["notify_lists"] = notify_lists
        __props__.__dict__["reflow_type"] = reflow_type
        __props__.__dict__["restricted_roles"] = restricted_roles
        __props__.__dict__["template_variable_presets"] = template_variable_presets
        __props__.__dict__["template_variables"] = template_variables
        __props__.__dict__["title"] = title
        __props__.__dict__["url"] = url
        __props__.__dict__["widgets"] = widgets
        return Dashboard(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dashboardLists")
    def dashboard_lists(self) -> pulumi.Output[Optional[Sequence[int]]]:
        """
        A list of dashboard lists this dashboard belongs to.
        """
        return pulumi.get(self, "dashboard_lists")

    @property
    @pulumi.getter(name="dashboardListsRemoveds")
    def dashboard_lists_removeds(self) -> pulumi.Output[Sequence[int]]:
        """
        A list of dashboard lists this dashboard should be removed from. Internal only.
        """
        return pulumi.get(self, "dashboard_lists_removeds")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the dashboard.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="isReadOnly")
    def is_read_only(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether this dashboard is read-only. **Deprecated.** Prefer using `restricted_roles` to define which roles are required to edit the dashboard.
        """
        return pulumi.get(self, "is_read_only")

    @property
    @pulumi.getter(name="layoutType")
    def layout_type(self) -> pulumi.Output[str]:
        """
        The layout type of the dashboard. Valid values are `ordered`, `free`.
        """
        return pulumi.get(self, "layout_type")

    @property
    @pulumi.getter(name="notifyLists")
    def notify_lists(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The list of handles for the users to notify when changes are made to this dashboard.
        """
        return pulumi.get(self, "notify_lists")

    @property
    @pulumi.getter(name="reflowType")
    def reflow_type(self) -> pulumi.Output[Optional[str]]:
        """
        The reflow type of a new dashboard layout. Set this only when layout type is `ordered`. If set to `fixed`, the dashboard expects all widgets to have a layout, and if it's set to `auto`, widgets should not have layouts. Valid values are `auto`, `fixed`.
        """
        return pulumi.get(self, "reflow_type")

    @property
    @pulumi.getter(name="restrictedRoles")
    def restricted_roles(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        UUIDs of roles whose associated users are authorized to edit the dashboard.
        """
        return pulumi.get(self, "restricted_roles")

    @property
    @pulumi.getter(name="templateVariablePresets")
    def template_variable_presets(self) -> pulumi.Output[Optional[Sequence['outputs.DashboardTemplateVariablePreset']]]:
        """
        The list of selectable template variable presets for this dashboard.
        """
        return pulumi.get(self, "template_variable_presets")

    @property
    @pulumi.getter(name="templateVariables")
    def template_variables(self) -> pulumi.Output[Optional[Sequence['outputs.DashboardTemplateVariable']]]:
        """
        The list of template variables for this dashboard.
        """
        return pulumi.get(self, "template_variables")

    @property
    @pulumi.getter
    def title(self) -> pulumi.Output[str]:
        """
        The title of the dashboard.
        """
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def url(self) -> pulumi.Output[str]:
        """
        The URL of the dashboard.
        """
        return pulumi.get(self, "url")

    @property
    @pulumi.getter
    def widgets(self) -> pulumi.Output[Optional[Sequence['outputs.DashboardWidget']]]:
        """
        The list of widgets to display on the dashboard.
        """
        return pulumi.get(self, "widgets")

