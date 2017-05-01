from django import forms


class SpiderWordForm(forms.Form):
    word_search = forms.CharField(label="WORD SEARCH", max_length=100)
