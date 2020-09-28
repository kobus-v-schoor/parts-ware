import re
import mimetypes

from functools import reduce

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.exceptions import PermissionDenied

from .models import Tag, Container, Part
from .forms import ContainerForm

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
def download_datasheet(request, part_id):
    part = get_object_or_404(Part, pk=part_id)

    # check if user owns the part
    if part.user != request.user:
        raise PermissionDenied()

    # check if the part has a datasheet
    if not part.datasheet:
        raise PermissionDenied()

    # try and guess file type
    mime_type, _ = mimetypes.guess_type(part.datasheet.path)
    fname = part.datasheet.name

    # generate http response
    with open(part.datasheet.path, 'rb') as f:
        response = HttpResponse(f, content_type=mime_type)
        response['Content-Disposition'] = f"attachment; filename={fname}"

    return response

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
        q = Q(name__icontains=word)
        q |= Q(description__icontains=word)

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

@login_required
def add_container(request):
    successfully_added = False

    if request.method == 'POST':
        form = ContainerForm(request.POST)
        if form.is_valid():
            container = form.save(commit=False)
            container.user = request.user
            container.save()
            successfully_added = True
    else:
        form = ContainerForm()

    context = {
        'new_container': True,
        'successfully_added': successfully_added,
        'form': form,
    }

    return render(request, 'parts/container.html', context=context)
