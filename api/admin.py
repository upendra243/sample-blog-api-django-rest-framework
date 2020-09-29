from django.contrib import admin

from api.models import Article, Tag

# Register your models here.

class TagAdmin(admin.ModelAdmin):
    pass


class ArticleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
