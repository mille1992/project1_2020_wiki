from django.shortcuts import render
from django import forms
from . import util

class NewSearchForm(forms.Form):
    search = forms.CharField(label="New Search")

def index(request):
    EmptyForm = NewSearchForm()
    # if the page is called from the Search form
    if request.method == "POST":
        # get form data
        PostedForm = NewSearchForm(request.POST)
        # check form validity
        if PostedForm.is_valid():
            # pass form search data into variable
            searchInput = PostedForm.cleaned_data['search']
            content = util.get_entry(searchInput)
            # if search input has an exact entry match
            if content is not None:
                return render(request, "encyclopedia/entry.html", {
                    "entryTitle": searchInput, 
                    "entryContent": content,
                    "form": EmptyForm
                })
            # if search input has not an exact or no entry match
            else:
                # check for submatches in entries list
                matchedEntries = util.match_entries(searchInput)
                # if submatches were found display links to those matches
                if matchedEntries is not None:
                    return render(request, "encyclopedia/index.html", {
                        "entries": matchedEntries,
                        "form": EmptyForm
                    })
                else:
                    return render(request, "encyclopedia/error.html", {
                        "title": searchInput,
                        "form": EmptyForm
                    })
        else:
            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": EmptyForm
        })
    # if the page is called by any other but a POST request
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": EmptyForm
        })


def entry(request, title):
    content = util.get_entry(title)
    EmptyForm = NewSearchForm()
    if content is not None:
        return render(request, "encyclopedia/entry.html", {
            "entryTitle": title,
            "entryContent": content,
            "form": EmptyForm
        })
    else:

        return render(request, "encyclopedia/error.html", {
            "title": title,
            "form": EmptyForm
        })
