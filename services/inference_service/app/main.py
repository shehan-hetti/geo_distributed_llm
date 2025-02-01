from fastapi import FastAPI
from models import Prompts

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from uuid import UUID, uuid4

# cluster = Cluster(['0.0.0.0'], port=9042)
# session = cluster.connect('llm_data')
# Cassandra connection setup
auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
cluster = Cluster(['cassandra'], port=9042, auth_provider=auth_provider)
session = cluster.connect('llm_data')

app = FastAPI()

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

    return {"message": "prompt received successfully"}
