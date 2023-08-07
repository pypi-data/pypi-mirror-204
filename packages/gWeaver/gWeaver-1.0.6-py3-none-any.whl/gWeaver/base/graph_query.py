from typing import Any
import json



import pydgraph
import time


class dgraph_query:
    def __init__(self):
        self.client = pydgraph.DgraphClient(
            pydgraph.DgraphClientStub('localhost:9080'))
            

    def get_client(self):
        return self.client

    def read_data(self, query):
        # Create a new transaction.
        return self.client.txn(read_only=True).query(query)

    def create_data(self, data):
        # Create a new transaction.
        txn = self.client.txn()
        try:
            response = txn.mutate(set_obj=data)
            uid = response.uids
            txn.commit()
            print("Created data with uid = {}".format(uid))
            try:
                uid = list(uid.values())[0]
            except:
                pass
            return uid

        finally:
            txn.discard()

    def delete_data(self, data):
        deletetxn = self.client.txn()
        deletetxn.mutate(del_obj=data)
        deletetxn.commit()



