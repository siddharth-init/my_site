from django.contrib import admin
from .models import Author, Post, Tag


# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "email")
    list_filter = ("firstname", "lastname", "email")
    search_fields = ("firstname", "lastname", "email")
    filters = ("firstname", "lastname", "email")


admin.site.register(Author, AuthorAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "date")
    # search_fields = ("author", "title", "tags", "date")
    list_filter = (
        "author",
        "date",
        "tags",
    )

    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, PostAdmin)


class TagAdmin(admin.ModelAdmin):
    #  list_display = ("name",)
    #  search_fields = ("name",)
    #  filters = ("name",)
    pass


admin.site.register(Tag, TagAdmin)
