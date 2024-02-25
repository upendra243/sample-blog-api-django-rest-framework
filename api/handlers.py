from api.services import ArticleService
from protos import article_pb2_grpc


def grpc_handlers(server):
    article_pb2_grpc.add_PostControllerServicer_to_server(ArticleService.as_servicer(), server)
