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

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8
from ..ec2 import (
    FlowLogFormat as _FlowLogFormat_b7c2ba34,
    ICidrProvider as _ICidrProvider_28ddf5b0,
    IIpamPool as _IIpamPool_511f311d,
    ITransitGateway as _ITransitGateway_25936657,
    ITransitGatewayAttachment as _ITransitGatewayAttachment_64da8ffd,
    ITransitGatewayRouteTable as _ITransitGatewayRouteTable_56647ab2,
    Ipam as _Ipam_1ad3c981,
    TransitGatewayProps as _TransitGatewayProps_10a60d21,
)
from ..networkmanager import GlobalNetwork as _GlobalNetwork_79ec647c
from ..ram import (
    ISharedPrincipal as _ISharedPrincipal_9cde791b,
    ResourceShare as _ResourceShare_f0180713,
)


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.AddNetworkOptions",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zones": "availabilityZones",
        "max_azs": "maxAzs",
        "netmask": "netmask",
    },
)
class AddNetworkOptions:
    def __init__(
        self,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        netmask: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param availability_zones: 
        :param max_azs: 
        :param netmask: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d3c1346e4e259fee32303499f123223b892ff23852cdfdf5a57bf21cad7680)
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument max_azs", value=max_azs, expected_type=type_hints["max_azs"])
            check_type(argname="argument netmask", value=netmask, expected_type=type_hints["netmask"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if max_azs is not None:
            self._values["max_azs"] = max_azs
        if netmask is not None:
            self._values["netmask"] = netmask

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_azs(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_azs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def netmask(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("netmask")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddNetworkOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.AddPoolOptions",
    jsii_struct_bases=[],
    name_mapping={"cidrs": "cidrs", "default_netmask_length": "defaultNetmaskLength"},
)
class AddPoolOptions:
    def __init__(
        self,
        *,
        cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_netmask_length: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param cidrs: 
        :param default_netmask_length: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bafe93fe5666e81af7b6555c6e0b02d696c2267310d93ce406cc5b16333a1449)
            check_type(argname="argument cidrs", value=cidrs, expected_type=type_hints["cidrs"])
            check_type(argname="argument default_netmask_length", value=default_netmask_length, expected_type=type_hints["default_netmask_length"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cidrs is not None:
            self._values["cidrs"] = cidrs
        if default_netmask_length is not None:
            self._values["default_netmask_length"] = default_netmask_length

    @builtins.property
    def cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("cidrs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_netmask_length(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("default_netmask_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddPoolOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.AddSpokeNetworkProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zones": "availabilityZones",
        "cidr": "cidr",
        "default_instance_tenancy": "defaultInstanceTenancy",
        "enable_dns_hostnames": "enableDnsHostnames",
        "enable_dns_support": "enableDnsSupport",
        "flow_logs": "flowLogs",
        "gateway_endpoints": "gatewayEndpoints",
        "max_azs": "maxAzs",
        "vpc_name": "vpcName",
        "vpn_connections": "vpnConnections",
        "vpn_gateway": "vpnGateway",
        "vpn_gateway_asn": "vpnGatewayAsn",
        "vpn_route_propagation": "vpnRoutePropagation",
    },
)
class AddSpokeNetworkProps:
    def __init__(
        self,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[_ICidrProvider_28ddf5b0] = None,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union["FlowLogOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param availability_zones: 
        :param cidr: 
        :param default_instance_tenancy: 
        :param enable_dns_hostnames: 
        :param enable_dns_support: 
        :param flow_logs: 
        :param gateway_endpoints: 
        :param max_azs: 
        :param vpc_name: 
        :param vpn_connections: 
        :param vpn_gateway: 
        :param vpn_gateway_asn: 
        :param vpn_route_propagation: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__048409c4bedb08ed8edc9dda9cec65cb4087822a3dcae95d57c194d4e0613116)
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument default_instance_tenancy", value=default_instance_tenancy, expected_type=type_hints["default_instance_tenancy"])
            check_type(argname="argument enable_dns_hostnames", value=enable_dns_hostnames, expected_type=type_hints["enable_dns_hostnames"])
            check_type(argname="argument enable_dns_support", value=enable_dns_support, expected_type=type_hints["enable_dns_support"])
            check_type(argname="argument flow_logs", value=flow_logs, expected_type=type_hints["flow_logs"])
            check_type(argname="argument gateway_endpoints", value=gateway_endpoints, expected_type=type_hints["gateway_endpoints"])
            check_type(argname="argument max_azs", value=max_azs, expected_type=type_hints["max_azs"])
            check_type(argname="argument vpc_name", value=vpc_name, expected_type=type_hints["vpc_name"])
            check_type(argname="argument vpn_connections", value=vpn_connections, expected_type=type_hints["vpn_connections"])
            check_type(argname="argument vpn_gateway", value=vpn_gateway, expected_type=type_hints["vpn_gateway"])
            check_type(argname="argument vpn_gateway_asn", value=vpn_gateway_asn, expected_type=type_hints["vpn_gateway_asn"])
            check_type(argname="argument vpn_route_propagation", value=vpn_route_propagation, expected_type=type_hints["vpn_route_propagation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if cidr is not None:
            self._values["cidr"] = cidr
        if default_instance_tenancy is not None:
            self._values["default_instance_tenancy"] = default_instance_tenancy
        if enable_dns_hostnames is not None:
            self._values["enable_dns_hostnames"] = enable_dns_hostnames
        if enable_dns_support is not None:
            self._values["enable_dns_support"] = enable_dns_support
        if flow_logs is not None:
            self._values["flow_logs"] = flow_logs
        if gateway_endpoints is not None:
            self._values["gateway_endpoints"] = gateway_endpoints
        if max_azs is not None:
            self._values["max_azs"] = max_azs
        if vpc_name is not None:
            self._values["vpc_name"] = vpc_name
        if vpn_connections is not None:
            self._values["vpn_connections"] = vpn_connections
        if vpn_gateway is not None:
            self._values["vpn_gateway"] = vpn_gateway
        if vpn_gateway_asn is not None:
            self._values["vpn_gateway_asn"] = vpn_gateway_asn
        if vpn_route_propagation is not None:
            self._values["vpn_route_propagation"] = vpn_route_propagation

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cidr(self) -> typing.Optional[_ICidrProvider_28ddf5b0]:
        result = self._values.get("cidr")
        return typing.cast(typing.Optional[_ICidrProvider_28ddf5b0], result)

    @builtins.property
    def default_instance_tenancy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy]:
        result = self._values.get("default_instance_tenancy")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy], result)

    @builtins.property
    def enable_dns_hostnames(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_dns_hostnames")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_dns_support(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_dns_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def flow_logs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "FlowLogOptions"]]:
        result = self._values.get("flow_logs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "FlowLogOptions"]], result)

    @builtins.property
    def gateway_endpoints(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]]:
        result = self._values.get("gateway_endpoints")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]], result)

    @builtins.property
    def max_azs(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_azs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("vpc_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_connections(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]]:
        result = self._values.get("vpn_connections")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]], result)

    @builtins.property
    def vpn_gateway(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("vpn_gateway")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpn_gateway_asn(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("vpn_gateway_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpn_route_propagation(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]]:
        result = self._values.get("vpn_route_propagation")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddSpokeNetworkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.AllocatePrivateNetworkOptions",
    jsii_struct_bases=[],
    name_mapping={"netmask": "netmask", "pool": "pool"},
)
class AllocatePrivateNetworkOptions:
    def __init__(
        self,
        *,
        netmask: typing.Optional[jsii.Number] = None,
        pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param netmask: 
        :param pool: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1edcf1c081b844711051faa1818771b547c90031be28d3b0f04a24516485f5eb)
            check_type(argname="argument netmask", value=netmask, expected_type=type_hints["netmask"])
            check_type(argname="argument pool", value=pool, expected_type=type_hints["pool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if netmask is not None:
            self._values["netmask"] = netmask
        if pool is not None:
            self._values["pool"] = pool

    @builtins.property
    def netmask(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("netmask")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pool(self) -> typing.Optional[builtins.str]:
        result = self._values.get("pool")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AllocatePrivateNetworkOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.FlowLogOptions",
    jsii_struct_bases=[_aws_cdk_aws_ec2_ceddda9d.FlowLogOptions],
    name_mapping={
        "destination": "destination",
        "log_format": "logFormat",
        "max_aggregation_interval": "maxAggregationInterval",
        "traffic_type": "trafficType",
        "log_format_definition": "logFormatDefinition",
    },
)
class FlowLogOptions(_aws_cdk_aws_ec2_ceddda9d.FlowLogOptions):
    def __init__(
        self,
        *,
        destination: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination] = None,
        log_format: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.LogFormat]] = None,
        max_aggregation_interval: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval] = None,
        traffic_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType] = None,
        log_format_definition: typing.Optional[_FlowLogFormat_b7c2ba34] = None,
    ) -> None:
        '''
        :param destination: Specifies the type of destination to which the flow log data is to be published. Flow log data can be published to CloudWatch Logs or Amazon S3 Default: FlowLogDestinationType.toCloudWatchLogs()
        :param log_format: The fields to include in the flow log record, in the order in which they should appear. If multiple fields are specified, they will be separated by spaces. For full control over the literal log format string, pass a single field constructed with ``LogFormat.custom()``. See https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html#flow-log-records Default: - default log format is used.
        :param max_aggregation_interval: The maximum interval of time during which a flow of packets is captured and aggregated into a flow log record. Default: FlowLogMaxAggregationInterval.TEN_MINUTES
        :param traffic_type: The type of traffic to log. You can log traffic that the resource accepts or rejects, or all traffic. Default: ALL
        :param log_format_definition: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61356c6c988a747170b0fff518aeff55bb37140b2f2bb3a8395a7676df11d939)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument log_format", value=log_format, expected_type=type_hints["log_format"])
            check_type(argname="argument max_aggregation_interval", value=max_aggregation_interval, expected_type=type_hints["max_aggregation_interval"])
            check_type(argname="argument traffic_type", value=traffic_type, expected_type=type_hints["traffic_type"])
            check_type(argname="argument log_format_definition", value=log_format_definition, expected_type=type_hints["log_format_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination is not None:
            self._values["destination"] = destination
        if log_format is not None:
            self._values["log_format"] = log_format
        if max_aggregation_interval is not None:
            self._values["max_aggregation_interval"] = max_aggregation_interval
        if traffic_type is not None:
            self._values["traffic_type"] = traffic_type
        if log_format_definition is not None:
            self._values["log_format_definition"] = log_format_definition

    @builtins.property
    def destination(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination]:
        '''Specifies the type of destination to which the flow log data is to be published.

        Flow log data can be published to CloudWatch Logs or Amazon S3

        :default: FlowLogDestinationType.toCloudWatchLogs()
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination], result)

    @builtins.property
    def log_format(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.LogFormat]]:
        '''The fields to include in the flow log record, in the order in which they should appear.

        If multiple fields are specified, they will be separated by spaces. For full control over the literal log format
        string, pass a single field constructed with ``LogFormat.custom()``.

        See https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html#flow-log-records

        :default: - default log format is used.
        '''
        result = self._values.get("log_format")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.LogFormat]], result)

    @builtins.property
    def max_aggregation_interval(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval]:
        '''The maximum interval of time during which a flow of packets is captured and aggregated into a flow log record.

        :default: FlowLogMaxAggregationInterval.TEN_MINUTES
        '''
        result = self._values.get("max_aggregation_interval")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval], result)

    @builtins.property
    def traffic_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType]:
        '''The type of traffic to log.

        You can log traffic that the resource accepts or rejects, or all traffic.

        :default: ALL
        '''
        result = self._values.get("traffic_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType], result)

    @builtins.property
    def log_format_definition(self) -> typing.Optional[_FlowLogFormat_b7c2ba34]:
        result = self._values.get("log_format_definition")
        return typing.cast(typing.Optional[_FlowLogFormat_b7c2ba34], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FlowLogOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FourTierNetwork(
    _aws_cdk_aws_ec2_ceddda9d.Vpc,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2_patterns.FourTierNetwork",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[_ICidrProvider_28ddf5b0] = None,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        nat_gateway_provider: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider] = None,
        nat_gateways: typing.Optional[jsii.Number] = None,
        nat_gateway_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param availability_zones: 
        :param cidr: 
        :param default_instance_tenancy: 
        :param enable_dns_hostnames: 
        :param enable_dns_support: 
        :param flow_logs: 
        :param gateway_endpoints: 
        :param max_azs: 
        :param nat_gateway_provider: 
        :param nat_gateways: 
        :param nat_gateway_subnets: 
        :param vpc_name: 
        :param vpn_connections: 
        :param vpn_gateway: 
        :param vpn_gateway_asn: 
        :param vpn_route_propagation: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01b54dda1f6044b8b90a294f4af2c53fd512620a5e619adafd6d687a35f35dc3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FourTierNetworkProps(
            availability_zones=availability_zones,
            cidr=cidr,
            default_instance_tenancy=default_instance_tenancy,
            enable_dns_hostnames=enable_dns_hostnames,
            enable_dns_support=enable_dns_support,
            flow_logs=flow_logs,
            gateway_endpoints=gateway_endpoints,
            max_azs=max_azs,
            nat_gateway_provider=nat_gateway_provider,
            nat_gateways=nat_gateways,
            nat_gateway_subnets=nat_gateway_subnets,
            vpc_name=vpc_name,
            vpn_connections=vpn_connections,
            vpn_gateway=vpn_gateway,
            vpn_gateway_asn=vpn_gateway_asn,
            vpn_route_propagation=vpn_route_propagation,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addVpcFlowLog")
    def add_vpc_flow_log(
        self,
        id: builtins.str,
        *,
        log_format_definition: typing.Optional[_FlowLogFormat_b7c2ba34] = None,
        destination: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination] = None,
        log_format: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.LogFormat]] = None,
        max_aggregation_interval: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval] = None,
        traffic_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType] = None,
    ) -> _aws_cdk_aws_ec2_ceddda9d.FlowLog:
        '''
        :param id: -
        :param log_format_definition: 
        :param destination: Specifies the type of destination to which the flow log data is to be published. Flow log data can be published to CloudWatch Logs or Amazon S3 Default: FlowLogDestinationType.toCloudWatchLogs()
        :param log_format: The fields to include in the flow log record, in the order in which they should appear. If multiple fields are specified, they will be separated by spaces. For full control over the literal log format string, pass a single field constructed with ``LogFormat.custom()``. See https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html#flow-log-records Default: - default log format is used.
        :param max_aggregation_interval: The maximum interval of time during which a flow of packets is captured and aggregated into a flow log record. Default: FlowLogMaxAggregationInterval.TEN_MINUTES
        :param traffic_type: The type of traffic to log. You can log traffic that the resource accepts or rejects, or all traffic. Default: ALL
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb697f4884edaa9946bcf623d36e26bbc15cba6a321ac50f29f26b8fdef42b2a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = FlowLogOptions(
            log_format_definition=log_format_definition,
            destination=destination,
            log_format=log_format,
            max_aggregation_interval=max_aggregation_interval,
            traffic_type=traffic_type,
        )

        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.FlowLog, jsii.invoke(self, "addVpcFlowLog", [id, options]))

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "netmask"))

    @builtins.property
    @jsii.member(jsii_name="defaultInstanceTenancy")
    def default_instance_tenancy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy]:
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy], jsii.get(self, "defaultInstanceTenancy"))

    @builtins.property
    @jsii.member(jsii_name="enableDnsHostnames")
    def enable_dns_hostnames(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableDnsHostnames"))

    @builtins.property
    @jsii.member(jsii_name="enableDnsSupport")
    def enable_dns_support(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableDnsSupport"))

    @builtins.property
    @jsii.member(jsii_name="ipamPool")
    def ipam_pool(self) -> typing.Optional[_IIpamPool_511f311d]:
        return typing.cast(typing.Optional[_IIpamPool_511f311d], jsii.get(self, "ipamPool"))

    @builtins.property
    @jsii.member(jsii_name="maxAzs")
    def max_azs(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAzs"))

    @builtins.property
    @jsii.member(jsii_name="vpcName")
    def vpc_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcName"))


class FourTierNetworkHub(
    FourTierNetwork,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2_patterns.FourTierNetworkHub",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[_ICidrProvider_28ddf5b0] = None,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        default_transit_gateway_route_table: typing.Optional[_ITransitGatewayRouteTable_56647ab2] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        global_network: typing.Optional[_GlobalNetwork_79ec647c] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        sharing: typing.Optional[typing.Union["FourTierNetworkShareProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param availability_zones: 
        :param cidr: 
        :param default_instance_tenancy: 
        :param default_transit_gateway_route_table: 
        :param enable_dns_hostnames: 
        :param enable_dns_support: 
        :param flow_logs: 
        :param gateway_endpoints: 
        :param global_network: 
        :param max_azs: 
        :param sharing: 
        :param vpc_name: 
        :param vpn_connections: 
        :param vpn_gateway: 
        :param vpn_gateway_asn: 
        :param vpn_route_propagation: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32ace25eaf0b1bdeb7c9833547b92ca28254092d01db9ebc9696fce2260b43d9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FourTierNetworkHubProps(
            availability_zones=availability_zones,
            cidr=cidr,
            default_instance_tenancy=default_instance_tenancy,
            default_transit_gateway_route_table=default_transit_gateway_route_table,
            enable_dns_hostnames=enable_dns_hostnames,
            enable_dns_support=enable_dns_support,
            flow_logs=flow_logs,
            gateway_endpoints=gateway_endpoints,
            global_network=global_network,
            max_azs=max_azs,
            sharing=sharing,
            vpc_name=vpc_name,
            vpn_connections=vpn_connections,
            vpn_gateway=vpn_gateway,
            vpn_gateway_asn=vpn_gateway_asn,
            vpn_route_propagation=vpn_route_propagation,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addSpoke")
    def add_spoke(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[_ICidrProvider_28ddf5b0] = None,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> "FourTierNetworkSpoke":
        '''
        :param scope: -
        :param id: -
        :param availability_zones: 
        :param cidr: 
        :param default_instance_tenancy: 
        :param enable_dns_hostnames: 
        :param enable_dns_support: 
        :param flow_logs: 
        :param gateway_endpoints: 
        :param max_azs: 
        :param vpc_name: 
        :param vpn_connections: 
        :param vpn_gateway: 
        :param vpn_gateway_asn: 
        :param vpn_route_propagation: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b427eb756711b9be0d1724b92283f7b8b658149d02d0860ddfaae4ca009451a6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AddSpokeNetworkProps(
            availability_zones=availability_zones,
            cidr=cidr,
            default_instance_tenancy=default_instance_tenancy,
            enable_dns_hostnames=enable_dns_hostnames,
            enable_dns_support=enable_dns_support,
            flow_logs=flow_logs,
            gateway_endpoints=gateway_endpoints,
            max_azs=max_azs,
            vpc_name=vpc_name,
            vpn_connections=vpn_connections,
            vpn_gateway=vpn_gateway,
            vpn_gateway_asn=vpn_gateway_asn,
            vpn_route_propagation=vpn_route_propagation,
        )

        return typing.cast("FourTierNetworkSpoke", jsii.invoke(self, "addSpoke", [scope, id, props]))

    @jsii.member(jsii_name="enableTransitGateway")
    def enable_transit_gateway(
        self,
        *,
        amazon_side_asn: typing.Optional[jsii.Number] = None,
        auto_accept_shared_attachments: typing.Optional[builtins.bool] = None,
        cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_route_table_association: typing.Optional[builtins.bool] = None,
        default_route_table_id: typing.Optional[builtins.str] = None,
        default_route_table_propagation: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        dns_support: typing.Optional[builtins.bool] = None,
        multicast_support: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        vpn_ecmp_support: typing.Optional[builtins.bool] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> _ITransitGateway_25936657:
        '''
        :param amazon_side_asn: 
        :param auto_accept_shared_attachments: 
        :param cidr_blocks: 
        :param default_route_table_association: 
        :param default_route_table_id: 
        :param default_route_table_propagation: 
        :param description: 
        :param dns_support: 
        :param multicast_support: 
        :param name: 
        :param vpn_ecmp_support: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        props = _TransitGatewayProps_10a60d21(
            amazon_side_asn=amazon_side_asn,
            auto_accept_shared_attachments=auto_accept_shared_attachments,
            cidr_blocks=cidr_blocks,
            default_route_table_association=default_route_table_association,
            default_route_table_id=default_route_table_id,
            default_route_table_propagation=default_route_table_propagation,
            description=description,
            dns_support=dns_support,
            multicast_support=multicast_support,
            name=name,
            vpn_ecmp_support=vpn_ecmp_support,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        return typing.cast(_ITransitGateway_25936657, jsii.invoke(self, "enableTransitGateway", [props]))

    @builtins.property
    @jsii.member(jsii_name="sharing")
    def sharing(self) -> "FourTierNetworkShareProperties":
        return typing.cast("FourTierNetworkShareProperties", jsii.get(self, "sharing"))

    @builtins.property
    @jsii.member(jsii_name="defaultTransitGatewayRouteTable")
    def default_transit_gateway_route_table(
        self,
    ) -> typing.Optional[_ITransitGatewayRouteTable_56647ab2]:
        return typing.cast(typing.Optional[_ITransitGatewayRouteTable_56647ab2], jsii.get(self, "defaultTransitGatewayRouteTable"))

    @builtins.property
    @jsii.member(jsii_name="globalNetwork")
    def global_network(self) -> typing.Optional[_GlobalNetwork_79ec647c]:
        return typing.cast(typing.Optional[_GlobalNetwork_79ec647c], jsii.get(self, "globalNetwork"))

    @builtins.property
    @jsii.member(jsii_name="transitGateway")
    def transit_gateway(self) -> typing.Optional[_ITransitGateway_25936657]:
        return typing.cast(typing.Optional[_ITransitGateway_25936657], jsii.get(self, "transitGateway"))


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.FourTierNetworkHubProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "availability_zones": "availabilityZones",
        "cidr": "cidr",
        "default_instance_tenancy": "defaultInstanceTenancy",
        "default_transit_gateway_route_table": "defaultTransitGatewayRouteTable",
        "enable_dns_hostnames": "enableDnsHostnames",
        "enable_dns_support": "enableDnsSupport",
        "flow_logs": "flowLogs",
        "gateway_endpoints": "gatewayEndpoints",
        "global_network": "globalNetwork",
        "max_azs": "maxAzs",
        "sharing": "sharing",
        "vpc_name": "vpcName",
        "vpn_connections": "vpnConnections",
        "vpn_gateway": "vpnGateway",
        "vpn_gateway_asn": "vpnGatewayAsn",
        "vpn_route_propagation": "vpnRoutePropagation",
    },
)
class FourTierNetworkHubProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[_ICidrProvider_28ddf5b0] = None,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        default_transit_gateway_route_table: typing.Optional[_ITransitGatewayRouteTable_56647ab2] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        global_network: typing.Optional[_GlobalNetwork_79ec647c] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        sharing: typing.Optional[typing.Union["FourTierNetworkShareProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param availability_zones: 
        :param cidr: 
        :param default_instance_tenancy: 
        :param default_transit_gateway_route_table: 
        :param enable_dns_hostnames: 
        :param enable_dns_support: 
        :param flow_logs: 
        :param gateway_endpoints: 
        :param global_network: 
        :param max_azs: 
        :param sharing: 
        :param vpc_name: 
        :param vpn_connections: 
        :param vpn_gateway: 
        :param vpn_gateway_asn: 
        :param vpn_route_propagation: 
        '''
        if isinstance(sharing, dict):
            sharing = FourTierNetworkShareProperties(**sharing)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e120a9a594264d414d234533b6a6694a2e18b423a355c83676f0931ec9be90)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument default_instance_tenancy", value=default_instance_tenancy, expected_type=type_hints["default_instance_tenancy"])
            check_type(argname="argument default_transit_gateway_route_table", value=default_transit_gateway_route_table, expected_type=type_hints["default_transit_gateway_route_table"])
            check_type(argname="argument enable_dns_hostnames", value=enable_dns_hostnames, expected_type=type_hints["enable_dns_hostnames"])
            check_type(argname="argument enable_dns_support", value=enable_dns_support, expected_type=type_hints["enable_dns_support"])
            check_type(argname="argument flow_logs", value=flow_logs, expected_type=type_hints["flow_logs"])
            check_type(argname="argument gateway_endpoints", value=gateway_endpoints, expected_type=type_hints["gateway_endpoints"])
            check_type(argname="argument global_network", value=global_network, expected_type=type_hints["global_network"])
            check_type(argname="argument max_azs", value=max_azs, expected_type=type_hints["max_azs"])
            check_type(argname="argument sharing", value=sharing, expected_type=type_hints["sharing"])
            check_type(argname="argument vpc_name", value=vpc_name, expected_type=type_hints["vpc_name"])
            check_type(argname="argument vpn_connections", value=vpn_connections, expected_type=type_hints["vpn_connections"])
            check_type(argname="argument vpn_gateway", value=vpn_gateway, expected_type=type_hints["vpn_gateway"])
            check_type(argname="argument vpn_gateway_asn", value=vpn_gateway_asn, expected_type=type_hints["vpn_gateway_asn"])
            check_type(argname="argument vpn_route_propagation", value=vpn_route_propagation, expected_type=type_hints["vpn_route_propagation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if cidr is not None:
            self._values["cidr"] = cidr
        if default_instance_tenancy is not None:
            self._values["default_instance_tenancy"] = default_instance_tenancy
        if default_transit_gateway_route_table is not None:
            self._values["default_transit_gateway_route_table"] = default_transit_gateway_route_table
        if enable_dns_hostnames is not None:
            self._values["enable_dns_hostnames"] = enable_dns_hostnames
        if enable_dns_support is not None:
            self._values["enable_dns_support"] = enable_dns_support
        if flow_logs is not None:
            self._values["flow_logs"] = flow_logs
        if gateway_endpoints is not None:
            self._values["gateway_endpoints"] = gateway_endpoints
        if global_network is not None:
            self._values["global_network"] = global_network
        if max_azs is not None:
            self._values["max_azs"] = max_azs
        if sharing is not None:
            self._values["sharing"] = sharing
        if vpc_name is not None:
            self._values["vpc_name"] = vpc_name
        if vpn_connections is not None:
            self._values["vpn_connections"] = vpn_connections
        if vpn_gateway is not None:
            self._values["vpn_gateway"] = vpn_gateway
        if vpn_gateway_asn is not None:
            self._values["vpn_gateway_asn"] = vpn_gateway_asn
        if vpn_route_propagation is not None:
            self._values["vpn_route_propagation"] = vpn_route_propagation

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cidr(self) -> typing.Optional[_ICidrProvider_28ddf5b0]:
        result = self._values.get("cidr")
        return typing.cast(typing.Optional[_ICidrProvider_28ddf5b0], result)

    @builtins.property
    def default_instance_tenancy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy]:
        result = self._values.get("default_instance_tenancy")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy], result)

    @builtins.property
    def default_transit_gateway_route_table(
        self,
    ) -> typing.Optional[_ITransitGatewayRouteTable_56647ab2]:
        result = self._values.get("default_transit_gateway_route_table")
        return typing.cast(typing.Optional[_ITransitGatewayRouteTable_56647ab2], result)

    @builtins.property
    def enable_dns_hostnames(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_dns_hostnames")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_dns_support(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_dns_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def flow_logs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, FlowLogOptions]]:
        result = self._values.get("flow_logs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, FlowLogOptions]], result)

    @builtins.property
    def gateway_endpoints(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]]:
        result = self._values.get("gateway_endpoints")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]], result)

    @builtins.property
    def global_network(self) -> typing.Optional[_GlobalNetwork_79ec647c]:
        result = self._values.get("global_network")
        return typing.cast(typing.Optional[_GlobalNetwork_79ec647c], result)

    @builtins.property
    def max_azs(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_azs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sharing(self) -> typing.Optional["FourTierNetworkShareProperties"]:
        result = self._values.get("sharing")
        return typing.cast(typing.Optional["FourTierNetworkShareProperties"], result)

    @builtins.property
    def vpc_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("vpc_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_connections(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]]:
        result = self._values.get("vpn_connections")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]], result)

    @builtins.property
    def vpn_gateway(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("vpn_gateway")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpn_gateway_asn(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("vpn_gateway_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpn_route_propagation(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]]:
        result = self._values.get("vpn_route_propagation")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FourTierNetworkHubProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.FourTierNetworkProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zones": "availabilityZones",
        "cidr": "cidr",
        "default_instance_tenancy": "defaultInstanceTenancy",
        "enable_dns_hostnames": "enableDnsHostnames",
        "enable_dns_support": "enableDnsSupport",
        "flow_logs": "flowLogs",
        "gateway_endpoints": "gatewayEndpoints",
        "max_azs": "maxAzs",
        "nat_gateway_provider": "natGatewayProvider",
        "nat_gateways": "natGateways",
        "nat_gateway_subnets": "natGatewaySubnets",
        "vpc_name": "vpcName",
        "vpn_connections": "vpnConnections",
        "vpn_gateway": "vpnGateway",
        "vpn_gateway_asn": "vpnGatewayAsn",
        "vpn_route_propagation": "vpnRoutePropagation",
    },
)
class FourTierNetworkProps:
    def __init__(
        self,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[_ICidrProvider_28ddf5b0] = None,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        nat_gateway_provider: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider] = None,
        nat_gateways: typing.Optional[jsii.Number] = None,
        nat_gateway_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param availability_zones: 
        :param cidr: 
        :param default_instance_tenancy: 
        :param enable_dns_hostnames: 
        :param enable_dns_support: 
        :param flow_logs: 
        :param gateway_endpoints: 
        :param max_azs: 
        :param nat_gateway_provider: 
        :param nat_gateways: 
        :param nat_gateway_subnets: 
        :param vpc_name: 
        :param vpn_connections: 
        :param vpn_gateway: 
        :param vpn_gateway_asn: 
        :param vpn_route_propagation: 
        '''
        if isinstance(nat_gateway_subnets, dict):
            nat_gateway_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**nat_gateway_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce9f1c80c97704155becd995a7614b98797ff3dcfedcb6c14a3c861d8ffa5d99)
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument default_instance_tenancy", value=default_instance_tenancy, expected_type=type_hints["default_instance_tenancy"])
            check_type(argname="argument enable_dns_hostnames", value=enable_dns_hostnames, expected_type=type_hints["enable_dns_hostnames"])
            check_type(argname="argument enable_dns_support", value=enable_dns_support, expected_type=type_hints["enable_dns_support"])
            check_type(argname="argument flow_logs", value=flow_logs, expected_type=type_hints["flow_logs"])
            check_type(argname="argument gateway_endpoints", value=gateway_endpoints, expected_type=type_hints["gateway_endpoints"])
            check_type(argname="argument max_azs", value=max_azs, expected_type=type_hints["max_azs"])
            check_type(argname="argument nat_gateway_provider", value=nat_gateway_provider, expected_type=type_hints["nat_gateway_provider"])
            check_type(argname="argument nat_gateways", value=nat_gateways, expected_type=type_hints["nat_gateways"])
            check_type(argname="argument nat_gateway_subnets", value=nat_gateway_subnets, expected_type=type_hints["nat_gateway_subnets"])
            check_type(argname="argument vpc_name", value=vpc_name, expected_type=type_hints["vpc_name"])
            check_type(argname="argument vpn_connections", value=vpn_connections, expected_type=type_hints["vpn_connections"])
            check_type(argname="argument vpn_gateway", value=vpn_gateway, expected_type=type_hints["vpn_gateway"])
            check_type(argname="argument vpn_gateway_asn", value=vpn_gateway_asn, expected_type=type_hints["vpn_gateway_asn"])
            check_type(argname="argument vpn_route_propagation", value=vpn_route_propagation, expected_type=type_hints["vpn_route_propagation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if cidr is not None:
            self._values["cidr"] = cidr
        if default_instance_tenancy is not None:
            self._values["default_instance_tenancy"] = default_instance_tenancy
        if enable_dns_hostnames is not None:
            self._values["enable_dns_hostnames"] = enable_dns_hostnames
        if enable_dns_support is not None:
            self._values["enable_dns_support"] = enable_dns_support
        if flow_logs is not None:
            self._values["flow_logs"] = flow_logs
        if gateway_endpoints is not None:
            self._values["gateway_endpoints"] = gateway_endpoints
        if max_azs is not None:
            self._values["max_azs"] = max_azs
        if nat_gateway_provider is not None:
            self._values["nat_gateway_provider"] = nat_gateway_provider
        if nat_gateways is not None:
            self._values["nat_gateways"] = nat_gateways
        if nat_gateway_subnets is not None:
            self._values["nat_gateway_subnets"] = nat_gateway_subnets
        if vpc_name is not None:
            self._values["vpc_name"] = vpc_name
        if vpn_connections is not None:
            self._values["vpn_connections"] = vpn_connections
        if vpn_gateway is not None:
            self._values["vpn_gateway"] = vpn_gateway
        if vpn_gateway_asn is not None:
            self._values["vpn_gateway_asn"] = vpn_gateway_asn
        if vpn_route_propagation is not None:
            self._values["vpn_route_propagation"] = vpn_route_propagation

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cidr(self) -> typing.Optional[_ICidrProvider_28ddf5b0]:
        result = self._values.get("cidr")
        return typing.cast(typing.Optional[_ICidrProvider_28ddf5b0], result)

    @builtins.property
    def default_instance_tenancy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy]:
        result = self._values.get("default_instance_tenancy")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy], result)

    @builtins.property
    def enable_dns_hostnames(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_dns_hostnames")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_dns_support(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_dns_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def flow_logs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, FlowLogOptions]]:
        result = self._values.get("flow_logs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, FlowLogOptions]], result)

    @builtins.property
    def gateway_endpoints(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]]:
        result = self._values.get("gateway_endpoints")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]], result)

    @builtins.property
    def max_azs(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_azs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nat_gateway_provider(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider]:
        result = self._values.get("nat_gateway_provider")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider], result)

    @builtins.property
    def nat_gateways(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("nat_gateways")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nat_gateway_subnets(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        result = self._values.get("nat_gateway_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def vpc_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("vpc_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_connections(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]]:
        result = self._values.get("vpn_connections")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]], result)

    @builtins.property
    def vpn_gateway(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("vpn_gateway")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpn_gateway_asn(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("vpn_gateway_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpn_route_propagation(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]]:
        result = self._values.get("vpn_route_propagation")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FourTierNetworkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.FourTierNetworkShareProperties",
    jsii_struct_bases=[],
    name_mapping={
        "allow_external_principals": "allowExternalPrincipals",
        "auto_add_accounts": "autoAddAccounts",
        "pricipals": "pricipals",
    },
)
class FourTierNetworkShareProperties:
    def __init__(
        self,
        *,
        allow_external_principals: typing.Optional[builtins.bool] = None,
        auto_add_accounts: typing.Optional[builtins.bool] = None,
        pricipals: typing.Optional[typing.Sequence[_ISharedPrincipal_9cde791b]] = None,
    ) -> None:
        '''
        :param allow_external_principals: 
        :param auto_add_accounts: 
        :param pricipals: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bba6d7153869452d0a1b515208e0e7160367751697fbee237f3d54f9f8411a28)
            check_type(argname="argument allow_external_principals", value=allow_external_principals, expected_type=type_hints["allow_external_principals"])
            check_type(argname="argument auto_add_accounts", value=auto_add_accounts, expected_type=type_hints["auto_add_accounts"])
            check_type(argname="argument pricipals", value=pricipals, expected_type=type_hints["pricipals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_external_principals is not None:
            self._values["allow_external_principals"] = allow_external_principals
        if auto_add_accounts is not None:
            self._values["auto_add_accounts"] = auto_add_accounts
        if pricipals is not None:
            self._values["pricipals"] = pricipals

    @builtins.property
    def allow_external_principals(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("allow_external_principals")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_add_accounts(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("auto_add_accounts")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pricipals(self) -> typing.Optional[typing.List[_ISharedPrincipal_9cde791b]]:
        result = self._values.get("pricipals")
        return typing.cast(typing.Optional[typing.List[_ISharedPrincipal_9cde791b]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FourTierNetworkShareProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FourTierNetworkSpoke(
    FourTierNetwork,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2_patterns.FourTierNetworkSpoke",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        hub: FourTierNetworkHub,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[_ICidrProvider_28ddf5b0] = None,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param hub: 
        :param availability_zones: 
        :param cidr: 
        :param default_instance_tenancy: 
        :param enable_dns_hostnames: 
        :param enable_dns_support: 
        :param flow_logs: 
        :param gateway_endpoints: 
        :param max_azs: 
        :param vpc_name: 
        :param vpn_connections: 
        :param vpn_gateway: 
        :param vpn_gateway_asn: 
        :param vpn_route_propagation: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7fc919bd6ebf5b551769cb4313098a0e49891c0d5e533cf159dc7f303b04473)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FourTierNetworkSpokeProps(
            hub=hub,
            availability_zones=availability_zones,
            cidr=cidr,
            default_instance_tenancy=default_instance_tenancy,
            enable_dns_hostnames=enable_dns_hostnames,
            enable_dns_support=enable_dns_support,
            flow_logs=flow_logs,
            gateway_endpoints=gateway_endpoints,
            max_azs=max_azs,
            vpc_name=vpc_name,
            vpn_connections=vpn_connections,
            vpn_gateway=vpn_gateway,
            vpn_gateway_asn=vpn_gateway_asn,
            vpn_route_propagation=vpn_route_propagation,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="transitGateway")
    def transit_gateway(self) -> _ITransitGateway_25936657:
        return typing.cast(_ITransitGateway_25936657, jsii.get(self, "transitGateway"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachment")
    def transit_gateway_attachment(self) -> _ITransitGatewayAttachment_64da8ffd:
        return typing.cast(_ITransitGatewayAttachment_64da8ffd, jsii.get(self, "transitGatewayAttachment"))


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.FourTierNetworkSpokeProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "hub": "hub",
        "availability_zones": "availabilityZones",
        "cidr": "cidr",
        "default_instance_tenancy": "defaultInstanceTenancy",
        "enable_dns_hostnames": "enableDnsHostnames",
        "enable_dns_support": "enableDnsSupport",
        "flow_logs": "flowLogs",
        "gateway_endpoints": "gatewayEndpoints",
        "max_azs": "maxAzs",
        "vpc_name": "vpcName",
        "vpn_connections": "vpnConnections",
        "vpn_gateway": "vpnGateway",
        "vpn_gateway_asn": "vpnGatewayAsn",
        "vpn_route_propagation": "vpnRoutePropagation",
    },
)
class FourTierNetworkSpokeProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        hub: FourTierNetworkHub,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[_ICidrProvider_28ddf5b0] = None,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param hub: 
        :param availability_zones: 
        :param cidr: 
        :param default_instance_tenancy: 
        :param enable_dns_hostnames: 
        :param enable_dns_support: 
        :param flow_logs: 
        :param gateway_endpoints: 
        :param max_azs: 
        :param vpc_name: 
        :param vpn_connections: 
        :param vpn_gateway: 
        :param vpn_gateway_asn: 
        :param vpn_route_propagation: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f20b71c01dce683a9711971685bfd423a84bb51b3ae70144ed170d14b6b7721)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument hub", value=hub, expected_type=type_hints["hub"])
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument default_instance_tenancy", value=default_instance_tenancy, expected_type=type_hints["default_instance_tenancy"])
            check_type(argname="argument enable_dns_hostnames", value=enable_dns_hostnames, expected_type=type_hints["enable_dns_hostnames"])
            check_type(argname="argument enable_dns_support", value=enable_dns_support, expected_type=type_hints["enable_dns_support"])
            check_type(argname="argument flow_logs", value=flow_logs, expected_type=type_hints["flow_logs"])
            check_type(argname="argument gateway_endpoints", value=gateway_endpoints, expected_type=type_hints["gateway_endpoints"])
            check_type(argname="argument max_azs", value=max_azs, expected_type=type_hints["max_azs"])
            check_type(argname="argument vpc_name", value=vpc_name, expected_type=type_hints["vpc_name"])
            check_type(argname="argument vpn_connections", value=vpn_connections, expected_type=type_hints["vpn_connections"])
            check_type(argname="argument vpn_gateway", value=vpn_gateway, expected_type=type_hints["vpn_gateway"])
            check_type(argname="argument vpn_gateway_asn", value=vpn_gateway_asn, expected_type=type_hints["vpn_gateway_asn"])
            check_type(argname="argument vpn_route_propagation", value=vpn_route_propagation, expected_type=type_hints["vpn_route_propagation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hub": hub,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if cidr is not None:
            self._values["cidr"] = cidr
        if default_instance_tenancy is not None:
            self._values["default_instance_tenancy"] = default_instance_tenancy
        if enable_dns_hostnames is not None:
            self._values["enable_dns_hostnames"] = enable_dns_hostnames
        if enable_dns_support is not None:
            self._values["enable_dns_support"] = enable_dns_support
        if flow_logs is not None:
            self._values["flow_logs"] = flow_logs
        if gateway_endpoints is not None:
            self._values["gateway_endpoints"] = gateway_endpoints
        if max_azs is not None:
            self._values["max_azs"] = max_azs
        if vpc_name is not None:
            self._values["vpc_name"] = vpc_name
        if vpn_connections is not None:
            self._values["vpn_connections"] = vpn_connections
        if vpn_gateway is not None:
            self._values["vpn_gateway"] = vpn_gateway
        if vpn_gateway_asn is not None:
            self._values["vpn_gateway_asn"] = vpn_gateway_asn
        if vpn_route_propagation is not None:
            self._values["vpn_route_propagation"] = vpn_route_propagation

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hub(self) -> FourTierNetworkHub:
        result = self._values.get("hub")
        assert result is not None, "Required property 'hub' is missing"
        return typing.cast(FourTierNetworkHub, result)

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cidr(self) -> typing.Optional[_ICidrProvider_28ddf5b0]:
        result = self._values.get("cidr")
        return typing.cast(typing.Optional[_ICidrProvider_28ddf5b0], result)

    @builtins.property
    def default_instance_tenancy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy]:
        result = self._values.get("default_instance_tenancy")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy], result)

    @builtins.property
    def enable_dns_hostnames(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_dns_hostnames")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_dns_support(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_dns_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def flow_logs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.FlowLogOptions]]:
        result = self._values.get("flow_logs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.FlowLogOptions]], result)

    @builtins.property
    def gateway_endpoints(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]]:
        result = self._values.get("gateway_endpoints")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]], result)

    @builtins.property
    def max_azs(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_azs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("vpc_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_connections(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]]:
        result = self._values.get("vpn_connections")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]], result)

    @builtins.property
    def vpn_gateway(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("vpn_gateway")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpn_gateway_asn(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("vpn_gateway_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpn_route_propagation(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]]:
        result = self._values.get("vpn_route_propagation")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FourTierNetworkSpokeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.GetVpcConfigurationOptions",
    jsii_struct_bases=[],
    name_mapping={"netmask": "netmask"},
)
class GetVpcConfigurationOptions:
    def __init__(self, *, netmask: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param netmask: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73f84a5059463abc39d6faf377aa45c4e72d149e1f0cdf8660f2dd4a4e699efe)
            check_type(argname="argument netmask", value=netmask, expected_type=type_hints["netmask"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if netmask is not None:
            self._values["netmask"] = netmask

    @builtins.property
    def netmask(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("netmask")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GetVpcConfigurationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IpAddressManager(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2_patterns.IpAddressManager",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        sharing: typing.Optional[typing.Union["IpAddressManagerSharingProps", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_allocation_mask: typing.Optional[jsii.Number] = None,
        vpc_pool_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_region_mask: typing.Optional[jsii.Number] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param regions: 
        :param sharing: 
        :param vpc_allocation_mask: 
        :param vpc_pool_cidrs: 
        :param vpc_region_mask: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5bbc27e214643b7b9d138ec1be6d1c8d83e4ff65e813ac16c1afea0a01c0aed)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IpAddressManagerProps(
            regions=regions,
            sharing=sharing,
            vpc_allocation_mask=vpc_allocation_mask,
            vpc_pool_cidrs=vpc_pool_cidrs,
            vpc_region_mask=vpc_region_mask,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addRegion")
    def add_region(self, region: builtins.str) -> None:
        '''
        :param region: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d1ee3c61abc8dc1d2e619121864558a6a5427f0f16c5d8a598cb68d7ab3a3f)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        return typing.cast(None, jsii.invoke(self, "addRegion", [region]))

    @jsii.member(jsii_name="getVpcConfiguration")
    def get_vpc_configuration(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        netmask: typing.Optional[jsii.Number] = None,
    ) -> _ICidrProvider_28ddf5b0:
        '''
        :param scope: -
        :param id: -
        :param netmask: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2084a4b321f056ea50163ac40ebe793a26b0beac1d255cd4bec4b080b511843)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = GetVpcConfigurationOptions(netmask=netmask)

        return typing.cast(_ICidrProvider_28ddf5b0, jsii.invoke(self, "getVpcConfiguration", [scope, id, options]))

    @jsii.member(jsii_name="privateVpcPoolForEnvironment")
    def _private_vpc_pool_for_environment(
        self,
        account: builtins.str,
        region: builtins.str,
    ) -> _IIpamPool_511f311d:
        '''
        :param account: -
        :param region: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b404496af7848b9388bd86ad8d5d357cc5c2b44e88d4483f2e10ee13f5cf74be)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        return typing.cast(_IIpamPool_511f311d, jsii.invoke(self, "privateVpcPoolForEnvironment", [account, region]))

    @jsii.member(jsii_name="privateVpcPoolForRegion")
    def _private_vpc_pool_for_region(self, region: builtins.str) -> _IIpamPool_511f311d:
        '''
        :param region: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9b0425143c6a5f335913f94bf436e919ec10601881712e3ad1174811d6ce161)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        return typing.cast(_IIpamPool_511f311d, jsii.invoke(self, "privateVpcPoolForRegion", [region]))

    @jsii.member(jsii_name="registerAccount")
    def _register_account(
        self,
        account: builtins.str,
        pool: _IIpamPool_511f311d,
    ) -> None:
        '''
        :param account: -
        :param pool: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c82b599c8d1db4dca2c0b4ea748776ad7c5f35028ef3d218517ae47d9e5906d7)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument pool", value=pool, expected_type=type_hints["pool"])
        return typing.cast(None, jsii.invoke(self, "registerAccount", [account, pool]))

    @jsii.member(jsii_name="registerCidr")
    def register_cidr(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        cidr: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cidr: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40b8b9f3ec39cfa131ae90cec05dae5574e5732a20011027bad77df02d7e33b9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
        return typing.cast(None, jsii.invoke(self, "registerCidr", [scope, id, cidr]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_VPC_ALLOCATION_MASK")
    def DEFAULT_VPC_ALLOCATION_MASK(cls) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.sget(cls, "DEFAULT_VPC_ALLOCATION_MASK"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_VPC_POOL_CIDRS")
    def DEFAULT_VPC_POOL_CIDRS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "DEFAULT_VPC_POOL_CIDRS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_VPC_REGION_MASK")
    def DEFAULT_VPC_REGION_MASK(cls) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.sget(cls, "DEFAULT_VPC_REGION_MASK"))

    @builtins.property
    @jsii.member(jsii_name="allowExternalPricipals")
    def allow_external_pricipals(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "allowExternalPricipals"))

    @builtins.property
    @jsii.member(jsii_name="ipam")
    def ipam(self) -> _Ipam_1ad3c981:
        return typing.cast(_Ipam_1ad3c981, jsii.get(self, "ipam"))

    @builtins.property
    @jsii.member(jsii_name="sharingEnabled")
    def sharing_enabled(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "sharingEnabled"))

    @builtins.property
    @jsii.member(jsii_name="vpcAllocationMask")
    def vpc_allocation_mask(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vpcAllocationMask"))

    @builtins.property
    @jsii.member(jsii_name="resourceShare")
    def resource_share(self) -> typing.Optional[_ResourceShare_f0180713]:
        return typing.cast(typing.Optional[_ResourceShare_f0180713], jsii.get(self, "resourceShare"))


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.IpAddressManagerProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "regions": "regions",
        "sharing": "sharing",
        "vpc_allocation_mask": "vpcAllocationMask",
        "vpc_pool_cidrs": "vpcPoolCidrs",
        "vpc_region_mask": "vpcRegionMask",
    },
)
class IpAddressManagerProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        sharing: typing.Optional[typing.Union["IpAddressManagerSharingProps", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_allocation_mask: typing.Optional[jsii.Number] = None,
        vpc_pool_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc_region_mask: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param regions: 
        :param sharing: 
        :param vpc_allocation_mask: 
        :param vpc_pool_cidrs: 
        :param vpc_region_mask: 
        '''
        if isinstance(sharing, dict):
            sharing = IpAddressManagerSharingProps(**sharing)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba6a3618628a126f74720a6e6078d9d69aab82d46ddf292343434ce66bb23af2)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument sharing", value=sharing, expected_type=type_hints["sharing"])
            check_type(argname="argument vpc_allocation_mask", value=vpc_allocation_mask, expected_type=type_hints["vpc_allocation_mask"])
            check_type(argname="argument vpc_pool_cidrs", value=vpc_pool_cidrs, expected_type=type_hints["vpc_pool_cidrs"])
            check_type(argname="argument vpc_region_mask", value=vpc_region_mask, expected_type=type_hints["vpc_region_mask"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if regions is not None:
            self._values["regions"] = regions
        if sharing is not None:
            self._values["sharing"] = sharing
        if vpc_allocation_mask is not None:
            self._values["vpc_allocation_mask"] = vpc_allocation_mask
        if vpc_pool_cidrs is not None:
            self._values["vpc_pool_cidrs"] = vpc_pool_cidrs
        if vpc_region_mask is not None:
            self._values["vpc_region_mask"] = vpc_region_mask

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sharing(self) -> typing.Optional["IpAddressManagerSharingProps"]:
        result = self._values.get("sharing")
        return typing.cast(typing.Optional["IpAddressManagerSharingProps"], result)

    @builtins.property
    def vpc_allocation_mask(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("vpc_allocation_mask")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc_pool_cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("vpc_pool_cidrs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc_region_mask(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("vpc_region_mask")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IpAddressManagerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.IpAddressManagerSharingProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_external_pricipals": "allowExternalPricipals",
        "enabled": "enabled",
    },
)
class IpAddressManagerSharingProps:
    def __init__(
        self,
        *,
        allow_external_pricipals: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param allow_external_pricipals: 
        :param enabled: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__625f9f8c0a5d69c3e4b2374c91d8e564230c3262a5c1305b19ec565ab3ffed26)
            check_type(argname="argument allow_external_pricipals", value=allow_external_pricipals, expected_type=type_hints["allow_external_pricipals"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_external_pricipals is not None:
            self._values["allow_external_pricipals"] = allow_external_pricipals
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def allow_external_pricipals(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("allow_external_pricipals")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IpAddressManagerSharingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkController(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2_patterns.NetworkController",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        default_netmask: typing.Optional[jsii.Number] = None,
        flow_log_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        flow_log_format: typing.Optional[_FlowLogFormat_b7c2ba34] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param default_netmask: 
        :param flow_log_bucket: 
        :param flow_log_format: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d930e3de8c120c3fc5f5c70030691aa4f52aa6e26d49c32535c5bce5c960935e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NetworkControllerProps(
            default_netmask=default_netmask,
            flow_log_bucket=flow_log_bucket,
            flow_log_format=flow_log_format,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addHub")
    def add_hub(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        default_transit_gateway_route_table: typing.Optional[_ITransitGatewayRouteTable_56647ab2] = None,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        netmask: typing.Optional[jsii.Number] = None,
    ) -> FourTierNetworkHub:
        '''
        :param scope: -
        :param id: -
        :param default_transit_gateway_route_table: 
        :param availability_zones: 
        :param max_azs: 
        :param netmask: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74ba1ec928c092f33aeb546fda189638c35c356996133e040cb167d089e3f343)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = AddHubOptions(
            default_transit_gateway_route_table=default_transit_gateway_route_table,
            availability_zones=availability_zones,
            max_azs=max_azs,
            netmask=netmask,
        )

        return typing.cast(FourTierNetworkHub, jsii.invoke(self, "addHub", [scope, id, options]))

    @jsii.member(jsii_name="addSpoke")
    def add_spoke(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        netmask: typing.Optional[jsii.Number] = None,
    ) -> FourTierNetworkSpoke:
        '''
        :param scope: -
        :param id: -
        :param availability_zones: 
        :param max_azs: 
        :param netmask: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f39726d5378c607c7d2408b015e8aed7d5f87a4d39b2235dbde97aa46e8daba2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = AddNetworkOptions(
            availability_zones=availability_zones, max_azs=max_azs, netmask=netmask
        )

        return typing.cast(FourTierNetworkSpoke, jsii.invoke(self, "addSpoke", [scope, id, options]))

    @jsii.member(jsii_name="registerAccount")
    def _register_account(self, account: builtins.str) -> None:
        '''
        :param account: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a94042b91cf18ea51b81a0607a52121519d15828b001d7f2a7c825c4dc5c4f9)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
        return typing.cast(None, jsii.invoke(self, "registerAccount", [account]))

    @jsii.member(jsii_name="registerCidr")
    def register_cidr(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        cidr: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cidr: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1f41e11dc1855fbe7fdce1aa48beabad7f48a7b2857e27f90757c5dd4ffc621)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
        return typing.cast(None, jsii.invoke(self, "registerCidr", [scope, id, cidr]))

    @jsii.member(jsii_name="registerRegion")
    def _register_region(self, region: builtins.str) -> None:
        '''
        :param region: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ea0364f3254929215baedf3bfe5eb8fb59ce1151f770db5cfc4eb7f7dd9754c)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        return typing.cast(None, jsii.invoke(self, "registerRegion", [region]))

    @builtins.property
    @jsii.member(jsii_name="addressManager")
    def address_manager(self) -> IpAddressManager:
        return typing.cast(IpAddressManager, jsii.get(self, "addressManager"))

    @builtins.property
    @jsii.member(jsii_name="defaultNetmask")
    def default_netmask(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultNetmask"))

    @builtins.property
    @jsii.member(jsii_name="flowLogBucket")
    def flow_log_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.get(self, "flowLogBucket"))

    @builtins.property
    @jsii.member(jsii_name="flowLogFormat")
    def flow_log_format(self) -> _FlowLogFormat_b7c2ba34:
        return typing.cast(_FlowLogFormat_b7c2ba34, jsii.get(self, "flowLogFormat"))

    @builtins.property
    @jsii.member(jsii_name="globalNetwork")
    def global_network(self) -> _GlobalNetwork_79ec647c:
        return typing.cast(_GlobalNetwork_79ec647c, jsii.get(self, "globalNetwork"))

    @builtins.property
    @jsii.member(jsii_name="registeredAccounts")
    def registered_accounts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "registeredAccounts"))

    @builtins.property
    @jsii.member(jsii_name="registeredRegions")
    def registered_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "registeredRegions"))


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.NetworkControllerProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "default_netmask": "defaultNetmask",
        "flow_log_bucket": "flowLogBucket",
        "flow_log_format": "flowLogFormat",
    },
)
class NetworkControllerProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        default_netmask: typing.Optional[jsii.Number] = None,
        flow_log_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        flow_log_format: typing.Optional[_FlowLogFormat_b7c2ba34] = None,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param default_netmask: 
        :param flow_log_bucket: 
        :param flow_log_format: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eee37f6e80a88db3d1de97179d49c53732c2177cd8790b1b68e521aa37f3e9d)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument default_netmask", value=default_netmask, expected_type=type_hints["default_netmask"])
            check_type(argname="argument flow_log_bucket", value=flow_log_bucket, expected_type=type_hints["flow_log_bucket"])
            check_type(argname="argument flow_log_format", value=flow_log_format, expected_type=type_hints["flow_log_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if default_netmask is not None:
            self._values["default_netmask"] = default_netmask
        if flow_log_bucket is not None:
            self._values["flow_log_bucket"] = flow_log_bucket
        if flow_log_format is not None:
            self._values["flow_log_format"] = flow_log_format

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_netmask(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("default_netmask")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def flow_log_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        result = self._values.get("flow_log_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    @builtins.property
    def flow_log_format(self) -> typing.Optional[_FlowLogFormat_b7c2ba34]:
        result = self._values.get("flow_log_format")
        return typing.cast(typing.Optional[_FlowLogFormat_b7c2ba34], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkControllerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.TransitGatewayHubConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "allow_external": "allowExternal",
        "auto_accept_shared_attachments": "autoAcceptSharedAttachments",
        "auto_discovery": "autoDiscovery",
        "default_route_table_id": "defaultRouteTableId",
        "principals": "principals",
    },
)
class TransitGatewayHubConfiguration:
    def __init__(
        self,
        *,
        allow_external: typing.Optional[builtins.bool] = None,
        auto_accept_shared_attachments: typing.Optional[builtins.bool] = None,
        auto_discovery: typing.Optional[builtins.bool] = None,
        default_route_table_id: typing.Optional[builtins.str] = None,
        principals: typing.Optional[typing.Sequence[_ISharedPrincipal_9cde791b]] = None,
    ) -> None:
        '''
        :param allow_external: Allows Transit Gateway sharing with resources outside of the Transit Gateway owner account's AWS Organization. By default, resources cannot be shared with accounts outside of the organization.
        :param auto_accept_shared_attachments: Enable or disable automatic acceptance of attachment requests. When this is enabled, any transit gateway attachments created in other accounts where this transit gateway has been shared will be automatically created without manual intervention being needed in the account that did created the share.
        :param auto_discovery: Enables auto-discovery of AWS accounts via CDK resources. Account discovery uses stages and stacks to find all accounts that the CDK has resources for. Environment agnostic stages and stacks cannot be used for auto-discovery. With auto-discovery enabled, the stack containing the Transit Gateway will need to be updated before it will become available in newly added accounts. Because of this it is inferior to using grouping principals such as organizations or organizational units. If access to sharing via AWS OIrganizations is available, that should be preferred over auto-discovery. Transit gateway sharing will be anabled if either auto-discovery is enabled or principals are specified.
        :param default_route_table_id: The ID of the default Transit Gateway Route Table that got created for the Transit Gateway associated with this VPC. This is needed because the default route table is used for handling routing of all traffic within the organization but not exposed directly via CloudFormation. See `feature request <https://github.com/aws-cloudformation/cloudformation-coverage-roadmap/issues/180>`_ related to this in the AWS CloudFormation roadmap. This is only needed if the VPC is being configured to act as a hub for network traffic. Won't be available until after this stack has been deployed for the first time.
        :param principals: A list of principals which allow other accounts access to the Transit Gateway. With shared access, other accounts can create Attachments to facilitate cross account networking. Principals provided should not overlap with CDK resources if auto-discovery is enabled. Transit gateway sharing will be anabled if either auto-discovery is enabled or principals are specified.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6667797cf749d298a257c6c716db23d22c81c5c28b1dbf19334ef2de80ebcba5)
            check_type(argname="argument allow_external", value=allow_external, expected_type=type_hints["allow_external"])
            check_type(argname="argument auto_accept_shared_attachments", value=auto_accept_shared_attachments, expected_type=type_hints["auto_accept_shared_attachments"])
            check_type(argname="argument auto_discovery", value=auto_discovery, expected_type=type_hints["auto_discovery"])
            check_type(argname="argument default_route_table_id", value=default_route_table_id, expected_type=type_hints["default_route_table_id"])
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_external is not None:
            self._values["allow_external"] = allow_external
        if auto_accept_shared_attachments is not None:
            self._values["auto_accept_shared_attachments"] = auto_accept_shared_attachments
        if auto_discovery is not None:
            self._values["auto_discovery"] = auto_discovery
        if default_route_table_id is not None:
            self._values["default_route_table_id"] = default_route_table_id
        if principals is not None:
            self._values["principals"] = principals

    @builtins.property
    def allow_external(self) -> typing.Optional[builtins.bool]:
        '''Allows Transit Gateway sharing with resources outside of the Transit Gateway owner account's AWS Organization.

        By default, resources cannot be shared with accounts outside of the organization.
        '''
        result = self._values.get("allow_external")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_accept_shared_attachments(self) -> typing.Optional[builtins.bool]:
        '''Enable or disable automatic acceptance of attachment requests.

        When this is enabled, any transit gateway attachments created in other accounts where this
        transit gateway has been shared will be automatically created without manual intervention
        being needed in the account that did created the share.
        '''
        result = self._values.get("auto_accept_shared_attachments")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_discovery(self) -> typing.Optional[builtins.bool]:
        '''Enables auto-discovery of AWS accounts via CDK resources.

        Account discovery uses stages
        and stacks to find all accounts that the CDK has resources for.

        Environment agnostic stages and stacks cannot be used for auto-discovery.

        With auto-discovery enabled, the stack containing the Transit Gateway will need to be
        updated before it will become available in newly added accounts. Because of this it is
        inferior to using grouping principals such as organizations or organizational units.

        If access to sharing via AWS OIrganizations is available, that should be preferred over
        auto-discovery.

        Transit gateway sharing will be anabled if either auto-discovery is enabled or principals
        are specified.
        '''
        result = self._values.get("auto_discovery")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def default_route_table_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the default Transit Gateway Route Table that got created for the Transit Gateway associated with this VPC.

        This is needed because the default route table is used for handling routing of all traffic within
        the organization but not exposed directly via CloudFormation.

        See `feature request <https://github.com/aws-cloudformation/cloudformation-coverage-roadmap/issues/180>`_
        related to this in the AWS CloudFormation roadmap.

        This is only needed if the VPC is being configured to act as a hub for network traffic. Won't be
        available until after this stack has been deployed for the first time.
        '''
        result = self._values.get("default_route_table_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principals(self) -> typing.Optional[typing.List[_ISharedPrincipal_9cde791b]]:
        '''A list of principals which allow other accounts access to the Transit Gateway.

        With shared
        access, other accounts can create Attachments to facilitate cross account networking.

        Principals provided should not overlap with CDK resources if auto-discovery is enabled.

        Transit gateway sharing will be anabled if either auto-discovery is enabled or principals
        are specified.
        '''
        result = self._values.get("principals")
        return typing.cast(typing.Optional[typing.List[_ISharedPrincipal_9cde791b]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransitGatewayHubConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.TransitGatewaySpokeConfiguration",
    jsii_struct_bases=[],
    name_mapping={"transit_gateway_id": "transitGatewayId"},
)
class TransitGatewaySpokeConfiguration:
    def __init__(self, *, transit_gateway_id: builtins.str) -> None:
        '''
        :param transit_gateway_id: The ID of a Transit Gateway. This Transit Gateway may have been created by another VPC in the same account or shared by a VPC in another account. If this is passed then a Transit Gateway Attachment will be created for the specified Transit Gateway and a new one will not be created even if {@link TransitGatewayHubConfiguration.principal | principals} are provided.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a4c2c3e6825c2e1a0d5ead7abe49653b6e864843a82ccc9624945cfe7e9a77)
            check_type(argname="argument transit_gateway_id", value=transit_gateway_id, expected_type=type_hints["transit_gateway_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "transit_gateway_id": transit_gateway_id,
        }

    @builtins.property
    def transit_gateway_id(self) -> builtins.str:
        '''The ID of a Transit Gateway.

        This Transit Gateway may have been created by another VPC in the
        same account or shared by a VPC in another account. If this is passed then a Transit Gateway
        Attachment will be created for the specified Transit Gateway and a new one will not be created
        even if {@link TransitGatewayHubConfiguration.principal | principals} are provided.
        '''
        result = self._values.get("transit_gateway_id")
        assert result is not None, "Required property 'transit_gateway_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransitGatewaySpokeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.AddHubOptions",
    jsii_struct_bases=[AddNetworkOptions],
    name_mapping={
        "availability_zones": "availabilityZones",
        "max_azs": "maxAzs",
        "netmask": "netmask",
        "default_transit_gateway_route_table": "defaultTransitGatewayRouteTable",
    },
)
class AddHubOptions(AddNetworkOptions):
    def __init__(
        self,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        netmask: typing.Optional[jsii.Number] = None,
        default_transit_gateway_route_table: typing.Optional[_ITransitGatewayRouteTable_56647ab2] = None,
    ) -> None:
        '''
        :param availability_zones: 
        :param max_azs: 
        :param netmask: 
        :param default_transit_gateway_route_table: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c4ce4c01a87f778abb62e49cc5acd8a93062b58323030370dceef52e894cb84)
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument max_azs", value=max_azs, expected_type=type_hints["max_azs"])
            check_type(argname="argument netmask", value=netmask, expected_type=type_hints["netmask"])
            check_type(argname="argument default_transit_gateway_route_table", value=default_transit_gateway_route_table, expected_type=type_hints["default_transit_gateway_route_table"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if max_azs is not None:
            self._values["max_azs"] = max_azs
        if netmask is not None:
            self._values["netmask"] = netmask
        if default_transit_gateway_route_table is not None:
            self._values["default_transit_gateway_route_table"] = default_transit_gateway_route_table

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_azs(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_azs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def netmask(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("netmask")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_transit_gateway_route_table(
        self,
    ) -> typing.Optional[_ITransitGatewayRouteTable_56647ab2]:
        result = self._values.get("default_transit_gateway_route_table")
        return typing.cast(typing.Optional[_ITransitGatewayRouteTable_56647ab2], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddHubOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddHubOptions",
    "AddNetworkOptions",
    "AddPoolOptions",
    "AddSpokeNetworkProps",
    "AllocatePrivateNetworkOptions",
    "FlowLogOptions",
    "FourTierNetwork",
    "FourTierNetworkHub",
    "FourTierNetworkHubProps",
    "FourTierNetworkProps",
    "FourTierNetworkShareProperties",
    "FourTierNetworkSpoke",
    "FourTierNetworkSpokeProps",
    "GetVpcConfigurationOptions",
    "IpAddressManager",
    "IpAddressManagerProps",
    "IpAddressManagerSharingProps",
    "NetworkController",
    "NetworkControllerProps",
    "TransitGatewayHubConfiguration",
    "TransitGatewaySpokeConfiguration",
]

publication.publish()

def _typecheckingstub__24d3c1346e4e259fee32303499f123223b892ff23852cdfdf5a57bf21cad7680(
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    netmask: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bafe93fe5666e81af7b6555c6e0b02d696c2267310d93ce406cc5b16333a1449(
    *,
    cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_netmask_length: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048409c4bedb08ed8edc9dda9cec65cb4087822a3dcae95d57c194d4e0613116(
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidr: typing.Optional[_ICidrProvider_28ddf5b0] = None,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    vpc_name: typing.Optional[builtins.str] = None,
    vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_gateway: typing.Optional[builtins.bool] = None,
    vpn_gateway_asn: typing.Optional[jsii.Number] = None,
    vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1edcf1c081b844711051faa1818771b547c90031be28d3b0f04a24516485f5eb(
    *,
    netmask: typing.Optional[jsii.Number] = None,
    pool: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61356c6c988a747170b0fff518aeff55bb37140b2f2bb3a8395a7676df11d939(
    *,
    destination: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination] = None,
    log_format: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.LogFormat]] = None,
    max_aggregation_interval: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval] = None,
    traffic_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType] = None,
    log_format_definition: typing.Optional[_FlowLogFormat_b7c2ba34] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01b54dda1f6044b8b90a294f4af2c53fd512620a5e619adafd6d687a35f35dc3(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidr: typing.Optional[_ICidrProvider_28ddf5b0] = None,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    nat_gateway_provider: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider] = None,
    nat_gateways: typing.Optional[jsii.Number] = None,
    nat_gateway_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_name: typing.Optional[builtins.str] = None,
    vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_gateway: typing.Optional[builtins.bool] = None,
    vpn_gateway_asn: typing.Optional[jsii.Number] = None,
    vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb697f4884edaa9946bcf623d36e26bbc15cba6a321ac50f29f26b8fdef42b2a(
    id: builtins.str,
    *,
    log_format_definition: typing.Optional[_FlowLogFormat_b7c2ba34] = None,
    destination: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination] = None,
    log_format: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.LogFormat]] = None,
    max_aggregation_interval: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval] = None,
    traffic_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ace25eaf0b1bdeb7c9833547b92ca28254092d01db9ebc9696fce2260b43d9(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidr: typing.Optional[_ICidrProvider_28ddf5b0] = None,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    default_transit_gateway_route_table: typing.Optional[_ITransitGatewayRouteTable_56647ab2] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    global_network: typing.Optional[_GlobalNetwork_79ec647c] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    sharing: typing.Optional[typing.Union[FourTierNetworkShareProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_name: typing.Optional[builtins.str] = None,
    vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_gateway: typing.Optional[builtins.bool] = None,
    vpn_gateway_asn: typing.Optional[jsii.Number] = None,
    vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b427eb756711b9be0d1724b92283f7b8b658149d02d0860ddfaae4ca009451a6(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidr: typing.Optional[_ICidrProvider_28ddf5b0] = None,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    vpc_name: typing.Optional[builtins.str] = None,
    vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_gateway: typing.Optional[builtins.bool] = None,
    vpn_gateway_asn: typing.Optional[jsii.Number] = None,
    vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e120a9a594264d414d234533b6a6694a2e18b423a355c83676f0931ec9be90(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidr: typing.Optional[_ICidrProvider_28ddf5b0] = None,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    default_transit_gateway_route_table: typing.Optional[_ITransitGatewayRouteTable_56647ab2] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    global_network: typing.Optional[_GlobalNetwork_79ec647c] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    sharing: typing.Optional[typing.Union[FourTierNetworkShareProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_name: typing.Optional[builtins.str] = None,
    vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_gateway: typing.Optional[builtins.bool] = None,
    vpn_gateway_asn: typing.Optional[jsii.Number] = None,
    vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9f1c80c97704155becd995a7614b98797ff3dcfedcb6c14a3c861d8ffa5d99(
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidr: typing.Optional[_ICidrProvider_28ddf5b0] = None,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    nat_gateway_provider: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider] = None,
    nat_gateways: typing.Optional[jsii.Number] = None,
    nat_gateway_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_name: typing.Optional[builtins.str] = None,
    vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_gateway: typing.Optional[builtins.bool] = None,
    vpn_gateway_asn: typing.Optional[jsii.Number] = None,
    vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba6d7153869452d0a1b515208e0e7160367751697fbee237f3d54f9f8411a28(
    *,
    allow_external_principals: typing.Optional[builtins.bool] = None,
    auto_add_accounts: typing.Optional[builtins.bool] = None,
    pricipals: typing.Optional[typing.Sequence[_ISharedPrincipal_9cde791b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7fc919bd6ebf5b551769cb4313098a0e49891c0d5e533cf159dc7f303b04473(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    hub: FourTierNetworkHub,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidr: typing.Optional[_ICidrProvider_28ddf5b0] = None,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    vpc_name: typing.Optional[builtins.str] = None,
    vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_gateway: typing.Optional[builtins.bool] = None,
    vpn_gateway_asn: typing.Optional[jsii.Number] = None,
    vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f20b71c01dce683a9711971685bfd423a84bb51b3ae70144ed170d14b6b7721(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    hub: FourTierNetworkHub,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidr: typing.Optional[_ICidrProvider_28ddf5b0] = None,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    vpc_name: typing.Optional[builtins.str] = None,
    vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_gateway: typing.Optional[builtins.bool] = None,
    vpn_gateway_asn: typing.Optional[jsii.Number] = None,
    vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73f84a5059463abc39d6faf377aa45c4e72d149e1f0cdf8660f2dd4a4e699efe(
    *,
    netmask: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5bbc27e214643b7b9d138ec1be6d1c8d83e4ff65e813ac16c1afea0a01c0aed(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    sharing: typing.Optional[typing.Union[IpAddressManagerSharingProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_allocation_mask: typing.Optional[jsii.Number] = None,
    vpc_pool_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_region_mask: typing.Optional[jsii.Number] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d1ee3c61abc8dc1d2e619121864558a6a5427f0f16c5d8a598cb68d7ab3a3f(
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2084a4b321f056ea50163ac40ebe793a26b0beac1d255cd4bec4b080b511843(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    netmask: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b404496af7848b9388bd86ad8d5d357cc5c2b44e88d4483f2e10ee13f5cf74be(
    account: builtins.str,
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b0425143c6a5f335913f94bf436e919ec10601881712e3ad1174811d6ce161(
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82b599c8d1db4dca2c0b4ea748776ad7c5f35028ef3d218517ae47d9e5906d7(
    account: builtins.str,
    pool: _IIpamPool_511f311d,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b8b9f3ec39cfa131ae90cec05dae5574e5732a20011027bad77df02d7e33b9(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    cidr: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6a3618628a126f74720a6e6078d9d69aab82d46ddf292343434ce66bb23af2(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    sharing: typing.Optional[typing.Union[IpAddressManagerSharingProps, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_allocation_mask: typing.Optional[jsii.Number] = None,
    vpc_pool_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_region_mask: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625f9f8c0a5d69c3e4b2374c91d8e564230c3262a5c1305b19ec565ab3ffed26(
    *,
    allow_external_pricipals: typing.Optional[builtins.bool] = None,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d930e3de8c120c3fc5f5c70030691aa4f52aa6e26d49c32535c5bce5c960935e(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    default_netmask: typing.Optional[jsii.Number] = None,
    flow_log_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    flow_log_format: typing.Optional[_FlowLogFormat_b7c2ba34] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ba1ec928c092f33aeb546fda189638c35c356996133e040cb167d089e3f343(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    default_transit_gateway_route_table: typing.Optional[_ITransitGatewayRouteTable_56647ab2] = None,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    netmask: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39726d5378c607c7d2408b015e8aed7d5f87a4d39b2235dbde97aa46e8daba2(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    netmask: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a94042b91cf18ea51b81a0607a52121519d15828b001d7f2a7c825c4dc5c4f9(
    account: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1f41e11dc1855fbe7fdce1aa48beabad7f48a7b2857e27f90757c5dd4ffc621(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    cidr: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ea0364f3254929215baedf3bfe5eb8fb59ce1151f770db5cfc4eb7f7dd9754c(
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eee37f6e80a88db3d1de97179d49c53732c2177cd8790b1b68e521aa37f3e9d(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    default_netmask: typing.Optional[jsii.Number] = None,
    flow_log_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    flow_log_format: typing.Optional[_FlowLogFormat_b7c2ba34] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6667797cf749d298a257c6c716db23d22c81c5c28b1dbf19334ef2de80ebcba5(
    *,
    allow_external: typing.Optional[builtins.bool] = None,
    auto_accept_shared_attachments: typing.Optional[builtins.bool] = None,
    auto_discovery: typing.Optional[builtins.bool] = None,
    default_route_table_id: typing.Optional[builtins.str] = None,
    principals: typing.Optional[typing.Sequence[_ISharedPrincipal_9cde791b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a4c2c3e6825c2e1a0d5ead7abe49653b6e864843a82ccc9624945cfe7e9a77(
    *,
    transit_gateway_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4ce4c01a87f778abb62e49cc5acd8a93062b58323030370dceef52e894cb84(
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    netmask: typing.Optional[jsii.Number] = None,
    default_transit_gateway_route_table: typing.Optional[_ITransitGatewayRouteTable_56647ab2] = None,
) -> None:
    """Type checking stubs"""
    pass
