

class graph_engine:
    def __init__(self, data, model, pk):
        self.data = data
        self.primary_key = pk
        self.model = model
        self.predicates = model.predicates
        self.edges = model.edges
        self.reverse_edge = model.reverse_edge
        self.dgraph_type = model.dgraph_type
        self.reverse_graph_type = model.reverse_graph_type
        
        self.result = {}
        self.c_count = 0

    def connect_predicates(self):
        sub = {}
        print("predicates = ", self.predicates, self.data)
        for p in self.predicates:
            if p in self.data:
                self.c_count += 1
                sub.update(
                    {self.dgraph_type+"."+p: self.data.get(p)})
        if self.primary_key:
            sub.update({"uid": self.primary_key})
        return sub

    def connect_edges(self):
        result = {}
        node_edges = {}
        for item in self.edges:
            if item in self.data:
                node_name = self.edges.get(item)
                if type(self.data[item]) == dict:
                    if type(node_name) == set:
                        self.c_count += 1
                        node_edges = {}
                        for edge in node_name:
                            if edge != "uid":
                                node_edges.update({
                                    self.dgraph_type+"."+item+" | "+edge: self.data[item][edge]})
                            else:
                                node_edges.update({
                                    edge: self.data[item][edge]})
                    result.update({
                        self.dgraph_type+"."+item: node_edges

                    })

                elif type(self.data[item]) == list:
                    if type(node_name) == list:
                        uids = []
                        for edge in self.data[item]:
                            uids.append({"uid": edge})
                            self.c_count += 1
                        result.update(
                            {self.dgraph_type+"."+item: uids})
                else:
                    node_edges = {}
                    self.c_count += 1
                    node_edges.update({
                        node_name: self.data[item]})

                    result.update({
                        self.dgraph_type+"."+item: node_edges

                    })
        return result

    def connect_reverse_edge(self) -> dict:
        (item, item_value), = self.reverse_edge.items()
        if item_value in self.data:
            value = self.data[item_value]
            sub = self.connect_predicates()
            sub.update(self.connect_edges())
            return {"uid": value, self.reverse_graph_type+"."+item: sub,
                    "dgraph.type": self.reverse_graph_type
                    }
        else:
            return {}

    def connect(self):
        count = 0
        if any(self.reverse_edge):
            self.result.update(self.connect_reverse_edge())
        else:
            sub = self.connect_predicates()
            sub.update(self.connect_edges())
            self.result.update(sub)
            self.result.update(
                {
                    "dgraph.type": self.dgraph_type
                }
            )

        self.n_counts = count
        return self.result

    def count(self):
        return self.n_counts

    def completeness(self):
        if self.n_counts == len(self.edges)+len(self.predicates):
            return {"is_active": True}
        else:
            return {"is_active": False}
