import grpc
from google.protobuf.json_format import MessageToDict

from pb.llm_node1_server_pb2 import LLMNode1Request
from pb.llm_node1_server_pb2_grpc import process_part1Stub


class Node1Client(object):       

    def get_hiddenstates(prompt):
        channel = grpc.insecure_channel("llm_node1:50052")
        stub = process_part1Stub(channel)
        try:
            stub = stub.GetHiddenStates(LLMNode1Request(prompt=prompt))

            return MessageToDict(
                stub,
                preserving_proto_field_name=True
                # ,
                # including_default_value_fields=True
            )

        except grpc.RpcError as rpc_error:
            return {
                "ERROR": rpc_error.details()
            }