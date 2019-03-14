from django.contrib import admin

# Register your models here.
from .models import Post
# admin.site.register(Post)
@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'slug', 'author', 'body','publish','status',) # list_display属性指定那些字段在详情页中显示出来
    list_filter = ('status', 'created', 'publish', 'author',)
    date_hierarchy = 'publish'
    search_fields = ('title', 'body',)
    raw_id_fields = ('author',)
    prepopulated_fields = {'slug': ('title',)}