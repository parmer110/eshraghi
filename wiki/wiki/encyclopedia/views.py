from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from markdown2 import Markdown

from . import util

class NewEntry(forms.Form):

    title = forms.CharField(label="", help_text="", max_length=30, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Title',
            'class': 'input-fld'
            }))

    entry = forms.CharField(label="", help_text="",   
        widget=forms.Textarea(attrs={
            'placeholder': 'Entry context...',
            'class': 'area-fld'
            }))
    
    submit = forms.CharField(label="", help_text="", 
        widget=forms.TextInput(attrs={
            'type': 'submit',
            'class': 'submit-btn',
            'value': 'Save'
        }))

    control = forms.CharField(required=False, label="", help_text="", widget=forms.TextInput(attrs={
        'type': 'text',
        'hidden': 'hidden',
        'value': ''
    }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    
    entry = util.get_entry(title)

    if request.method == "POST":
        form = NewEntry(initial={'entry': entry, 'title': title})
        form.fields['title'].widget.attrs={'hidden': 'hidden'}
        form.fields['control'].widget.attrs={'value': 'edit', 'hidden': 'hidden'}
        return render(request, "encyclopedia/editable.html", {
            "form": form
        })
    else:
        # The entry not exist
        if not entry:
            message = "The requested encyclopedia entry was not found!"
            url = "../static/specific/styles.css"
            return render(request, "specific/error.html", {
                "message": message,
                "bg": url,
                "header_title": "404"
            })
        # Return considered entry
        else:
            # MarkDown preperation
            markdowner = Markdown()
            entry = markdowner.convert(entry)
            
            return render(request, "encyclopedia/entry.html", {
                "title":title,
                "entry":entry,
                "entries": util.list_entries()
            })

def search(request):
    query = request.GET.get('q')
    if not query:
        return index(request)
    elif util.get_entry(query):
        return entry(request, query)
    else:
        f_lst=[]
        lst = util.list_entries()
        for item  in lst:
            l_item = item.lower()
            if query.lower() in l_item:
                f_lst.append(item)
        return render(request, "encyclopedia/search.html", {
            "entries": f_lst
        })

def new(request):
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["entry"]
            control = form.cleaned_data["control"]
            if control == "edit" or not util.get_entry(title):
                util.save_entry(title, content)
                if control == "edit":
                    request.method = "GET"
                    return entry(request, title)
                else:
                    return HttpResponseRedirect(reverse('index'))
            else:
                message = "This entry is existed!"
                url = "../static/specific/styles.css"
                return render(request, "specific/error.html", {
                    "message": message,
                    "bg": url,
                    "header_title": "Error!"
                })
        else:
            return render(request, "encyclopedia/editable.html", {
                "form": form
            })
    return render(request, "encyclopedia/editable.html", {
        "form": NewEntry()
    })
