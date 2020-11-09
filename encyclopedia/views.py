from django.shortcuts import render
from django import forms
from . import util
import random
import markdown2
from markdown2 import Markdown


class NewSearchForm(forms.Form):
    search = forms.CharField(label="New Search")


class NewCreateEntryForm(forms.Form):
    newTitle = forms.CharField(label="New title")
    newContent = forms.CharField(label="New entry", widget=forms.Textarea(
        attrs={"rows": 1, "cols": 1, "width": 50}))

def index(request):
    EmptyForm = NewSearchForm()
    entrylist = util.list_entries()
    randomEntry = random.choice(entrylist)
    markdowner = Markdown() 

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
                content = markdowner.convert(content)
                return render(request, "encyclopedia/entry.html", {
                    "entryTitle": searchInput,
                    "entryContent": content,
                    "form": EmptyForm,
                    "randomEntry": randomEntry
                })
            # if search input has not an exact or no entry match
            else:
                # check for submatches in entries list
                matchedEntries = util.match_entries(searchInput)
                # if submatches were found display links to those matches
                if matchedEntries is not None:
                    return render(request, "encyclopedia/index.html", {
                        "entries": matchedEntries,
                        "form": EmptyForm,
                        "randomEntry": randomEntry
                    })
                else:
                    return render(request, "encyclopedia/error.html", {
                        "title": searchInput,
                        "form": EmptyForm,
                        "errorMessage": f" Your search: {{searchInput}}, did not yield any result. Please try another search input.",
                        "randomEntry": randomEntry
                    })
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(),
                "form": EmptyForm,
                "randomEntry": randomEntry
            })
    # if the page is called by any other but a POST request
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": EmptyForm,
            "randomEntry": randomEntry
        })


def entry(request, title):
    content = util.get_entry(title)
    entrylist = util.list_entries()
    EmptyForm = NewSearchForm()
    randomEntry = random.choice(entrylist) 
    markdowner = Markdown() 

    if content is not None:
        content = markdowner.convert(content)
        return render(request, "encyclopedia/entry.html", {
            "entryTitle": title,
            "entryContent": content,
            "form": EmptyForm,
            "randomEntry": randomEntry
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "form": EmptyForm,
            "errorMessage": f" Your search: <b><u>{ title }</b></u>, did not yield any result. Please try another search input.",
            "randomEntry": randomEntry
        })


def createNewEntry(request):
    EmptyForm = NewSearchForm()
    entrylist = util.list_entries()
    randomEntry = random.choice(entrylist) 
    markdowner = Markdown() 

    if request.method == "POST":
        CreatedEntryForm = NewCreateEntryForm(request.POST)
        if CreatedEntryForm.is_valid():
            createdEntryTitle = CreatedEntryForm.cleaned_data['newTitle']
            createdEntryContent = CreatedEntryForm.cleaned_data['newContent']
            # check whether entry already exists otherwise present error
            checkEntryExistance = util.get_entry(createdEntryTitle)
            # if entry already exists
            if checkEntryExistance is None:
                # save entry submitted via POST request
                util.save_entry(createdEntryTitle, createdEntryContent)
                createdEntryContent = markdowner.convert(createdEntryContent)
                return render(request, "encyclopedia/entry.html", {
                    "entryTitle": createdEntryTitle,
                    "entryContent": createdEntryContent,
                    "form": EmptyForm,
                    "randomEntry": randomEntry
                })
            # if entry does exist already, render error message
            else:
                return render(request, "encyclopedia/error.html", {
                    "title": "Saving unsuccessful",
                    "form": EmptyForm,
                    "errorMessage": f"The entry <i><b>{createdEntryTitle}</i></b> already exists. Please go to that entry and edit it instead.",
                    "randomEntry": randomEntry
                })
        # if form data is not valid
        else:
            return render(request, "encyclopedia/error.html", {
                "title": "Saving unsuccessful",
                "form": EmptyForm,
                "errorMessage": f" Your entry could not be saved",
                "randomEntry": randomEntry
            })
    # if request method is not POST, render a templated to input a new entry
    else:
        CreateEntryForm = NewCreateEntryForm()
        return render(request, "encyclopedia/createEntry.html", {
            "entryForm": CreateEntryForm,
            "form": EmptyForm,
            "randomEntry": randomEntry
        })


def editEntry(request, entryTitle):
    entrylist = util.list_entries()
    randomEntry = random.choice(entrylist) 
    entryContent = util.get_entry(entryTitle)
    EmptyForm = NewSearchForm()
    markdowner = Markdown() 

    if request.method == "POST":
            print(request.POST)
            editedcontent = request.POST["editedContent"] 
            util.save_entry(entryTitle, editedcontent)
            editedcontent = markdowner.convert(editedcontent)
            return render(request, "encyclopedia/entry.html", {
                "entryTitle": entryTitle,
                "entryContent": editedcontent,
                "form": EmptyForm,
                "randomEntry": randomEntry
            })
    else:
        # if entry exists edit it else error
        if entryContent is not None:
            return render(request, "encyclopedia/editEntry.html", {
                "entryTitle": entryTitle,
                "entryContent": entryContent,
                "form": EmptyForm,
                "randomEntry": randomEntry
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "title": "Entry not found",
                "form": EmptyForm,
                "errorMessage": f" The entry you are trying to edit could no tbe found",
                "randomEntry": randomEntry
            })    
        

