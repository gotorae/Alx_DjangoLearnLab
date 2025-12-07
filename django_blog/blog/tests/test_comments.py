

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from blog.models import Post, Comment

User = get_user_model()

class CommentTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='author', password='Pass12345!')
        self.other = User.objects.create_user(username='other', password='Pass12345!')
        self.post = Post.objects.create(title='Post', content='Body', author=self.author)

    def test_comment_visibility_on_post_detail(self):
        Comment.objects.create(post=self.post, author=self.author, content='Hi')
        resp = self.client.get(reverse('posts-detail', args=[self.post.pk]))
        self.assertContains(resp, 'Comments (1)')
        self.assertContains(resp, 'Hi')

    def test_create_comment_requires_login(self):
        url = reverse('comments-create', args=[self.post.pk])
        resp = self.client.post(url, {'content': 'New comment'})
        self.assertNotEqual(resp.status_code, 200)  # redirect to login
        self.client.login(username='author', password='Pass12345!')
        resp = self.client.post(url, {'content': 'New comment'})
        self.assertRedirects(resp, reverse('posts-detail', args=[self.post.pk]))
        self.assertTrue(Comment.objects.filter(content='New comment').exists())

    def test_edit_delete_only_comment_author(self):
        c = Comment.objects.create(post=self.post, author=self.author, content='Hi')
        edit_url = reverse('comments-edit', args=[c.pk])
        del_url = reverse('comments-delete', args=[c.pk])

        # other user cannot edit
        self.client.login(username='other', password='Pass12345!')
        resp = self.client.post(edit_url, {'content': 'Hack'})
        self.assertNotEqual(resp.status_code, 302)

        # author can edit
        self.client.login(username='author', password='Pass12345!')
        resp = self.client.post(edit_url, {'content': 'Edited'})
        self.assertRedirects(resp, reverse('posts-detail', args=[self.post.pk]))
        c.refresh_from_db()
        self.assertEqual(c.content, 'Edited')

        # author can delete
        resp = self.client.post(del_url)
        self.assertRedirects(resp, reverse('posts-detail', args=[self.post.pk]))
        self.assertFalse(Comment.objects.filter(pk=c.pk).exists())


# ✅ New tests for tagging and search
class TagSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='author', password='Pass12345!')
        self.client.login(username='author', password='Pass12345!')
        self.p1 = Post.objects.create(title='Django Tips', content='Learn Django basics', author=self.user)
        self.p2 = Post.objects.create(title='Insurance Models', content='Life underwriting', author=self.user)
        # Add tags (works for django-taggit or custom Tag model)
        self.p1.tags.add('django', 'tips')
        self.p2.tags.add('insurance', 'life')

    def test_posts_by_tag(self):
        url = reverse('posts-by-tag', args=['django'])
        resp = self.client.get(url)
        self.assertContains(resp, 'Django Tips')
        self.assertNotContains(resp, 'Insurance Models')

    def test_search_by_title(self):
        resp = self.client.get(reverse('post-search'), {'q': 'Django'})
