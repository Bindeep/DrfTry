import json
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


def get_url(name):
    return {
        'blog_list': lambda: reverse('blog:blog_list'),
        'blog_create': lambda: reverse('blog:blog_list')
    }.get(name)()


class UserAndTokenMixin:

    def setUp(self):
        norm_data = {
            'username': 'normal',
            'password': 'admin1234'
        }
        spr_usr = {
            'username': 'super',
            'email': 'email@bmail.com',
            'password': 'admin1234'
        }
        self.super_user = User.objects.create_superuser(**spr_usr)
        self.normal_user = User.objects.create_user(**norm_data)
        self.normal_token = Token.objects.create(user=self.normal_user)
        self.super_token = Token.objects.create(user=self.super_user)
        self.client = APIClient()


class BlogTestCase(UserAndTokenMixin, APITestCase):

    #
    # def test_create_account(self):
    #     """
    #     Ensure we can create a new account object.
    #     """
    #     url = reverse('account-list')
    #     data = {'name': 'DabApps'}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Account.objects.count(), 1)
    #     self.assertEqual(Account.objects.get().name, 'DabApps')

    def test_if_list_blog_using_unauthenticated_users(self):
        """
        Ensure we cannot list the blogs when unauthenticated
        """
        url = get_url('blog_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_if_list_blog_using_authenticated_users(self):
        """
        Ensure we can list the blogs when authenticated
        """
        url = get_url('blog_list')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_blog_can_be_created(self):
        """
        Ensure we can create the blog
        :return:
        """
        url = get_url('blog_create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        data = {
            'title': 'Test Title',
            'content': 'Test Content',
            'author': self.normal_user.id
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertDictContainsSubset(data, response.data)
        for key in data.keys():
            self.assertEqual(data.get(key), response.data.get(key))
        # self.assertIn(data.values(), response.data.values())
