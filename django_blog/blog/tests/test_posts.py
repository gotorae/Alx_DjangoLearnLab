

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from blog.models import Post

User = get_user_model()

class PostCrudTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='author', password='Pass12345!')
        self.other = User.objects.create_user(username='other', password='Pass12345!')
        self.post = Post.objects.create(title='Hello', content='World', author=self.author)

    def test_list_and_detail_accessible_to_all(self):
        resp = self.client.get(reverse('posts-list'))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('posts-detail', args=[self.post.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_create_requires_login(self):
        resp = self.client.get(reverse('posts-create'))
        self.assertNotEqual(resp.status_code, 200)  # redirect to login
        self.client.login(username='author', password='Pass12345!')
        resp = self.client.post(reverse('posts-create'), {
            'title': 'New',
            'content': 'Post',
            'tags': 'django, tips'  # ✅ include tags if using taggit
        })
        self.assertRedirects(resp, reverse('posts-list'))
        self.assertTrue(Post.objects.filter(title='New').exists())
        new_post = Post.objects.get(title='New')
        self.assertIn('django', new_post.tags.names())  # taggit check

    def test_update_and_delete_only_author(self):
        # Other user cannot edit/delete
        self.client.login(username='other', password='Pass12345!')
        resp = self.client.get(reverse('posts-update', args=[self.post.pk]))
        self.assertEqual(resp.status_code, 403) if resp.status_code == 403 else self.assertNotEqual(resp.status_code, 200)
        resp = self.client.post(reverse('posts-update', args=[self.post.pk]), {'title': 'Hack', 'content': 'Hack'})
        self.assertNotEqual(resp.status_code, 302)

        # Author can edit
        self.client.login(username='author', password='Pass12345!')
        resp = self.client.post(reverse('posts-update', args=[self.post.pk]), {'title': 'Edited', 'content': 'Ok', 'tags': 'python'})
        self.assertRedirects(resp, reverse('posts-list'))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Edited')
        self.assertIn('python', self.post.tags.names())

        # Author can delete
        resp = self.client.post(reverse('posts-delete', args=[self.post.pk]))
        self.assertRedirects(resp, reverse('posts-list'))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())


# ✅ New tests for tagging and search
class TagSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='author', password='Pass12345!')
        self.client.login(username='author', password='Pass12345!')
        self.p1 = Post.objects.create(title='Django Tips', content='Learn Django basics', author=self.user)
        self.p2 = Post.objects.create(title='Insurance Models', content='Life underwriting', author=self.user)
        # Add tags (works for django-taggit)
        self.p1.tags.add('django', 'tips')
        self.p2.tags.add('insurance', 'life')

    def test_posts_by_tag(self):
        url = reverse('posts-by-tag', args=['django'])
        resp = self.client.get(url)
        self.assertContains(resp, 'Django Tips')
        self.assertNotContains(resp, 'Insurance Models')

    def test_search_by_title(self):
        resp = self.client.get(reverse('post-search'), {'q': 'Django'})
        self.assertContains(resp, 'Django Tips')
        self.assertNotContains(resp, 'Insurance Models')

    def test_search_by_content(self):
        resp = self.client.get(reverse('post-search'), {'q': 'underwriting'})
        self.assertContains(resp, 'Insurance Models')

    def test_search_by_tag_name(self):
        resp = self.client.get(reverse('post-search'), {'q': 'life'})
        self.assertContains(resp, 'Insurance Models')

    def test_empty_query_returns_no_results(self):
        resp = self.client.get(reverse('post-search'), {'q': ''})
        self.assertContains(resp, 'Enter a keyword')  # adjust based on template
