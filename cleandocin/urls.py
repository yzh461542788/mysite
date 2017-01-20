from django.conf.urls import url
from cleandocin import views

urlpatterns = [
    url(r'^$', view=views.home),
    url(r'^doc/(?P<doc_id>[0-9]+)/$', view=views.doc),
    url(r'^search/$', view=views.search),
    url(r'^search/', view=views.search),
    url(r'^download/(?P<doc_id>[0-9]+)/$', view=views.download)
]
