# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['MfaOktaArgs', 'MfaOkta']

@pulumi.input_type
class MfaOktaArgs:
    def __init__(__self__, *,
                 api_token: pulumi.Input[str],
                 org_name: pulumi.Input[str],
                 base_url: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 primary_email: Optional[pulumi.Input[bool]] = None,
                 username_format: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a MfaOkta resource.
        :param pulumi.Input[str] api_token: Okta API token.
        :param pulumi.Input[str] org_name: Name of the organization to be used in the Okta API.
        :param pulumi.Input[str] base_url: The base domain to use for API requests.
        :param pulumi.Input[str] namespace: Target namespace. (requires Enterprise)
        :param pulumi.Input[bool] primary_email: Only match the primary email for the account.
        :param pulumi.Input[str] username_format: A template string for mapping Identity names to MFA methods.
        """
        pulumi.set(__self__, "api_token", api_token)
        pulumi.set(__self__, "org_name", org_name)
        if base_url is not None:
            pulumi.set(__self__, "base_url", base_url)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if primary_email is not None:
            pulumi.set(__self__, "primary_email", primary_email)
        if username_format is not None:
            pulumi.set(__self__, "username_format", username_format)

    @property
    @pulumi.getter(name="apiToken")
    def api_token(self) -> pulumi.Input[str]:
        """
        Okta API token.
        """
        return pulumi.get(self, "api_token")

    @api_token.setter
    def api_token(self, value: pulumi.Input[str]):
        pulumi.set(self, "api_token", value)

    @property
    @pulumi.getter(name="orgName")
    def org_name(self) -> pulumi.Input[str]:
        """
        Name of the organization to be used in the Okta API.
        """
        return pulumi.get(self, "org_name")

    @org_name.setter
    def org_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "org_name", value)

    @property
    @pulumi.getter(name="baseUrl")
    def base_url(self) -> Optional[pulumi.Input[str]]:
        """
        The base domain to use for API requests.
        """
        return pulumi.get(self, "base_url")

    @base_url.setter
    def base_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "base_url", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        """
        Target namespace. (requires Enterprise)
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace", value)

    @property
    @pulumi.getter(name="primaryEmail")
    def primary_email(self) -> Optional[pulumi.Input[bool]]:
        """
        Only match the primary email for the account.
        """
        return pulumi.get(self, "primary_email")

    @primary_email.setter
    def primary_email(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "primary_email", value)

    @property
    @pulumi.getter(name="usernameFormat")
    def username_format(self) -> Optional[pulumi.Input[str]]:
        """
        A template string for mapping Identity names to MFA methods.
        """
        return pulumi.get(self, "username_format")

    @username_format.setter
    def username_format(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username_format", value)


@pulumi.input_type
class _MfaOktaState:
    def __init__(__self__, *,
                 api_token: Optional[pulumi.Input[str]] = None,
                 base_url: Optional[pulumi.Input[str]] = None,
                 method_id: Optional[pulumi.Input[str]] = None,
                 mount_accessor: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 namespace_id: Optional[pulumi.Input[str]] = None,
                 namespace_path: Optional[pulumi.Input[str]] = None,
                 org_name: Optional[pulumi.Input[str]] = None,
                 primary_email: Optional[pulumi.Input[bool]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 username_format: Optional[pulumi.Input[str]] = None,
                 uuid: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering MfaOkta resources.
        :param pulumi.Input[str] api_token: Okta API token.
        :param pulumi.Input[str] base_url: The base domain to use for API requests.
        :param pulumi.Input[str] method_id: Method ID.
        :param pulumi.Input[str] mount_accessor: Mount accessor.
        :param pulumi.Input[str] name: Method name.
        :param pulumi.Input[str] namespace: Target namespace. (requires Enterprise)
        :param pulumi.Input[str] namespace_id: Method's namespace ID.
        :param pulumi.Input[str] namespace_path: Method's namespace path.
        :param pulumi.Input[str] org_name: Name of the organization to be used in the Okta API.
        :param pulumi.Input[bool] primary_email: Only match the primary email for the account.
        :param pulumi.Input[str] type: MFA type.
        :param pulumi.Input[str] username_format: A template string for mapping Identity names to MFA methods.
        :param pulumi.Input[str] uuid: Resource UUID.
        """
        if api_token is not None:
            pulumi.set(__self__, "api_token", api_token)
        if base_url is not None:
            pulumi.set(__self__, "base_url", base_url)
        if method_id is not None:
            pulumi.set(__self__, "method_id", method_id)
        if mount_accessor is not None:
            pulumi.set(__self__, "mount_accessor", mount_accessor)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if namespace_id is not None:
            pulumi.set(__self__, "namespace_id", namespace_id)
        if namespace_path is not None:
            pulumi.set(__self__, "namespace_path", namespace_path)
        if org_name is not None:
            pulumi.set(__self__, "org_name", org_name)
        if primary_email is not None:
            pulumi.set(__self__, "primary_email", primary_email)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if username_format is not None:
            pulumi.set(__self__, "username_format", username_format)
        if uuid is not None:
            pulumi.set(__self__, "uuid", uuid)

    @property
    @pulumi.getter(name="apiToken")
    def api_token(self) -> Optional[pulumi.Input[str]]:
        """
        Okta API token.
        """
        return pulumi.get(self, "api_token")

    @api_token.setter
    def api_token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "api_token", value)

    @property
    @pulumi.getter(name="baseUrl")
    def base_url(self) -> Optional[pulumi.Input[str]]:
        """
        The base domain to use for API requests.
        """
        return pulumi.get(self, "base_url")

    @base_url.setter
    def base_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "base_url", value)

    @property
    @pulumi.getter(name="methodId")
    def method_id(self) -> Optional[pulumi.Input[str]]:
        """
        Method ID.
        """
        return pulumi.get(self, "method_id")

    @method_id.setter
    def method_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "method_id", value)

    @property
    @pulumi.getter(name="mountAccessor")
    def mount_accessor(self) -> Optional[pulumi.Input[str]]:
        """
        Mount accessor.
        """
        return pulumi.get(self, "mount_accessor")

    @mount_accessor.setter
    def mount_accessor(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mount_accessor", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Method name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        """
        Target namespace. (requires Enterprise)
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace", value)

    @property
    @pulumi.getter(name="namespaceId")
    def namespace_id(self) -> Optional[pulumi.Input[str]]:
        """
        Method's namespace ID.
        """
        return pulumi.get(self, "namespace_id")

    @namespace_id.setter
    def namespace_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace_id", value)

    @property
    @pulumi.getter(name="namespacePath")
    def namespace_path(self) -> Optional[pulumi.Input[str]]:
        """
        Method's namespace path.
        """
        return pulumi.get(self, "namespace_path")

    @namespace_path.setter
    def namespace_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace_path", value)

    @property
    @pulumi.getter(name="orgName")
    def org_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the organization to be used in the Okta API.
        """
        return pulumi.get(self, "org_name")

    @org_name.setter
    def org_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_name", value)

    @property
    @pulumi.getter(name="primaryEmail")
    def primary_email(self) -> Optional[pulumi.Input[bool]]:
        """
        Only match the primary email for the account.
        """
        return pulumi.get(self, "primary_email")

    @primary_email.setter
    def primary_email(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "primary_email", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        MFA type.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="usernameFormat")
    def username_format(self) -> Optional[pulumi.Input[str]]:
        """
        A template string for mapping Identity names to MFA methods.
        """
        return pulumi.get(self, "username_format")

    @username_format.setter
    def username_format(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username_format", value)

    @property
    @pulumi.getter
    def uuid(self) -> Optional[pulumi.Input[str]]:
        """
        Resource UUID.
        """
        return pulumi.get(self, "uuid")

    @uuid.setter
    def uuid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "uuid", value)


class MfaOkta(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_token: Optional[pulumi.Input[str]] = None,
                 base_url: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 org_name: Optional[pulumi.Input[str]] = None,
                 primary_email: Optional[pulumi.Input[bool]] = None,
                 username_format: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource for configuring the okta MFA method.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_vault as vault

        example = vault.identity.MfaOkta("example",
            api_token="token1",
            base_url="qux.baz.com",
            org_name="org1")
        ```

        ## Import

        Resource can be imported using its `uuid` field, e.g.

        ```sh
         $ pulumi import vault:identity/mfaOkta:MfaOkta example 0d89c36a-4ff5-4d70-8749-bb6a5598aeec
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_token: Okta API token.
        :param pulumi.Input[str] base_url: The base domain to use for API requests.
        :param pulumi.Input[str] namespace: Target namespace. (requires Enterprise)
        :param pulumi.Input[str] org_name: Name of the organization to be used in the Okta API.
        :param pulumi.Input[bool] primary_email: Only match the primary email for the account.
        :param pulumi.Input[str] username_format: A template string for mapping Identity names to MFA methods.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MfaOktaArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for configuring the okta MFA method.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_vault as vault

        example = vault.identity.MfaOkta("example",
            api_token="token1",
            base_url="qux.baz.com",
            org_name="org1")
        ```

        ## Import

        Resource can be imported using its `uuid` field, e.g.

        ```sh
         $ pulumi import vault:identity/mfaOkta:MfaOkta example 0d89c36a-4ff5-4d70-8749-bb6a5598aeec
        ```

        :param str resource_name: The name of the resource.
        :param MfaOktaArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MfaOktaArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_token: Optional[pulumi.Input[str]] = None,
                 base_url: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 org_name: Optional[pulumi.Input[str]] = None,
                 primary_email: Optional[pulumi.Input[bool]] = None,
                 username_format: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MfaOktaArgs.__new__(MfaOktaArgs)

            if api_token is None and not opts.urn:
                raise TypeError("Missing required property 'api_token'")
            __props__.__dict__["api_token"] = None if api_token is None else pulumi.Output.secret(api_token)
            __props__.__dict__["base_url"] = base_url
            __props__.__dict__["namespace"] = namespace
            if org_name is None and not opts.urn:
                raise TypeError("Missing required property 'org_name'")
            __props__.__dict__["org_name"] = org_name
            __props__.__dict__["primary_email"] = primary_email
            __props__.__dict__["username_format"] = username_format
            __props__.__dict__["method_id"] = None
            __props__.__dict__["mount_accessor"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["namespace_id"] = None
            __props__.__dict__["namespace_path"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["uuid"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["apiToken"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(MfaOkta, __self__).__init__(
            'vault:identity/mfaOkta:MfaOkta',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            api_token: Optional[pulumi.Input[str]] = None,
            base_url: Optional[pulumi.Input[str]] = None,
            method_id: Optional[pulumi.Input[str]] = None,
            mount_accessor: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            namespace: Optional[pulumi.Input[str]] = None,
            namespace_id: Optional[pulumi.Input[str]] = None,
            namespace_path: Optional[pulumi.Input[str]] = None,
            org_name: Optional[pulumi.Input[str]] = None,
            primary_email: Optional[pulumi.Input[bool]] = None,
            type: Optional[pulumi.Input[str]] = None,
            username_format: Optional[pulumi.Input[str]] = None,
            uuid: Optional[pulumi.Input[str]] = None) -> 'MfaOkta':
        """
        Get an existing MfaOkta resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_token: Okta API token.
        :param pulumi.Input[str] base_url: The base domain to use for API requests.
        :param pulumi.Input[str] method_id: Method ID.
        :param pulumi.Input[str] mount_accessor: Mount accessor.
        :param pulumi.Input[str] name: Method name.
        :param pulumi.Input[str] namespace: Target namespace. (requires Enterprise)
        :param pulumi.Input[str] namespace_id: Method's namespace ID.
        :param pulumi.Input[str] namespace_path: Method's namespace path.
        :param pulumi.Input[str] org_name: Name of the organization to be used in the Okta API.
        :param pulumi.Input[bool] primary_email: Only match the primary email for the account.
        :param pulumi.Input[str] type: MFA type.
        :param pulumi.Input[str] username_format: A template string for mapping Identity names to MFA methods.
        :param pulumi.Input[str] uuid: Resource UUID.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _MfaOktaState.__new__(_MfaOktaState)

        __props__.__dict__["api_token"] = api_token
        __props__.__dict__["base_url"] = base_url
        __props__.__dict__["method_id"] = method_id
        __props__.__dict__["mount_accessor"] = mount_accessor
        __props__.__dict__["name"] = name
        __props__.__dict__["namespace"] = namespace
        __props__.__dict__["namespace_id"] = namespace_id
        __props__.__dict__["namespace_path"] = namespace_path
        __props__.__dict__["org_name"] = org_name
        __props__.__dict__["primary_email"] = primary_email
        __props__.__dict__["type"] = type
        __props__.__dict__["username_format"] = username_format
        __props__.__dict__["uuid"] = uuid
        return MfaOkta(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiToken")
    def api_token(self) -> pulumi.Output[str]:
        """
        Okta API token.
        """
        return pulumi.get(self, "api_token")

    @property
    @pulumi.getter(name="baseUrl")
    def base_url(self) -> pulumi.Output[Optional[str]]:
        """
        The base domain to use for API requests.
        """
        return pulumi.get(self, "base_url")

    @property
    @pulumi.getter(name="methodId")
    def method_id(self) -> pulumi.Output[str]:
        """
        Method ID.
        """
        return pulumi.get(self, "method_id")

    @property
    @pulumi.getter(name="mountAccessor")
    def mount_accessor(self) -> pulumi.Output[str]:
        """
        Mount accessor.
        """
        return pulumi.get(self, "mount_accessor")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Method name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def namespace(self) -> pulumi.Output[Optional[str]]:
        """
        Target namespace. (requires Enterprise)
        """
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter(name="namespaceId")
    def namespace_id(self) -> pulumi.Output[str]:
        """
        Method's namespace ID.
        """
        return pulumi.get(self, "namespace_id")

    @property
    @pulumi.getter(name="namespacePath")
    def namespace_path(self) -> pulumi.Output[str]:
        """
        Method's namespace path.
        """
        return pulumi.get(self, "namespace_path")

    @property
    @pulumi.getter(name="orgName")
    def org_name(self) -> pulumi.Output[str]:
        """
        Name of the organization to be used in the Okta API.
        """
        return pulumi.get(self, "org_name")

    @property
    @pulumi.getter(name="primaryEmail")
    def primary_email(self) -> pulumi.Output[Optional[bool]]:
        """
        Only match the primary email for the account.
        """
        return pulumi.get(self, "primary_email")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        MFA type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="usernameFormat")
    def username_format(self) -> pulumi.Output[Optional[str]]:
        """
        A template string for mapping Identity names to MFA methods.
        """
        return pulumi.get(self, "username_format")

    @property
    @pulumi.getter
    def uuid(self) -> pulumi.Output[str]:
        """
        Resource UUID.
        """
        return pulumi.get(self, "uuid")

