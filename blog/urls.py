from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.PostListView.as_view(),
        name="blog",
    ),
    path(
        "<int:pk>/",
        views.PostDetailView.as_view(),
        name="post_detail",
    ),
    path(
        "new/",
        views.PostCreateView.as_view(),
        name="create_post",
    ),
    path(
        "<int:pk>/update/",
        views.PostUpdateView.as_view(),
        name="update",
    ),
    path(
        "<int:pk>/delete/",
        views.PostDeleteView.as_view(),
        name="delete",
    ),
]
