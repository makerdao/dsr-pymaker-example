# This file is part of Maker Keeper Framework.
#
# Copyright (C) 2019 KentonPrescott
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import pytest

import time
from typing import List
import logging

from web3 import Web3

from dsrdemo.dsr_proxy_demo import DsrProxyDemo
from dsrdemo.dsr_manager_demo import DsrManagerDemo
from pymaker import Address
from pymaker.deployment import DssDeployment
from pymaker.numeric import Wad, Rad

from tests.test_dsrmanager import mint_dai

def print_out(testName: str):
    print("")
    print(f"{testName}")
    print("")


class TestDsrDemo:

    def test_dsr_proxy_demo(self, mcd: DssDeployment, our_address: Address, dsr_proxy_demo: DsrProxyDemo):
        print_out("test_dsr_proxy_demo")

        dai = Wad.from_number(28)
        mint_dai(mcd=mcd, amount=dai, ilkName='ETH-A', our_address=our_address)

        dsr_proxy_demo.main()

        assert mcd.dai.balance_of(our_address) > dai

    def test_dsr_manager_demo(self, mcd: DssDeployment, our_address: Address, dsr_manager_demo: DsrManagerDemo):
        print_out("test_dsr_manager_demo")

        dai = Wad.from_number(28)
        mint_dai(mcd=mcd, amount=dai, ilkName='ETH-A', our_address=our_address)

        dsr_manager_demo.main()

        assert mcd.dai.balance_of(our_address) > dai

