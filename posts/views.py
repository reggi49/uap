from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from .models import Post
from    .forms import PostForm

def post_create(request):
    form = PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,"Berhasil Menambah Artikel")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.success(request,"Gagal Menambah Artikel")
    context = {
        "form":form,
    }
    return render(request,"post_form.html",context)

def post_detail(request,id):
    instance = get_object_or_404(Post, id=id)
    context = {
        "title": instance.title,
        "instance":instance
    }
    return render(request,"post_detail.html",context)
    # return HttpResponse("<h1>posts</h1>")

def post_list(request):
    queryset_list = Post.objects.all()
    paginator = Paginator (queryset_list,10)

    page = request.GET.get('page')
    try:
        queryset =  paginator.page(page)
    except PageNotAnInteger:
        queryset  = paginator.page(1)
    except EmptyPage:
        queryset  = paginator.page(Paginator.num_pages)

    context = {
        "object_list" : queryset
    }
    return render(request,"post_list.html",context)
    # return HttpResponse("<h1>list</h1>")

def post_update(request,id=None):
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
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request,"Berhasil Menghapus Artikel")
    return redirect("posts:post_list")
