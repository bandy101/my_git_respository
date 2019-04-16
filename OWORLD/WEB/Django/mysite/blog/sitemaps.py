from django.contrib.sitemaps import Sitemap
from .models import Post


# Django默认会调用数据对象的get_absolute_url()获取对应的URL，
# 如果想手工指定具体的URL，可以为PostSitemap添加一个location方法。
# lastmod方法接收items()返回的每一个数据对象然后返回其更新时间。

class PostSitemap(Sitemap):
    changefreq = 'weekly'   # 更新频率
    priority = 0.9  # 优先级

    def items(self):
        return Post.published.all()

    # 修改日期
    def lastmod(self, obj):
        return obj.updated