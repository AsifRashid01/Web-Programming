from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from . import util
import markdown2

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title")
    content = forms.CharField(widget=forms.Textarea)

    content.widget.attrs.update(size='30')


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)

    if content == None:
        return render(request, "encyclopedia/noentry.html")

    content_html = markdown2.markdown(content)

    return render(request, "encyclopedia/entry.html", {
        "content": content_html,
        "title": title
    })

def search(request):

    q = request.GET.get('q').strip()
    if q in util.list_entries():
        return redirect("entry", title=q)

    related_entries = [entry for entry in util.list_entries() if q.lower() in entry.lower()]

    if related_entries == []:
        return render(request, "encyclopedia/noentry.html")

    return render(request, "encyclopedia/search.html", {"entries": related_entries, "q": q})

def new_page(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        entry_form = NewEntryForm(request.POST)
        
        # check whether it's valid:
        if entry_form.is_valid():
            
            # process the data in form.cleaned_data as required
            entry_title = entry_form.cleaned_data["title"]
            entry_content = entry_form.cleaned_data["content"]
            
            print(entry_title)
            print(entry_content)
            
            # Check if title exists, if not then save it
            saved_entries = [x.lower() for x in util.list_entries()]

            if entry_title.lower() in saved_entries:
                return HttpResponse("Entry already exists!")
            
            util.save_entry(entry_title, entry_content)
            
            # redirect to the new entry page:
            return redirect("entry", title=entry_title)

    # if a GET (or any other method) we'll create a blank form
    else:
        entry_form = NewEntryForm()


    return render(request, "encyclopedia/new_page.html", {
        "form": entry_form
    })