from django_grpc_framework import proto_serializerss

from api.models import Article


class ArticleSerializer(proto_serializers.ModelProtoSerializer):
    created_by = proto_serializerss.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'description',
            'body',
            'tags',
            'createdAt',
            'updatedAt',
            'favorited',
            'favoritesCount',
            'created_by'
        ]
