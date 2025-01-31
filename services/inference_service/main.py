from fastapi import FastAPI
from models import Prompts

from cassandra.cluster import Cluster

cluster = Cluster(['0.0.0.0'], port=9042)
session = cluster.connect('llm_data')

app = FastAPI()


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
    session.execute(prepared_statement, [prompts.id, prompts.prompt])

    return {"message": "prompt received successfully"}
