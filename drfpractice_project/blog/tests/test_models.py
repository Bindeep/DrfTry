from django.test import TestCase
from ..models.blog import Blog
from django.contrib.auth.models import User


class BlogTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='bindeep', password='admin1234')

    def _create_blog(self, data):
        return Blog.objects.create(**data)

    def _valid_data(self):
        self.title = 'This is test title'
        self.content = 'This is test content'
        return {
            'title': self.title,
            'content': self.content,
            'author': self.user
        }

    def _invalid_data(self):
        data = self._valid_data()
        data = data.update({'title': 'This is the invalid title' * 100})
        return data

    def test_if_blog_can_create_with_valid_data(self):
        blog_data = self._valid_data()
        blog = self._create_blog(blog_data)
        self.assertEqual(blog.title, self.title)

    def test_if_blog_can_create_with_invalid_data(self):
        data = {
            'title': 'this is the title ' * 100,
            'content': 'this is the content',
            'author': self.user
        }
        Blog.objects.create(**data)

