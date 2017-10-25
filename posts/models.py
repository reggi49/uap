from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType

from comments.models import Comment
class PostManager(models.Manager):
    def activate(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())
    def categories(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False)
# Create your models here.
def upload_location(instance, filename):
    #filebase, extension = filename.split(".")
    return "%s_%s" %(instance.id, filename)

class SlideShow(models.Model):
    title = models.CharField(max_length=256)
    summary = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=256)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='slideshow/%Y/%m')
    #album = models.ForeignKey(Album)
    active = models.BooleanField(default = False)

    def __unicode__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    content = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=120)
    level_select = (
        (0,'Parent Level'),
        (1,'Child Level'),
    )
    id_level = models.IntegerField(choices=level_select,default=0)
    id_parent = models.ForeignKey("self",null=True, blank=True)

    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("posts:post_categories", kwargs= {"id":self.id})
        # return "/categories/%d/" %(self.id)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    id_kategori = models.ForeignKey(Category, blank=True, null=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,null=True, blank=True)
    content = models.TextField()
    be_read = models.IntegerField(blank=True,default=0,null=True)
    draft = models.BooleanField(default = False)
    publish = models.DateField(auto_now = False,auto_now_add=False)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    def __unicode__(self):
        return self.image

    def get_absolute_url(self):
        return reverse("posts:post_detail", kwargs= {"slug":self.slug})
        # return "/posts/%s/" %(self.id)
    class Meta:
        ordering = ["-timestamp","-updated"]

    def get_markdown(self):
        content = self.content
        return mark_safe(markdown(content))

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs
    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

def create_slug (instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug = new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender = Post)
