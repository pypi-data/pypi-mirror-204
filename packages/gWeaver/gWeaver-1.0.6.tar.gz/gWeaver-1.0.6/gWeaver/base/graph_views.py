
from typing import Any
from rest_framework.views import APIView
from .graph_actions import graph_actions



class GraphView(APIView):
    action = None

    def __init__(self,*args, **kwargs) -> None:
        self.actions = graph_actions(self.action)
        super().__init__(**kwargs)
    

    def get(self, *args, **kwargs):
        return self.actions.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.actions.post(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.actions.put(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.actions.delete(*args, **kwargs)
    


