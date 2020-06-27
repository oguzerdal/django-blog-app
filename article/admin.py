from django.contrib import admin

# Register your models here.

from .models import Article, Comment


admin.site.register(Comment)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = ["title","author","created_date","content"]
    list_display_links = ["title"]
    search_fields = ["title"]
    list_filter =["created_date"]
    list_filter = ["title"]

    class Meta:
        model=Article