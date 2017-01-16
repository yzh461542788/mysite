import taggit
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from taggit.managers import TaggableManager

from blog.models import Blog, Category


# Create your views here.

def home(request):
    return HttpResponse("Too young, too simple. Sometimes naive.")


def post(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, "blog/blog_post.html", context={"blog": blog})


def category(request):
    cate = Category.objects.all()
    return render(request, 'blog/category.html', context={'category': cate})


def blog_list(request, cate_slug=None, tag_slug=None):
    if not cate_slug and not tag_slug:
        blogs = Blog.objects.all()
        title = None
    elif cate_slug:
        cate = get_object_or_404(Category, slug=cate_slug)
        blogs = Blog.objects.filter(category=cate)
        title = cate.title
    else:  # elif tag_slug
        try:
            tag = Blog.tags.get(slug=tag_slug)
            blogs = Blog.objects.filter(tags__slug__in=[tag_slug])
            title = tag.name
        except ObjectDoesNotExist:
            raise Http404('No such tag')
    return render(request, 'blog/blog_list.html', context={'blogs': blogs, 'title': title})
