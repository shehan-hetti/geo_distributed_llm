import logging  
import json
import re
  
from grpc import StatusCode  
from grpc_interceptor.exceptions import NotFound, GrpcException 
from prometheus_client import start_http_server, Counter, Gauge
 
  
from pb.router_pb2 import RouterResponse  
from pb.router_pb2_grpc import RouterServicer  

from clients.Node1Client import Node1Client
from clients.Node2Client import Node2Client

#Define metrics
REQUESTS_TOTAL = Counter('inference_routing_requests_total', 'Total number of requests to Inference Routing server')
  
class RouterBaseService(RouterServicer):  
      
    def GetResult(self, request, context): 
        logging.info('>>>>>> recieved request: ',request)

        # Define the number of tokens to generate
        num_tokens_to_generate = 10

        # route to node 1
        logging.info('>>>>>> routing to node 1 ...')
        json_data = Node1Client.get_hiddenstates(request.prompt)
        # hidden_states = json.loads(json_data["hidden_states"])

        generated_text = request.prompt

        # loop to generate token one by one
        for _ in range(num_tokens_to_generate):
            # Increment the counter
            REQUESTS_TOTAL.inc()

            #route to node 2
            logging.info('>>>>>> routing to node 2 ...')
            output = Node2Client.get_generatedText(json_data["hidden_states"])
            
            # Extract the latest generated token            
            new_token = output["generated_text"]

            # Append new token to the generated text
            generated_text += " " + new_token
            generated_text = re.sub(r'\s([?.!",;:])', r'\1', generated_text)

            # Update hidden states using the newly generated text
            # route to node 1
            logging.info('>>>>>> routing to node 1 ...')
            json_data = Node1Client.get_hiddenstates(generated_text)            

          
        return RouterResponse(result =generated_text)