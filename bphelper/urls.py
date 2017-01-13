from django.conf.urls import url
from bphelper import views

urlpatterns = [
    url(r'^$', view=views.home),
]
