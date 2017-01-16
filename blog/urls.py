from django.conf.urls import url

from blog import views

urlpatterns = [
    url(r'^$', views.blog_list),
    url(r'^article/(?P<blog_id>\d+)/$', views.post),
    url(r'^category/$', views.category),
    url(r'^category/(?P<cate_slug>.+)/$', views.blog_list),
    url(r'^tag/(?P<tag_slug>.+)/$', views.blog_list)
]
