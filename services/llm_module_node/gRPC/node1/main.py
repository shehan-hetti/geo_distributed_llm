import logging
from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor

# from config import LogSettings
from pb.llm_node1_server_pb2_grpc import add_process_part1Servicer_to_server
from service.node1_service import Node1BaseService


class Node1Service(Node1BaseService):
    pass


def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_process_part1Servicer_to_server(Node1Service(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    # logging.basicConfig(level=LogSettings.info_level, format=LogSettings.log_format)
    logging.info("Getting HiddenStates...") 

    serve()