FROM python:3.12
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip install grpcio grpcio-tools grpc_interceptor
COPY . .
EXPOSE 50051
CMD ["python", "./main.py"] 