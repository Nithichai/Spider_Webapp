from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', view=views.spider_webpage),
    url('^/graph_json', view=views.show_graph, name='show_graph')
]
