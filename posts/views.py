
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
from .models import Post, SlideShow, Contact, Category
from .forms import PostForm,ContactForm
from .utils import get_read_time

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
    form = CommentForm(request.POST or None, initial = initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type  = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = obj_id,
            content = content_data,
            parent = parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    instance.be_read = instance.be_read+1
    instance.save(update_fields=['be_read'])
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
    queryset_list = Post.objects.activate()[:7]
    slideshow_list = SlideShow.objects.all()
    most_read  = Post.objects.order_by('-be_read')[:6]
    categories = Category.objects.filter(id_level= 0)
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.activate()[:7]
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
        "page_request_var" : page_request_var,
        "today" : today,
        "slideshow" :slideshow_list,
        "most_read" : most_read,
        "categories" : categories,
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

def post_contact(request):
    form = ContactForm(request.POST or None,request.FILES or None)
    categories = Category.objects.filter(id_level= 0)
    if form.is_valid():
        name = form.cleaned_data.get("name")
        email = form.cleaned_data.get("email")
        content_data = form.cleaned_data.get("content")

        new_contact, created = Contact.objects.get_or_create(
            name = name,
            email = email,
            content = content_data,
        )
        messages.success(request,"Succesfull send a messages")
        return HttpResponseRedirect('/contact/')
    context = {
        "contact_form":form,
        "categories" : categories,
    }
    return render(request,"post_contact.html",context)

def post_indeks(request):
    today = timezone.now().date()
    queryset_list = Post.objects.activate()[7:]
    categories = Category.objects.filter(id_level= 0)
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.activate()[7:]
    query = request.GET.get("search")
    queryset_search = Post.objects.all()
    if query:
        queryset_list = queryset_search.filter(
        Q(title__icontains =query)|
        Q(content__icontains =query)).distinct()
        if queryset_list.count() > 0 :
            messages.success(request,"Articles found",extra_tags='some-tags')
        else:
            messages.success(request,"Not found article like ",extra_tags='some-tags')
    paginator = Paginator (queryset_list,8)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset =  paginator.page(page)
    except PageNotAnInteger:
        queryset  = paginator.page(1)
    except EmptyPage:
        queryset  = paginator.page(Paginator.num_pages)

    context = {
        "title" : 'Indeks',
        "object_list" : queryset,
        "page_request_var" : page_request_var,
        "today" : today,
        "categories" : categories,
    }
    return render(request,"post_indeks.html",context)

def post_categories(request,id=None):
    today = timezone.now().date()
    # id_parent = Post.objects.select_related().filter(id_kategori__id_kategori__id_parent=id)
    # print id_parent
    queryset_list = Post.objects.filter(id_kategori__id_parent=id)
    print queryset_list
    categories = Category.objects.filter(id_level= 0)
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.filter(id_kategori=id)
    query = request.GET.get("search")
    paginator = Paginator (queryset_list,8)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset =  paginator.page(page)
    except PageNotAnInteger:
        queryset  = paginator.page(1)
    except EmptyPage:
        queryset  = paginator.page(Paginator.num_pages)

    context = {
        "title" : 'Categories',
        "object_list" : queryset,
        "page_request_var" : page_request_var,
        "today" : today,
        "categories" : categories,
    }
    return render(request,"post_indeks.html",context)
