
from django.contrib import messages
from urllib import quote_plus
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.contenttypes.models import ContentType

# Create your views here.
from comments.models import Comment
from comments.forms import CommentForm
from .models import Post
from .forms import PostForm

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    if not request.user.is_authenticated():
        raise Http404

    form = PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,"Berhasil Menambah Artikel")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.success(request,"Gagal Menambah Artikel")
    context = {
        "form":form,
    }
    return render(request,"post_form.html",context)

def post_detail(request,slug):
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_super:
            raise Http404
    share_string = quote_plus(instance.content)
    initial_data = {
        "content_type" : instance.get_content_type,
        "object_id": instance.id
    }
    form = ContentForm(request.Post or None, initial = initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type  = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        new_comment, created = Comment.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = obj_id,
            content = content_data,
        )
    comments = instance.comments
    context = {
        "title": instance.title,
        "instance":instance,
        "share_string": share_string,
        "comments" : comments,
        "comment_form" : form,
    }
    return render(request,"post_detail.html",context)
    # return HttpResponse("<h1>posts</h1>")

def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.activate()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    query = request.GET.get("search")
    if query:
        queryset_list = queryset_list.filter(
        Q(title__icontains =query)|
        Q(content__icontains =query)).distinct()
    paginator = Paginator (queryset_list,10)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset =  paginator.page(page)
    except PageNotAnInteger:
        queryset  = paginator.page(1)
    except EmptyPage:
        queryset  = paginator.page(Paginator.num_pages)

    context = {
        "object_list" : queryset,
        "page_request_var": page_request_var,
        "today":today,
    }
    return render(request,"post_list.html",context)
    # return HttpResponse("<h1>list</h1>")

def post_update(request,id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None,request.FILES or None, instance = instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,"Berhasil Mengedit Artikel",extra_tags='some-tags')
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.success(request,"Gagal Mengedit Artikel",extra_tags='some-tags')
    context = {
        "title": instance.title,
        "instance":instance,
        "form":form,
    }
    return render(request,"post_form.html",context)

def post_delete(request,id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request,"Berhasil Menghapus Artikel")
    return redirect("posts:post_list")
