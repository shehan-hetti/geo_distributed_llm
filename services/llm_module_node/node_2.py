from fastapi import FastAPI
from pydantic import BaseModel
import torch
from model_shard import GPT2Part2  # Import model structure
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer
from typing import List


# Load model
model_name = "gpt2"
full_model = AutoModelForCausalLM.from_pretrained(model_name)

# Initialize FastAPI app
app = FastAPI()

# Load Part 2
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model_part2 = GPT2Part2(full_model)  # Initialize model structure
model_part2.load_state_dict(torch.load("model_part2.pth", map_location="cpu"))
model_part2.eval()

class HiddenStateRequest(BaseModel):
    hidden_states: List[List[List[float]]]
    num_return_sequences: int = 1
    max_length: int = 20
    #hidden_states: List[List[float]]

class PromptResponse(BaseModel):
    #responses: List[str]
    response: str

@app.post("/process_part2", response_model=PromptResponse)
async def process_part2(request: HiddenStateRequest):
    # Convert hidden states back to tensor
    hidden_states = torch.tensor(request.hidden_states, dtype=torch.float32)

    # Debug hidden states shape
    print(f"Hidden states shape (received at Node 2): {hidden_states.size()}")

    with torch.no_grad():
        logits = model_part2(hidden_states)

    # Convert logits to output tokens
    predicted_ids = torch.argmax(logits, dim=-1)
    print(f"predicted IDs: {predicted_ids}")

    output_text = tokenizer.decode(predicted_ids[0], skip_special_tokens=True)

    return {"response": output_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)  # Node 2 runs on port 8002
    