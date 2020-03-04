from django.contrib import admin
from .models import  Article, Tag

class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)

admin.site.register(Article, ArticleAdmin) 
admin.site.register(Tag)




