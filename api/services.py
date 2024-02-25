import grpc
from google.protobuf import empty_pb2
from django_grpc_framework.services import Service
from api.models import Article
from api.grpc_serializers import ArticleSerializer


class ArticleService(Service):
    def List(self, request, context):
        article = Article.objects.all()
        serializer = ArticleSerializer(article, many=True)
        for msg in serializer.message:
            yield msg

    def Create(self, request, context):
        serializer = ArticleSerializer(message=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.message

    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            self.context.abort(grpc.StatusCode.NOT_FOUND, 'Article:%s not found!' % pk)

    def Retrieve(self, request, context):
        article = self.get_object(request.id)
        serializer = ArticleSerializer(article)
        return serializer.message

    def Update(self, request, context):
        article = self.get_object(request.id)
        serializer = ArticleSerializer(article, message=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.message

    def Destroy(self, request, context):
        article = self.get_object(request.id)
        article.delete()
        return empty_pb2.Empty()

