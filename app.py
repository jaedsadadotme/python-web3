import json
import requests
from datetime import datetime
from pytz import timezone
from web3 import Web3

web3    = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
wallet = "<token_address>"


with open('contract/Exchange.json', 'r') as exchage_definition:
 exchage = json.load(exchage_definition)

with open('contract/ABI.json', 'r') as fac_definition:
 factory = json.load(fac_definition)

with open('contract/Token.json', 'r') as token_definition:
 token = json.load(token_definition)

with open('contract/DOP.json', 'r') as abi_definition:
 abi = json.load(abi_definition)

address     = abi['Dopple']['Pool']['DiamondHands']['address']
abi         = abi['Dopple']['Pool']['DiamondHands']['ABI']

BUSD    = web3.toChecksumAddress(token['BUSD'])
DOP     = web3.toChecksumAddress(token['DOP'])
Twin     = web3.toChecksumAddress(token['TWIN'])

factory_address = exchage["Twindex"]["Factory"]
factory_abi = factory["Factory"]
factory_pair    = factory["Pairs"]


def getDopPrice(factory_address,factory_abi,factory_pair,InputTokenAddr,OutputTokenAddr) :
    web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
    pancake_factory_address = web3.toChecksumAddress(factory_address)
    contract        = web3.eth.contract(address=pancake_factory_address, abi=factory_abi)
    pair_address    = contract.functions.getPair(InputTokenAddr,OutputTokenAddr).call()
    pair1           = web3.eth.contract(abi=factory_pair, address=pair_address)
    reserves = pair1.functions.getReserves().call()
    reserve0 = reserves[0]
    reserve1 = reserves[1]

    return f'${reserve1/reserve0}'

def getTwinPrice(factory_address,factory_abi,factory_pair,InputTokenAddr,OutputTokenAddr) :
    web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
    pancake_factory_address = web3.toChecksumAddress(factory_address)
    contract        = web3.eth.contract(address=pancake_factory_address, abi=factory_abi)
    pair_address    = contract.functions.getPair(InputTokenAddr,OutputTokenAddr).call()
    pair1           = web3.eth.contract(abi=factory_pair, address=pair_address)
    reserves = pair1.functions.getReserves().call()
    reserve0 = reserves[0]
    reserve1 = reserves[1]

    return f'${reserve1/reserve0}'

def getDiamonHand(abi , address) : 
    contract        = web3.eth.contract( abi=abi, address=web3.toChecksumAddress(address) )
    balance         = contract.functions.userInfo(wallet).call()
    reward          = web3.fromWei( contract.functions.pendingReward(wallet).call(), "ether" )
    return str(reward)
    
dopReward   = getDiamonHand(abi,address)
dopPrice    = getDopPrice(factory_address,factory_abi,factory_pair,BUSD,DOP)
twinPrice   = getTwinPrice(factory_address,factory_abi,factory_pair,BUSD,Twin)

## bot
text = """
{}
**************************
Price
dop price   => {}
twin price  => {}
---
Reward
dop reward  => {} DOP
**************************
""".format(
        datetime.now(timezone('Asia/Bangkok')).strftime("%d/%m/%Y %H:%M:%S"),
        dopPrice,
        twinPrice,
        dopReward
    )


print(text)