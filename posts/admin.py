from django.contrib import admin
from .models import Post, SlideShow, Contact, Category
# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title","updated","timestamp"]
    list_display_links = ["title","updated"]
    list_filter = ["updated","timestamp"]
    search_fields = ["title","content"]
    class Meta:
        model = Post

class SlideShowModelAdmin(admin.ModelAdmin):
    search_fields = ["title","summary"]
    class Meta:
        model = SlideShow

class ContactModelAdmin(admin.ModelAdmin):
    search_fields = ["name","email"]
    class Meta:
        model = Contact

class CategoryModelAdmin(admin.ModelAdmin):
    search_fields = ["name","id_level","id_kategori"]
    list_display = ["name","id_level","id_kategori"]
    class Meta:
        model = Category

admin.site.register(Post)
admin.site.register(SlideShow)
admin.site.register(Contact)
admin.site.register(Category)
