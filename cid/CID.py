
from datetime import datetime
from aleph_client.synchronous import create_aggregate


import json
import os
from os import path

from aleph.sdk.chains.ethereum import ETHAccount

def load_config():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config

config = load_config()


account = ETHAccount(private_key=bytes.fromhex(config["private_key"]))

def send_aggregate_aleph(key : str, dict, channel):
    return create_aggregate(account, key, dict , channel)



class CID_Storage:
    def __init__(self): #initiate the class
         return

    def add_cid(self, owner: str, cid: str): # add a new cid to the json file of the owner
        if not path.exists(f'{path.curdir}/alljson'):
            os.mkdir(f'{path.curdir}/alljson') 
        filename = f'{path.curdir}/alljson/{owner}.json'
        timestamp = datetime.now().timestamp()  # Get current Unix timestamp

        # Check if file exists
        if path.isfile(filename):
            with open(filename, 'r') as fp:
                cid_storage = json.load(fp)
        else:
            cid_storage = {}
        cid_storage[timestamp] = cid
        with open(f'alljson/{owner}.json', 'w') as f:
         # Écriture de la structure de données dans le fichier en format JSON
            json.dump(cid_storage, f, indent=4)
        return

    def push_cid(self, owner: str):#do this every 5 min for rediffusion 
        filename = f'{path.curdir}/alljson/{owner}.json'
        # Check if file exists
        if path.isfile(filename) is False: raise Exception("File not found")

        # Push CID to Aleph
        with open(filename, 'r') as fp:
            cid_storage = json.load(fp)
        send_aggregate_aleph(account, owner+"@"+next(iter(cid_storage))  , cid_storage , owner) # next(iter(cid_storage)) == get first element
        return
    
    def push_cid_and_delete(self, owner: str):#do this when streamer stop live
        self.push_cid(owner)
        filename = f'{path.curdir}/alljson/{owner}.json'
        os.remove(filename)#remove json form the disk if was push to aleph
        return