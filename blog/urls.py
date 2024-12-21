
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
import blog.views


urlpatterns = [
    path('index', blog.views.get_index_page),
    path('detail/<int:article_id>', blog.views.get_detail_page)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)