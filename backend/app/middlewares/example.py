"""
@文件        :__init__.py
@说明        :omc是Operation & Maintenance Center 的首字母缩写
@时间        :2025/06/06 18:58:40
@作者        :xiaozheng
@邮箱        :13124421402@163.com
@版本        :1.0.0
"""

from simplejrpc.interfaces import RPCMiddleware

class ExampleMiddleware(RPCMiddleware):
    """ """

    def process_request(self, request, context):
        # print("[middleware-request] ", request, context)
        return request

    def process_response(self, response, context):
        # print("[middleware-response] ", response, context)
        return response