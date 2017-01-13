from django.http import HttpResponse
from django.shortcuts import render
import re
import requests
from .models import *
from bs4 import BeautifulSoup


# Create your views here.
def home(request):
    return HttpResponse(render(request, template_name='clendocin/home.html'))


def search(request):
    key = request.GET.get('key', None)
    if not key:
        return HttpResponse(render(request, template_name='clendocin/home.html'))
    url = r'http://www.docin.com/search.do?searchcat=1001&nkey={key}'.format(key=key)
    response = requests.get(url)
    if not response.ok:
        return 404

    results = []
    soup = BeautifulSoup(response.text, 'html.parser')
    for result in soup.select('dl.clear'):
        title = result.find(class_='title').text.strip()
        href = result.find('a').get('href')
        href = '/cleandocin/doc/' + re.compile(r'/p-[0-9]+').match(href).group()[3:]
        results.append({'title': title, 'href': href})
    return HttpResponse(render(request, template_name='clendocin/search_result.html', context={'results': results}))


def doc(request, doc_id):
    # first query doc id in local database
    try:
        document = Document.objects.get(id=doc_id)
    except Document.DoesNotExist:
        document = None
    if document:
        if document.valid:
            return HttpResponse(render(request, template_name='clendocin/doc.html',
                                       context={'pages': list(range(document.page_num)),
                                                'doc_id': doc_id,
                                                'title': document.title}))
        else:
            return HttpResponse(404)
    else:
        # if the doc id is not stored, send a request to docin.com to get doc info
        url = r'http://www.docin.com/p-{0}.html'.format(doc_id)
        response = requests.get(url)
        # the resource doesn't exist
        if not response.ok:
            Document.objects.create(id=doc_id, valid=False)
            return HttpResponse(404)

        # get doc info from docin.com
        soup = BeautifulSoup(response.text, 'html.parser')
        doc_info = soup.find(class_='info_list')
        if not doc_info:
            Document.objects.create(id=doc_id, valid=False, pending=True)
            return HttpResponse(404)
        doc_info = doc_info.contents
        document = Document()
        document.id = int(doc_id)
        document.title = soup.find(class_='doc_title').string
        document.fmt = doc_info[3].find('em').get('title')
        document.page_num = int(re.compile(r'[0-9]+').match(doc_info[7].string).group())
        document.size = doc_info[11].string
        document.valid = True
        document.save()
        for t in doc_info[23].find_all('a'):
            document.tag.add(Tag.objects.get_or_create(name=t.text)[0])
        document.save()
        return HttpResponse(render(request, template_name='clendocin/doc.html',
                                   context={'pages': list(range(int(document.page_num))),
                                            'doc_id': doc_id,
                                            'title': document.title}))
