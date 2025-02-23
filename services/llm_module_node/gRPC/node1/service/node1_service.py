import logging
import json
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM
from typing import List

import sys
# sys.path.append("..")
# from model.model_shard import GPT2Part1  # Import your model structure
from model_shard import GPT2Part1

from grpc import StatusCode  
from grpc_interceptor.exceptions import NotFound, GrpcException  
  
from pb.llm_node1_server_pb2 import LLMNode1Response  
from pb.llm_node1_server_pb2_grpc import process_part1Servicer

# Load model
model_name = "gpt2"
full_model = AutoModelForCausalLM.from_pretrained(model_name)

# Load tokenizer and model Part 1
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model_part1 = GPT2Part1(full_model)  # Initialize model structure
model_part1.load_state_dict(torch.load("model_part1.pth", map_location="cpu"))
model_part1.eval()
 
class Node1BaseService(process_part1Servicer):  
      
    def GetHiddenStates(self, request, context): 
        logging.info('>>>>>> request:',request) 
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

        # print(f">>>>>>>>> hidden states : {hidden_states.tolist()}")       
  
        return LLMNode1Response(hidden_states=json.dumps(hidden_states.tolist()))