from .base.graph_models  import GraphModel

class Specification(GraphModel):
     
    predicates = [
        "service_name",
        "service_description",
        "service_function",
        "service_criteria"
    ]
    edges = {
        "service_status_dependancy": ["uid"],
        "service_dependancy": ["uid"],
        "service_tasks": ["uid"],
    }
    dgraph_type = "Services"