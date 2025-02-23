FROM python:3.12
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install grpcio grpcio-tools grpc_interceptor
COPY . .
EXPOSE 50051
CMD ["python3", "./main.py"] 