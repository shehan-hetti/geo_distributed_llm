import logging  
import json
import re
  
from grpc import StatusCode  
from grpc_interceptor.exceptions import NotFound, GrpcException  
  
from pb.router_pb2 import RouterResponse  
from pb.router_pb2_grpc import RouterServicer  

from clients.Node1Client import Node1Client
from clients.Node2Client import Node2Client
  
class RouterBaseService(RouterServicer):  
      
    def GetResult(self, request, context): 
        logging.info('>>>>>> request:',request) 
        print('>>>>>> request:',request)

        # Define the number of tokens to generate
        num_tokens_to_generate = 20

        # route to node 1
        json_data = Node1Client.get_hiddenstates(request.prompt)
        # hidden_states = json.loads(json_data["hidden_states"])
        print('>>>>>> recieved hidden_states')

        logging.info('json data',json_data.items)

        generated_text = request.prompt

        # loop to generate token one by one
        for _ in range(num_tokens_to_generate):

            #route to node 2
            output = Node2Client.get_generatedText(json_data["hidden_states"])
            logging.info('output ',output)
            print('>>>>>> output',output)

            # Extract the latest generated token            
            new_token = output["generated_text"]
            print('>>>>>> new_token',new_token)

            # Append new token to the generated text
            generated_text += " " + new_token
            generated_text = re.sub(r'\s([?.!",;:])', r'\1', generated_text)

            # Update hidden states using the newly generated text
            # route to node 1
            json_data = Node1Client.get_hiddenstates(generated_text)

            print("Generated Text:", generated_text)

          
        return RouterResponse(result =generated_text)