from django.urls import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from pages.models import Post


class PostListAPIViewTest(APITestCase):
    def test_get_posts_list_authenticate_user(self):
        user = mommy.make(User)
        self.client.force_authenticate(user)
        mommy.make(Post, author=user, _quantity=10)
        response = self.client.get(reverse('posts-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_get_posts_list_anonymous_user(self):
        user = mommy.make(User)
        mommy.make(Post, author=user)
        response = self.client.get(reverse('posts-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PostCreateAPIViewTest(APITestCase):
    def test_create_post_authenticate_user(self):
        user = mommy.make(User)
        self.client.force_authenticate(user)
        post_data = {'title': 'test', 'content': 'test'}
        response = self.client.post(reverse('post-create'), data=post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_anonymous_user(self):
        post_data = {'title': 'test', 'content': 'test'}
        response = self.client.post(reverse('post-create'), data=post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PostLikeAPIViewTest(APITestCase):
    def test_like_unlike_post_authenticate_user(self):
        like_user = mommy.make(User)
        post_author = mommy.make(User)
        self.client.force_authenticate(like_user)
        post = mommy.make(Post, author=post_author)

        # initial number of likes
        self.assertEqual(post.likes.count(), 0)

        # like post
        response = self.client.get(
            reverse('post-like', kwargs={'pk': post.pk}))
        self.assertEqual(post.likes.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # unlike post
        response = self.client.get(
            reverse('post-like', kwargs={'pk': post.pk}))
        self.assertEqual(post.likes.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_unlike_post_anonymous_user(self):
        post_author = mommy.make(User)
        post = mommy.make(Post, author=post_author)
        response = self.client.get(
            reverse('post-like', kwargs={'pk': post.pk}))
        self.assertEqual(post.likes.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PostRetrieveUpdateDestroyAPIViewTest(APITestCase):
    def test_retrieve_update_delete_post_authenticate_user(self):
        user = mommy.make(User)
        self.client.force_authenticate(user)
        post = mommy.make(Post, author=user)

        retrieve_response = self.client.get(
            reverse('post-retrieve', kwargs={'pk': post.pk}))
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)

        patch_response = self.client.patch(
            reverse('post-update-delete', kwargs={'pk': post.pk}),
            data={'title': 'test'}
        )
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

        put_response = self.client.put(
            reverse('post-update-delete', kwargs={'pk': post.pk}),
            data={'title': 'test', 'content': 'test', 'author': post.author}
        )
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

        delete_response = self.client.delete(
            reverse('post-update-delete', kwargs={'pk': post.pk}))
        self.assertEqual(delete_response.status_code,
                         status.HTTP_204_NO_CONTENT)

    def test_retrieve_update_delete_other_user_post(self):
        post_author = mommy.make(User)
        post = mommy.make(Post, author=post_author)
        login_user = mommy.make(User)
        self.client.force_authenticate(login_user)

        # login user can get others posts
        retrieve_response = self.client.get(
            reverse('post-retrieve', kwargs={'pk': post.pk}))
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)

        # login user can not update others posts
        patch_response = self.client.patch(
            reverse('post-update-delete', kwargs={'pk': post.pk}),
            data={'title': 'test'}
        )
        self.assertEqual(patch_response.status_code, status.HTTP_404_NOT_FOUND)

        # login user can not update others posts
        put_response = self.client.put(
            reverse('post-update-delete', kwargs={'pk': post.pk}),
            data={'title': 'test', 'content': 'test', 'author': post.author}
        )
        self.assertEqual(put_response.status_code, status.HTTP_404_NOT_FOUND)

        # login user can not delete others posts
        delete_response = self.client.delete(
            reverse('post-update-delete', kwargs={'pk': post.pk}))
        self.assertEqual(delete_response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_retrieve_update_delete_post_anonymous_user(self):
        user = mommy.make(User)
        post = mommy.make(Post, author=user)

        retrieve_response = self.client.get(
            reverse('post-retrieve', kwargs={'pk': post.pk}))
        self.assertEqual(retrieve_response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

        patch_response = self.client.patch(
            reverse('post-update-delete', kwargs={'pk': post.pk}),
            data={'title': 'test'}
        )
        self.assertEqual(patch_response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

        put_response = self.client.put(
            reverse('post-update-delete', kwargs={'pk': post.pk}),
            data={'title': 'test', 'content': 'test', 'author': post.author}
        )
        self.assertEqual(put_response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

        delete_response = self.client.delete(
            reverse('post-update-delete', kwargs={'pk': post.pk}))
        self.assertEqual(delete_response.status_code,
                         status.HTTP_401_UNAUTHORIZED)
