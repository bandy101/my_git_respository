from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count

def post_list(request,tag_slug=None):
    # posts = Post.published.all()
    # return render(request, 'blog/post/list.html', {'posts': posts})
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    # 使用django 自带分页
    paginator = Paginator(object_list,2) # 每页显示三篇文章
    page = request.GET.get('page') # django自带分页参数
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page参数非整数返回第一页
        posts  = paginator.page(1)
    except EmptyPage:
        # 如果超出总页数返回最后一页
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{'page':page,'posts':posts,'tag':tag})

from .forms import CommentForm

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status="published", publish__year=year, publish__month=month,
                             publish__day=day)

    new_comment =  None                         
    # 通过外键对post对象执行查询获得所需的QuerySet()
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():     # 验证表单数据
            # 通过表单直接创建数据对象 不提交到数据库
            new_comment = comment_form.save(commit=False)
            # 设置外键为当前文章
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()       
    
        # 显示相近Tag的文章列表
    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_tags = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_tags.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    
    # values_list方法返回指定的字段的值构成的元组，通过指定flat=True，让其结果变成一个列表比如[1, 2, 3, ...]
    # 选出所有包含上述标签的文章并且排除当前文章
    # 使用Count对每个文章按照标签计数，并生成一个新字段same_tags用于存放计数的结果
    # 按照相同标签的数量，降序排列结果，然后截取前四个结果作为最终传入模板的数据对象。

    return render(request, 'blog/post/detail.html', {'post': post,'comments':comments,'new_comment':new_comment,'comment_form':comment_form,'similar_posts':similar_posts})

from  django.views.generic import ListView
class PostListView(ListView):
    # Django内置的ListView返回的变量名称叫做page_obj 修改模板T
    # model = Post    # 可用queryset = Post.published.all() 替代
    queryset = Post.published.all()
    print (queryset)
    context_object_name='posts'    # 如果不设置context_object_name参数，默认的变量名称是object_list
    paginate_by = 2 # 每页的显示文章数
    template_name = 'blog/post/list.html'

from .forms import EmailPostForm
def post_share(request,post_id):
    post = get_object_or_404(Post,id=post_id,status='published')
    sent = False
    if request.method=='POST':
        # 表单提交
        form = EmailPostForm(request.POST)
        if form.is_valid(): # 验证表单数据是否有效
    #   如果表单验证成功，可以通过form.cleaned_data属性访问表单内所有通过验证的数据，这个属性类似于一个字典，包含字段名与值构成的键值对。
    #   如果表单验证失败，form.cleaned_data只会包含通过验证的数据。
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, '1255381744@qq.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'form':form,'post':post,'sent':sent})