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

__all__ = [
    'GetRolesResult',
    'AwaitableGetRolesResult',
    'get_roles',
    'get_roles_output',
]

@pulumi.output_type
class GetRolesResult:
    """
    A collection of values returned by getRoles.
    """
    def __init__(__self__, filter=None, id=None, roles=None):
        if filter and not isinstance(filter, str):
            raise TypeError("Expected argument 'filter' to be a str")
        pulumi.set(__self__, "filter", filter)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if roles and not isinstance(roles, list):
            raise TypeError("Expected argument 'roles' to be a list")
        pulumi.set(__self__, "roles", roles)

    @property
    @pulumi.getter
    def filter(self) -> Optional[str]:
        """
        Filter all roles by the given string.
        """
        return pulumi.get(self, "filter")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def roles(self) -> Sequence['outputs.GetRolesRoleResult']:
        """
        List of Roles
        """
        return pulumi.get(self, "roles")


class AwaitableGetRolesResult(GetRolesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRolesResult(
            filter=self.filter,
            id=self.id,
            roles=self.roles)


def get_roles(filter: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRolesResult:
    """
    Use this data source to retrieve information about multiple roles for use in other resources.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_datadog as datadog

    foo = datadog.get_roles(filter="Datadog")
    ```


    :param str filter: Filter all roles by the given string.
    """
    __args__ = dict()
    __args__['filter'] = filter
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('datadog:index/getRoles:getRoles', __args__, opts=opts, typ=GetRolesResult).value

    return AwaitableGetRolesResult(
        filter=__ret__.filter,
        id=__ret__.id,
        roles=__ret__.roles)


@_utilities.lift_output_func(get_roles)
def get_roles_output(filter: Optional[pulumi.Input[Optional[str]]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRolesResult]:
    """
    Use this data source to retrieve information about multiple roles for use in other resources.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_datadog as datadog

    foo = datadog.get_roles(filter="Datadog")
    ```


    :param str filter: Filter all roles by the given string.
    """
    ...
