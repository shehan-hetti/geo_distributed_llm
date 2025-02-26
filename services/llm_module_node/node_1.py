from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer
from model_shard import GPT2Part1  # Import your model structure
from transformers import AutoModelForCausalLM
from typing import List

# Load model
model_name = "gpt2"
full_model = AutoModelForCausalLM.from_pretrained(model_name)

# Initialize FastAPI app
app = FastAPI()

# Load tokenizer and model Part 1
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model_part1 = GPT2Part1(full_model)  # Initialize model structure
model_part1.load_state_dict(torch.load("model_part1.pth", map_location="cpu"))
model_part1.eval()

class PromptRequest(BaseModel):
    prompt: str

class HiddenStatesResponse(BaseModel):
    response: List[List[List[float]]]
    #response: List[List[float]]

@app.post("/process_part1", response_model=HiddenStatesResponse)
async def process_part1(request: PromptRequest):
    inputs = tokenizer(request.prompt, return_tensors="pt")
    print(f"Tokenized inputs: {inputs}")

    input_ids = inputs["input_ids"]
    print(f"Input IDs: {input_ids}")

    # Check the size of input_ids
    print(f"Size of input_ids: {input_ids.size()}")

    with torch.no_grad():
        hidden_states = model_part1(input_ids)

    # Check the size of the output (hidden states)
    print(f"Size of output (hidden states): {hidden_states.size()}")

    return {"response": hidden_states.tolist()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)  # Node 1 runs on port 8001
