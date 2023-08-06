from ..managers.client import dgraph_client


# client = dgraph_client().get_client()

class SchemaGenerator:
    def __init__(self, graph_models: list) -> None:
        self.graph_models = graph_models
        self.schema = ""

    def generate_schema(self) -> str:
        self.schema = "\n".join([
            f"dgraph.type:{model.dgraph_type}\t"
            + "\t".join(f"{predicate}:string" for predicate in model.predicates)
            + "\t"
            + "\t".join(f"{edge}:uid" if type(edge_type) != list else f"{edge}:[uid]" for edge, edge_type in model.edges.items())
            for model in self.graph_models
        ])
        return self.schema
    
    def get_schema(self):
        return ""
    
    def post_schema(self, client):
        self.generate_schema()
        print(self.schema)
        # client.alter(self.schema)


class GraphModel:
    predicates = []
    edges = {}
    reverse_edge = {}
    reverse_graph_type = {}
    dgraph_type = ""



