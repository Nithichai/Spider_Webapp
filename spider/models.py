from __future__ import print_function
from __future__ import unicode_literals
# from django.db import models
from urlparse import urlparse
# from nodebox.graphics.physics import Graph
import networkx
import os
import json
import operator


class SpiderGraph:
    def __init__(self):
        self.indexing_dict = {}
        self.list_website = []
        self.pack_indexing()
        self.refresh_weblist()

    def pack_indexing(self):
        for file_name in os.listdir(os.getcwd() + "\\indexing"):
            file_read = open(os.getcwd() + "\\indexing\\" + file_name, "r+")
            self.indexing_dict.update(json.loads(file_read.read()))
            file_read.close()

    def refresh_weblist(self):
        self.list_website = []
        for file_name in os.listdir(os.getcwd() + "\\websiteList"):
            name = file_name.replace("_", ".").replace("#", "/").replace("$", ":").replace(".json", "")
            self.list_website.append(name)
        return self.list_website

    def set_graph_dict(self, website):
        website = self.set_website(website)
        file_name = self.get_file_name(website)
        json_dict = self.get_json_dict(file_name)
        if json_dict == "no website":
            return {}
        graph = self.get_graph(website, json_dict)
        used_dict = self.set_n_used(website, json_dict)
        node_list, edge_list = self.get_dict_for_website(graph, used_dict)
        return {"nodes": node_list, "links": edge_list}

    def set_website(self, website):
        if len(website) > 0:
            parsed_uri = urlparse(website)
            if parsed_uri.scheme == "" or parsed_uri.netloc == "":
                return ""
            return ('{uri.scheme}://{uri.netloc}{uri.path}'.format(uri=parsed_uri)).strip("/")
        return ""

    def get_file_name(self, website):
        website = self.website_formatter(website)
        return website.replace(".", "_").replace("/", "#").replace(":", "$") + ".json"

    def get_json_dict(self, file_name):
        if file_name not in os.listdir(os.getcwd() + "\\websiteList"):
            return "no website"
        file_data = open(os.getcwd() + "\\websiteList\\" + file_name, "r+")
        json_string = file_data.read()
        file_data.close()
        return json.loads(json_string)

    def get_netloc(self, website):
        return urlparse(website).netloc.encode("ascii", "ignore")

    def website_formatter(self, website):
        parsed_uri = urlparse(website)
        return ('{uri.scheme}://{uri.netloc}{uri.path}'.format(uri=parsed_uri)).strip("/")

    def get_graph(self, root_website, json_dict):
        g = networkx.DiGraph()
        for netloc_uni in json_dict[root_website]:  # use netloc in json_dict
            netloc = netloc_uni.encode("ascii", "ignore")  # change unicode to string
            for website_uni in json_dict[root_website][netloc]:  # use website in json_dict
                website = website_uni.encode("ascii", "ignore")  # change unicode to string
                if self.get_netloc(website) != "":  # netloc has word
                    g.add_node(self.get_netloc(website))  # add netloc in draw graph
                # use child website
                for child_website_uni in json_dict[root_website][netloc][website]["website"]:
                    child_website = child_website_uni.encode("ascii", "ignore")
                    # add netloc of child website into draw graph
                    if self.get_netloc(child_website) != "":
                        g.add_node(self.get_netloc(child_website))
                    # detect netloc of website and child-website is not same
                    if self.get_netloc(website) != self.get_netloc(child_website) \
                            and self.get_netloc(website) != "" \
                            and self.get_netloc(child_website) != "":
                        # add edge website to child-website to draw graph
                        g.add_edge(self.get_netloc(child_website), self.get_netloc(website))
        return g

    def set_n_used(self, root_website, json_dict):
        dict_netloc_used = {}
        for netloc in json_dict[root_website]:  # use netloc in json_dict
            netloc = netloc.encode("ascii", "ignore")  # change unicode to string
            if netloc not in dict_netloc_used:  # netloc not in dict used
                dict_netloc_used[netloc] = 0  # set netloc in dict and set 0
            for website in json_dict[root_website][netloc]:  # get website in dict
                website = website.encode("ascii", "ignore")  # change unicode to string
                # netloc has word
                if self.get_netloc(website) != "" and self.get_netloc(website) not in dict_netloc_used:
                    dict_netloc_used[self.get_netloc(website)] = 0
                # get child website in list
                for child_website in json_dict[root_website][netloc][website]["website"]:
                    child_website = child_website.encode("ascii", "ignore")  # encode website
                    # child's netloc not in dict used
                    if self.get_netloc(child_website) not in dict_netloc_used:
                        dict_netloc_used[self.get_netloc(child_website)] = 0  # set netloc in dict and set 0
                    # child's netloc and website's netloc is not same
                    if self.get_netloc(child_website) != netloc:
                        dict_netloc_used[self.get_netloc(child_website)] += 1  # add value in used dict
        return dict_netloc_used

    def get_dict_for_website(self, g, used):
        node_list = []
        for node in g.nodes():
            node_list.append({"id": str(node)})
        edge_list = []
        for edge in g.edges():
            edge_list.append({"source": str(edge[0]), "target": str(edge[1])})
        return node_list, edge_list

    def ranking(self, word):
        rank_dict = {}
        for word_in in self.indexing_dict:  # get word from list
            # sort data
            rank_dict[word_in] = sorted(self.indexing_dict[word_in].items(), key=operator.itemgetter(1), reverse=True)

        dict_index = {}
        word = word.strip().lower()  # set word to lower
        word_list = word.split()  # get list word from GUI
        if len(word_list) == 1:  # Found only one word
            if word in rank_dict:  # detect word is in word dict
                for data_pack in rank_dict[word]:  # loop data pack from dict of word
                    website = data_pack[0]  # get website
                    n_used = data_pack[1]["used"]  # get number of used
                    n_word = data_pack[1]["word"]  # get number of word
                    dict_index[website] = [n_used, n_word]
        elif len(word_list) > 1:  # Word more than 1
            list_set_website = []  # Set list of website set
            index_set = 0  # Set index of set
            for word in word_list:  # Loop word in word list
                if word in rank_dict:  # Detect word is in list
                    list_set_website.append(set())  # Add set to list
                    for data_pack in rank_dict[word]:  # get data pack from dict of word
                        website = data_pack[0]  # get website
                        list_set_website[index_set].add(website)  # Set website into set
                else:
                    del word_list[word_list.index(word)]  # delete word that not found
                index_set += 1  # add index of set

            if len(word_list) == 0 or len(list_set_website) == 0:
                return {}
            else:
                total_set = list_set_website[0]  # get set of first word
                for i in range(1, len(list_set_website)):  # loop to get all set
                    total_set = total_set & list_set_website[i]  # find website is same
                for data_pack in rank_dict[word_list[0]]:  # get data pack
                    website = data_pack[0]  # get website
                    if website in total_set:  # website in set
                        n_used = data_pack[1]["used"]  # get number of used
                        n_word = data_pack[1]["word"]  # get number of word
                        dict_index[website] = [n_used, n_word]
        print(dict_index)
        return dict_index
