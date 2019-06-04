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
        print(contract.call().checkApoliceIdExists(idApolice))
        if (contract.functions.checkApoliceIdExists(idApolice).call()):
            tx_hash = web3.eth.getTransaction(args["transactionId"])
            if tx_hash == None:
                return {'mensagem' :'transactionId invalido'}, 201
            else:
                return {'mensagem' :'Apolice e TransactionID validos'}, 200
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
    ganache_url = "HTTP://127.0.0.1:8545"
    #ganache_url ='http://52.234.224.83:8555/sandbox/b45e30bf12'
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    #Pega o primeiro Account do BlockChain
    web3.eth.defaultAccount = web3.eth.accounts[0]

    # #Cria o SmartContract
    abi = json.loads('[{"constant":false,"inputs":[],"name":"apolice","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"apoliceid","type":"bytes32"}],"name":"checkApoliceIdExists","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"apolices","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"apoliceid","type":"bytes32"}],"name":"incluiApolice","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"}]')
    bytecode = "608060405234801561001057600080fd5b506102df806100206000396000f3fe60806040526004361061004a5760003560e01c806364dd881b1461004c5780636537dc2b146100635780638da5cb5b146100b6578063906b749d1461010d578063e7144e901461015c575b005b34801561005857600080fd5b5061006161018a565b005b34801561006f57600080fd5b5061009c6004803603602081101561008657600080fd5b81019080803590602001909291905050506101cc565b604051808215151515815260200191505060405180910390f35b3480156100c257600080fd5b506100cb610222565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34801561011957600080fd5b506101466004803603602081101561013057600080fd5b8101908080359060200190929190505050610247565b6040518082815260200191505060405180910390f35b6101886004803603602081101561017257600080fd5b8101908080359060200190929190505050610268565b005b336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550565b600080600090505b6001805490508110156102175782600182815481106101ef57fe5b9060005260206000200154141561020a57600191505061021d565b80806001019150506101d4565b50600090505b919050565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6001818154811061025457fe5b906000526020600020016000915090505481565b610271816101cc565b1561027b57600080fd5b60018190806001815401808255809150509060018203906000526020600020016000909192909190915055505056fea265627a7a7230582029b13ed9eba0cc43764dce594144d00a07b11b62b48aafd12717266881c5e98564736f6c63430005090032"
    Greeter = web3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = Greeter.constructor().transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    contract = web3.eth.contract(
        # address = Web3.toChecksumAddress("0x17956ba5f4291844bc25aedb27e69bc11b5bda39"),
        address = tx_receipt.contractAddress,
        abi=abi
    )
    
    #Porta do WebService
    app.run(port='5002')