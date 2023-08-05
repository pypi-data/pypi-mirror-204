# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from terrascope_api.models import imagery_pb2 as imagery__pb2


class ImageryApiStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.search = channel.unary_unary(
                '/oi.papi.imagery.ImageryApi/search',
                request_serializer=imagery__pb2.ImagerySearchRequest.SerializeToString,
                response_deserializer=imagery__pb2.ImagerySearchResponse.FromString,
                )


class ImageryApiServicer(object):
    """Missing associated documentation comment in .proto file."""

    def search(self, request, context):
        """
        Retrieve the available imagery that matches the specified search request.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ImageryApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'search': grpc.unary_unary_rpc_method_handler(
                    servicer.search,
                    request_deserializer=imagery__pb2.ImagerySearchRequest.FromString,
                    response_serializer=imagery__pb2.ImagerySearchResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'oi.papi.imagery.ImageryApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ImageryApi(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def search(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/oi.papi.imagery.ImageryApi/search',
            imagery__pb2.ImagerySearchRequest.SerializeToString,
            imagery__pb2.ImagerySearchResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
