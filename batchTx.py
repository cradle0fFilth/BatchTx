from web3 import Web3
from dotenv import load_dotenv
import os
import requests

#load env
load_dotenv()
rpc = os.getenv('rpc')
private_key = os.getenv('private_key')
chain_Id = os.getenv('chain_Id')
my_address = Web3.to_checksum_address(os.getenv('my_address'))
to_address = Web3.to_checksum_address(os.getenv('to_address'))
num_transactions = int(os.getenv('num_transactions'))

def send_batch_transaction(params):
    batch = []
    id = 0
    for p in params:
        batch.append(
            {
                "jsonrpc": "2.0",
                "method": "eth_sendRawTransaction",
                "params":[p],
                "id":id,
            }
        )
        id += 1
    for transaction in batch:
        print(transaction)
    return requests.post(url=rpc,json=batch if id>1 else batch[0]).json()

def sign_transaction(
        my_address,to_address,nonce,private_key,web3,value=0,gas=30000,gas_price=5
):
    tx = {
        "from":my_address,
        "to": to_address,
        "nonce":nonce,
        "value":Web3.to_wei(value,"ether"),
        "gas":gas,
        "gasPrice":Web3.to_wei(gas_price,"gwei"),
        "data":"0x646174613a2c7b2270223a226273632d3230222c226f70223a226d696e74222c227469636b223a22736f6669222c22616d74223a2234227d",
        "chainId":chain_Id,
    }
    try:
        signed_tx = web3.eth.account.sign_transaction(tx,private_key)
    except Exception as e:
        print(f"sign Error:{e}")
    return signed_tx.rawTransaction.hex()

def my_function():
    signed_txs = [] 
    web3 = Web3(Web3.HTTPProvider(rpc))
    start_nonce = web3.eth.get_transaction_count(my_address)
    print(f"Connected to Ethereum: {web3.is_connected()}")
    print(f"Balance: {Web3.from_wei(web3.eth.get_balance(my_address), 'ether')}")
    for i in range(num_transactions):
        signed_tx = sign_transaction(my_address=my_address,to_address=to_address,nonce=start_nonce,private_key=private_key,web3=web3)
        print(signed_tx)
        signed_txs.append(signed_tx)
        start_nonce+=1
        print(signed_txs[i])
    try:
        response = send_batch_transaction(signed_txs)
        # print response
        print(response)
    except Exception as e:
        print(f"Post Error:{e}")

if __name__=="__main__":
    print("start:")
    my_function()
