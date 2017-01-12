from django.conf.urls import url

from cleandocin import views

urlpatterns = [
    url(r'^$', view=views.home, name='home'),
    url(r'^doc/(?P<doc_id>[0-9]+)/(?P<max_page>[0-9]+)/$', view=views.doc, name='doc')
]
