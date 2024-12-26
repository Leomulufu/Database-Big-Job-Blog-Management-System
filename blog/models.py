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
    # 文章的主图片
    image = models.ImageField(upload_to='article_images/', null=True, blank=True)  # 这是主图
    # 文章的视频
    video = models.FileField(upload_to='article_videos/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # 如果文章没有设置主图片，并且存在与文章关联的图片，自动将第一张图片设置为主图片
        if not self.image:
            image = Image.objects.filter(article=self).first()  # 获取与该文章关联的第一张图片
            if image:
                self.image = image.image  # 将图片设置为文章的主图片
        super(Article, self).save(*args, **kwargs)  # 调用父类的保存方法

    def __str__(self):
        return self.title

class Image(models.Model):
    # 外键关联到文章，表示每篇文章可以有多个附加图片
    article = models.ForeignKey(Article, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='article_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)  # 可选的图像说明

    def __str__(self):
        return f"Image for {self.article.title}"

class Video(models.Model):
    article = models.ForeignKey(Article, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='article_videos/')
    caption = models.CharField(max_length=255, blank=True, null=True)  # 可选的视频说明
  # 可选的视频说明

    def __str__(self):
        return f"Video for {self.article.title}"