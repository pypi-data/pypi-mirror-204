
import pydgraph
import time


class dgraph_client:
    def __init__(self):
        try:
            self.client = pydgraph.DgraphClient(
                pydgraph.DgraphClientStub('localhost:9080'))
        except:
            raise Exception("Dgraph server not running")

    def get_client(self):
        return self.client

    def read_data(self, query):
        # Create a new transaction.
        return self.client.txn(read_only=True).query(query)

    def create_data(self, p):
        # Create a new transaction.
        txn = self.client.txn()
        try:
            response = txn.mutate(set_obj=p)
            uid = response.uids
            txn.commit()
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
