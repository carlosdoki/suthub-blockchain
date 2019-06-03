import json
from web3 import Web3
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from json import dumps

app = Flask(__name__)
api = Api(app)

class Blockchain(Resource):
    
    #GET consulta a ApoliceID e o TransactionID do BlockChain
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("apoliceId")
        parser.add_argument("transactionId")
        args = parser.parse_args()
            
        idApolice = bytes(args["apoliceId"], encoding='utf-8')
        if (contract.functions.checkApoliceIdExists(idApolice).call()):
            tx_hash = web3.eth.getTransaction(args["transactionId"])
            if tx_hash == None:
                return {'mensagem' :'transactionId invalido'}, 201
            else:
                return {'mensagem' :'Apolice ja cadastrada'}, 200
        else:
            return {'mensagem' :'Apolice nao encontrada'}, 404
            
    #POST inclusao da ApoliceID no BlockChain
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        args = parser.parse_args()
        idApolice = bytes(args["id"], encoding='utf-8')
        if (contract.functions.checkApoliceIdExists(idApolice).call() == False):
            tx_hash = contract.functions.incluiApolice(idApolice).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            retorno = { 
                "transactionId" : web3.toHex(tx_hash)
            }
            return retorno, 201
        else:
            return {'mensagem' :'Apolice ja cadastrada'}, 400


# Route_1
api.add_resource(Blockchain, '/blockchain') 

if __name__ == '__main__':
    
    #Rede Blockchain
    ganache_url = "HTTP://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    #Pega o primeiro Account do BlockChain
    web3.eth.defaultAccount = web3.eth.accounts[0]

    #Cria o SmartContract
    abi = json.loads('[{"constant":false,"inputs":[],"name":"kill","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"apoliceid","type":"bytes32"}],"name":"checkApoliceIdExists","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"apolices","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"apoliceid","type":"bytes32"}],"name":"incluiApolice","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"}]')
    bytecode = "6060604052341561000f57600080fd5b336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506103718061005e6000396000f30060606040526004361061006d576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806341c0e1b51461006f5780636537dc2b146100845780638da5cb5b146100c3578063906b749d14610118578063e7144e9014610157575b005b341561007a57600080fd5b610082610173565b005b341561008f57600080fd5b6100a9600480803560001916906020019091905050610204565b604051808215151515815260200191505060405180910390f35b34156100ce57600080fd5b6100d6610264565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b341561012357600080fd5b6101396004808035906020019091905050610289565b60405180826000191660001916815260200191505060405180910390f35b6101716004808035600019169060200190919050506102ad565b005b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161415610202576000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16ff5b565b600080600090505b60018054905081101561025957826000191660018281548110151561022d57fe5b90600052602060002090015460001916141561024c576001915061025e565b808060010191505061020c565b600091505b50919050565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60018181548110151561029857fe5b90600052602060002090016000915090505481565b6102b681610204565b1515156102c257600080fd5b600180548060010182816102d691906102f4565b91600052602060002090016000839091909150906000191690555050565b81548183558181151161031b5781836000526020600020918201910161031a9190610320565b5b505050565b61034291905b8082111561033e576000816000905550600101610326565b5090565b905600a165627a7a723058204e8c9ea30147612fed3f9da0cd7afa764389ef725f5e44caeb5c9f7cce97ef9a0029"
    Apolice = web3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = Apolice.constructor().transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    contract = web3.eth.contract(
        address = tx_receipt.contractAddress,
        abi=abi
    )
    
    #Porta do WebService
    app.run(port='5002')