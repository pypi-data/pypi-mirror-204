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
    'GetThemeResult',
    'AwaitableGetThemeResult',
    'get_theme',
    'get_theme_output',
]

@pulumi.output_type
class GetThemeResult:
    """
    A collection of values returned by getTheme.
    """
    def __init__(__self__, background_image_url=None, brand_id=None, email_template_touch_point_variant=None, end_user_dashboard_touch_point_variant=None, error_page_touch_point_variant=None, favicon_url=None, id=None, links=None, logo_url=None, primary_color_contrast_hex=None, primary_color_hex=None, secondary_color_contrast_hex=None, secondary_color_hex=None, sign_in_page_touch_point_variant=None, theme_id=None):
        if background_image_url and not isinstance(background_image_url, str):
            raise TypeError("Expected argument 'background_image_url' to be a str")
        pulumi.set(__self__, "background_image_url", background_image_url)
        if brand_id and not isinstance(brand_id, str):
            raise TypeError("Expected argument 'brand_id' to be a str")
        pulumi.set(__self__, "brand_id", brand_id)
        if email_template_touch_point_variant and not isinstance(email_template_touch_point_variant, str):
            raise TypeError("Expected argument 'email_template_touch_point_variant' to be a str")
        pulumi.set(__self__, "email_template_touch_point_variant", email_template_touch_point_variant)
        if end_user_dashboard_touch_point_variant and not isinstance(end_user_dashboard_touch_point_variant, str):
            raise TypeError("Expected argument 'end_user_dashboard_touch_point_variant' to be a str")
        pulumi.set(__self__, "end_user_dashboard_touch_point_variant", end_user_dashboard_touch_point_variant)
        if error_page_touch_point_variant and not isinstance(error_page_touch_point_variant, str):
            raise TypeError("Expected argument 'error_page_touch_point_variant' to be a str")
        pulumi.set(__self__, "error_page_touch_point_variant", error_page_touch_point_variant)
        if favicon_url and not isinstance(favicon_url, str):
            raise TypeError("Expected argument 'favicon_url' to be a str")
        pulumi.set(__self__, "favicon_url", favicon_url)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if links and not isinstance(links, str):
            raise TypeError("Expected argument 'links' to be a str")
        pulumi.set(__self__, "links", links)
        if logo_url and not isinstance(logo_url, str):
            raise TypeError("Expected argument 'logo_url' to be a str")
        pulumi.set(__self__, "logo_url", logo_url)
        if primary_color_contrast_hex and not isinstance(primary_color_contrast_hex, str):
            raise TypeError("Expected argument 'primary_color_contrast_hex' to be a str")
        pulumi.set(__self__, "primary_color_contrast_hex", primary_color_contrast_hex)
        if primary_color_hex and not isinstance(primary_color_hex, str):
            raise TypeError("Expected argument 'primary_color_hex' to be a str")
        pulumi.set(__self__, "primary_color_hex", primary_color_hex)
        if secondary_color_contrast_hex and not isinstance(secondary_color_contrast_hex, str):
            raise TypeError("Expected argument 'secondary_color_contrast_hex' to be a str")
        pulumi.set(__self__, "secondary_color_contrast_hex", secondary_color_contrast_hex)
        if secondary_color_hex and not isinstance(secondary_color_hex, str):
            raise TypeError("Expected argument 'secondary_color_hex' to be a str")
        pulumi.set(__self__, "secondary_color_hex", secondary_color_hex)
        if sign_in_page_touch_point_variant and not isinstance(sign_in_page_touch_point_variant, str):
            raise TypeError("Expected argument 'sign_in_page_touch_point_variant' to be a str")
        pulumi.set(__self__, "sign_in_page_touch_point_variant", sign_in_page_touch_point_variant)
        if theme_id and not isinstance(theme_id, str):
            raise TypeError("Expected argument 'theme_id' to be a str")
        pulumi.set(__self__, "theme_id", theme_id)

    @property
    @pulumi.getter(name="backgroundImageUrl")
    def background_image_url(self) -> str:
        """
        Background image URL
        """
        return pulumi.get(self, "background_image_url")

    @property
    @pulumi.getter(name="brandId")
    def brand_id(self) -> str:
        return pulumi.get(self, "brand_id")

    @property
    @pulumi.getter(name="emailTemplateTouchPointVariant")
    def email_template_touch_point_variant(self) -> str:
        """
        (Enum) Variant for email templates (`OKTA_DEFAULT`, `FULL_THEME`)
        """
        return pulumi.get(self, "email_template_touch_point_variant")

    @property
    @pulumi.getter(name="endUserDashboardTouchPointVariant")
    def end_user_dashboard_touch_point_variant(self) -> str:
        """
        (Enum) Variant for the Okta End-User Dashboard (`OKTA_DEFAULT`, `WHITE_LOGO_BACKGROUND`, `FULL_THEME`, `LOGO_ON_FULL_WHITE_BACKGROUND`)
        """
        return pulumi.get(self, "end_user_dashboard_touch_point_variant")

    @property
    @pulumi.getter(name="errorPageTouchPointVariant")
    def error_page_touch_point_variant(self) -> str:
        """
        (Enum) Variant for the error page (`OKTA_DEFAULT`, `BACKGROUND_SECONDARY_COLOR`, `BACKGROUND_IMAGE`)
        """
        return pulumi.get(self, "error_page_touch_point_variant")

    @property
    @pulumi.getter(name="faviconUrl")
    def favicon_url(self) -> str:
        """
        Favicon URL
        """
        return pulumi.get(self, "favicon_url")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Theme URL
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def links(self) -> str:
        """
        Link relations for this object - JSON HAL - Discoverable resources related to the brand
        """
        return pulumi.get(self, "links")

    @property
    @pulumi.getter(name="logoUrl")
    def logo_url(self) -> str:
        """
        Logo URL
        """
        return pulumi.get(self, "logo_url")

    @property
    @pulumi.getter(name="primaryColorContrastHex")
    def primary_color_contrast_hex(self) -> str:
        """
        Primary color contrast hex code
        """
        return pulumi.get(self, "primary_color_contrast_hex")

    @property
    @pulumi.getter(name="primaryColorHex")
    def primary_color_hex(self) -> str:
        """
        Primary color hex code
        """
        return pulumi.get(self, "primary_color_hex")

    @property
    @pulumi.getter(name="secondaryColorContrastHex")
    def secondary_color_contrast_hex(self) -> str:
        """
        Secondary color contrast hex code
        """
        return pulumi.get(self, "secondary_color_contrast_hex")

    @property
    @pulumi.getter(name="secondaryColorHex")
    def secondary_color_hex(self) -> str:
        """
        Secondary color hex code
        """
        return pulumi.get(self, "secondary_color_hex")

    @property
    @pulumi.getter(name="signInPageTouchPointVariant")
    def sign_in_page_touch_point_variant(self) -> str:
        """
        (Enum) Variant for the Okta Sign-In Page (`OKTA_DEFAULT`, `BACKGROUND_SECONDARY_COLOR`, `BACKGROUND_IMAGE`)
        """
        return pulumi.get(self, "sign_in_page_touch_point_variant")

    @property
    @pulumi.getter(name="themeId")
    def theme_id(self) -> str:
        return pulumi.get(self, "theme_id")


