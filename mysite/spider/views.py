from __future__ import print_function
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import JsonResponse
from models import SpiderGraph


dict_graph = {}
dict_index = {}
spider_graph = SpiderGraph()


def show_graph(request):
    global dict_graph
    return JsonResponse(dict_graph)


def spider_webpage(request):
    if request.method == 'POST':
        global dict_index
        if 'graph_text' in request.POST:
            global dict_graph, spider_graph
            dict_graph = spider_graph.set_graph_dict(request.POST['graph_text'])
        elif 'word_text' in request.POST:
            word = request.POST['word_text']
            global spider_graph
            dict_index = spider_graph.ranking(word)
        return render(request, 'spider_templates/home.html', {'index_dict': dict_index})
    return render(request, 'spider_templates/home.html')

