from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
