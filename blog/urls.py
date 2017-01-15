from django.conf.urls import url

from blog import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^article/(?P<blog_id>\d+)/$', views.post),
    url(r'^category/(?P<slug>\d+)/$', views.category)
]
