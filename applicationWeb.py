import json
import pickle
from web3 import Web3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from json import dumps, loads, JSONEncoder, JSONDecoder


app = Flask(__name__)
api = Api(app)

class UnlockAccount(Resource):
    def get(self,account,password):
        tx = web3.personal.unlockAccount(web3.toChecksumAddress(account), password)
        if  tx == True:
           return {'mensagem' :'Conta desbloqueada com sucesso'}, 200
        else:
           return {'mensagem' :'Erro ao desbloquear a Conta'}, 501

class CreateAccount(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("password")
        args = parser.parse_args()
        password = args["password"]
        tx = web3.personal.newAccount(password)
        if tx == None:
            return {'mensagem' :'Erro ao criar Account'}, 201
        else:
            return {'account' : tx}, 200

class Blockchain(Resource):
    
    #GET consulta a ApoliceID e o TransactionID do BlockChain
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("apoliceId")
        parser.add_argument("transactionId")
        args = parser.parse_args()
            
        idApolice = bytes(args["apoliceId"], encoding='utf-8')
        tx_hash = web3.eth.getTransaction(args["transactionId"])
        if tx_hash == None:
            return {'mensagem' :'transactionId invalido'}, 201
        else:
            if ("'blockNumber': null" in tx_hash):
                return {'mensagem' : 'Transacao nao validada no blockchain, aguarde'}, 202
            else:
                return {'mensagem' :'TransactionID validos'}, 200
            
    #POST inclusao da ApoliceID no BlockChain
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        args = parser.parse_args()
        idApolice = bytes(args["id"], encoding='utf-8')
        txn0 = {'gas': 48000}
        tx_hash = contract.functions.incluiApolice(idApolice).transact(txn0)
        retorno = { 
            "transactionId" : web3.toHex(tx_hash)
        }
        return retorno, 201

# Route_1
api.add_resource(Blockchain, '/blockchain') 
api.add_resource(UnlockAccount, '/account/unlock/<string:account>/<string:password>') 
api.add_resource(CreateAccount, '/account/create') 

if __name__ == '__main__':
    
    #Rede Blockchain
    ganache_url = "https://dokiteste2.blockchain.azure.com:3200/OEQQrIa6RDQ8we60GeES0Ofj"
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    #Pega o primeiro Account do BlockChain
    web3.eth.defaultAccount = web3.eth.accounts[0]

    # #Cria o SmartContract
    abi = '''
    [
	{
		"constant": false,
		"inputs": [],
		"name": "apolice",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "apoliceid",
				"type": "bytes32"
			}
		],
		"name": "checkApoliceIdExists",
		"outputs": [
			{
				"name": "success",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"name": "apolices",
		"outputs": [
			{
				"name": "",
				"type": "bytes32"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "apoliceid",
				"type": "bytes32"
			}
		],
		"name": "incluiApolice",
		"outputs": [],
		"payable": true,
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"payable": true,
		"stateMutability": "payable",
		"type": "fallback"
	}
    ]
    '''
    
    address = Web3.toChecksumAddress("0x37ad045e862e2ea1a6e889764a8961ca30e9e22f") 
    contract = web3.eth.contract(address, abi=abi)
    
    app.run(port='5002')