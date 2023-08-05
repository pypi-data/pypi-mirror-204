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
    'GetNamespacesResult',
    'AwaitableGetNamespacesResult',
    'get_namespaces',
]

@pulumi.output_type
class GetNamespacesResult:
    """
    A collection of values returned by getNamespaces.
    """
    def __init__(__self__, id=None, namespaces=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if namespaces and not isinstance(namespaces, list):
            raise TypeError("Expected argument 'namespaces' to be a list")
        pulumi.set(__self__, "namespaces", namespaces)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def namespaces(self) -> Sequence[str]:
        """
        `(list of strings)` - a list of namespaces available in the cluster.
        """
        return pulumi.get(self, "namespaces")


class AwaitableGetNamespacesResult(GetNamespacesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNamespacesResult(
            id=self.id,
            namespaces=self.namespaces)


def get_namespaces(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNamespacesResult:
    """
    Retrieve a list of namespaces available in Nomad.
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('nomad:index/getNamespaces:getNamespaces', __args__, opts=opts, typ=GetNamespacesResult).value

    return AwaitableGetNamespacesResult(
        id=__ret__.id,
        namespaces=__ret__.namespaces)
