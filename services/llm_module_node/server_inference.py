import requests
import torch
import numpy as np

# Text input
text = "A man went to the bar to get a drink. Then he ordered a Beer. Then started"

# Step 1: Send input to Node 1
response_part1 = requests.post(
    "http://127.0.0.1:8001/process_part1",
    json={"prompt": text},
)
hidden_states = torch.tensor(response_part1.json()["response"])

# Debug hidden states shape
print(f"Hidden states shape (received from Node 1): {hidden_states.size()}")

# Step 2: Send hidden states to Node 2
response_part2 = requests.post(
    "http://127.0.0.1:8002/process_part2",
    json={"hidden_states": hidden_states.tolist(),
          "num_return_sequences": 1,
          "max_length": 100
        }
)

output_text = response_part2.json()["response"]

print("Generated Text:", output_text)
