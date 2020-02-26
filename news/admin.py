from django.contrib import admin
from .models import Editor, Article, Tag

class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)

admin.site.register(Editor)
admin.site.register(Article, ArticleAdmin) 
admin.site.register(Tag)




