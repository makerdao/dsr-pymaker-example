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

from dsrdemo.dsrdemo import DsrDemo
from pymaker import Address
from pymaker.deployment import DssDeployment
from pymaker.numeric import Wad, Rad

from tests.test_dss import wrap_eth, frob


def create_dai_token(mcd: DssDeployment, our_address: Address):
    collateral = mcd.collaterals['ETH-B']
    ilk = collateral.ilk
    # TestVat.ensure_clean_urn(mcd, collateral, our_address)
    initial_dai = mcd.vat.dai(our_address)
    wrap_eth(mcd, our_address, Wad.from_number(9))

    # Ensure our collateral enters the urn
    collateral_balance_before = collateral.gem.balance_of(our_address)
    collateral.approve(our_address)
    assert collateral.adapter.join(our_address, Wad.from_number(9)).transact()
    assert collateral.gem.balance_of(our_address) == collateral_balance_before - Wad.from_number(9)

    # Add collateral without generating Dai
    frob(mcd, collateral, our_address, dink=Wad.from_number(3), dart=Wad(0))
    print(f"After adding collateral:         {mcd.vat.urn(ilk, our_address)}")
    assert mcd.vat.urn(ilk, our_address).ink == Wad.from_number(3)
    assert mcd.vat.urn(ilk, our_address).art == Wad(0)
    assert mcd.vat.gem(ilk, our_address) == Wad.from_number(9) - mcd.vat.urn(ilk, our_address).ink
    assert mcd.vat.dai(our_address) == initial_dai

    # Generate some Dai
    frob(mcd, collateral, our_address, dink=Wad(0), dart=Wad.from_number(153))
    print(f"After generating dai:            {mcd.vat.urn(ilk, our_address)}")
    assert mcd.vat.urn(ilk, our_address).ink == Wad.from_number(3)
    assert mcd.vat.urn(ilk, our_address).art == Wad.from_number(153)
    assert mcd.vat.dai(our_address) == initial_dai + Rad.from_number(153)
    assert mcd.vat.hope(mcd.dai_adapter.address).transact(from_address=our_address)
    assert mcd.dai_adapter.exit(our_address, Wad.from_number(153)).transact(from_address=our_address)
    assert mcd.dai.balance_of(our_address) == Wad.from_number(153)



def print_out(testName: str):
    print("")
    print(f"{testName}")
    print("")


class TestDsrDemo:

    def test_dsrdemo(self, mcd: DssDeployment, our_address: Address, dsrdemo: DsrDemo):
        print_out("test_dsrdemo")

        create_dai_token(mcd, our_address)
        assert mcd.dai.balance_of(our_address) == Wad.from_number(153)
        dsrdemo.main()
        #assert Wad(153000000000315522920) != Wad(153000000000000000000)
        assert mcd.dai.balance_of(our_address) != Wad.from_number(153)

