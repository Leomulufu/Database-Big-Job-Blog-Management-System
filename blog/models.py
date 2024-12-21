from django.db import models
from tinymce.models import HTMLField

# Create your models here.

class Article(models.Model):
    # 文章的唯一ID
    article_id = models.AutoField(primary_key=True)
    # 文章标题
    title = models.TextField()
    # 文章的摘要
    brief_content = models.TextField()
    # 文章的主要内容
    content = models.TextField()
    # 文章的发布日期
    publish_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Image(models.Model):
    article = models.ForeignKey(Article, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='article_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)  # 可选的图像说明

    def __str__(self):
        return f"Image for {self.article.title}"


class Video(models.Model):
    article = models.ForeignKey(Article, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='article_videos/')
    caption = models.CharField(max_length=255, blank=True, null=True)  # 可选的视频说明

    def __str__(self):
        return f"Video for {self.article.title}"