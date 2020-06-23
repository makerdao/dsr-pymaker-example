import argparse
import logging
import sys
import time

from web3 import Web3, HTTPProvider
from pymaker import Address, Transact, Calldata
from pymaker.numeric import Wad, Ray, Rad
from pymaker.deployment import DssDeployment
from pymaker.dsrmanager import DsrManager
from pymaker.keys import register_keys
from pymaker.lifecycle import Lifecycle


class DsrManagerDemo:
    """ DSR Python Integration Example using dsr-manager
    """


    def __init__(self, args, **kwargs):
        parser = argparse.ArgumentParser("dsrdemo")

        parser.add_argument("--eth-from", type=str, required=True,
                                help="Ethereum address from which to send transactions; checksummed (e.g. '0x12AebC')")

        parser.add_argument("--rpc-host", type=str, default="localhost",
                                help="JSON-RPC host (default: `localhost')")

        parser.add_argument("--network", type=str, required=True,
                            help="Network that you're running the Keeper on (options, 'mainnet', 'kovan', 'testnet')")

        parser.add_argument("--rpc-port", type=int, default=8545,
                                help="JSON-RPC port (default: `8545')")

        parser.add_argument("--rpc-timeout", type=int, default=10,
                                help="JSON-RPC timeout (in seconds, default: 10)")

        parser.add_argument("--eth-key", type=str, nargs='*',
                                help="Ethereum private key(s) to use (e.g. 'key_file=/path/to/keystore.json,pass_file=/path/to/passphrase.txt')")
        self.arguments = parser.parse_args(args)

        self.web3 = kwargs['web3'] if 'web3' in kwargs else Web3(HTTPProvider(endpoint_uri=f"https://{self.arguments.rpc_host}:{self.arguments.rpc_port}",
                                                                                request_kwargs={"timeout": self.arguments.rpc_timeout}))
        self.web3.eth.defaultAccount = self.arguments.eth_from
        register_keys(self.web3, self.arguments.eth_key)
        self.our_address = Address(self.arguments.eth_from)

        # Instantiate the dss and dsr classes
        self.dss = DssDeployment.from_network(web3=self.web3, network=self.arguments.network)


    def main(self):

        # Assuming that our_address has at least 1 ERC20 Dai in its posession
        dai = Wad.from_number(20)

        # Saving the initial Dai balance of the user for calculations further down
        initialDaiBalance = self.dss.dai.balance_of(self.our_address)

        # Approving the DsrManager to move Dai from our wallet to the DSR
        self.dss.dai.approve(self.dss.dsr_manager.address).transact(from_address=self.our_address)
        print(f"Approved DsrManager to take {dai} Dai")

        # Adding Dai to the DSR - Amount specified the dai variable.
        self.dss.dsr_manager.join(self.our_address, dai).transact(from_address=self.our_address)
        print(f"Added {dai} Dai to DSR")

        # Calculating the balance of our Dai in DSR
        daiBalance = self.dss.dsr_manager.dai_of(self.our_address)
        print(f"Dai Balance in the DSR: {daiBalance}")

        # Note: if the DSR is 0%, the resulting Dai balance may be 1 wei less
        # than what deposited (due to rounding)
        print(f"Wait 1 minute for Dai to accrue some DSR proceeds")
        time.sleep(60)

        # Retrieving all Dai from DSR. For exiting a specific amount, use self.dss.dsr_manager.exit()
        assert self.dss.dsr_manager.exitAll(self.our_address).transact(from_address=self.our_address)

        # Calculating how much Dai you have earned, by checking the difference between the initial and final Dai balance
        finalDaiBalance = self.dss.dai.balance_of(self.our_address)
        balanceDifference = finalDaiBalance - initialDaiBalance

        print(f"Retrieved  {balanceDifference + dai} Dai from DSR") # We are adding the amount of Dai you added to DSR to get the full amount retrieved.
        print(f"You earned {balanceDifference} Dai")


if __name__ == '__main__':
    DsrManagerDemo(sys.argv[1:]).main()
