from __future__ import unicode_literals

from rest_framework import serializers

from posts.models import Post

post_detail_url = serializers.HyperlinkedIdentityField(
    view_name = 'posts-api:detail',
    lookup_field = 'pk'
    )

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'title',
            'id_kategori',
            'image',
            'content',
            'be_read',
            'draft',
            'publish',
        ]

class PostListSerializer(serializers.ModelSerializer):
    url = post_detail_url
    image = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'url',
            'id',
            'user',
            'title',
            'id_kategori',
            'slug',
            'image',
            'be_read',
            'draft',
            'publish',
            'updated',
            'timestamp'
        ]
    def get_image(self, obj):
        if 'http' in obj.image.url:
            try :
                image = obj.image.url
            except:
                image = None
        else:
            image = obj.image
        return image

class PostDetailSerializer(serializers.ModelSerializer):
    url = post_detail_url
    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'title',
            'id_kategori',
            'slug',
            'url',
            'image',
            'content',
            'be_read',
            'draft',
            'publish',
            'updated',
            'timestamp'
        ]
