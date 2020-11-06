from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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
