import logging
from fastapi import FastAPI
# from models import Prompts

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from uuid import uuid4

from pydantic import BaseModel

import grpc
# from inferencerouter_pb2 import RouterRequest
# from inferencerouter_pb2_grpc import RouterStub
from pb.router_pb2 import RouterRequest
from pb.router_pb2_grpc import RouterStub


# cluster = Cluster(['0.0.0.0'], port=9042)
# session = cluster.connect('llm_data')
# Cassandra connection setup
auth_provider = PlainTextAuthProvider(
    username='cassandra', password='cassandra')
cluster = Cluster(['cassandra'], port=9042, auth_provider=auth_provider)
session = cluster.connect('llm_data')

# gRPC client setup
# Replace with your gRPC server address
grpc_channel = grpc.insecure_channel('inference-routing-service:50051')
grpc_client = RouterStub(grpc_channel)

app = FastAPI()


class Prompts(BaseModel):
    prompt: str


@app.get("/")
def read_root():
    return {"message": "Welcome to the Geo-Distributed Large Language Model Serving and Fine-Tuning Platform"}


@app.get("/prompts")
async def get_prompts() -> list[Prompts]:
    rows = session.execute('SELECT * FROM prompts;')
    rows = list(rows)
    for row in rows:
        print(row.id, row.prompt)
    return [{"id": row.id, "prompt": row.prompt} for row in rows]


@app.post("/prompts")
async def create_todo(prompts: Prompts):
    prepared_statement = session.prepare(
        'INSERT INTO prompts (id, prompt) VALUES (?, ?)')
    id = uuid4()
    session.execute(prepared_statement, [id, prompts.prompt])

    logging.info('create_todo called')

    # Send the prompt to the gRPC server
    grpc_request = RouterRequest(prompt=prompts.prompt)
    grpc_response = grpc_client.GetResult(grpc_request)
    print("gRPC Response:", grpc_response.result)

    return {"response": grpc_response.result}
