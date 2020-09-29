from rest_framework import serializers

from api.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'description',
            'body',
            'tags',
            'featuredImage',
            'createdAt',
            'updatedAt',
            'favorited',
            'favoritesCount',
            'created_by'
        ]
