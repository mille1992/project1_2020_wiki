from django.shortcuts import render
from django import forms
from . import util

class NewSearchForm(forms.Form):
    search = forms.CharField(label="New Search")

def index(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            searchInput = form.cleaned_data['search']
            content = util.get_entry(searchInput)
        
            return render(request, "encyclopedia/entry.html", {
                "entryTitle": searchInput, "entryContent": content
            })
        else:
            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": NewSearchForm()
        })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": NewSearchForm()
        })


def entry(request, title):
    content = util.get_entry(title)
    if content is not None:
        return render(request, "encyclopedia/entry.html", {
            "entryTitle": title, "entryContent": content
        })
    else:

        return render(request, "encyclopedia/error.html", {
            "title": title
        })
