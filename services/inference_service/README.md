<!-- docker run -it --name cassandra -p 9042:9042 cassandra

CREATE KEYSPACE llm_data WITH REPLICATION = {
  'class' : 'SimpleStrategy', 'replication_factor' : 1
};

DESC KEYSPACE llm_data;

CREATE TABLE Prompts (
  id int PRIMARY KEY,
  prompt text
);


pip install "fastapi[standard]"
pip install cassandra-driver

fastapi dev main.py -->