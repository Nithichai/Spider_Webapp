from __future__ import print_function
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from models import SpiderGraph


dict_graph = {}
dict_index = {}
spider_graph = SpiderGraph()


def show_graph(request):
    global dict_graph
    return JsonResponse(dict_graph)

def spider_webpage(request):
    global dict_index, spider_graph, dict_graph
    if request.method == 'POST':
        if 'graph_text' in request.POST:
            dict_graph = spider_graph.set_graph_dict(request.POST['graph_text'])
        elif 'word_text' in request.POST:
            word = request.POST['word_text']
            dict_index = spider_graph.ranking(word)
        return render(request, 'spider_templates/home.html', {'index_dict': dict_index, 'list_website': spider_graph.refresh_weblist()})
    else:
        dict_graph = {}
    return render(request, 'spider_templates/home.html', {'list_website': spider_graph.refresh_weblist()})