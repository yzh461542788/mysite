import os
import re

import requests
import zipfile
from bs4 import BeautifulSoup
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import smart_str

from .models import *


# Create your views here.
def home(request):
    return render(request, 'clendocin/home.html')


def search(request):
    key = request.GET.get('key', None)
    if not key:
        return render(request, 'clendocin/home.html')
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
    return render(request, 'clendocin/search_result.html', context={'results': results})


def doc(request, doc_id):
    # first query doc id in local database
    try:
        document = Document.objects.get(id=doc_id)
    except Document.DoesNotExist:
        document = None
    if document:
        if not document.valid:
            raise Http404
    else:
        # if the doc id is not stored, send a request to docin.com to get doc info
        url = r'http://www.docin.com/p-{0}.html'.format(doc_id)
        response = requests.get(url)
        # the resource doesn't exist
        if not response.ok:
            Document.objects.create(id=doc_id, valid=False)
            raise Http404

        # get doc info from docin.com
        soup = BeautifulSoup(response.text, 'html.parser')
        doc_info = soup.find(class_='info_list')
        if not doc_info:
            Document.objects.create(id=doc_id, valid=False, pending=True)
            raise Http404
        doc_info = doc_info.contents
        document = Document()
        document.id = int(doc_id)
        document.title = soup.find(class_='doc_title').string
        document.fmt = doc_info[3].find('em').get('title')
        document.page_num = int(re.compile(r'[0-9]+').match(doc_info[7].string).group())
        document.size = doc_info[11].string
        document.valid = True
        document.save()
        if len(doc_info) > 23:
            for t in doc_info[23].find_all('a'):
                document.tag.add(Tag.objects.get_or_create(name=t.text)[0])
            document.save()
    return render(request, 'clendocin/doc.html',
                  context={'pages': list(range(int(document.page_num))),
                           'doc': document})


def download(request, doc_id):
    try:
        document = Document.objects.get(id=doc_id)
    except Document.DoesNotExist:
        document = None
    if document:
        if not document.valid:
            raise Http404
    else:
        # if the doc id is not stored, send a request to docin.com to get doc info
        url = r'http://www.docin.com/p-{0}.html'.format(doc_id)
        response = requests.get(url)
        # the resource doesn't exist
        if not response.ok:
            Document.objects.create(id=doc_id, valid=False)
            raise Http404

        # get doc info from docin.com
        soup = BeautifulSoup(response.text, 'html.parser')
        doc_info = soup.find(class_='info_list')
        if not doc_info:
            Document.objects.create(id=doc_id, valid=False, pending=True)
            raise Http404
        doc_info = doc_info.contents
        document = Document()
        document.id = int(doc_id)
        document.title = soup.find(class_='doc_title').string
        document.fmt = doc_info[3].find('em').get('title')
        document.page_num = int(re.compile(r'[0-9]+').match(doc_info[7].string).group())
        document.size = doc_info[11].string
        document.valid = True
        document.save()
        if len(doc_info) > 23:
            for t in doc_info[23].find_all('a'):
                document.tag.add(Tag.objects.get_or_create(name=t.text)[0])
            document.save()

    def zipdir(path, zip_file):
        for root, dirs, files in os.walk(path):
            for file in files:
                zip_file.write(os.path.join(root, file))

    swf_file = 'PageViewer.swf'
    path = 'static/cleandocin/'
    html_file = path + document.title + ".html"

    with open(html_file, "w") as f:
        f.write(
            render_to_string('clendocin/pure_doc.html', context={'pages': list(range(int(document.page_num))),
                                                                 'doc': document}))

    zip_name = document.title + ".zip"
    full_path = path + zip_name
    zout = zipfile.ZipFile(full_path, mode='w')
    zipdir(path + 'js/', zout)
    zout.write(html_file)
    zout.write(path + swf_file)
    zout.close()

    with open(full_path, 'rb') as f:
        response = HttpResponse(f, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{filename}"'.format(filename=zip_name)
        response['Content-Length'] = os.path.getsize(path + zip_name)

    os.remove(full_path)
    os.remove(html_file)
    return response
