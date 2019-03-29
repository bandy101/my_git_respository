from django.contrib import admin
from .models import Post,Comment

# Register your models here.
# 向管理后台内添加模型
# admin.site.register(Post)
# @admin.register()装饰器的功能与之前的
#       admin.site.register()一样，用于将PostAdmin类注册成Post的管理类。

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status') # 字段在详情页面显示出来
    # 页面出现了一个右侧边栏用于筛选结果，这个功能由list_filter属性控制
    list_filter = ('status', 'created', 'publish', 'author',)
    # 定义搜索栏
    search_fields = ('title', 'body',)
    # 输入文章标题时，slug字段会根据标题自动填充，设置了prepopulated_fields属性中slug字段与title字段的对应关系
    prepopulated_fields = {'slug': ('title',)}
    # author字段旁边出现了一个搜索图标
    # ，并且可以按照ID来查找和显示作者，如果在用户数量很大的时候，这就方便太多了。
    raw_id_fields = ('author',)
    # 搜索栏的下方，出现了时间层级导航条
    date_hierarchy = 'publish'
    # 排序的依据
    ordering = ('status', 'publish',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','active')
    list_filter = ('created','active')
    search_fields = ('name', 'email', 'body')

