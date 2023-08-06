from __future__ import annotations
import sys
import os
import asyncio

sys.path.append(os.path.dirname("sharingiscaring"))
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub
from sharingiscaring.GRPCClient.health_pb2_grpc import HealthStub

from sharingiscaring.GRPCClient.types_pb2 import *
import grpc
import base58
import base64
from sharingiscaring.enums import NET
import datetime as dt
from rich.progress import track
from rich import print
from enum import Enum
from google.protobuf.json_format import MessageToJson, MessageToDict
from google.protobuf import message
import sys
import os
import time
from rich.console import Console

console = Console()


from sharingiscaring.GRPCClient.queries._GetPoolInfo import Mixin as _GetPoolInfo
from sharingiscaring.GRPCClient.queries._GetPoolDelegatorsRewardPeriod import (
    Mixin as _GetPoolDelegatorsRewardPeriod,
)
from sharingiscaring.GRPCClient.queries._GetPassiveDelegatorsRewardPeriod import (
    Mixin as _GetPassiveDelegatorsRewardPeriod,
)
from sharingiscaring.GRPCClient.queries._GetAccountList import Mixin as _GetAccountList
from sharingiscaring.GRPCClient.queries._GetBakerList import Mixin as _GetBakerList
from sharingiscaring.GRPCClient.queries._GetBlocksAtHeight import (
    Mixin as _GetBlocksAtHeight,
)
from sharingiscaring.GRPCClient.queries._GetFinalizedBlocks import (
    Mixin as _GetFinalizedBlocks,
)
from sharingiscaring.GRPCClient.queries._GetInstanceInfo import (
    Mixin as _GetInstanceInfo,
)
from sharingiscaring.GRPCClient.queries._GetInstanceList import (
    Mixin as _GetInstanceList,
)
from sharingiscaring.GRPCClient.queries._GetAnonymityRevokers import (
    Mixin as _GetAnonymityRevokers,
)
from sharingiscaring.GRPCClient.queries._GetIdentityProviders import (
    Mixin as _GetIdentityProviders,
)
from sharingiscaring.GRPCClient.queries._GetPoolDelegators import (
    Mixin as _GetPoolDelegators,
)
from sharingiscaring.GRPCClient.queries._GetPassiveDelegators import (
    Mixin as _GetPassiveDelegators,
)
from sharingiscaring.GRPCClient.queries._GetAccountInfo import Mixin as _GetAccountInfo
from sharingiscaring.GRPCClient.queries._GetBlockInfo import Mixin as _GetBlockInfo
from sharingiscaring.GRPCClient.queries._GetElectionInfo import (
    Mixin as _GetElectionInfo,
)
from sharingiscaring.GRPCClient.queries._GetTokenomicsInfo import (
    Mixin as _GetTokenomicsInfo,
)
from sharingiscaring.GRPCClient.queries._GetPassiveDelegationInfo import (
    Mixin as _GetPassiveDelegationInfo,
)
from sharingiscaring.GRPCClient.queries._GetBlockTransactionEvents import (
    Mixin as _GetBlockTransactionEvents,
)
from sharingiscaring.GRPCClient.queries._GetBlockSpecialEvents import (
    Mixin as _GetBlockSpecialEvents,
)
from sharingiscaring.GRPCClient.queries._GetBlockPendingUpdates import (
    Mixin as _GetBlockPendingUpdates,
)
from sharingiscaring.GRPCClient.queries._GetModuleSource import (
    Mixin as _GetModuleSource,
)
from sharingiscaring.GRPCClient.queries._GetBlockChainParameters import (
    Mixin as _GetBlockChainParameters,
)
from sharingiscaring.GRPCClient.queries._InvokeInstance import (
    Mixin as _InvokeInstance,
)

from sharingiscaring.GRPCClient.queries._CheckHealth import (
    Mixin as _CheckHealth,
)


class GRPCClient(
    _GetPoolInfo,
    _GetAccountList,
    _GetBakerList,
    _GetInstanceInfo,
    _GetInstanceList,
    _GetFinalizedBlocks,
    _GetBlocksAtHeight,
    _GetIdentityProviders,
    _GetAnonymityRevokers,
    _GetPassiveDelegationInfo,
    _GetPassiveDelegators,
    _GetPoolDelegators,
    _GetPoolDelegatorsRewardPeriod,
    _GetPassiveDelegatorsRewardPeriod,
    _GetAccountInfo,
    _GetBlockInfo,
    _GetElectionInfo,
    _GetBlockTransactionEvents,
    _GetBlockSpecialEvents,
    _GetBlockPendingUpdates,
    _GetTokenomicsInfo,
    _GetModuleSource,
    _GetBlockChainParameters,
    _InvokeInstance,
    _CheckHealth,
):
    def __init__(self, net: str = "mainnet"):
        self.net = NET(net)
        self.host_index = {NET.MAINNET: 0, NET.TESTNET: 0}
        self.hosts = {}
        self.hosts[NET.MAINNET] = [
            {"host": "localhost", "port": 20000},
            {"host": "31.21.31.76", "port": 20001},
            {"host": "207.180.201.8", "port": 20000},
        ]
        self.hosts[NET.TESTNET] = [
            {"host": "localhost", "port": 20001},
            {"host": "31.21.31.76", "port": 20002},
            {"host": "207.180.201.8", "port": 20001},
        ]
        self.connect()

    def connect(self):
        self.channel = grpc.insecure_channel(
            f"{self.hosts[self.net][self.host_index[self.net]]['host']}:{self.hosts[self.net][self.host_index[self.net]]['port']}"
        )
        # console.log(
        #     f"GRPCClient for {self.net.value} Connecting on: {self.hosts[self.net][self.host_index[self.net]]['host']}:{self.hosts[self.net][self.host_index[self.net]]['port']}"
        # )
        self.stub = QueriesStub(self.channel)
        self.health = HealthStub(self.channel)
        try:
            grpc.channel_ready_future(self.channel).result(timeout=1)
            console.log(
                f"GRPCClient for {self.net.value} Connected on : {self.hosts[self.net][self.host_index[self.net]]['host']}:{self.hosts[self.net][self.host_index[self.net]]['port']}"
            )
        except grpc.FutureTimeoutError:
            console.log(
                f"GRPCClient for {self.net.value} Timeout for  : {self.hosts[self.net][self.host_index[self.net]]['host']}:{self.hosts[self.net][self.host_index[self.net]]['port']}"
            )

    def switch_to_net(self, net: str = "mainnet"):
        # only switch when we need to connect to a different net
        if not net:
            net = NET.MAINNET.value

        if net != self.net.value:
            self.net = NET(net)
            self.connect()

    def check_connection(self, function_name=None):
        connected = False
        while not connected:
            try:
                grpc.channel_ready_future(self.channel).result(timeout=1)
                connected = True

            except grpc.FutureTimeoutError:
                console.log(
                    f"GRPCClient for {self.net.value} Timeout for  : {self.hosts[self.net][self.host_index[self.net]]['host']}:{self.hosts[self.net][self.host_index[self.net]]['port']}"
                )
                self.host_index[self.net] += 1
                if self.host_index[self.net] == len(self.hosts[self.net]):
                    self.host_index[self.net] = 0
                self.connect()

    def momentary_connect_to_different_host(self, host: dict, net: str = "mainnet"):
        # only switch when we need to connect to a different net
        if not net:
            net = NET.MAINNET

        current_hosts = self.hosts
        current_index = self.host_index

        self.hosts = [host]
        self.net = NET(net)
        self.connect()
