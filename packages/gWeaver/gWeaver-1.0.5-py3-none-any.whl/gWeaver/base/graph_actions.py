from .node_connector import graph_engine
from .response_constructor import response
from django.core.exceptions import ValidationError
import time
import asyncio


class graph_actions:

            
    def __init__(self,request,actions) -> None:

        self.dqquery = actions.dqquery
        self.entity = actions.entity
        self.addons = actions.addons
        self.function_args = actions.function_args
        self.request = request
        self.res = response(request)
        self.serializer = actions.serializer
        self.fields = actions.fields
        self.primary_key = actions.primary_key
        self.pk_field = actions.pk_field
        
    
    def get(self,pk=None):
        processed_data = {}
        if not pk:
            raise ValidationError("pk is required")
        result = self.dqquery.all(pk).get(self.entity)
        len_data = len(result)
        if len_data == 0:
            return self.res.out(["ok", [], "no data"])
        for processed_data in result:
            self.function_args.update(
                {"processed_data": processed_data})
            if self.addons:
                processed_data = self.plugin_func(self.addons,
                                                  method="GET", processed_data=processed_data)
        if processed_data:
            return self.res.paginated(["ok", result, "success"])
        else:
            return self.res.out(["error", [], "error"])

    def ser_check(self):
        print("request data = ", self.request.data)
        ser = self.serializer(
            data=self.request.data,
            context={'request': self.request}
        )
        if ser.is_valid():
            processed = graph_engine(ser.validated_data,
                                     self.fields(self.entity)(), self.primary_key)
            data = processed.connect()
            return True, data, ser.validated_data
        else:
            return False, ser.errors, []

    async def process_data(self, function, **kwargs):
        return function(**kwargs)

    async def create_task(self, function, **kwargs):
        task = asyncio.create_task(self.process_data(function, **kwargs))
        return True

    def execute_async(self, function, **kwargs):
        return asyncio.run(self.create_task(function, **kwargs))

    def plugin_func(self, function, **kwargs):
        processed_data = kwargs.get("processed_data")
        for func in function:
            if kwargs["method"] in func["methods"]:
                processed_data = func["function"](self)
        return processed_data

    def modify(self, **kwargs):
        processed_data = kwargs["processed_data"]
        ser_data = kwargs["ser_data"]
        processed_data.update(
            {self.entity+".modified_on": time.time()})

        processed_data["id"] = self.primary_key
        self.function_args.update({"processed_data": processed_data,
                                   "ser_data": ser_data})

        if self.addons:
            processed_data = self.plugin_func(self.addons,
                                              method="PUT", processed_data=processed_data)

        self.dqquery.create(processed_data)
        # if any field in ser_data is of type "list", delete it
        for key, value in ser_data.items():
            if isinstance(value, list):
                try:
                    getattr(self.dqquery,"delete_"+key)(self.primary_key, value)
                except:
                    pass

    def create(self, **kwargs):
        processed_data = kwargs["processed_data"]
        print("proicessed_data = ", processed_data)
        ser_data = kwargs["ser_data"]

        processed_data.update({self.entity+".created_on": time.time()})

        uid = self.dqquery.create(processed_data)
        processed_data["id"] = uid
        self.function_args.update({"processed_data": processed_data,
                                   "ser_data": ser_data})
        if self.addons:
            processed_data = self.plugin_func(self.addons,
                                              method="POST", processed_data=processed_data)

    def put(self):
        status, processed_data, ser_data = self.ser_check()
        if status:
            try:
                self.execute_async(
                    self.modify, processed_data=processed_data, ser_data=ser_data)
                return self.res.out(["ok", [], "modified"])
            except:
                return self.res.out(["error", processed_data, "error"])
        else:
            return self.res.out(["error", processed_data, "error"])

    def post(self):
        status, processed_data, ser_data = self.ser_check()
        print("status, processed data, ser data = ", status, processed_data, ser_data)
        if status:
            try:
                self.execute_async(
                    self.create, processed_data=processed_data, ser_data=ser_data)
                return self.res.out(["ok", [], "added"])
            except:
                return self.res.out(["error", processed_data, "error"])
        else:
            return self.res.out(["error", processed_data, "error"])

    def delete(self):
        item = self.request.query_params.get(self.pk_field)
        if not item:
            item = self.request.data.get(self.pk_field)
        if type(item) != list:
            item = [item]

        try:
            self.dqquery.delete(item, self.primary_key)
            return self.res.out(["ok", "item deleted", "success"])
        except:
            return self.res.out(["error", "", "error"])
