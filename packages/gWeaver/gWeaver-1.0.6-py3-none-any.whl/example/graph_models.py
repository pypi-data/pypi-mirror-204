from gWeaver.base.base_models  import GraphModel

class serviceModel(GraphModel):
     
    predicates = [
        "name",
        "description",
        "function",
        "criteria"
    ]
    edges = {
        "status_dependancy": ["uid"],
        "dependancy": ["uid"],
        "tasks": ["uid"],
    }
    dgraph_type = "Services"
    primary_key = "uid"
