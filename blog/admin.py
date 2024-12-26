from django.contrib import admin

# Register your models here.

from blog.models import Article, Image, Video

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1  # 默认显示 1 个空白的图片字段，可以上传图片

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1  # 默认显示 1 个空白的视频字段，可以上传视频

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date')  # 你可以根据需求调整显示字段
    search_fields = ('title', 'brief_content')
    list_filter = ('publish_date',)

    # 将图片和视频内联显示在文章表单中
    #inlines = [ImageInline, VideoInline]

    # 在表单中显示的字段
    fields = ('title', 'brief_content', 'content','image','video')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Image)  # 注册图片模型
admin.site.register(Video)  # 注册视频模型
