# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SecretBackendIntermediateSetSignedArgs', 'SecretBackendIntermediateSetSigned']

@pulumi.input_type
class SecretBackendIntermediateSetSignedArgs:
    def __init__(__self__, *,
                 backend: pulumi.Input[str],
                 certificate: pulumi.Input[str],
                 namespace: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SecretBackendIntermediateSetSigned resource.
        :param pulumi.Input[str] backend: The PKI secret backend the resource belongs to.
        :param pulumi.Input[str] certificate: Specifies the PEM encoded certificate. May optionally append additional
               CA certificates to populate the whole chain, which will then enable returning the full chain from
               issue and sign operations.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault#namespace).
               *Available only for Vault Enterprise*.
        """
        pulumi.set(__self__, "backend", backend)
        pulumi.set(__self__, "certificate", certificate)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)

    @property
    @pulumi.getter
    def backend(self) -> pulumi.Input[str]:
        """
        The PKI secret backend the resource belongs to.
        """
        return pulumi.get(self, "backend")

    @backend.setter
    def backend(self, value: pulumi.Input[str]):
        pulumi.set(self, "backend", value)

    @property
    @pulumi.getter
    def certificate(self) -> pulumi.Input[str]:
        """
        Specifies the PEM encoded certificate. May optionally append additional
        CA certificates to populate the whole chain, which will then enable returning the full chain from
        issue and sign operations.
        """
        return pulumi.get(self, "certificate")

    @certificate.setter
    def certificate(self, value: pulumi.Input[str]):
        pulumi.set(self, "certificate", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace to provision the resource in.
        The value should not contain leading or trailing forward slashes.
        The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault#namespace).
        *Available only for Vault Enterprise*.
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace", value)


@pulumi.input_type
class _SecretBackendIntermediateSetSignedState:
    def __init__(__self__, *,
                 backend: Optional[pulumi.Input[str]] = None,
                 certificate: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering SecretBackendIntermediateSetSigned resources.
        :param pulumi.Input[str] backend: The PKI secret backend the resource belongs to.
        :param pulumi.Input[str] certificate: Specifies the PEM encoded certificate. May optionally append additional
               CA certificates to populate the whole chain, which will then enable returning the full chain from
               issue and sign operations.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault#namespace).
               *Available only for Vault Enterprise*.
        """
        if backend is not None:
            pulumi.set(__self__, "backend", backend)
        if certificate is not None:
            pulumi.set(__self__, "certificate", certificate)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)

    @property
    @pulumi.getter
    def backend(self) -> Optional[pulumi.Input[str]]:
        """
        The PKI secret backend the resource belongs to.
        """
        return pulumi.get(self, "backend")

    @backend.setter
    def backend(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "backend", value)

    @property
    @pulumi.getter
    def certificate(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the PEM encoded certificate. May optionally append additional
        CA certificates to populate the whole chain, which will then enable returning the full chain from
        issue and sign operations.
        """
        return pulumi.get(self, "certificate")

    @certificate.setter
    def certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace to provision the resource in.
        The value should not contain leading or trailing forward slashes.
        The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault#namespace).
        *Available only for Vault Enterprise*.
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace", value)


class SecretBackendIntermediateSetSigned(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backend: Optional[pulumi.Input[str]] = None,
                 certificate: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_vault as vault

        root = vault.Mount("root",
            path="pki-root",
            type="pki",
            description="root",
            default_lease_ttl_seconds=8640000,
            max_lease_ttl_seconds=8640000)
        intermediate = vault.Mount("intermediate",
            path="pki-int",
            type=root.type,
            description="intermediate",
            default_lease_ttl_seconds=86400,
            max_lease_ttl_seconds=86400)
        example_secret_backend_root_cert = vault.pki_secret.SecretBackendRootCert("exampleSecretBackendRootCert",
            backend=root.path,
            type="internal",
            common_name="RootOrg Root CA",
            ttl="86400",
            format="pem",
            private_key_format="der",
            key_type="rsa",
            key_bits=4096,
            exclude_cn_from_sans=True,
            ou="Organizational Unit",
            organization="RootOrg",
            country="US",
            locality="San Francisco",
            province="CA")
        example_secret_backend_intermediate_cert_request = vault.pki_secret.SecretBackendIntermediateCertRequest("exampleSecretBackendIntermediateCertRequest",
            backend=intermediate.path,
            type=example_secret_backend_root_cert.type,
            common_name="SubOrg Intermediate CA")
        example_secret_backend_root_sign_intermediate = vault.pki_secret.SecretBackendRootSignIntermediate("exampleSecretBackendRootSignIntermediate",
            backend=root.path,
            csr=example_secret_backend_intermediate_cert_request.csr,
            common_name="SubOrg Intermediate CA",
            exclude_cn_from_sans=True,
            ou="SubUnit",
            organization="SubOrg",
            country="US",
            locality="San Francisco",
            province="CA",
            revoke=True)
        example_secret_backend_intermediate_set_signed = vault.pki_secret.SecretBackendIntermediateSetSigned("exampleSecretBackendIntermediateSetSigned",
            backend=intermediate.path,
            certificate=example_secret_backend_root_sign_intermediate.certificate)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backend: The PKI secret backend the resource belongs to.
        :param pulumi.Input[str] certificate: Specifies the PEM encoded certificate. May optionally append additional
               CA certificates to populate the whole chain, which will then enable returning the full chain from
               issue and sign operations.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault#namespace).
               *Available only for Vault Enterprise*.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SecretBackendIntermediateSetSignedArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_vault as vault

        root = vault.Mount("root",
            path="pki-root",
            type="pki",
            description="root",
            default_lease_ttl_seconds=8640000,
            max_lease_ttl_seconds=8640000)
        intermediate = vault.Mount("intermediate",
            path="pki-int",
            type=root.type,
            description="intermediate",
            default_lease_ttl_seconds=86400,
            max_lease_ttl_seconds=86400)
        example_secret_backend_root_cert = vault.pki_secret.SecretBackendRootCert("exampleSecretBackendRootCert",
            backend=root.path,
            type="internal",
            common_name="RootOrg Root CA",
            ttl="86400",
            format="pem",
            private_key_format="der",
            key_type="rsa",
            key_bits=4096,
            exclude_cn_from_sans=True,
            ou="Organizational Unit",
            organization="RootOrg",
            country="US",
            locality="San Francisco",
            province="CA")
        example_secret_backend_intermediate_cert_request = vault.pki_secret.SecretBackendIntermediateCertRequest("exampleSecretBackendIntermediateCertRequest",
            backend=intermediate.path,
            type=example_secret_backend_root_cert.type,
            common_name="SubOrg Intermediate CA")
        example_secret_backend_root_sign_intermediate = vault.pki_secret.SecretBackendRootSignIntermediate("exampleSecretBackendRootSignIntermediate",
            backend=root.path,
            csr=example_secret_backend_intermediate_cert_request.csr,
            common_name="SubOrg Intermediate CA",
            exclude_cn_from_sans=True,
            ou="SubUnit",
            organization="SubOrg",
            country="US",
            locality="San Francisco",
            province="CA",
            revoke=True)
        example_secret_backend_intermediate_set_signed = vault.pki_secret.SecretBackendIntermediateSetSigned("exampleSecretBackendIntermediateSetSigned",
            backend=intermediate.path,
            certificate=example_secret_backend_root_sign_intermediate.certificate)
        ```

        :param str resource_name: The name of the resource.
        :param SecretBackendIntermediateSetSignedArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SecretBackendIntermediateSetSignedArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backend: Optional[pulumi.Input[str]] = None,
                 certificate: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SecretBackendIntermediateSetSignedArgs.__new__(SecretBackendIntermediateSetSignedArgs)

            if backend is None and not opts.urn:
                raise TypeError("Missing required property 'backend'")
            __props__.__dict__["backend"] = backend
            if certificate is None and not opts.urn:
                raise TypeError("Missing required property 'certificate'")
            __props__.__dict__["certificate"] = certificate
            __props__.__dict__["namespace"] = namespace
        super(SecretBackendIntermediateSetSigned, __self__).__init__(
            'vault:pkiSecret/secretBackendIntermediateSetSigned:SecretBackendIntermediateSetSigned',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            backend: Optional[pulumi.Input[str]] = None,
            certificate: Optional[pulumi.Input[str]] = None,
            namespace: Optional[pulumi.Input[str]] = None) -> 'SecretBackendIntermediateSetSigned':
        """
        Get an existing SecretBackendIntermediateSetSigned resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backend: The PKI secret backend the resource belongs to.
        :param pulumi.Input[str] certificate: Specifies the PEM encoded certificate. May optionally append additional
               CA certificates to populate the whole chain, which will then enable returning the full chain from
               issue and sign operations.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault#namespace).
               *Available only for Vault Enterprise*.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SecretBackendIntermediateSetSignedState.__new__(_SecretBackendIntermediateSetSignedState)

        __props__.__dict__["backend"] = backend
        __props__.__dict__["certificate"] = certificate
        __props__.__dict__["namespace"] = namespace
        return SecretBackendIntermediateSetSigned(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def backend(self) -> pulumi.Output[str]:
        """
        The PKI secret backend the resource belongs to.
        """
        return pulumi.get(self, "backend")

    @property
    @pulumi.getter
    def certificate(self) -> pulumi.Output[str]:
        """
        Specifies the PEM encoded certificate. May optionally append additional
        CA certificates to populate the whole chain, which will then enable returning the full chain from
        issue and sign operations.
        """
        return pulumi.get(self, "certificate")

    @property
    @pulumi.getter
    def namespace(self) -> pulumi.Output[Optional[str]]:
        """
        The namespace to provision the resource in.
        The value should not contain leading or trailing forward slashes.
        The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault#namespace).
        *Available only for Vault Enterprise*.
        """
        return pulumi.get(self, "namespace")

