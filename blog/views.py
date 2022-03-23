from django.urls import reverse_lazy
from django.views import generic

from .forms import PostForm
from .models import Post


class PostListView(generic.ListView):
    model = Post
    template_name = "blog/blog.html"
    context_object_name = "post"

    def get_queryset(self):
        return Post.objects.filter(status="pub").order_by("-datetime_modified")


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


class PostCreateView(generic.CreateView):
    form_class = PostForm
    template_name = "blog/add_new_post.html"


class PostUpdateView(generic.UpdateView):
    form_class = PostForm
    template_name = "blog/edit_post.html"
    model = Post


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy("blog")
