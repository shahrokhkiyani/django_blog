from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase

from .models import Post


class BlogPostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user1")

        self.post1 = Post.objects.create(
            title="post1",
            text="this is description of post1",
            status=Post.STATUS_CHOICES[0][0],
            author=self.user,
        )

        self.post2 = Post.objects.create(
            title="post2",
            text="lerem ipsum",
            status=Post.STATUS_CHOICES[1][0],
            author=self.user,
        )

    def test_post_detail(self):
        self.assertEqual(self.post1.title, "post1")

    def test_posts_list_url(self):
        response = self.client.get("/blog/")
        self.assertEqual(response.status_code, 200)

    def test_post_title_on_blog_list_page(self):
        response = self.client.get("/blog/")
        self.assertContains(response, self.post1.title)

    def test_post_title(self):
        response = self.client.get("/blog/")
        self.assertContains(response, self.post1.title)

    def test_post_detail_url(self):
        response = self.client.get(f"/blog/{self.post1.id}/")
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view(self):
        response = self.client.get(reverse("post_detail", args=[self.post1.id]))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)

    def test_status_404(self):
        response = self.client.get(reverse("post_detail", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_draft_post_not_show_in_posts_list(self):
        response = self.client.get(reverse("post_detail", args=[self.post1.id]))
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title)

    def test_post_create_view(self):
        response = self.client.post(
            reverse("create_post"),
            {
                "title": "some title",
                "text": "some text",
                "status": "pub",
                "author": self.user.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, "some title")
        self.assertEqual(Post.objects.last().text, "some text")
        self.assertEqual(Post.objects.last().status, "pub")

    def test_post_update_view(self):
        response = self.client.post(
            reverse(
                "update",
                args=[self.post2.id],
            ),
            {
                "title": "some title updated",
                "text": "some text updated",
                "status": "pub",
                "author": self.post2.author,
            },
        )

    def test_post_delete(self):
        response = self.client.post(
            reverse("delete", args=[self.post1.id]),
        )
        self.assertEqual(
            response.status_code,
            302,
        )
