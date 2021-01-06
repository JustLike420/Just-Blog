from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Tag, Post, Category, Comment


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}  # автоматическое составление url из названия


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'post')
    list_filter = ('user', 'post')
    list_display_links = ('text', 'user', 'post')
    read_only_fields = ('user', 'post')


class PostAdmin(admin.ModelAdmin):
    # prepopulated_fields = {"slug": ("title",)}
    save_as = True
    save_on_top = True
    list_display = ('id', 'slug', 'title', 'created_at', 'user', 'get_photo')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('category', 'tags')
    read_only_fields = ('views', 'created_at',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return '-'

    get_photo.short_description = 'Фото'


admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
