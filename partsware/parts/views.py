import re

from functools import reduce

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import Tag, Container, Part

@login_required
def index(request):
    tags = Tag.objects.filter(user=request.user)
    containers = Container.objects.filter(user=request.user)
    parts = Part.objects.filter(user=request.user)

    context = {
        'tags': tags,
        'containers': containers,
        'parts': parts,
    }

    return render(request, 'parts/index.html', context=context)

@login_required
@require_POST
def search(request):
    # retrieve query
    query = request.POST.get("search", None).strip()
    if not query:
        return redirect('parts:index')

    # pre-process query to all-lowercase and remove special chars
    query = query.lower()
    query = re.sub("[^0-9a-zA-Z]+", " ", query)

    # split query into its separate words
    query = query.split()

    def construct_query(word):
        q = Q(name__contains=word)
        q |= Q(description__contains=word)

        return q

    # build query from words
    q = reduce(lambda x, y: x | y, [construct_query(word) for word in query])

    # filter parts
    parts = Part.objects.filter(user=request.user)
    parts = parts.filter(q)

    # return results
    context = {
        'parts': parts
    }

    return render(request, 'parts/search.html', context=context)
