from django.db.models import Q

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    ListAPIView
    )

from rest_framework.permissions import(
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)



from posts.models import Post
from .pagination import PostLimitOffsetPagination,PostPageNumberPagination
from .permissions import IsOwnerOrReadOnly

from .serializers import (
    PostCreateSerializer,
    PostListSerializer,
    PostDetailSerializer
    )

class PostListAPIView(ListAPIView):
    serializer_class =  PostListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title','content']
    pagination_class = PostLimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        #queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        queryset_list = Post.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)|
                Q(slug__icontains=query)
                ).distinct()
        return queryset_list

class PostCategoriesAPIView(ListAPIView):
    serializer_class =  PostListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title','content']
    pagination_class = PostLimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        #queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        cat_id = self.kwargs['id']
        queryset_list = Post.objects.filter(id_kategori=cat_id)
        # queryset_list = Post.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)|
                Q(slug__icontains=query)
                ).distinct()
        return queryset_list

class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated]
