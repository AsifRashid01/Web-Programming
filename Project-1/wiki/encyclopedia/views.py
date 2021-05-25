from django.shortcuts import render, redirect
#from django import forms
from django.http import HttpResponseRedirect, HttpResponse

from . import util
import markdown2

#class NewTaskForm(forms.Form):
 #   task = forms.CharField(label="Entry Query")


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