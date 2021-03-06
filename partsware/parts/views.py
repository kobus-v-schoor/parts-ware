import re
import mimetypes

from functools import reduce

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.exceptions import PermissionDenied

from parts.models import Tag, Container, Part
from parts.forms import ContainerForm, PartForm

@login_required
def index(request):
    tags = Tag.objects.filter(user=request.user)
    containers = Container.objects.filter(user=request.user)
    parts = Part.objects.filter(user=request.user)

    context = {
        'no_nav_search': True,
        'tags': tags,
        'containers': containers,
        'parts': parts,
    }

    return render(request, 'parts/index.html', context=context)

@login_required
def media(request, media_type, part_id):
    # check if the media type is allowed
    if media_type not in ['datasheet', 'pinout', 'image']:
        raise PermissionDenied()

    # retrieve the part object
    part = get_object_or_404(Part, pk=part_id)

    # check if the user owns the part
    if part.user != request.user:
        raise PermissionDenied()

    # get the file field
    if media_type == 'datasheet':
        file_field = part.datasheet
    elif media_type == 'pinout':
        file_field = part.pinout
    else:
        file_field = part.image

    # check if the file exists
    if not file_field:
        raise PermissionDenied()

    # try and guess file type
    mime_type, _ = mimetypes.guess_type(file_field.path)

    # get the file name for download
    fname = file_field.name

    # generate http response
    with open(file_field.path, 'rb') as f:
        response = HttpResponse(f, content_type=mime_type)
        response['Content-Disposition'] = f"filename={fname}"

    return response

@login_required
@require_POST
def search(request):
    # retrieve query
    query = request.POST.get("search", "").strip()

    # lowercase and split query into its separate words
    query = query.lower().split()

    tags = []
    words = []

    # separate query into tags and words
    for word in query:
        if word.startswith('tag:'):
            word = word[4:]
            if word:
                tags.append(word)
        else:
            words.append(word)

    # start with an empty query
    q = Q()

    # and all the tags
    if tags:
        for tag in tags:
            try:
                tag = Tag.objects.get(user=request.user, name=tag)
                q &= Q(tags=tag)
            except:
                pass

    # all the words are or'ed
    def word_query(word):
        q = Q(name__icontains=word)
        q |= Q(description__icontains=word)

        return q

    # final query looks like (tag & tag & (word | word | word))
    if words:
        q &= reduce(lambda x, y: x | y, [word_query(word) for word in words])

    # filter the parts
    q = Q(user=request.user) & q
    parts = Part.objects.filter(q)

    # sort results
    sort_by = request.POST.get('sort-by', 'name')
    if sort_by == 'container':
        parts = parts.order_by('container', 'location')
    elif sort_by == 'quantity':
        parts = parts.order_by('quantity')
    elif sort_by == 'price':
        parts = parts.order_by('price')

    # return results
    context = {
        'parts': parts,
        'query': request.POST.get("search", ""),
    }

    return render(request, 'parts/search.html', context=context)

@login_required
def all_parts(request):
    context = {
        'parts': Part.objects.filter(user=request.user),
    }

    return render(request, 'parts/search.html', context=context)

@login_required
def list_containers(request):
    containers = Container.objects.filter(user=request.user).order_by('name')

    context = {
        'containers': containers,
    }

    return render(request, 'parts/list_containers.html', context=context)

@login_required
def add_container(request):
    success = False

    if request.method == 'POST':
        form = ContainerForm(request.POST)
        if form.is_valid():
            container = form.save(commit=False)
            container.user = request.user
            container.save()
            success = True
    else:
        form = ContainerForm()

    context = {
        'new_container': True,
        'success': success,
        'post_url': reverse('parts:add_container'),
        'form': form,
    }

    return render(request, 'parts/container.html', context=context)

@login_required
def edit_container(request, container_id):
    container = get_object_or_404(Container, pk=container_id)

    # check if user owns container
    if container.user != request.user:
        raise PermissionDenied()

    success = False

    if request.method == 'POST':
        form = ContainerForm(request.POST, instance=container)
        if form.is_valid():
            form.save()
            success = True
    else:
        form = ContainerForm(instance=container)

    context = {
        'new_container': False,
        'has_parts': container.part_set.exists(),
        'success': success,
        'post_url': reverse('parts:edit_container',
                            kwargs={'container_id': container_id}),
        'form': form,
        'container_id': container.pk,
    }

    return render(request, 'parts/container.html', context=context)

@login_required
def delete_container(request, container_id):
    container = get_object_or_404(Container, pk=container_id)

    # check if user owns container
    if container.user != request.user:
        raise PermissionDenied()

    container.delete()

    return redirect('parts:list_containers')

@login_required
def view_part(request, part_id):
    part = get_object_or_404(Part, pk=part_id)

    if part.user != request.user:
        raise PermissionDenied()

    context = {
        'part': part,
    }

    return render(request, 'parts/view_part.html', context=context)

@login_required
def add_part(request):
    success = False

    if request.method == 'POST':
        form = PartForm(request.POST, request.FILES)
        form.user = request.user
        if form.is_valid():
            # create part
            part = form.save(commit=False)
            part.user = request.user

            # parse tags field
            tags = [s.strip() for s in form.cleaned_data['tags'].split(',')]

            if tags:
                # save part so we can add the tags
                part.save()

                # get/create tags and add them to the part
                for tag in tags:
                    tag, created = Tag.objects.get_or_create(user=request.user,
                                                             name=tag)
                    part.tags.add(tag)

            part.save()
            success = True
            form = PartForm()
    else:
        form = PartForm()

    # filter out the containers to only contain this user's containers
    containers = Container.objects.filter(user=request.user)
    form.fields["container"].queryset = containers

    context = {
        'new_part': True,
        'success': success,
        'form': form,
        'post_url': reverse('parts:add_part'),
    }

    return render(request, 'parts/part.html', context=context)

@login_required
def edit_part(request, part_id):
    part = get_object_or_404(Part, pk=part_id)

    if part.user != request.user:
        raise PermissionDenied()

    success = False

    if request.method == 'POST':
        form = PartForm(request.POST, request.FILES, instance=part)
        form.user = request.user

        if form.is_valid():
            part = form.save(commit=False)

            # parse tags field
            tags = [s.strip() for s in form.cleaned_data['tags'].split(',')]

            part.tags.clear()
            if tags:
                # get/create tags and add them to the part
                for tag in tags:
                    tag, created = Tag.objects.get_or_create(user=request.user,
                                                             name=tag)
                    part.tags.add(tag)

            # update part
            part.save()
            success = True

            # repopulate form so that newly-upload files are also shown
            form = PartForm(instance=part,
                            initial={'tags': form.cleaned_data['tags']})

    else:
        tag_str = ','.join(str(t) for t in part.tags.all())
        form = PartForm(instance=part, initial={'tags': tag_str})

    context = {
        'new_part': False,
        'form': form,
        'part': part,
        'success': success,
        'post_url': reverse('parts:edit_part', kwargs={'part_id': part_id}),
    }

    return render(request, 'parts/part.html', context=context)

@login_required
def delete_part(request, part_id):
    part = get_object_or_404(Part, pk=part_id)

    if part.user != request.user:
        raise PermissionDenied()

    part.delete()

    return redirect('parts:index')
