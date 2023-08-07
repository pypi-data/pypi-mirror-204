from .graph_models import *
from .query import *
from .serializer import *
from .addons import *
from gWeaver.base.graph_actions import *


class servicesActions(graph_actions2):
    dqquery = serviceQuery
    serializer = serviceSerializer
    model = serviceModel
    add_functions = []
    # add_functions = [
    #                  {"function": write_image,
    #                      "methods": ["POST","PUT"]},
    #                  {"function": read_image,
    #                      "methods": ["GET"]},]