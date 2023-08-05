# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['UserArgs', 'User']

@pulumi.input_type
class UserArgs:
    def __init__(__self__, *,
                 app_id: pulumi.Input[str],
                 user_id: pulumi.Input[str],
                 password: Optional[pulumi.Input[str]] = None,
                 profile: Optional[pulumi.Input[str]] = None,
                 retain_assignment: Optional[pulumi.Input[bool]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a User resource.
        :param pulumi.Input[str] app_id: App to associate user with.
        :param pulumi.Input[str] user_id: User to associate the application with.
        :param pulumi.Input[str] password: The password to use.
        :param pulumi.Input[str] profile: The JSON profile of the App User.
        :param pulumi.Input[bool] retain_assignment: Retain the user association on destroy. If set to true, the resource will be removed from state but not from the Okta app.
        :param pulumi.Input[str] username: The username to use for the app user. In case the user is assigned to the app with 
               'SHARED_USERNAME_AND_PASSWORD' credentials scheme, this field will be computed and should not be set.
        """
        pulumi.set(__self__, "app_id", app_id)
        pulumi.set(__self__, "user_id", user_id)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if profile is not None:
            pulumi.set(__self__, "profile", profile)
        if retain_assignment is not None:
            pulumi.set(__self__, "retain_assignment", retain_assignment)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> pulumi.Input[str]:
        """
        App to associate user with.
        """
        return pulumi.get(self, "app_id")

    @app_id.setter
    def app_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "app_id", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Input[str]:
        """
        User to associate the application with.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_id", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The password to use.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter
    def profile(self) -> Optional[pulumi.Input[str]]:
        """
        The JSON profile of the App User.
        """
        return pulumi.get(self, "profile")

    @profile.setter
    def profile(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "profile", value)

    @property
    @pulumi.getter(name="retainAssignment")
    def retain_assignment(self) -> Optional[pulumi.Input[bool]]:
        """
        Retain the user association on destroy. If set to true, the resource will be removed from state but not from the Okta app.
        """
        return pulumi.get(self, "retain_assignment")

    @retain_assignment.setter
    def retain_assignment(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "retain_assignment", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        """
        The username to use for the app user. In case the user is assigned to the app with 
        'SHARED_USERNAME_AND_PASSWORD' credentials scheme, this field will be computed and should not be set.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


@pulumi.input_type
class _UserState:
    def __init__(__self__, *,
                 app_id: Optional[pulumi.Input[str]] = None,
                 has_shared_username: Optional[pulumi.Input[bool]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 profile: Optional[pulumi.Input[str]] = None,
                 retain_assignment: Optional[pulumi.Input[bool]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering User resources.
        :param pulumi.Input[str] app_id: App to associate user with.
        :param pulumi.Input[str] password: The password to use.
        :param pulumi.Input[str] profile: The JSON profile of the App User.
        :param pulumi.Input[bool] retain_assignment: Retain the user association on destroy. If set to true, the resource will be removed from state but not from the Okta app.
        :param pulumi.Input[str] user_id: User to associate the application with.
        :param pulumi.Input[str] username: The username to use for the app user. In case the user is assigned to the app with 
               'SHARED_USERNAME_AND_PASSWORD' credentials scheme, this field will be computed and should not be set.
        """
        if app_id is not None:
            pulumi.set(__self__, "app_id", app_id)
        if has_shared_username is not None:
            pulumi.set(__self__, "has_shared_username", has_shared_username)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if profile is not None:
            pulumi.set(__self__, "profile", profile)
        if retain_assignment is not None:
            pulumi.set(__self__, "retain_assignment", retain_assignment)
        if user_id is not None:
            pulumi.set(__self__, "user_id", user_id)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> Optional[pulumi.Input[str]]:
        """
        App to associate user with.
        """
        return pulumi.get(self, "app_id")

    @app_id.setter
    def app_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "app_id", value)

    @property
    @pulumi.getter(name="hasSharedUsername")
    def has_shared_username(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "has_shared_username")

    @has_shared_username.setter
    def has_shared_username(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "has_shared_username", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The password to use.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter
    def profile(self) -> Optional[pulumi.Input[str]]:
        """
        The JSON profile of the App User.
        """
        return pulumi.get(self, "profile")

    @profile.setter
    def profile(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "profile", value)

    @property
    @pulumi.getter(name="retainAssignment")
    def retain_assignment(self) -> Optional[pulumi.Input[bool]]:
        """
        Retain the user association on destroy. If set to true, the resource will be removed from state but not from the Okta app.
        """
        return pulumi.get(self, "retain_assignment")

    @retain_assignment.setter
    def retain_assignment(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "retain_assignment", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> Optional[pulumi.Input[str]]:
        """
        User to associate the application with.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_id", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        """
        The username to use for the app user. In case the user is assigned to the app with 
        'SHARED_USERNAME_AND_PASSWORD' credentials scheme, this field will be computed and should not be set.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


class User(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_id: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 profile: Optional[pulumi.Input[str]] = None,
                 retain_assignment: Optional[pulumi.Input[bool]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.app.User("example",
            app_id="<app_id>",
            user_id="<user id>",
            username="example")
        ```

        ## Import

        An Application User can be imported via the Okta ID.

        ```sh
         $ pulumi import okta:app/user:User example &#60;app id&#62;/&#60;user id&#62;
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] app_id: App to associate user with.
        :param pulumi.Input[str] password: The password to use.
        :param pulumi.Input[str] profile: The JSON profile of the App User.
        :param pulumi.Input[bool] retain_assignment: Retain the user association on destroy. If set to true, the resource will be removed from state but not from the Okta app.
        :param pulumi.Input[str] user_id: User to associate the application with.
        :param pulumi.Input[str] username: The username to use for the app user. In case the user is assigned to the app with 
               'SHARED_USERNAME_AND_PASSWORD' credentials scheme, this field will be computed and should not be set.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.app.User("example",
            app_id="<app_id>",
            user_id="<user id>",
            username="example")
        ```

        ## Import

        An Application User can be imported via the Okta ID.

        ```sh
         $ pulumi import okta:app/user:User example &#60;app id&#62;/&#60;user id&#62;
        ```

        :param str resource_name: The name of the resource.
        :param UserArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_id: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 profile: Optional[pulumi.Input[str]] = None,
                 retain_assignment: Optional[pulumi.Input[bool]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserArgs.__new__(UserArgs)

            if app_id is None and not opts.urn:
                raise TypeError("Missing required property 'app_id'")
            __props__.__dict__["app_id"] = app_id
            __props__.__dict__["password"] = None if password is None else pulumi.Output.secret(password)
            __props__.__dict__["profile"] = profile
            __props__.__dict__["retain_assignment"] = retain_assignment
            if user_id is None and not opts.urn:
                raise TypeError("Missing required property 'user_id'")
            __props__.__dict__["user_id"] = user_id
            __props__.__dict__["username"] = username
            __props__.__dict__["has_shared_username"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["password"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(User, __self__).__init__(
            'okta:app/user:User',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            app_id: Optional[pulumi.Input[str]] = None,
            has_shared_username: Optional[pulumi.Input[bool]] = None,
            password: Optional[pulumi.Input[str]] = None,
            profile: Optional[pulumi.Input[str]] = None,
            retain_assignment: Optional[pulumi.Input[bool]] = None,
            user_id: Optional[pulumi.Input[str]] = None,
            username: Optional[pulumi.Input[str]] = None) -> 'User':
        """
        Get an existing User resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] app_id: App to associate user with.
        :param pulumi.Input[str] password: The password to use.
        :param pulumi.Input[str] profile: The JSON profile of the App User.
        :param pulumi.Input[bool] retain_assignment: Retain the user association on destroy. If set to true, the resource will be removed from state but not from the Okta app.
        :param pulumi.Input[str] user_id: User to associate the application with.
        :param pulumi.Input[str] username: The username to use for the app user. In case the user is assigned to the app with 
               'SHARED_USERNAME_AND_PASSWORD' credentials scheme, this field will be computed and should not be set.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UserState.__new__(_UserState)

        __props__.__dict__["app_id"] = app_id
        __props__.__dict__["has_shared_username"] = has_shared_username
        __props__.__dict__["password"] = password
        __props__.__dict__["profile"] = profile
        __props__.__dict__["retain_assignment"] = retain_assignment
        __props__.__dict__["user_id"] = user_id
        __props__.__dict__["username"] = username
        return User(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> pulumi.Output[str]:
        """
        App to associate user with.
        """
        return pulumi.get(self, "app_id")

    @property
    @pulumi.getter(name="hasSharedUsername")
    def has_shared_username(self) -> pulumi.Output[bool]:
        return pulumi.get(self, "has_shared_username")

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[Optional[str]]:
        """
        The password to use.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter
    def profile(self) -> pulumi.Output[Optional[str]]:
        """
        The JSON profile of the App User.
        """
        return pulumi.get(self, "profile")

    @property
    @pulumi.getter(name="retainAssignment")
    def retain_assignment(self) -> pulumi.Output[Optional[bool]]:
        """
        Retain the user association on destroy. If set to true, the resource will be removed from state but not from the Okta app.
        """
        return pulumi.get(self, "retain_assignment")

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Output[str]:
        """
        User to associate the application with.
        """
        return pulumi.get(self, "user_id")

    @property
    @pulumi.getter
    def username(self) -> pulumi.Output[Optional[str]]:
        """
        The username to use for the app user. In case the user is assigned to the app with 
        'SHARED_USERNAME_AND_PASSWORD' credentials scheme, this field will be computed and should not be set.
        """
        return pulumi.get(self, "username")

