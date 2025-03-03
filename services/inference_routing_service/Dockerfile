FROM python:3.12
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install grpcio grpcio-tools grpc_interceptor
RUN pip3 install prometheus_client
COPY . .
EXPOSE 50051 8001
CMD ["python3", "./main.py"] 