from pydantic import BaseModel
import torch
import json
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer
from typing import List

import sys
# sys.path.append("..")
# from model.model_shard import GPT2Part2  # Import your model structure
from model_shard import GPT2Part2  # Import your model structure

from grpc import StatusCode  
from grpc_interceptor.exceptions import NotFound, GrpcException  
  
from pb.llm_node2_server_pb2 import LLMNode2Response  
from pb.llm_node2_server_pb2_grpc import process_part2Servicer

# Load model
model_name = "gpt2"
full_model = AutoModelForCausalLM.from_pretrained(model_name)

# Load Part 2
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model_part2 = GPT2Part2(full_model)  # Initialize model structure
model_part2.load_state_dict(torch.load("model_part2.pth", map_location="cpu"))
model_part2.eval()
 
class Node2BaseService(process_part2Servicer):  
      
    def GetGeneratedText(self, request, context):
        # Convert hidden states back to tensor
        hidden_states = torch.tensor(json.loads(request.hidden_states), dtype=torch.float32)
        
        # Debug hidden states shape
        print(f"Hidden states shape (received at Node 2): {hidden_states.size()}")

        with torch.no_grad():
            logits = model_part2(hidden_states)

        # Convert logits to output tokens
        predicted_ids = torch.argmax(logits, dim=-1)
        print(f"predicted IDs: {predicted_ids}")  

        output_text = tokenizer.decode(predicted_ids[0], skip_special_tokens=True)    
  
        return LLMNode2Response(generated_text=output_text)