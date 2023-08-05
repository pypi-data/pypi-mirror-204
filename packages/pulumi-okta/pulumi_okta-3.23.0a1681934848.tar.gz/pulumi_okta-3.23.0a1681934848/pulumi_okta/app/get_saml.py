# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetSamlResult',
    'AwaitableGetSamlResult',
    'get_saml',
    'get_saml_output',
]

@pulumi.output_type
class GetSamlResult:
    """
    A collection of values returned by getSaml.
    """
    def __init__(__self__, accessibility_error_redirect_url=None, accessibility_login_redirect_url=None, accessibility_self_service=None, acs_endpoints=None, active_only=None, app_settings_json=None, assertion_signed=None, attribute_statements=None, audience=None, authn_context_class_ref=None, auto_submit_toolbar=None, default_relay_state=None, destination=None, digest_algorithm=None, features=None, groups=None, hide_ios=None, hide_web=None, honor_force_authn=None, id=None, idp_issuer=None, inline_hook_id=None, key_id=None, label=None, label_prefix=None, links=None, name=None, recipient=None, request_compressed=None, response_signed=None, saml_signed_request_enabled=None, signature_algorithm=None, single_logout_certificate=None, single_logout_issuer=None, single_logout_url=None, skip_groups=None, skip_users=None, sp_issuer=None, sso_url=None, status=None, subject_name_id_format=None, subject_name_id_template=None, user_name_template=None, user_name_template_push_status=None, user_name_template_suffix=None, user_name_template_type=None, users=None):
        if accessibility_error_redirect_url and not isinstance(accessibility_error_redirect_url, str):
            raise TypeError("Expected argument 'accessibility_error_redirect_url' to be a str")
        pulumi.set(__self__, "accessibility_error_redirect_url", accessibility_error_redirect_url)
        if accessibility_login_redirect_url and not isinstance(accessibility_login_redirect_url, str):
            raise TypeError("Expected argument 'accessibility_login_redirect_url' to be a str")
        pulumi.set(__self__, "accessibility_login_redirect_url", accessibility_login_redirect_url)
        if accessibility_self_service and not isinstance(accessibility_self_service, bool):
            raise TypeError("Expected argument 'accessibility_self_service' to be a bool")
        pulumi.set(__self__, "accessibility_self_service", accessibility_self_service)
        if acs_endpoints and not isinstance(acs_endpoints, list):
            raise TypeError("Expected argument 'acs_endpoints' to be a list")
        pulumi.set(__self__, "acs_endpoints", acs_endpoints)
        if active_only and not isinstance(active_only, bool):
            raise TypeError("Expected argument 'active_only' to be a bool")
        pulumi.set(__self__, "active_only", active_only)
        if app_settings_json and not isinstance(app_settings_json, str):
            raise TypeError("Expected argument 'app_settings_json' to be a str")
        pulumi.set(__self__, "app_settings_json", app_settings_json)
        if assertion_signed and not isinstance(assertion_signed, bool):
            raise TypeError("Expected argument 'assertion_signed' to be a bool")
        pulumi.set(__self__, "assertion_signed", assertion_signed)
        if attribute_statements and not isinstance(attribute_statements, list):
            raise TypeError("Expected argument 'attribute_statements' to be a list")
        pulumi.set(__self__, "attribute_statements", attribute_statements)
        if audience and not isinstance(audience, str):
            raise TypeError("Expected argument 'audience' to be a str")
        pulumi.set(__self__, "audience", audience)
        if authn_context_class_ref and not isinstance(authn_context_class_ref, str):
            raise TypeError("Expected argument 'authn_context_class_ref' to be a str")
        pulumi.set(__self__, "authn_context_class_ref", authn_context_class_ref)
        if auto_submit_toolbar and not isinstance(auto_submit_toolbar, bool):
            raise TypeError("Expected argument 'auto_submit_toolbar' to be a bool")
        pulumi.set(__self__, "auto_submit_toolbar", auto_submit_toolbar)
        if default_relay_state and not isinstance(default_relay_state, str):
            raise TypeError("Expected argument 'default_relay_state' to be a str")
        pulumi.set(__self__, "default_relay_state", default_relay_state)
        if destination and not isinstance(destination, str):
            raise TypeError("Expected argument 'destination' to be a str")
        pulumi.set(__self__, "destination", destination)
        if digest_algorithm and not isinstance(digest_algorithm, str):
            raise TypeError("Expected argument 'digest_algorithm' to be a str")
        pulumi.set(__self__, "digest_algorithm", digest_algorithm)
        if features and not isinstance(features, list):
            raise TypeError("Expected argument 'features' to be a list")
        pulumi.set(__self__, "features", features)
        if groups and not isinstance(groups, list):
            raise TypeError("Expected argument 'groups' to be a list")
        if groups is not None:
            warnings.warn("""The `groups` field is now deprecated for the data source `okta_app_saml`, please replace all uses of this with: `okta_app_group_assignments`""", DeprecationWarning)
            pulumi.log.warn("""groups is deprecated: The `groups` field is now deprecated for the data source `okta_app_saml`, please replace all uses of this with: `okta_app_group_assignments`""")

        pulumi.set(__self__, "groups", groups)
        if hide_ios and not isinstance(hide_ios, bool):
            raise TypeError("Expected argument 'hide_ios' to be a bool")
        pulumi.set(__self__, "hide_ios", hide_ios)
        if hide_web and not isinstance(hide_web, bool):
            raise TypeError("Expected argument 'hide_web' to be a bool")
        pulumi.set(__self__, "hide_web", hide_web)
        if honor_force_authn and not isinstance(honor_force_authn, bool):
            raise TypeError("Expected argument 'honor_force_authn' to be a bool")
        pulumi.set(__self__, "honor_force_authn", honor_force_authn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if idp_issuer and not isinstance(idp_issuer, str):
            raise TypeError("Expected argument 'idp_issuer' to be a str")
        pulumi.set(__self__, "idp_issuer", idp_issuer)
        if inline_hook_id and not isinstance(inline_hook_id, str):
            raise TypeError("Expected argument 'inline_hook_id' to be a str")
        pulumi.set(__self__, "inline_hook_id", inline_hook_id)
        if key_id and not isinstance(key_id, str):
            raise TypeError("Expected argument 'key_id' to be a str")
        pulumi.set(__self__, "key_id", key_id)
        if label and not isinstance(label, str):
            raise TypeError("Expected argument 'label' to be a str")
        pulumi.set(__self__, "label", label)
        if label_prefix and not isinstance(label_prefix, str):
            raise TypeError("Expected argument 'label_prefix' to be a str")
        pulumi.set(__self__, "label_prefix", label_prefix)
        if links and not isinstance(links, str):
            raise TypeError("Expected argument 'links' to be a str")
        pulumi.set(__self__, "links", links)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if recipient and not isinstance(recipient, str):
            raise TypeError("Expected argument 'recipient' to be a str")
        pulumi.set(__self__, "recipient", recipient)
        if request_compressed and not isinstance(request_compressed, bool):
            raise TypeError("Expected argument 'request_compressed' to be a bool")
        pulumi.set(__self__, "request_compressed", request_compressed)
        if response_signed and not isinstance(response_signed, bool):
            raise TypeError("Expected argument 'response_signed' to be a bool")
        pulumi.set(__self__, "response_signed", response_signed)
        if saml_signed_request_enabled and not isinstance(saml_signed_request_enabled, bool):
            raise TypeError("Expected argument 'saml_signed_request_enabled' to be a bool")
        pulumi.set(__self__, "saml_signed_request_enabled", saml_signed_request_enabled)
        if signature_algorithm and not isinstance(signature_algorithm, str):
            raise TypeError("Expected argument 'signature_algorithm' to be a str")
        pulumi.set(__self__, "signature_algorithm", signature_algorithm)
        if single_logout_certificate and not isinstance(single_logout_certificate, str):
            raise TypeError("Expected argument 'single_logout_certificate' to be a str")
        pulumi.set(__self__, "single_logout_certificate", single_logout_certificate)
        if single_logout_issuer and not isinstance(single_logout_issuer, str):
            raise TypeError("Expected argument 'single_logout_issuer' to be a str")
        pulumi.set(__self__, "single_logout_issuer", single_logout_issuer)
        if single_logout_url and not isinstance(single_logout_url, str):
            raise TypeError("Expected argument 'single_logout_url' to be a str")
        pulumi.set(__self__, "single_logout_url", single_logout_url)
        if skip_groups and not isinstance(skip_groups, bool):
            raise TypeError("Expected argument 'skip_groups' to be a bool")
        pulumi.set(__self__, "skip_groups", skip_groups)
        if skip_users and not isinstance(skip_users, bool):
            raise TypeError("Expected argument 'skip_users' to be a bool")
        pulumi.set(__self__, "skip_users", skip_users)
        if sp_issuer and not isinstance(sp_issuer, str):
            raise TypeError("Expected argument 'sp_issuer' to be a str")
        pulumi.set(__self__, "sp_issuer", sp_issuer)
        if sso_url and not isinstance(sso_url, str):
            raise TypeError("Expected argument 'sso_url' to be a str")
        pulumi.set(__self__, "sso_url", sso_url)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if subject_name_id_format and not isinstance(subject_name_id_format, str):
            raise TypeError("Expected argument 'subject_name_id_format' to be a str")
        pulumi.set(__self__, "subject_name_id_format", subject_name_id_format)
        if subject_name_id_template and not isinstance(subject_name_id_template, str):
            raise TypeError("Expected argument 'subject_name_id_template' to be a str")
        pulumi.set(__self__, "subject_name_id_template", subject_name_id_template)
        if user_name_template and not isinstance(user_name_template, str):
            raise TypeError("Expected argument 'user_name_template' to be a str")
        pulumi.set(__self__, "user_name_template", user_name_template)
        if user_name_template_push_status and not isinstance(user_name_template_push_status, str):
            raise TypeError("Expected argument 'user_name_template_push_status' to be a str")
        pulumi.set(__self__, "user_name_template_push_status", user_name_template_push_status)
        if user_name_template_suffix and not isinstance(user_name_template_suffix, str):
            raise TypeError("Expected argument 'user_name_template_suffix' to be a str")
        pulumi.set(__self__, "user_name_template_suffix", user_name_template_suffix)
        if user_name_template_type and not isinstance(user_name_template_type, str):
            raise TypeError("Expected argument 'user_name_template_type' to be a str")
        pulumi.set(__self__, "user_name_template_type", user_name_template_type)
        if users and not isinstance(users, list):
            raise TypeError("Expected argument 'users' to be a list")
        if users is not None:
            warnings.warn("""The `users` field is now deprecated for the data source `okta_app_saml`, please replace all uses of this with: `okta_app_user_assignments`""", DeprecationWarning)
            pulumi.log.warn("""users is deprecated: The `users` field is now deprecated for the data source `okta_app_saml`, please replace all uses of this with: `okta_app_user_assignments`""")

        pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter(name="accessibilityErrorRedirectUrl")
    def accessibility_error_redirect_url(self) -> str:
        """
        Custom error page URL.
        """
        return pulumi.get(self, "accessibility_error_redirect_url")

    @property
    @pulumi.getter(name="accessibilityLoginRedirectUrl")
    def accessibility_login_redirect_url(self) -> str:
        """
        Custom login page URL.
        """
        return pulumi.get(self, "accessibility_login_redirect_url")

    @property
    @pulumi.getter(name="accessibilitySelfService")
    def accessibility_self_service(self) -> bool:
        """
        Enable self-service.
        """
        return pulumi.get(self, "accessibility_self_service")

    @property
    @pulumi.getter(name="acsEndpoints")
    def acs_endpoints(self) -> Sequence[str]:
        """
        An array of ACS endpoints. You can configure a maximum of 100 endpoints.
        """
        return pulumi.get(self, "acs_endpoints")

    @property
    @pulumi.getter(name="activeOnly")
    def active_only(self) -> Optional[bool]:
        return pulumi.get(self, "active_only")

    @property
    @pulumi.getter(name="appSettingsJson")
    def app_settings_json(self) -> str:
        """
        Application settings in JSON format.
        """
        return pulumi.get(self, "app_settings_json")

    @property
    @pulumi.getter(name="assertionSigned")
    def assertion_signed(self) -> bool:
        """
        Determines whether the SAML assertion is digitally signed.
        """
        return pulumi.get(self, "assertion_signed")

    @property
    @pulumi.getter(name="attributeStatements")
    def attribute_statements(self) -> Sequence['outputs.GetSamlAttributeStatementResult']:
        """
        List of SAML Attribute statements.
        """
        return pulumi.get(self, "attribute_statements")

    @property
    @pulumi.getter
    def audience(self) -> str:
        """
        Audience restriction.
        """
        return pulumi.get(self, "audience")

    @property
    @pulumi.getter(name="authnContextClassRef")
    def authn_context_class_ref(self) -> str:
        """
        Identifies the SAML authentication context class for the assertion’s authentication statement.
        """
        return pulumi.get(self, "authn_context_class_ref")

    @property
    @pulumi.getter(name="autoSubmitToolbar")
    def auto_submit_toolbar(self) -> bool:
        """
        Display auto submit toolbar.
        """
        return pulumi.get(self, "auto_submit_toolbar")

    @property
    @pulumi.getter(name="defaultRelayState")
    def default_relay_state(self) -> str:
        """
        Identifies a specific application resource in an IDP initiated SSO scenario.
        """
        return pulumi.get(self, "default_relay_state")

    @property
    @pulumi.getter
    def destination(self) -> str:
        """
        Identifies the location where the SAML response is intended to be sent inside the SAML assertion.
        """
        return pulumi.get(self, "destination")

    @property
    @pulumi.getter(name="digestAlgorithm")
    def digest_algorithm(self) -> str:
        """
        Determines the digest algorithm used to digitally sign the SAML assertion and response.
        """
        return pulumi.get(self, "digest_algorithm")

    @property
    @pulumi.getter
    def features(self) -> Sequence[str]:
        """
        features enabled.
        """
        return pulumi.get(self, "features")

    @property
    @pulumi.getter
    def groups(self) -> Sequence[str]:
        """
        List of groups IDs assigned to the application.
        """
        return pulumi.get(self, "groups")

    @property
    @pulumi.getter(name="hideIos")
    def hide_ios(self) -> bool:
        """
        Do not display application icon on mobile app.
        """
        return pulumi.get(self, "hide_ios")

    @property
    @pulumi.getter(name="hideWeb")
    def hide_web(self) -> bool:
        """
        Do not display application icon to users
        """
        return pulumi.get(self, "hide_web")

    @property
    @pulumi.getter(name="honorForceAuthn")
    def honor_force_authn(self) -> bool:
        """
        Prompt user to re-authenticate if SP asks for it.
        """
        return pulumi.get(self, "honor_force_authn")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        id of application.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="idpIssuer")
    def idp_issuer(self) -> str:
        """
        SAML issuer ID.
        """
        return pulumi.get(self, "idp_issuer")

    @property
    @pulumi.getter(name="inlineHookId")
    def inline_hook_id(self) -> str:
        """
        Saml Inline Hook associated with the application.
        """
        return pulumi.get(self, "inline_hook_id")

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> str:
        """
        Certificate key ID.
        """
        return pulumi.get(self, "key_id")

    @property
    @pulumi.getter
    def label(self) -> Optional[str]:
        """
        label of application.
        """
        return pulumi.get(self, "label")

    @property
    @pulumi.getter(name="labelPrefix")
    def label_prefix(self) -> Optional[str]:
        return pulumi.get(self, "label_prefix")

    @property
    @pulumi.getter
    def links(self) -> str:
        """
        Generic JSON containing discoverable resources related to the app.
        """
        return pulumi.get(self, "links")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        name of application.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def recipient(self) -> str:
        """
        The location where the app may present the SAML assertion.
        """
        return pulumi.get(self, "recipient")

    @property
    @pulumi.getter(name="requestCompressed")
    def request_compressed(self) -> Optional[bool]:
        """
        Denotes whether the request is compressed or not.
        """
        return pulumi.get(self, "request_compressed")

    @property
    @pulumi.getter(name="responseSigned")
    def response_signed(self) -> bool:
        """
        Determines whether the SAML auth response message is digitally signed.
        """
        return pulumi.get(self, "response_signed")

    @property
    @pulumi.getter(name="samlSignedRequestEnabled")
    def saml_signed_request_enabled(self) -> bool:
        """
        SAML Signed Request enabled
        """
        return pulumi.get(self, "saml_signed_request_enabled")

    @property
    @pulumi.getter(name="signatureAlgorithm")
    def signature_algorithm(self) -> str:
        """
        Signature algorithm used ot digitally sign the assertion and response.
        """
        return pulumi.get(self, "signature_algorithm")

    @property
    @pulumi.getter(name="singleLogoutCertificate")
    def single_logout_certificate(self) -> str:
        """
        x509 encoded certificate that the Service Provider uses to sign Single Logout requests.
        """
        return pulumi.get(self, "single_logout_certificate")

    @property
    @pulumi.getter(name="singleLogoutIssuer")
    def single_logout_issuer(self) -> str:
        """
        The issuer of the Service Provider that generates the Single Logout request.
        """
        return pulumi.get(self, "single_logout_issuer")

    @property
    @pulumi.getter(name="singleLogoutUrl")
    def single_logout_url(self) -> str:
        """
        The location where the logout response is sent.
        """
        return pulumi.get(self, "single_logout_url")

    @property
    @pulumi.getter(name="skipGroups")
    def skip_groups(self) -> Optional[bool]:
        return pulumi.get(self, "skip_groups")

    @property
    @pulumi.getter(name="skipUsers")
    def skip_users(self) -> Optional[bool]:
        return pulumi.get(self, "skip_users")

    @property
    @pulumi.getter(name="spIssuer")
    def sp_issuer(self) -> str:
        """
        SAML service provider issuer.
        """
        return pulumi.get(self, "sp_issuer")

    @property
    @pulumi.getter(name="ssoUrl")
    def sso_url(self) -> str:
        """
        Single Sign-on Url.
        """
        return pulumi.get(self, "sso_url")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        status of application.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="subjectNameIdFormat")
    def subject_name_id_format(self) -> str:
        """
        Identifies the SAML processing rules.
        """
        return pulumi.get(self, "subject_name_id_format")

    @property
    @pulumi.getter(name="subjectNameIdTemplate")
    def subject_name_id_template(self) -> str:
        """
        Template for app user's username when a user is assigned to the app.
        """
        return pulumi.get(self, "subject_name_id_template")

    @property
    @pulumi.getter(name="userNameTemplate")
    def user_name_template(self) -> str:
        """
        Username template.
        """
        return pulumi.get(self, "user_name_template")

    @property
    @pulumi.getter(name="userNameTemplatePushStatus")
    def user_name_template_push_status(self) -> str:
        """
        Push username on update.
        """
        return pulumi.get(self, "user_name_template_push_status")

    @property
    @pulumi.getter(name="userNameTemplateSuffix")
    def user_name_template_suffix(self) -> str:
        """
        Username template suffix.
        """
        return pulumi.get(self, "user_name_template_suffix")

    @property
    @pulumi.getter(name="userNameTemplateType")
    def user_name_template_type(self) -> str:
        """
        Username template type.
        """
        return pulumi.get(self, "user_name_template_type")

    @property
    @pulumi.getter
    def users(self) -> Sequence[str]:
        """
        List of users IDs assigned to the application.
        """
        return pulumi.get(self, "users")


