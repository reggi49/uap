from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from markdown_deux import markdown
from django.utils.safestring import mark_safe

from comments.models import Comment
class PostManager(models.Manager):
    def activate(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())
# Create your models here.
def upload_location(instance, filename):
    #filebase, extension = filename.split(".")
    return "%s_%s" %(instance.id, filename)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,null=True, blank=True)
    content = models.TextField()
    draft = models.BooleanField(default = False)
    publish = models.DateField(auto_now = False,auto_now_add=False)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()
    def __unicode__(self):
        return self.title
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
