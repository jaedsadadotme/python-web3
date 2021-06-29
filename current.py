import json
from web3 import Web3

web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
BUSD = web3.toChecksumAddress('0xe9e7cea3dedca5984780bafc599bd69add087d56')
WBNB = web3.toChecksumAddress('0x844fa82f1e54824655470970f7004dd90546bb28')
InputTokenAddr = BUSD
OutputTokenAddr = WBNB

pancake_factory_address = web3.toChecksumAddress('0x4e66fda7820c53c1a2f601f84918c375205eac3e')

with open('contract/factory.json', 'r') as abi_definition:
 abi = json.load(abi_definition)

with open('contract/pair.json', 'r') as abi_definition:
 parsed_pair = json.load(abi_definition)

contract        = web3.eth.contract(address=pancake_factory_address, abi=abi)
pair_address    = contract.functions.getPair(InputTokenAddr,OutputTokenAddr).call()
pair1           = web3.eth.contract(abi=parsed_pair, address=pair_address)
reserves = pair1.functions.getReserves().call()
reserve0 = reserves[0]
reserve1 = reserves[1]

print(f'current price is : ${reserve1/reserve0}')