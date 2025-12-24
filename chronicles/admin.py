from django.contrib import admin

from .models import Post, Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "publish"]
    list_filter = ["status"]
    prepopulated_fields = {"slug": ("title",)}
    show_facets = admin.ShowFacets.ALWAYS
