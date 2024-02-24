
from datetime import datetime


"""
if __name__ == "__main__":
    app.run()
"""

import json
import os
from os import path


class CID_Storage:
    def __init__(self): #initiate the class
         return

    def add_cid(self, owner: str, cid: str): # add a new cid to the json file of the owner
        if not path.exists(f'{path.curdir}/alljson'):
            os.mkdir(f'{path.curdir}/alljson') 
        filename = f'{path.curdir}/alljson/{owner}.json'
        timestamp = datetime.now().timestamp()  # Get current Unix timestamp

        # Check if file exists
        if path.isfile(filename) is False:#create new json with name of the owner if the file not exist (means streamm just started)
                    with open(filename, 'w') as json_file:json.dump([],json_file, indent=4,  separators=(',',': '))

        with open(filename, 'r') as fp:
            cid_storage = json.load(fp)
        cid_storage.append({ #add new cid to the json with his timestamp
            "timestamp": timestamp,
            "cid": cid,
            })
        with open(filename, 'w') as json_file:json.dump(cid_storage, json_file, indent=4,  separators=(',',': '))
        return

    def push_cid(self, owner: str):#do this when stream ends
        filename = f'{path.curdir}/alljson/{owner}.json'
        # Check if file exists
        if path.isfile(filename) is False: raise Exception("File not found")

        # Push CID to Aleph

        #add agreate location to all  steam in aleph for this owner

        os.remove(filename)#remove json form the disk if was push to aleph
        return