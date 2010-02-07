
from django import forms
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from posterousq.forms import PostForm
from posterousq.models import Post
from posterousq.utils import JsonHttpResponse, coerce_put_post


def form(request, id=None):    
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        post = None
    return render_to_response(
        'posterousq/form.html', 
        {'form': PostForm(instance=post)},
        context_instance=RequestContext(request),
    )
    
def post(request, id=None):
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return JsonHttpResponse({'valid': True}, status=201)
        else:
            return JsonHttpResponse({'valid': False,'data': form.errors}, status=400)
    elif request.method == 'PUT':
        post = get_object_or_404(Post, pk=id)
        coerce_put_post(request)
        form = PostForm(instance=post, data=request.PUT, files=request.FILES)
        if form.is_valid():
            form.save()
            return JsonHttpResponse({'valid': True}, status=200)
        else:
            return JsonHttpResponse({'valid': False,'data': form.errors}, status=409)
    elif request.method == 'DELETE':
        post = get_object_or_404(Post, pk=id)
        post.delete()
        return HttpResponse(status=204)
    else:
        if id is not None:
            return JsonHttpResponse({'valid': True,'data': get_object_or_404(Post, pk=id)}, status=200)
        else:
            return JsonHttpResponse({'valid': True, 'data': Post.objects.all()}, status=200)

def not_found(request):
    return HttpResponseNotFound()