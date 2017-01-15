from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from blog.models import Blog


# Create your views here.

def home(request):
    return HttpResponse("Too young, too simple. Sometimes naive.")


def post(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, "")


def category(request):
    return 'category'