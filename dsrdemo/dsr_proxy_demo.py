import argparse
import logging
import sys
import time

from web3 import Web3, HTTPProvider
from pymaker import Address, Transact, Calldata
from pymaker.numeric import Wad, Ray, Rad
from pymaker.proxy import DSProxy
from pymaker.deployment import DssDeployment
from pymaker.dsr import Dsr
from pymaker.keys import register_keys
from pymaker.lifecycle import Lifecycle


class DsrProxyDemo:
    """ DSR Python Integration Example using DSProxy
    """
    # _DAI_AMOUNT is the amount of Dai we are adding to the DSR in this demo. Set to 1 Dai as standard.
    _DAI_AMOUNT = Wad.from_number(1)
    _USER_PROXY = None

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
        self.dsr = Dsr(self.dss, self.our_address)


    def main(self):
        # Checking if the user has a DS-Proxy - if not, we build one.
        if self.dsr.has_proxy() == False:
            print("No DS-Proxy found - Building new proxy...")
            self.dsr.build_proxy().transact()
            print("Built new proxy at: " + self.dsr.get_proxy().address.address)

        if self.dsr.has_proxy() == True:
            self._USER_PROXY = self.dsr.get_proxy()
            print("Existing DS-Proxy found at: " + self.dsr.get_proxy().address.address)

        # Saving the User Proxy in a variable
        self._USER_PROXY = self.dsr.get_proxy()

        # Saving the initial Dai balance of the user for calculations further down
        self.initialDaiBalance = self.dsr.mcd.dai.balance_of(self.our_address)

        # Approving the DS-Proxy to move Dai from our wallet to the DSR
        self.approve()
        print("Approved DS-Proxy to spend Dai")

        # Adding Dai to the DSR - Amount specified nby _DAI_AMOUNT variable.
        self.addDaiToDsr()
        print(f"Added      {self._DAI_AMOUNT} Dai to DSR")

        # Calculating the balance of our Dai in DSR.
        self.DsrBalance = self.dsr.get_balance(self._USER_PROXY.address)

        # Note: if the DSR is 0%, the resulting Dai balance may be 1 wei less
        # than what deposited (due to rounding)
        print(f"Wait 1 minute for Dai to accrue DSR proceeds")
        time.sleep(60)

        # Retrieving all Dai from DSR.
        self.exitAllDaiFromDsr()

        # Calculating how much Dai you have earned, by checking the difference between the initial and final Dai balance
        self.finalDaiBalance = self.dsr.mcd.dai.balance_of(self.our_address)
        self.balanceDifference = self.finalDaiBalance - self.initialDaiBalance

        print(f"Retrieved  {self.balanceDifference + self._DAI_AMOUNT} Dai from DSR") # We are adding the amount of Dai you added to DSR to get the full amount retrieved.
        print(f"You earned {self.balanceDifference} Dai")

    def approve(self):
        self.dsr.mcd.dai.approve(self._USER_PROXY.address).transact()

    def addDaiToDsr(self):
        self.dsr.join(self._DAI_AMOUNT, self._USER_PROXY).transact()

    def exitDaiFromDsr(self, dai: Wad):
        self.dsr.exit(dai, self._USER_PROXY).transact()

    def exitAllDaiFromDsr(self):
        self.dsr.exit_all(self._USER_PROXY).transact()

if __name__ == '__main__':
    DsrProxyDemo(sys.argv[1:]).main()
