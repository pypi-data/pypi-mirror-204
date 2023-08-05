# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['ResourceSetArgs', 'ResourceSet']

@pulumi.input_type
class ResourceSetArgs:
    def __init__(__self__, *,
                 description: pulumi.Input[str],
                 label: pulumi.Input[str],
                 resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ResourceSet resource.
        :param pulumi.Input[str] description: A description of the Resource Set.
        :param pulumi.Input[str] label: Unique name given to the Resource Set.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resources: The endpoints that reference the resources to be included in the new Resource Set. At least one
               endpoint must be specified when creating resource set.
        """
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "label", label)
        if resources is not None:
            pulumi.set(__self__, "resources", resources)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Input[str]:
        """
        A description of the Resource Set.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: pulumi.Input[str]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def label(self) -> pulumi.Input[str]:
        """
        Unique name given to the Resource Set.
        """
        return pulumi.get(self, "label")

    @label.setter
    def label(self, value: pulumi.Input[str]):
        pulumi.set(self, "label", value)

    @property
    @pulumi.getter
    def resources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The endpoints that reference the resources to be included in the new Resource Set. At least one
        endpoint must be specified when creating resource set.
        """
        return pulumi.get(self, "resources")

    @resources.setter
    def resources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "resources", value)


@pulumi.input_type
class _ResourceSetState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 label: Optional[pulumi.Input[str]] = None,
                 resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering ResourceSet resources.
        :param pulumi.Input[str] description: A description of the Resource Set.
        :param pulumi.Input[str] label: Unique name given to the Resource Set.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resources: The endpoints that reference the resources to be included in the new Resource Set. At least one
               endpoint must be specified when creating resource set.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if label is not None:
            pulumi.set(__self__, "label", label)
        if resources is not None:
            pulumi.set(__self__, "resources", resources)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of the Resource Set.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def label(self) -> Optional[pulumi.Input[str]]:
        """
        Unique name given to the Resource Set.
        """
        return pulumi.get(self, "label")

    @label.setter
    def label(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "label", value)

    @property
    @pulumi.getter
    def resources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The endpoints that reference the resources to be included in the new Resource Set. At least one
        endpoint must be specified when creating resource set.
        """
        return pulumi.get(self, "resources")

    @resources.setter
    def resources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "resources", value)


class ResourceSet(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 label: Optional[pulumi.Input[str]] = None,
                 resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        This resource allows the creation and manipulation of Okta Resource Sets as custom collections of Okta resources. You can use
        Okta Resource Sets to assign Custom Roles to administrators who are scoped to the designated resources.
        The `resources` field supports the following:
         - Apps
         - Groups
         - All Users within a Group
         - All Users within the org
         - All Groups within the org
         - All Apps within the org
         - All Apps of the same type

        > **NOTE:** This an `Early Access` feature.

        ## Import

        Okta Resource Set can be imported via the Okta ID.

        ```sh
         $ pulumi import okta:index/resourceSet:ResourceSet example &#60;resource_set_id&#62;
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A description of the Resource Set.
        :param pulumi.Input[str] label: Unique name given to the Resource Set.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resources: The endpoints that reference the resources to be included in the new Resource Set. At least one
               endpoint must be specified when creating resource set.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ResourceSetArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This resource allows the creation and manipulation of Okta Resource Sets as custom collections of Okta resources. You can use
        Okta Resource Sets to assign Custom Roles to administrators who are scoped to the designated resources.
        The `resources` field supports the following:
         - Apps
         - Groups
         - All Users within a Group
         - All Users within the org
         - All Groups within the org
         - All Apps within the org
         - All Apps of the same type

        > **NOTE:** This an `Early Access` feature.

        ## Import

        Okta Resource Set can be imported via the Okta ID.

        ```sh
         $ pulumi import okta:index/resourceSet:ResourceSet example &#60;resource_set_id&#62;
        ```

        :param str resource_name: The name of the resource.
        :param ResourceSetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResourceSetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 label: Optional[pulumi.Input[str]] = None,
                 resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ResourceSetArgs.__new__(ResourceSetArgs)

            if description is None and not opts.urn:
                raise TypeError("Missing required property 'description'")
            __props__.__dict__["description"] = description
            if label is None and not opts.urn:
                raise TypeError("Missing required property 'label'")
            __props__.__dict__["label"] = label
            __props__.__dict__["resources"] = resources
        super(ResourceSet, __self__).__init__(
            'okta:index/resourceSet:ResourceSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            label: Optional[pulumi.Input[str]] = None,
            resources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'ResourceSet':
        """
        Get an existing ResourceSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A description of the Resource Set.
        :param pulumi.Input[str] label: Unique name given to the Resource Set.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resources: The endpoints that reference the resources to be included in the new Resource Set. At least one
               endpoint must be specified when creating resource set.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ResourceSetState.__new__(_ResourceSetState)

        __props__.__dict__["description"] = description
        __props__.__dict__["label"] = label
        __props__.__dict__["resources"] = resources
        return ResourceSet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        A description of the Resource Set.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def label(self) -> pulumi.Output[str]:
        """
        Unique name given to the Resource Set.
        """
        return pulumi.get(self, "label")

    @property
    @pulumi.getter
    def resources(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The endpoints that reference the resources to be included in the new Resource Set. At least one
        endpoint must be specified when creating resource set.
        """
        return pulumi.get(self, "resources")

