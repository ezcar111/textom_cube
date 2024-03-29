# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from proto import EarthlingProtocol_pb2 as proto_dot_EarthlingProtocol__pb2


class EarthlingStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Echo = channel.unary_unary(
                '/Earthling/Echo',
                request_serializer=proto_dot_EarthlingProtocol__pb2.EchoRequest.SerializeToString,
                response_deserializer=proto_dot_EarthlingProtocol__pb2.EchoResponse.FromString,
                )
        self.ReportIdleWorker = channel.unary_unary(
                '/Earthling/ReportIdleWorker',
                request_serializer=proto_dot_EarthlingProtocol__pb2.ReportRequest.SerializeToString,
                response_deserializer=proto_dot_EarthlingProtocol__pb2.ReportResponse.FromString,
                )
        self.NotifyTask = channel.unary_unary(
                '/Earthling/NotifyTask',
                request_serializer=proto_dot_EarthlingProtocol__pb2.TaskRequest.SerializeToString,
                response_deserializer=proto_dot_EarthlingProtocol__pb2.TaskResponse.FromString,
                )


class EarthlingServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Echo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReportIdleWorker(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def NotifyTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_EarthlingServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Echo': grpc.unary_unary_rpc_method_handler(
                    servicer.Echo,
                    request_deserializer=proto_dot_EarthlingProtocol__pb2.EchoRequest.FromString,
                    response_serializer=proto_dot_EarthlingProtocol__pb2.EchoResponse.SerializeToString,
            ),
            'ReportIdleWorker': grpc.unary_unary_rpc_method_handler(
                    servicer.ReportIdleWorker,
                    request_deserializer=proto_dot_EarthlingProtocol__pb2.ReportRequest.FromString,
                    response_serializer=proto_dot_EarthlingProtocol__pb2.ReportResponse.SerializeToString,
            ),
            'NotifyTask': grpc.unary_unary_rpc_method_handler(
                    servicer.NotifyTask,
                    request_deserializer=proto_dot_EarthlingProtocol__pb2.TaskRequest.FromString,
                    response_serializer=proto_dot_EarthlingProtocol__pb2.TaskResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Earthling', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Earthling(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Echo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Earthling/Echo',
            proto_dot_EarthlingProtocol__pb2.EchoRequest.SerializeToString,
            proto_dot_EarthlingProtocol__pb2.EchoResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReportIdleWorker(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Earthling/ReportIdleWorker',
            proto_dot_EarthlingProtocol__pb2.ReportRequest.SerializeToString,
            proto_dot_EarthlingProtocol__pb2.ReportResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def NotifyTask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Earthling/NotifyTask',
            proto_dot_EarthlingProtocol__pb2.TaskRequest.SerializeToString,
            proto_dot_EarthlingProtocol__pb2.TaskResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
