# Dai Savings Rate Python Integration Example

[![Build Status](https://travis-ci.org/makerdao/dsr-pymaker-example.svg?branch=master)](https://travis-ci.org/makerdao/dsr-pymaker-example)
[![codecov](https://codecov.io/gh/makerdao/dsr-pymaker-example/branch/master/graph/badge.svg)](https://codecov.io/gh/makerdao/dsr-pymaker-example)

This code example shows how you can integrate Dai Savings Rate functionality using the Maker Python API: Pymaker.

The `dsr_manager_demo` example uses DsrManager and implements:
* Adding Dai to the DSR
* Retrieving Dai balance in DSR
* Retrieving Dai from the DSR

The `dsr_proxy_demo` example uses a DSProxy and implements:

* Building a user proxy
* Adding Dai to the DSR
* Retrieving Dai balance in DSR
* Retrieving Dai from the DSR

**We reccommend that first time users go through the [DSR Integration Guide](https://github.com/makerdao/developerguides/blob/master/dai/dsr-integration-guide/dsr-integration-guide-01.md) to get an initial understanding of how Dai Savings Rate works.**

## Installation

Prerequisites:
- [Python v3.6.6](https://www.python.org/downloads/release/python-366/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/)
    - This project requires *virtualenv* to be installed if you want to use Maker's python tools. This helps with making sure that you are running the right version of python and checks that all of the pip packages that are installed in the **install.sh** are in the right place and have the right versions.

In order to clone the project and install required third-party packages please execute:
```
git clone https://github.com/makerdao/dsr-pymaker-example
cd dsr-pymaker-example
git submodule update --init --recursive
./install.sh
```

For some known Ubuntu and macOS issues see the [pymaker](https://github.com/makerdao/pymaker) README.

## Usage

### To test on a local testchain

Prerequisites:
* Download [docker and docker-compose](https://www.docker.com/get-started)

This project uses [pytest](https://docs.pytest.org/en/latest/) for unit testing.  Testing of Multi-collateral Dai is
performed on a Dockerized local testchain included in `test\config`.

You can then run the test with:
```
./test.sh
```

### To test on Kovan/Mainnet

Create an executable bash script to easily spin up the demo. Copy the commands below into a new file, and save it as `run-dsr-manager-demo.sh` in the root directory of this repo `dsr-pymaker-example`.

```
#!/bin/bash
/full/path/to/dsr-pymaker-example/bin/dsr-manager-demo \
	--rpc-host 'sample.ParityNode.com' \
	--network 'kovan' \
	--eth-from '0xABCAddress' \
	--eth-key 'key_file=/full/path/to/keystoreFile.json,pass_file=/full/path/to/passphrase/file.txt' \
```

- `--rpc-host` should be set to a local or remote Parity or Geth Ethereum node. Note: Infura nodes will not work.
- `--network` should be set to `kovan` or `mainnet` depending on which Ethereum network you want to use.
- `--eth-from` should be set to the Ethereum public address you want to use for transactions
- `--eth-key` should be set to the private key file and pass phrase for the above public key.

In a terminal navigate to the `dsrdemo` folder and make the script executable by running the following command:
`chmod +x run-dsr-manager-demo.sh`

Start the demo by running the command `./run-dsr-manager-demo.sh` in the `dsr-pymaker-example` folder.

## License

See [COPYING](https://github.com/makerdao/dsr-pymaker-example/blob/master/COPYING) file.


### Disclaimer

YOU (MEANING ANY INDIVIDUAL OR ENTITY ACCESSING, USING OR BOTH THE SOFTWARE INCLUDED IN THIS GITHUB REPOSITORY) EXPRESSLY UNDERSTAND AND AGREE THAT YOUR USE OF THE SOFTWARE IS AT YOUR SOLE RISK.
THE SOFTWARE IN THIS GITHUB REPOSITORY IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
YOU RELEASE AUTHORS OR COPYRIGHT HOLDERS FROM ALL LIABILITY FOR YOU HAVING ACQUIRED OR NOT ACQUIRED CONTENT IN THIS GITHUB REPOSITORY. THE AUTHORS OR COPYRIGHT HOLDERS MAKE NO REPRESENTATIONS CONCERNING ANY CONTENT CONTAINED IN OR ACCESSED THROUGH THE SERVICE, AND THE AUTHORS OR COPYRIGHT HOLDERS WILL NOT BE RESPONSIBLE OR LIABLE FOR THE ACCURACY, COPYRIGHT COMPLIANCE, LEGALITY OR DECENCY OF MATERIAL CONTAINED IN OR ACCESSED THROUGH THIS GITHUB REPOSITORY.
