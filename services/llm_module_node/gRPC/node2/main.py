import logging
from config import LogSettings
from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor

# from config import LogSettings
from pb.llm_node2_server_pb2_grpc import add_process_part2Servicer_to_server
from service.node2_service import Node2BaseService


class Node2Service(Node2BaseService):
    pass


def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_process_part2Servicer_to_server(Node2Service(), server)
    server.add_insecure_port("[::]:50053")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=LogSettings.info_level, format=LogSettings.log_format)
    logging.info("LLM Node 2 started ...") 

    serve()