import logging
from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor

from config import LogSettings
from pb.inferencerouter_pb2_grpc import add_RouterServicer_to_server
from service.router import RouterBaseService


class RouterService(RouterBaseService):
    pass


def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_RouterServicer_to_server(RouterService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=LogSettings.info_level, format=LogSettings.log_format)
    logging.info('Router Service Started...')

    serve()