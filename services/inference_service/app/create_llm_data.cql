-- Create the keyspace if it doesn't exist
CREATE KEYSPACE IF NOT EXISTS llm_data
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

-- Use the keyspace
USE llm_data;

-- Create the table if it doesn't exist
CREATE TABLE IF NOT EXISTS Prompts (
    id UUID PRIMARY KEY,
    prompt text
);