class AwaitableGetSamlResult(GetSamlResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSamlResult(
            accessibility_error_redirect_url=self.accessibility_error_redirect_url,
            accessibility_login_redirect_url=self.accessibility_login_redirect_url,
            accessibility_self_service=self.accessibility_self_service,
            acs_endpoints=self.acs_endpoints,
            active_only=self.active_only,
            app_settings_json=self.app_settings_json,
            assertion_signed=self.assertion_signed,
            attribute_statements=self.attribute_statements,
            audience=self.audience,
            authn_context_class_ref=self.authn_context_class_ref,
            auto_submit_toolbar=self.auto_submit_toolbar,
            default_relay_state=self.default_relay_state,
            destination=self.destination,
            digest_algorithm=self.digest_algorithm,
            features=self.features,
            groups=self.groups,
            hide_ios=self.hide_ios,
            hide_web=self.hide_web,
            honor_force_authn=self.honor_force_authn,
            id=self.id,
            idp_issuer=self.idp_issuer,
            inline_hook_id=self.inline_hook_id,
            key_id=self.key_id,
            label=self.label,
            label_prefix=self.label_prefix,
            links=self.links,
            name=self.name,
            recipient=self.recipient,
            request_compressed=self.request_compressed,
            response_signed=self.response_signed,
            saml_signed_request_enabled=self.saml_signed_request_enabled,
            signature_algorithm=self.signature_algorithm,
            single_logout_certificate=self.single_logout_certificate,
            single_logout_issuer=self.single_logout_issuer,
            single_logout_url=self.single_logout_url,
            skip_groups=self.skip_groups,
            skip_users=self.skip_users,
            sp_issuer=self.sp_issuer,
            sso_url=self.sso_url,
            status=self.status,
            subject_name_id_format=self.subject_name_id_format,
            subject_name_id_template=self.subject_name_id_template,
            user_name_template=self.user_name_template,
            user_name_template_push_status=self.user_name_template_push_status,
            user_name_template_suffix=self.user_name_template_suffix,
            user_name_template_type=self.user_name_template_type,
            users=self.users)


def get_saml(active_only: Optional[bool] = None,
             id: Optional[str] = None,
             label: Optional[str] = None,
             label_prefix: Optional[str] = None,
             request_compressed: Optional[bool] = None,
             skip_groups: Optional[bool] = None,
             skip_users: Optional[bool] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSamlResult:
    """
    Use this data source to retrieve an SAML application from Okta.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_okta as okta

    example = okta.app.get_saml(label="Example App")
    ```


    :param bool active_only: tells the provider to query for only `ACTIVE` applications.
    :param str id: `id` of application to retrieve, conflicts with `label` and `label_prefix`.
    :param str label: The label of the app to retrieve, conflicts with `label_prefix` and `id`. Label uses
           the `?q=<label>` query parameter exposed by Okta's API. It should be noted that at this time this searches both `name`
           and `label`. This is used to avoid paginating through all applications.
    :param str label_prefix: Label prefix of the app to retrieve, conflicts with `label` and `id`. This will tell the
           provider to do a `starts with` query as opposed to an `equals` query.
    :param bool request_compressed: Denotes whether the request is compressed or not.
    :param bool skip_groups: Indicator that allows the app to skip `groups` sync. Default is `false`.
    :param bool skip_users: Indicator that allows the app to skip `users` sync. Default is `false`.
    """
    __args__ = dict()
    __args__['activeOnly'] = active_only
    __args__['id'] = id
    __args__['label'] = label
    __args__['labelPrefix'] = label_prefix
    __args__['requestCompressed'] = request_compressed
    __args__['skipGroups'] = skip_groups
    __args__['skipUsers'] = skip_users
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('okta:app/getSaml:getSaml', __args__, opts=opts, typ=GetSamlResult).value

    return AwaitableGetSamlResult(
        accessibility_error_redirect_url=__ret__.accessibility_error_redirect_url,
        accessibility_login_redirect_url=__ret__.accessibility_login_redirect_url,
        accessibility_self_service=__ret__.accessibility_self_service,
        acs_endpoints=__ret__.acs_endpoints,
        active_only=__ret__.active_only,
        app_settings_json=__ret__.app_settings_json,
        assertion_signed=__ret__.assertion_signed,
        attribute_statements=__ret__.attribute_statements,
        audience=__ret__.audience,
        authn_context_class_ref=__ret__.authn_context_class_ref,
        auto_submit_toolbar=__ret__.auto_submit_toolbar,
        default_relay_state=__ret__.default_relay_state,
        destination=__ret__.destination,
        digest_algorithm=__ret__.digest_algorithm,
        features=__ret__.features,
        groups=__ret__.groups,
        hide_ios=__ret__.hide_ios,
        hide_web=__ret__.hide_web,
        honor_force_authn=__ret__.honor_force_authn,
        id=__ret__.id,
        idp_issuer=__ret__.idp_issuer,
        inline_hook_id=__ret__.inline_hook_id,
        key_id=__ret__.key_id,
        label=__ret__.label,
        label_prefix=__ret__.label_prefix,
        links=__ret__.links,
        name=__ret__.name,
        recipient=__ret__.recipient,
        request_compressed=__ret__.request_compressed,
        response_signed=__ret__.response_signed,
        saml_signed_request_enabled=__ret__.saml_signed_request_enabled,
        signature_algorithm=__ret__.signature_algorithm,
        single_logout_certificate=__ret__.single_logout_certificate,
        single_logout_issuer=__ret__.single_logout_issuer,
        single_logout_url=__ret__.single_logout_url,
        skip_groups=__ret__.skip_groups,
        skip_users=__ret__.skip_users,
        sp_issuer=__ret__.sp_issuer,
        sso_url=__ret__.sso_url,
        status=__ret__.status,
        subject_name_id_format=__ret__.subject_name_id_format,
        subject_name_id_template=__ret__.subject_name_id_template,
        user_name_template=__ret__.user_name_template,
        user_name_template_push_status=__ret__.user_name_template_push_status,
        user_name_template_suffix=__ret__.user_name_template_suffix,
        user_name_template_type=__ret__.user_name_template_type,
        users=__ret__.users)


@_utilities.lift_output_func(get_saml)
def get_saml_output(active_only: Optional[pulumi.Input[Optional[bool]]] = None,
                    id: Optional[pulumi.Input[Optional[str]]] = None,
                    label: Optional[pulumi.Input[Optional[str]]] = None,
                    label_prefix: Optional[pulumi.Input[Optional[str]]] = None,
                    request_compressed: Optional[pulumi.Input[Optional[bool]]] = None,
                    skip_groups: Optional[pulumi.Input[Optional[bool]]] = None,
                    skip_users: Optional[pulumi.Input[Optional[bool]]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSamlResult]:
    """
    Use this data source to retrieve an SAML application from Okta.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_okta as okta

    example = okta.app.get_saml(label="Example App")
    ```


    :param bool active_only: tells the provider to query for only `ACTIVE` applications.
    :param str id: `id` of application to retrieve, conflicts with `label` and `label_prefix`.
    :param str label: The label of the app to retrieve, conflicts with `label_prefix` and `id`. Label uses
           the `?q=<label>` query parameter exposed by Okta's API. It should be noted that at this time this searches both `name`
           and `label`. This is used to avoid paginating through all applications.
    :param str label_prefix: Label prefix of the app to retrieve, conflicts with `label` and `id`. This will tell the
           provider to do a `starts with` query as opposed to an `equals` query.
    :param bool request_compressed: Denotes whether the request is compressed or not.
    :param bool skip_groups: Indicator that allows the app to skip `groups` sync. Default is `false`.
    :param bool skip_users: Indicator that allows the app to skip `users` sync. Default is `false`.
    """
    ...
