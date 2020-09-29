from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.mixins import RetrieveModelMixin

from api.models import Article, Tag
from api.permissions import IsOwnerOrReadOnly
from api.serializers import ArticleSerializer

# Create your views here.

def home(request):
    return render(request, 'home.html')


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        user_id = self.request.GET.get('user_id')
        queryset = Article.objects.all()
        if user_id:
            queryset = queryset.filter(created_by=user_id)
        return queryset

    def create(self, request, *args, **kwargs):
        # Create if new tags found
        tags = request.data.get('tags', [])
        for tag in tags:
            Tag.objects.get_or_create(name=tag)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):

        serializer.save(created_by=self.request.user)


# Get an article

def get_article(request, pk):
    if request.method == 'GET':
        pass


class GetArticle(APIView):
    def get(self):
        pass


class GetAricle2(APIView, RetrieveModelMixin):
    querset = ''
    serializer_class = ArticleSerializer

