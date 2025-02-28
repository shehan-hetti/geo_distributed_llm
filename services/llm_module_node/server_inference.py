import requests
import torch
import re

# Text input
text = "There was a family with 2 kids and a grandmother."

# Define the number of tokens to generate
num_tokens_to_generate = 40

# Step 1: Send input to Node 1
response_part1 = requests.post(
    "http://127.0.0.1:8001/process_part1",
    json={"prompt": text},
)

hidden_states = torch.tensor(response_part1.json()["response"])

# Debug hidden states shape
print(f"Hidden states shape (received from Node 1): {hidden_states.size()}")

generated_text = text

# loop to generate token one by one
for _ in range(num_tokens_to_generate):

    # Step 2: Send hidden states to Node 2
    response_part2 = requests.post(
        "http://127.0.0.1:8002/process_part2",
        json={
            "hidden_states": hidden_states.tolist()
        }
    )

    # Extract the latest generated token
    new_token = response_part2.json()["response"].strip()

    # Append new token to the generated text
    generated_text += " " + new_token
    generated_text = re.sub(r'\s([?.!",;:])', r'\1', generated_text)

    # Update hidden states using the newly generated text
    response_part1 = requests.post(
        "http://127.0.0.1:8001/process_part1",
        json={"prompt": generated_text}
    )

    hidden_states = torch.tensor(response_part1.json()["response"])

print("Generated Text:", generated_text)
