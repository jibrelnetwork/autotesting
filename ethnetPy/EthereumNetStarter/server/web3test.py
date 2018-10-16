import unittest
import json
import web3

from web3 import Web3, HTTPProvider, TestRPCProvider
# from solc import compile_source
from web3.contract import ConciseContract


class TestWeb3(unittest.TestCase):

    def test_start(self):

        # Solidity source code
        contract_source_code = '''
        pragma solidity ^0.4.0;

        contract Greeter {
            string public greeting;

            function Greeter() {
                greeting = 'Hello';
            }

            function setGreeting(string _greeting) public {
                greeting = _greeting;
            }

            function greet() constant returns (string) {
                return greeting;
            }
        }
        '''

        # compiled_sol = compile_source(contract_source_code)  # Compiled source code
        # contract_interface = compiled_sol['<stdin>:Greeter']

        # web3.py instance
        w3 = Web3(Web3.HTTPProvider("https://127.0.0.1:8545"))#Web3(TestRPCProvider())

        print(w3.eth.accounts)

        # Instantiate and deploy contract
        # contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

        # Get transaction hash from deployed contract
        # tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0], 'gas': 410000})

        # Get tx receipt to get contract address
        # tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        # contract_address = tx_receipt['contractAddress']

        # Contract instance in concise mode
        # abi = contract_interface['abi']
        # contract_instance = w3.eth.contract(address=contract_address, abi=abi, ContractFactoryClass=ConciseContract)

        # Getters + Setters for web3.eth.contract object
        # print('Contract value: {}'.format(contract_instance.greet()))
        # contract_instance.setGreeting('Nihao', transact={'from': w3.eth.accounts[0]})
        # print('Setting value to: Nihao')
        # print('Contract value: {}'.format(contract_instance.greet()))

        encrypted_key = "{\"version\":3,\"id\":\"e2d652a0-925c-40c1-aec7-592256173bae\",\"crypto\":{\"ciphertext\":\"ca7fbd2299544eab02b9f741294cae0bb3107587eef739d0203b68b7a746d613\",\"cipherparams\":{\"iv\":\"19b22f7ed837e803fdf042d8bb5f0dfe\"},\"kdf\":\"scrypt\",\"kdfparams\":{\"r\":6,\"p\":1,\"n\":4096,\"dklen\":32,\"salt\":\"c7371c13ef0cfd8f1424891271af8074cea712b781ac1a029764b6196b5ddcc5\"},\"mac\":\"16a93e10cf2e60c54fc3e5d98708db75ef425f8b224467aff6b1cbd73e11c2d1\",\"cipher\":\"aes-128-cbc\"},\"address\":\"0xe28b2dce91ee5ca57e54118b45671df6b79ade22\"}"
        private_key = w3.eth.account.decrypt(encrypted_key, '123') # HexBytes('0x68c76a938329b434347df8d87ff80bad44a26d1ab4751ee50b8dc96d5893934a')

        transaction = {'from': '', to': '0x94bC92C22045149B2D43C006B95fED326b2cE964', 'value': 1000000000, 'gas': 2000000, 'gasPrice': 234567897654321, 'nonce': 0, 'chainId': 1}
        signed = w3.eth.account.signTransaction(transaction, private_key)
        w3.eth.sendRawTransaction(signed.rawTransaction)

if __name__ == '__main__':
    unittest.main()