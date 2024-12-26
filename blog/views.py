from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse

from blog.models import Article, Image, Video

from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.


def article_content(request):
    if request.method == 'POST':
        # 获取文章 ID 用于编辑现有文章
        article_id = request.POST.get('article_id')
        article = None

        if article_id:
            article = get_object_or_404(Article, article_id=article_id)

        # 获取表单数据
        title = request.POST.get('title')
        brief_content = request.POST.get('brief_content')
        content = request.POST.get('content')

        # 处理上传的图片和视频
        if 'images' in request.FILES:
            images = request.FILES.getlist('images')  # 获取所有上传的图片
            for img in images:
                Image.objects.create(article=article, image=img)  # 创建图片记录

        if 'videos' in request.FILES:
            videos = request.FILES.getlist('videos')  # 获取所有上传的视频
            for video in videos:
                Video.objects.create(article=article, video=video)  # 创建视频记录

        # 编辑或创建文章
        if article:
            article.title = title
            article.brief_content = brief_content
            article.content = content
            article.save()
        else:
            article = Article.objects.create(
                title=title,
                brief_content=brief_content,
                content=content
            )

        return HttpResponse(f'Article {article.article_id} saved successfully.')
    else:
        # 如果是 GET 请求，渲染创建或编辑表单
        article_id = request.GET.get('article_id')
        article = None
        if article_id:
            article = get_object_or_404(Article, article_id=article_id)

        # 获取与文章相关联的图片和视频
        images = Image.objects.filter(article=article)
        videos = Video.objects.filter(article=article)

        return render(request, 'article_form.html', {
            'article': article,
            'images': images,
            'videos': videos
        })



def get_index_page(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    print('page param: ', page)

    all_article = Article.objects.all()
    top10_article_list = Article.objects.order_by('-publish_date')[:10]

    paginator = Paginator(all_article, 6)
    page_num = paginator.num_pages
    print('page num:', page_num)
    page_article_list = paginator.page(page)
    if page_article_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_article_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page

    return render(request, 'blog/index.html',
                  {
                      'article_list': page_article_list,
                      'page_num': range(1, page_num + 1),
                      'curr_page': page,
                      'next_page': next_page,
                      'previous_page': previous_page,
                      'top10_article_list': top10_article_list
                  }
                )


def get_detail_page(request, article_id):
    # 获取所有文章并初始化前后文章的变量
    all_article = Article.objects.all()
    curr_article = None
    previous_index = 0
    next_index = 0
    previous_article = None
    next_article = None

    # 遍历文章列表来查找当前文章以及其前后文章
    for index, article in enumerate(all_article):
        if index == 0:
            previous_index = 0
            next_index = index + 1
        elif index == len(all_article) - 1:
            previous_index = index - 1
            next_index = index
        else:
            previous_index = index - 1
            next_index = index + 1

        if article.article_id == article_id:
            curr_article = article
            previous_article = all_article[previous_index]
            next_article = all_article[next_index]
            break

    # 将文章内容按换行符分割
    section_list = curr_article.content.split('\n')

    # 渲染模板并传递数据
    return render(request, 'blog/detail.html', {
        'curr_article': curr_article,
        'section_list': section_list,
        'previous_article': previous_article,
        'next_article': next_article,
        'images': curr_article.images.all(),  # 传递该文章的所有附加图片
    })


def search_view(request):
    query = request.GET.get('query', '')
    issearch=False
    articles = Article.objects.all()
    if query:
        # 使用 Django 的 Q 对象进行复杂查询，这里进行了标题和内容的模糊匹配
        search_articles = Article.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        issearch = True
        # 获取前10篇文章
        top10_article_list = search_articles[:10]
    else:

        top10_article_list = articles[:10]

    return render(request, 'blog/search.html', {
        'articles': articles,
        'query': query,
        'top10_article_list': top10_article_list,
        'issearch':issearch
    })