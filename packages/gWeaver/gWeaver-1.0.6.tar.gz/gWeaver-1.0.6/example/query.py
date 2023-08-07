import json
from gWeaver.base.graph_query import dgraph_query
import pydgraph
import time


class serviceQuery(dgraph_query):

    client = pydgraph.DgraphClient(
            pydgraph.DgraphClientStub('localhost:9080'))
    
    def __init__(self):
        self.client = pydgraph.DgraphClient(
            pydgraph.DgraphClientStub('localhost:9080'))
        

    def all(self, *args, **kwargs):
        client = pydgraph.DgraphClient(
            pydgraph.DgraphClientStub('localhost:9080'))
        query = """
            {
            Services(func: has(Services.name)) @normalize{
            id : uid
            type: Services.type
            name: Services.name
            description: Services.description
            function: Services.function
            criteria: Services.criteria
            }}"""

        res = client.txn(read_only=True).query(query)
        res = json.loads(res.json)
        print(res)
        return res

    def get(self, service_id):

        query = """
            {
            Services (func: uid("""+service_id+"""))  @normalize{
            service_id : uid
            service_type: Services.service_type
            service_name: Services.service_name
            service_description: Services.service_description
            service_function: Services.service_function
            service_criteria: Services.service_criteria
            service_status_dependency: Services.service_status_dependency
            service_dependency: Services.service_dependency
            service_tasks: Services.service_tasks {
                task_id : uid
                task_name: Tasks.task_name
            }
            created_on:Services.created_on
            modified_on:Services.modified_on
            modified_by:Services.modified_by
            created_by:Services.created_by
            }}"""

        res = self.client.txn(read_only=True).query(query)
        service = json.loads(res.json)
        return service

    def create(self, data):
        return self.create_data(data)

    def delete(self, item, source):
        print("delete function uid is ", item)
        query1 = ""
        query2 = """
                uid
                dgraph.type
                Services.service_id
                Services.service_name
                Services.service_description
                Services.service_function
                Services.service_criteria
                Services.service_status_dependency
                Services.service_dependency
                Services.service_tasks
                Services.created_on
                Services.modified_on
                Services.is_active
                Services.modified_by
                Services.created_by
                
                    }
                }"""
        for c, i in enumerate(item):
            if c == 0:
                query1 += "{all(func: uid("+i+")) {"+query2
            else:
                query1 += ",{all"+str(c)+"(func: uid("+i+")) {"+query2

        print(query1)
        res1 = self.client.txn(read_only=True).query(query1)
        ppl1 = json.loads(res1.json)
        print(ppl1)

        for i in ppl1:
            try:
                txn = self.client.txn()
                if len(ppl1[i][0]["Services.service_name"]) > 1:
                    print("delete condition", ppl1[i][0])
                    # q3+=ppl1[i][0]

                    txn.mutate(del_obj=ppl1[i][0])
                    txn.commit()
            except:
                pass
