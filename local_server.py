#!/usr/bin/env python
# -*-coding: utf-8 -*-

import logging
import time
from concurrent import futures

import grpc

from call_invoker import CallInvoker
from rpc_package.callinvoker_pb2_grpc import CallInvokerServicer, add_CallInvokerServicer_to_server

invoker = CallInvoker()


class LocalServer(CallInvokerServicer):

    # 这里实现我们定义的接口
    def call(self, request, context):
        return invoker.call(request.route, request.params, request.description)


def serve():
    # 这里通过thread pool来并发处理server的任务
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 将对应的任务处理函数添加到rpc server中
    add_CallInvokerServicer_to_server(LocalServer(), server)

    # 这里使用的非安全接口，世界gRPC支持TLS/SSL安全连接，以及各种鉴权机制
    server.add_insecure_port('[::]:50000')
    server.start()
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    logging.basicConfig()
    serve()
