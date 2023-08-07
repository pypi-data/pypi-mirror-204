from collections import OrderedDict
from rest_framework.response import Response
import json
import os
from rest_framework.pagination import LimitOffsetPagination


class pagination(LimitOffsetPagination):
    def get_paginated_response(self, data, headers, status, message):
        return Response(OrderedDict([
            ("status", status),
            ("message", message),
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('result', data),
        ]), headers=headers)


class response:
    def __init__(self, request):
        self.request = request
        self.header = {}

    def headers(self, *args):
        j = {}
        count = 0
        for i in args:
            j.update({i: self.request.headers.get(args[count])})
            count += 1
        return j

    def request_parser(self, *args):
        j = {}
        count = 0
        for i in args:
            j.update({i: self.request.data.get(args[count])})
            count += 1
        return j

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            data
        ]))

    def response_build(self, data):
        try:
            # print("data", data)
            status = data[0]
            result = data[1]
            message = data[2]
        except:
            status = "error"
            result = data
            message = "error"
        data = {"status": status,
                "message": message, "result": result}
        return data

    def out(self, data, http_status=200, headers=None):
        data = self.response_build(data)
        if not headers:
            headers=self.header

        return Response(data=data, status=http_status,headers=headers)


    def paginated(self, data):

        data = self.response_build(data)
        if not data.get("result"):
            return self.out([data['status'], [], data['message']])
        offset = pagination()
        results = offset.paginate_queryset(
            data["result"], self.request, view=self)
        result = offset.get_paginated_response(
            results, self.header, data["status"], data["message"])
        return result

    def exception(self, msg):
        print("ERROR request blocked", msg)  # logging
        data = {"status": "ERROR", "message": "request blocked"}
        return Response(data=data, headers=self.header)
