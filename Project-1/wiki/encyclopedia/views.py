from django.shortcuts import render

from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    # retrieve entry using util
    content = util.get_entry(title)

    if content == None:
        return render(request, "encyclopedia/noentry.html")

    content_html = markdown2.markdown(content)

    return render(request, "encyclopedia/entry.html", {
        "content": content_html,
        "title": title
    })