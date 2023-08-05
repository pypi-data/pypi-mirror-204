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
    'GetDynamicResult',
    'AwaitableGetDynamicResult',
    'get_dynamic',
    'get_dynamic_output',
]

@pulumi.output_type
class GetDynamicResult:
    """
    A collection of values returned by getDynamic.
    """
    def __init__(__self__, filters=None, id=None, name_regex=None, type=None):
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def filters(self) -> Sequence[str]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        return pulumi.get(self, "type")


class AwaitableGetDynamicResult(GetDynamicResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDynamicResult(
            filters=self.filters,
            id=self.id,
            name_regex=self.name_regex,
            type=self.type)


def get_dynamic(filters: Optional[Sequence[str]] = None,
                name_regex: Optional[str] = None,
                type: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDynamicResult:
    """
    [docs-about-morefs]: /docs/providers/vsphere/index.html#use-of-managed-object-references-by-the-vsphere-provider

    The _get_dynamic_ data source can be used to get the [managed object reference ID][docs-about-morefs]
    of any tagged managed object in vCenter Server by providing a list of tag IDs
    and an optional regular expression to filter objects by name.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_vsphere as vsphere

    category = vsphere.get_tag_category(name="SomeCategory")
    tag1 = vsphere.get_tag(name="FirstTag",
        category_id=data["vsphere_tag_category"]["cat"]["id"])
    tag2 = vsphere.get_tag(name="SecondTag",
        category_id=data["vsphere_tag_category"]["cat"]["id"])
    dyn = vsphere.get_dynamic(filters=[
            tag1.id,
            tag1.id,
        ],
        name_regex="ubuntu",
        type="Datacenter")
    ```


    :param Sequence[str] filters: A list of tag IDs that must be present on an object to
           be a match.
    :param str name_regex: A regular expression that will be used to match
           the object's name.
    :param str type: The managed object type the returned object must match.
           The managed object types can be found in the managed object type section
           [here](https://developer.vmware.com/apis/968/vsphere).
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['nameRegex'] = name_regex
    __args__['type'] = type
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('vsphere:index/getDynamic:getDynamic', __args__, opts=opts, typ=GetDynamicResult).value

    return AwaitableGetDynamicResult(
        filters=__ret__.filters,
        id=__ret__.id,
        name_regex=__ret__.name_regex,
        type=__ret__.type)


@_utilities.lift_output_func(get_dynamic)
def get_dynamic_output(filters: Optional[pulumi.Input[Sequence[str]]] = None,
                       name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                       type: Optional[pulumi.Input[Optional[str]]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDynamicResult]:
    """
    [docs-about-morefs]: /docs/providers/vsphere/index.html#use-of-managed-object-references-by-the-vsphere-provider

    The _get_dynamic_ data source can be used to get the [managed object reference ID][docs-about-morefs]
    of any tagged managed object in vCenter Server by providing a list of tag IDs
    and an optional regular expression to filter objects by name.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_vsphere as vsphere

    category = vsphere.get_tag_category(name="SomeCategory")
    tag1 = vsphere.get_tag(name="FirstTag",
        category_id=data["vsphere_tag_category"]["cat"]["id"])
    tag2 = vsphere.get_tag(name="SecondTag",
        category_id=data["vsphere_tag_category"]["cat"]["id"])
    dyn = vsphere.get_dynamic(filters=[
            tag1.id,
            tag1.id,
        ],
        name_regex="ubuntu",
        type="Datacenter")
    ```


    :param Sequence[str] filters: A list of tag IDs that must be present on an object to
           be a match.
    :param str name_regex: A regular expression that will be used to match
           the object's name.
    :param str type: The managed object type the returned object must match.
           The managed object types can be found in the managed object type section
           [here](https://developer.vmware.com/apis/968/vsphere).
    """
    ...
