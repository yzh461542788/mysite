from django.http import HttpResponse
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import render


# Create your views here.
def home(request):
    url = static('x.jpg')
    return HttpResponse(render(request, template_name='home.html'))


def doc(request, doc_id, max_page):
    return HttpResponse(render(request, template_name='doc.html',
                               context={'pages': list(range(int(max_page))), 'doc_id': doc_id}))
