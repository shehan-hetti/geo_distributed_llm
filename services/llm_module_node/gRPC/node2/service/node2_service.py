import logging
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

# Apply top-k and top-p filtering
def top_k_top_p_filtering(logits, top_k=50, top_p=0.9, filter_value=-float("Inf")):

    if top_k > 0:
        top_k = min(top_k, logits.size(-1))
        indices_to_remove = logits < torch.topk(logits, top_k)[0][:, -1, None]
        logits[indices_to_remove] = filter_value

    if top_p > 0.0 and top_p < 1.0:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(torch.nn.functional.softmax(sorted_logits, dim=-1), dim=-1)
        sorted_indices_to_remove = cumulative_probs > top_p
        sorted_indices_to_remove[:, 1:] = sorted_indices_to_remove[:, :-1].clone()
        sorted_indices_to_remove[:, 0] = 0
        
        indices_to_remove = sorted_indices_to_remove.scatter(1, sorted_indices, sorted_indices_to_remove)
        logits[indices_to_remove] = filter_value

    return logits
 
class Node2BaseService(process_part2Servicer):     
    
    def GetGeneratedText(self, request, context):
        logging.info("Generating text ...") 

        ## Convert hidden states back to tensor
        hidden_states = torch.tensor(json.loads(request.hidden_states), dtype=torch.float32)

        with torch.no_grad():
            # Get logits from the model
            logits = model_part2(hidden_states)

        # Apply top-k and top-p filtering
        logits = top_k_top_p_filtering(logits[:, -1, :], top_k=50, top_p=0.9)

        # Sample next token using multinomial distribution
        probabilities = torch.softmax(logits, dim=-1)
        predicted_ids = torch.multinomial(probabilities, num_samples=1)

        # Decode the new token and append to generated text
        new_token = tokenizer.decode(predicted_ids[0], skip_special_tokens=True,clean_up_tokenization_spaces=True).strip()

        return LLMNode2Response(generated_text=new_token)