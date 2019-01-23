import unittest
from web3 import Web3
from solc import compile_source  # pip install py-solc
from web3.contract import ConciseContract

class TestWeb3(unittest.TestCase):

    def test_start(self):

        # Solidity source code
        contract_source_code = '''
        pragma solidity ^0.4.21;

        contract Greeter {
            string public greeting;

            function Greeter() public {
                greeting = 'Hello';
            }

            function setGreeting(string _greeting) public {
                greeting = _greeting;
            }

            function greet() view public returns (string) {
                return greeting;
            }
        }
        '''

        compiled_sol = compile_source(contract_source_code) # Compiled source code
        contract_interface = compiled_sol['<stdin>:Greeter']

        w3 = Web3(Web3.HTTPProvider("http://0.0.0.0:8545"))

        sender = '0x7aBEf471f4dF93938781BfDb681e053510Ba417A'
        encrypted_key = "{\"version\":3,\"id\":\"e2d652a0-925c-40c1-aec7-592256173bae\",\"crypto\":{\"ciphertext\":\"ca7fbd2299544eab02b9f741294cae0bb3107587eef739d0203b68b7a746d613\",\"cipherparams\":{\"iv\":\"19b22f7ed837e803fdf042d8bb5f0dfe\"},\"kdf\":\"scrypt\",\"kdfparams\":{\"r\":6,\"p\":1,\"n\":4096,\"dklen\":32,\"salt\":\"c7371c13ef0cfd8f1424891271af8074cea712b781ac1a029764b6196b5ddcc5\"},\"mac\":\"16a93e10cf2e60c54fc3e5d98708db75ef425f8b224467aff6b1cbd73e11c2d1\",\"cipher\":\"aes-128-cbc\"},\"address\":\"0xe28b2dce91ee5ca57e54118b45671df6b79ade22\"}"
        private_key = w3.eth.account.decrypt(encrypted_key, '123')  # HexBytes('0x68c76a938329b434347df8d87ff80bad44a26d1ab4751ee50b8dc96d5893934a')
        w3.eth.defaultAccount = w3.eth.accounts[0]
        w3.personal.unlockAccount(w3.eth.accounts[0], "123")

        # Instantiate and deploy contract
        Greeter = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

        transaction = {
            'from': sender,
            'gasPrice': w3.eth.gasPrice,
            'nonce': w3.eth.getTransactionCount(sender),
            'gas': 500000,
            'chainId': None
        }
        contract_tx = Greeter.constructor().buildTransaction(transaction)
        signed_ctx = w3.eth.account.signTransaction(contract_tx, private_key)



        # Submit the transaction that deploys the contract
        # tx_hash = Greeter.constructor().transact()
        # Wait for the transaction to be mined, and get the transaction receipt

        tx_hash = w3.eth.sendRawTransaction(signed_ctx.rawTransaction)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        # Create the contract instance with the newly-deployed address
        greeter = w3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=contract_interface['abi'],
        )

        # Display the default greeting from the contract
        print('Default contract greeting: {}'.format(
            greeter.functions.greet().call()
        ))

        print('Setting the greeting to Nihao...')
        tx_hash = greeter.functions.setGreeting('Nihao').transact()

        # Wait for transaction to be mined...
        w3.eth.waitForTransactionReceipt(tx_hash)

        # Display the new greeting value
        print('Updated contract greeting: {}'.format(
            greeter.functions.greet().call()
        ))

        # When issuing a lot of reads, try this more concise reader:
        reader = ConciseContract(greeter)
        assert reader.greet() == "Nihao"


        receiver = '0x94bC92C22045149B2D43C006B95fED326b2cE964'
        transaction = {'from': sender, 'to': receiver, 'value': 5000000000000000000, 'gas': 21000, 'gasPrice': 20000000000, 'nonce': w3.eth.getTransactionCount(sender)}
        signed = w3.eth.account.signTransaction(transaction, private_key)
        w3.eth.sendRawTransaction(signed.rawTransaction)

if __name__ == '__main__':
    unittest.main()