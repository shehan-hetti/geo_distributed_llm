import grpc
from google.protobuf.json_format import MessageToDict

from pb.llm_node2_server_pb2 import LLMNode2Request
from pb.llm_node2_server_pb2_grpc import process_part2Stub


class Node2Client(object):       

    def get_generatedText(hidden_states):
        # print('>>>>>> hidden_states',hidden_states)
        channel = grpc.insecure_channel("llm_node2:50053")
        stub = process_part2Stub(channel)
        try:
            stub = stub.GetGeneratedText(LLMNode2Request(hidden_states=hidden_states,num_return_sequences="1",max_length="20"))

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