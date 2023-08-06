'''
# `provider`

Refer to the Terraform Registory for docs: [`dns`](https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class DnsProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-dns.provider.DnsProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs dns}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
        update: typing.Optional[typing.Union["DnsProviderUpdate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs dns} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#alias DnsProvider#alias}
        :param update: update block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#update DnsProvider#update}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83bf38d9ae03bfa89c25f343b9ea5329f0d370be06091b19566d6b3f6633bd21)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DnsProviderConfig(alias=alias, update=update)

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional["DnsProviderUpdate"]:
        return typing.cast(typing.Optional["DnsProviderUpdate"], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da9e997daca8296d8b2e5f0ee3fa2d8644f51a678b4998934a3687ffb37f6084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> typing.Optional["DnsProviderUpdate"]:
        return typing.cast(typing.Optional["DnsProviderUpdate"], jsii.get(self, "update"))

    @update.setter
    def update(self, value: typing.Optional["DnsProviderUpdate"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfb3770f643917f6ff54865b8e6699e83d5b805f7be4dfca9457f94b1b303b0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-dns.provider.DnsProviderConfig",
    jsii_struct_bases=[],
    name_mapping={"alias": "alias", "update": "update"},
)
class DnsProviderConfig:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        update: typing.Optional[typing.Union["DnsProviderUpdate", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#alias DnsProvider#alias}
        :param update: update block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#update DnsProvider#update}
        '''
        if isinstance(update, dict):
            update = DnsProviderUpdate(**update)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff89cf22e9a26fed2a506744d38e6232134b31b6cade93c7995e77925523359f)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#alias DnsProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional["DnsProviderUpdate"]:
        '''update block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#update DnsProvider#update}
        '''
        result = self._values.get("update")
        return typing.cast(typing.Optional["DnsProviderUpdate"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-dns.provider.DnsProviderUpdate",
    jsii_struct_bases=[],
    name_mapping={
        "server": "server",
        "gssapi": "gssapi",
        "key_algorithm": "keyAlgorithm",
        "key_name": "keyName",
        "key_secret": "keySecret",
        "port": "port",
        "retries": "retries",
        "timeout": "timeout",
        "transport": "transport",
    },
)
class DnsProviderUpdate:
    def __init__(
        self,
        *,
        server: builtins.str,
        gssapi: typing.Optional[typing.Union["DnsProviderUpdateGssapi", typing.Dict[builtins.str, typing.Any]]] = None,
        key_algorithm: typing.Optional[builtins.str] = None,
        key_name: typing.Optional[builtins.str] = None,
        key_secret: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        retries: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[builtins.str] = None,
        transport: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param server: The hostname or IP address of the DNS server to send updates to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#server DnsProvider#server}
        :param gssapi: gssapi block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#gssapi DnsProvider#gssapi}
        :param key_algorithm: Required if ``key_name`` is set. When using TSIG authentication, the algorithm to use for HMAC. Valid values are ``hmac-md5``, ``hmac-sha1``, ``hmac-sha256`` or ``hmac-sha512``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#key_algorithm DnsProvider#key_algorithm}
        :param key_name: The name of the TSIG key used to sign the DNS update messages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#key_name DnsProvider#key_name}
        :param key_secret: Required if ``key_name`` is set A Base64-encoded string containing the shared secret to be used for TSIG. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#key_secret DnsProvider#key_secret}
        :param port: The target UDP port on the server where updates are sent to. Defaults to ``53``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#port DnsProvider#port}
        :param retries: How many times to retry on connection timeout. Defaults to ``3``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#retries DnsProvider#retries}
        :param timeout: Timeout for DNS queries. Valid values are durations expressed as ``500ms``, etc. or a plain number which is treated as whole seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#timeout DnsProvider#timeout}
        :param transport: Transport to use for DNS queries. Valid values are ``udp``, ``udp4``, ``udp6``, ``tcp``, ``tcp4``, or ``tcp6``. Any UDP transport will retry automatically with the equivalent TCP transport in the event of a truncated response. Defaults to ``udp``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#transport DnsProvider#transport}
        '''
        if isinstance(gssapi, dict):
            gssapi = DnsProviderUpdateGssapi(**gssapi)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d13f30fc44e99d87fcc72348a45e82b442b9705c51be72b7c208949a900678ea)
            check_type(argname="argument server", value=server, expected_type=type_hints["server"])
            check_type(argname="argument gssapi", value=gssapi, expected_type=type_hints["gssapi"])
            check_type(argname="argument key_algorithm", value=key_algorithm, expected_type=type_hints["key_algorithm"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument key_secret", value=key_secret, expected_type=type_hints["key_secret"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument retries", value=retries, expected_type=type_hints["retries"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument transport", value=transport, expected_type=type_hints["transport"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "server": server,
        }
        if gssapi is not None:
            self._values["gssapi"] = gssapi
        if key_algorithm is not None:
            self._values["key_algorithm"] = key_algorithm
        if key_name is not None:
            self._values["key_name"] = key_name
        if key_secret is not None:
            self._values["key_secret"] = key_secret
        if port is not None:
            self._values["port"] = port
        if retries is not None:
            self._values["retries"] = retries
        if timeout is not None:
            self._values["timeout"] = timeout
        if transport is not None:
            self._values["transport"] = transport

    @builtins.property
    def server(self) -> builtins.str:
        '''The hostname or IP address of the DNS server to send updates to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#server DnsProvider#server}
        '''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gssapi(self) -> typing.Optional["DnsProviderUpdateGssapi"]:
        '''gssapi block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#gssapi DnsProvider#gssapi}
        '''
        result = self._values.get("gssapi")
        return typing.cast(typing.Optional["DnsProviderUpdateGssapi"], result)

    @builtins.property
    def key_algorithm(self) -> typing.Optional[builtins.str]:
        '''Required if ``key_name`` is set.

        When using TSIG authentication, the algorithm to use for HMAC. Valid values are ``hmac-md5``, ``hmac-sha1``, ``hmac-sha256`` or ``hmac-sha512``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#key_algorithm DnsProvider#key_algorithm}
        '''
        result = self._values.get("key_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        '''The name of the TSIG key used to sign the DNS update messages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#key_name DnsProvider#key_name}
        '''
        result = self._values.get("key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_secret(self) -> typing.Optional[builtins.str]:
        '''Required if ``key_name`` is set A Base64-encoded string containing the shared secret to be used for TSIG.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#key_secret DnsProvider#key_secret}
        '''
        result = self._values.get("key_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The target UDP port on the server where updates are sent to. Defaults to ``53``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#port DnsProvider#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retries(self) -> typing.Optional[jsii.Number]:
        '''How many times to retry on connection timeout. Defaults to ``3``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#retries DnsProvider#retries}
        '''
        result = self._values.get("retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Timeout for DNS queries.

        Valid values are durations expressed as ``500ms``, etc. or a plain number which is treated as whole seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#timeout DnsProvider#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transport(self) -> typing.Optional[builtins.str]:
        '''Transport to use for DNS queries.

        Valid values are ``udp``, ``udp4``, ``udp6``, ``tcp``, ``tcp4``, or ``tcp6``. Any UDP transport will retry automatically with the equivalent TCP transport in the event of a truncated response. Defaults to ``udp``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#transport DnsProvider#transport}
        '''
        result = self._values.get("transport")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsProviderUpdate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-dns.provider.DnsProviderUpdateGssapi",
    jsii_struct_bases=[],
    name_mapping={
        "realm": "realm",
        "keytab": "keytab",
        "password": "password",
        "username": "username",
    },
)
class DnsProviderUpdateGssapi:
    def __init__(
        self,
        *,
        realm: builtins.str,
        keytab: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param realm: The Kerberos realm or Active Directory domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#realm DnsProvider#realm}
        :param keytab: This or ``password`` is required if ``username`` is set, not supported on Windows. The path to a keytab file containing a key for ``username``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#keytab DnsProvider#keytab}
        :param password: This or ``keytab`` is required if ``username`` is set. The matching password for ``username``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#password DnsProvider#password}
        :param username: The name of the user to authenticate as. If not set the current user session will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#username DnsProvider#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7014d1d1021660ba17144ae563b347a69e967d0adff111c7c0a48ab98549cef)
            check_type(argname="argument realm", value=realm, expected_type=type_hints["realm"])
            check_type(argname="argument keytab", value=keytab, expected_type=type_hints["keytab"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "realm": realm,
        }
        if keytab is not None:
            self._values["keytab"] = keytab
        if password is not None:
            self._values["password"] = password
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def realm(self) -> builtins.str:
        '''The Kerberos realm or Active Directory domain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#realm DnsProvider#realm}
        '''
        result = self._values.get("realm")
        assert result is not None, "Required property 'realm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def keytab(self) -> typing.Optional[builtins.str]:
        '''This or ``password`` is required if ``username`` is set, not supported on Windows.

        The path to a keytab file containing a key for ``username``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#keytab DnsProvider#keytab}
        '''
        result = self._values.get("keytab")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''This or ``keytab`` is required if ``username`` is set. The matching password for ``username``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#password DnsProvider#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The name of the user to authenticate as. If not set the current user session will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/dns/3.3.1/docs#username DnsProvider#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsProviderUpdateGssapi(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DnsProvider",
    "DnsProviderConfig",
    "DnsProviderUpdate",
    "DnsProviderUpdateGssapi",
]

publication.publish()

def _typecheckingstub__83bf38d9ae03bfa89c25f343b9ea5329f0d370be06091b19566d6b3f6633bd21(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias: typing.Optional[builtins.str] = None,
    update: typing.Optional[typing.Union[DnsProviderUpdate, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9e997daca8296d8b2e5f0ee3fa2d8644f51a678b4998934a3687ffb37f6084(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb3770f643917f6ff54865b8e6699e83d5b805f7be4dfca9457f94b1b303b0e(
    value: typing.Optional[DnsProviderUpdate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff89cf22e9a26fed2a506744d38e6232134b31b6cade93c7995e77925523359f(
    *,
    alias: typing.Optional[builtins.str] = None,
    update: typing.Optional[typing.Union[DnsProviderUpdate, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d13f30fc44e99d87fcc72348a45e82b442b9705c51be72b7c208949a900678ea(
    *,
    server: builtins.str,
    gssapi: typing.Optional[typing.Union[DnsProviderUpdateGssapi, typing.Dict[builtins.str, typing.Any]]] = None,
    key_algorithm: typing.Optional[builtins.str] = None,
    key_name: typing.Optional[builtins.str] = None,
    key_secret: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    retries: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[builtins.str] = None,
    transport: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7014d1d1021660ba17144ae563b347a69e967d0adff111c7c0a48ab98549cef(
    *,
    realm: builtins.str,
    keytab: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
