import markdown2
from django.core.urlresolvers import reverse
from django.db import models
from taggit.managers import TaggableManager


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog.views.category', kwargs={'category': self.slug})


class Blog(models.Model):
    class Meta:
        ordering = ['-pub_date']

    title = models.CharField(max_length=150)
    md_content = models.TextField(blank=True)
    html_content = models.TextField(blank=True)
    brief_content = models.TextField(blank=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    last_edit_date = models.DateTimeField('last edited', auto_now=True)
    category = models.ForeignKey(Category)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.html_content = markdown2.markdown(self.md_content, extras=["fenced-code-blocks", "tables"])
        self.brief_content = self.html_content[:self.html_content.find(r'<!--more-->')]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog.views.article', kwargs={'blog_id': self.id})


class Image(models.Model):
    def get_path(self, filename):
        return 'content/images/{article}/{filename}'.format(article=self.article.id, filename=filename)

    article = models.ForeignKey(Blog, related_name='images')
    image = models.ImageField(upload_to=get_path)


class Project(models.Model):
    class Meta:
        ordering = ['-id']

    title = models.CharField(max_length=150)
    url = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title
