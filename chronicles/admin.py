from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "publish"]
    list_filter = ["status"]
    prepopulated_fields = {"slug": ("title",)}
    show_facets = admin.ShowFacets.ALWAYS
