
from django.conf import settings
from django.urls import path
from . import views
import blog.views
from django.conf.urls.static import static
from django.views.static import serve

app_name = 'blog'  # 设置命名空间为 'blog'
urlpatterns = [
    path('index', blog.views.get_index_page),
    path('detail/<int:article_id>', blog.views.get_detail_page),
    path(r'media/(?P<path>.*)', serve,{'document_root': settings.MEDIA_ROOT}),
    path('search/', blog.views.search_view, name='search'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # 为媒体文件提供访问路径
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)