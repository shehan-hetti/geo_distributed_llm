import logging  
import json
  
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

        # route to node 1
        json_data = Node1Client.get_hiddenstates(request.prompt)
        # hidden_states = json.loads(json_data["hidden_states"])
        print('>>>>>> recieved hidden_states')

        logging.info('json data',json_data.items)

        #route to node 2
        output = Node2Client.get_generatedText(json_data["hidden_states"])
        generated_text = output["generated_text"]
        print('>>>>>> Generated Text',generated_text)
  
        return RouterResponse(result =generated_text)