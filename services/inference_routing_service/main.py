import logging
from concurrent import futures
from config import LogSettings
from prometheus_client import start_http_server, Counter, Gauge
import psutil
import time
import threading

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor

from pb.router_pb2_grpc import add_RouterServicer_to_server
from service.router import RouterBaseService

# Define Prometheus metrics
CPU_USAGE = Gauge('grpc_server_cpu_usage', 'CPU Usage of gRPC server (%)')
MEMORY_USAGE = Gauge('grpc_server_memory_usage', 'Memory Usage of gRPC server (MB)')

# Function to collect system metrics
def collect_metrics():
    while True:
        CPU_USAGE.set(psutil.cpu_percent())  # Get CPU usage in percentage
        MEMORY_USAGE.set(psutil.virtual_memory().used / (1024 * 1024))  # Get memory usage in MB
        time.sleep(5)  # Collect metrics every 5 seconds

class RouterService(RouterBaseService):
    pass


def serve():

    # start Prometheus metrics server on 8001
    start_http_server(8001)
    logging.info('Prometheus metrics available at http://localhost:8000/metrics')

    # Run the metrics collection in a separate thread
    metrics_thread = threading.Thread(target=collect_metrics, daemon=True)
    metrics_thread.start()

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