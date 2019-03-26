from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# 增加模型管理器 （默认objects）
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='draft')

class Post(models.Model):
    objects = models.Manager()  # 默认的管理器
    published = PublishedManager()  # 自定义管理器

    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    title = models.CharField(max_length=250)
    # unique_for_date 通过日期和简称可以找到唯一的一篇文章（或者找不到）
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    # on_delete参数表示删除外键关联的内容时候的操作  
    #   CASCADE意味着如果删除一个作者，将自动删除所有与这个作者关联的文章
    # related_name参数设置了从User到Post的反向关联关系，用blog_posts为这个反向关联关系命名
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    # 默认按照发布时间的逆序将查询结果排序
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title