import logging  
  
from grpc import StatusCode  
from grpc_interceptor.exceptions import NotFound, GrpcException  
  
from pb.inferencerouter_pb2 import RouterResponse  
from pb.inferencerouter_pb2_grpc import RouterServicer  
  
# mock_drinks = {  
#     "coffee": 10,  
#     "soda": 5,  
#     "beer": 0  
# }  
  
  
class RouterBaseService(RouterServicer):  
      
    def GetRoute(self, request, context): 
        logging.info('>>>>>> request:',request) 
        # drinks_stock = mock_drinks.get(request.order)  
  
        # if drinks_stock is None:  
        #     raise GrpcException(  
        #         details="Drink not Found",  
        #         status_code=StatusCode.NOT_FOUND,  
        #     )  
  
        # if drinks_stock == 0:  
        #     raise NotFound(  
        #         details="Drink out of stock",  
        #         status_code=StatusCode.NOT_FOUND,  
        #     )  
  
        return RouterResponse(next_node="Go to node 23")