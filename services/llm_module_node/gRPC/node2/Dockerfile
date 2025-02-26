FROM python:3.12
WORKDIR /app
RUN pip3 install grpcio grpcio-tools grpc_interceptor pydantic torch transformers
COPY . .
EXPOSE 50053
CMD ["python3", "./main.py"] 