class AwaitableGetThemeResult(GetThemeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetThemeResult(
            background_image_url=self.background_image_url,
            brand_id=self.brand_id,
            email_template_touch_point_variant=self.email_template_touch_point_variant,
            end_user_dashboard_touch_point_variant=self.end_user_dashboard_touch_point_variant,
            error_page_touch_point_variant=self.error_page_touch_point_variant,
            favicon_url=self.favicon_url,
            id=self.id,
            links=self.links,
            logo_url=self.logo_url,
            primary_color_contrast_hex=self.primary_color_contrast_hex,
            primary_color_hex=self.primary_color_hex,
            secondary_color_contrast_hex=self.secondary_color_contrast_hex,
            secondary_color_hex=self.secondary_color_hex,
            sign_in_page_touch_point_variant=self.sign_in_page_touch_point_variant,
            theme_id=self.theme_id)


def get_theme(brand_id: Optional[str] = None,
              theme_id: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetThemeResult:
    """
    Use this data source to retrieve a
    [Theme](https://developer.okta.com/docs/reference/api/brands/#theme-response-object)
    of a brand for an Okta orgnanization.


    :param str brand_id: Brand ID
    :param str theme_id: Theme ID
    """
    __args__ = dict()
    __args__['brandId'] = brand_id
    __args__['themeId'] = theme_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('okta:index/getTheme:getTheme', __args__, opts=opts, typ=GetThemeResult).value

    return AwaitableGetThemeResult(
        background_image_url=__ret__.background_image_url,
        brand_id=__ret__.brand_id,
        email_template_touch_point_variant=__ret__.email_template_touch_point_variant,
        end_user_dashboard_touch_point_variant=__ret__.end_user_dashboard_touch_point_variant,
        error_page_touch_point_variant=__ret__.error_page_touch_point_variant,
        favicon_url=__ret__.favicon_url,
        id=__ret__.id,
        links=__ret__.links,
        logo_url=__ret__.logo_url,
        primary_color_contrast_hex=__ret__.primary_color_contrast_hex,
        primary_color_hex=__ret__.primary_color_hex,
        secondary_color_contrast_hex=__ret__.secondary_color_contrast_hex,
        secondary_color_hex=__ret__.secondary_color_hex,
        sign_in_page_touch_point_variant=__ret__.sign_in_page_touch_point_variant,
        theme_id=__ret__.theme_id)


@_utilities.lift_output_func(get_theme)
def get_theme_output(brand_id: Optional[pulumi.Input[str]] = None,
                     theme_id: Optional[pulumi.Input[str]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetThemeResult]:
    """
    Use this data source to retrieve a
    [Theme](https://developer.okta.com/docs/reference/api/brands/#theme-response-object)
    of a brand for an Okta orgnanization.


    :param str brand_id: Brand ID
    :param str theme_id: Theme ID
    """
    ...
