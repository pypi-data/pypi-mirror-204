from ..managers.client import dgraph_client
import os
from django.apps import apps
from django.conf import settings

import pydgraph


# client = dgraph_client().get_client()

class SchemaGenerator:
    def __init__(self, graph_models: object) -> None:
        self.graph_models = graph_models
        self.schema = ""
        self.client = dgraph_client().get_client()
    

    

    def generate_dgraph_schema(self):
        schema = ""
        for app_config in apps.get_app_configs():
            app_name = app_config.name
            excludes_apps = [
                "django.contrib.admin",
                "django.contrib.auth",
                "django.contrib.contenttypes",
                "django.contrib.sessions",
                "django.contrib.messages",
                "django.contrib.staticfiles",

            ]
            if app_name in excludes_apps:
                continue
            graph_model_path = f"{settings.BASE_DIR}/{app_name}/graph_models.py"
            if os.path.exists(graph_model_path):
                with open(graph_model_path, "r") as f:
                    model_content = f.read()
                    code = compile(model_content, graph_model_path, "exec")
                    namespace = {}
                    exec(code, {"__name__": f"{app_name}.graph_model"}, namespace)
                    print(namespace)
                    for graph_model_class in namespace.values():
                        if graph_model_class.__name__ == "GraphModel":
                            continue
                        for predicate in graph_model_class.predicates:
                            
                            schema += f"{graph_model_class.dgraph_type}.{predicate}: string .\n"
                        for edge_name, edge_type in graph_model_class.edges.items():
                            if isinstance(edge_type, list):
                                edge_type = str(edge_type).replace("'", "")
                            schema += f"{graph_model_class.dgraph_type}.{edge_name}: {edge_type} @reverse .\n"
                        schema += f"type {graph_model_class.dgraph_type} {{\n"
                        for predicate in graph_model_class.predicates:
                            schema += f"\t{graph_model_class.dgraph_type}.{predicate}\n"
                        for edge_name, edge_type in graph_model_class.edges.items():
                            schema += f"\t{graph_model_class.dgraph_type}.{edge_name}\n"
                        for reverse_edge_name, reverse_edge_type in graph_model_class.reverse_edge.items():
                            schema += f"\t{graph_model_class.dgraph_type}.{reverse_edge_name}\n"
                        for reverse_graph_type_name, reverse_graph_type_type in graph_model_class.reverse_graph_type.items():
                            schema += f"\t{graph_model_class.dgraph_type}.{reverse_graph_type_name}\n"
                        schema += "}\n\n"
        return schema
    
    def post_to_dgraph(self):
        schema = self.generate_dgraph_schema()
        op = pydgraph.Operation(schema=schema, run_in_background=True)
        self.client.alter(op)





        







