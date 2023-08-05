# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from terrascope_api.models import data_type_pb2 as data__type__pb2


class DataTypeAPIStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.create = channel.unary_unary(
                '/oi.papi.DataTypeAPI/create',
                request_serializer=data__type__pb2.DataTypeCreateRequest.SerializeToString,
                response_deserializer=data__type__pb2.DataTypeCreateResponse.FromString,
                )
        self.get = channel.unary_unary(
                '/oi.papi.DataTypeAPI/get',
                request_serializer=data__type__pb2.DataTypeGetRequest.SerializeToString,
                response_deserializer=data__type__pb2.DataTypeGetResponse.FromString,
                )
        self.list = channel.unary_unary(
                '/oi.papi.DataTypeAPI/list',
                request_serializer=data__type__pb2.DataTypeListRequest.SerializeToString,
                response_deserializer=data__type__pb2.DataTypeListResponse.FromString,
                )


class DataTypeAPIServicer(object):
    """Missing associated documentation comment in .proto file."""

    def create(self, request, context):
        """
        Creates a new DataType.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """
        Gets a DataType that the user has access to.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list(self, request, context):
        """
        List all registered DataType.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DataTypeAPIServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'create': grpc.unary_unary_rpc_method_handler(
                    servicer.create,
                    request_deserializer=data__type__pb2.DataTypeCreateRequest.FromString,
                    response_serializer=data__type__pb2.DataTypeCreateResponse.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=data__type__pb2.DataTypeGetRequest.FromString,
                    response_serializer=data__type__pb2.DataTypeGetResponse.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=data__type__pb2.DataTypeListRequest.FromString,
                    response_serializer=data__type__pb2.DataTypeListResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'oi.papi.DataTypeAPI', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DataTypeAPI(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/oi.papi.DataTypeAPI/create',
            data__type__pb2.DataTypeCreateRequest.SerializeToString,
            data__type__pb2.DataTypeCreateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/oi.papi.DataTypeAPI/get',
            data__type__pb2.DataTypeGetRequest.SerializeToString,
            data__type__pb2.DataTypeGetResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def list(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/oi.papi.DataTypeAPI/list',
            data__type__pb2.DataTypeListRequest.SerializeToString,
            data__type__pb2.DataTypeListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
