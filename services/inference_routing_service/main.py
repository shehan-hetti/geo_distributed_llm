import logging
from concurrent import futures
from config import LogSettings
from prometheus_client import start_http_server, Counter, Gauge

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor

from pb.router_pb2_grpc import add_RouterServicer_to_server
from service.router import RouterBaseService

#Define metrics
REQUESTS_TOTAL = Counter('inference_routing_requests_total', 'Total number of requests to Inference Routing server')
ACTIVE_REQUESTS = Gauge('inference_routing_active_requests', 'Number of active requests to Inference Routing server')


class RouterService(RouterBaseService):
    pass


def serve():

    # start Prometheus metrics server on 8001
    start_http_server(8001)

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
    logging.info('NEW Router Service Started...')
    print("Router Service Started...") 

    serve()