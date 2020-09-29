import json

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from api.models import Article
from api.serializers import ArticleSerializer

# initialize the APIClient app
client = Client()


class CreateNewArticleTest(TestCase):
    """ Test module for inserting a new Article """

    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@gmail.com', password='test')
        self.valid_payload = {
            'title': 'How to learn Flask',
            'description': 'Ever wonder how?',
            'body': 'You have to believe'
        }
        self.invalid_payload = {
            'description': 'Ever wonder how?',
            'body': 'You have to believe'
        }

    def test_create_valid_article_with_valid_auth(self):
        client.login(username='test', password='test')
        response = client.post(
            reverse('article-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_valid_article_with_invalid_auth(self):
        client.login(username='test', password='invalid')
        response = client.post(
            reverse('article-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_invalid_article_with_valid_auth(self):
        client.login(username='test', password='test')
        response = client.post(
            reverse('article-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_article_with_invalid_auth(self):
        client.login(username='test', password='invalid')
        response = client.post(
            reverse('article-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_article_owner(self):
        client.login(username='test', password='test')
        response = client.post(
            reverse('article-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['created_by'], 'test')


class GetSingleArticleTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', email='test@gmail.com', password='test')
        self.article = Article.objects.create(
            title='How to learn Flask',
            description='Ever wonder how?',
            body='You have to believe',
            created_by=user)

    def test_get_valid_single_article(self):
        # Get from API
        url = "{0}{1}/".format(reverse('article-list'), self.article.pk)
        response = client.get(url)
        # Get from database
        article = Article.objects.get(pk=self.article.pk)
        serializer = ArticleSerializer(article)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_article(self):
        url = "{0}{1}/".format(reverse('article-list'), 30)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetAllArticleTest(TestCase):
    """ Test module for GET all Articles API """

    def setUp(self):
        user = User.objects.create_user(username='test', email='test@gmail.com', password='test')
        Article.objects.create(
            title='How to learn Flask', description='Ever wonder how?', body='You have to believe', created_by=user)
        Article.objects.create(
            title='How to learn Flask2', description='Ever wonder how2?', body='You have to believe2', created_by=user)
        Article.objects.create(
            title='How to learn Flask3', description='Ever wonder how3?', body='You have to believe3', created_by=user)
        Article.objects.create(
            title='How to learn Flask4', description='Ever wonder how4?', body='You have to believe4', created_by=user)

    def test_get_all_articles(self):
        # get API response
        response = client.get(reverse('article-list'))

        # get data from db
        articles = Article.objects.filter().order_by('id')
        serializer = ArticleSerializer(articles, many=True)

        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateSingleArticleTest(TestCase):
    """ Test module for updating an existing Article record """

    def setUp(self):
        self.user1 = User.objects.create_user(username='test1', email='test1@gmail.com', password='test1')
        self.user2 = User.objects.create_user(username='test2', email='test2@gmail.com', password='test2')

        self.article_of_user1 = Article.objects.create(
            title='How to learn Flask1',
            description='Ever wonder how1?',
            body='You have to believe1',
            created_by=self.user1
        )
        self.article_of_user2 = Article.objects.create(
            title='How to learn Flask2',
            description='Ever wonder how2?',
            body='You have to believe2',
            created_by=self.user2
        )
        self.valid_payload = {
            'title': 'Updated Title'
        }
        self.invalid_payload = {
            'title': ''
        }

    def test_valid_update_article(self):
        # Login with test1 user
        client.login(username='test1', password='test1')
        url = "{0}{1}/".format(reverse('article-list'), self.article_of_user1.pk)
        response = client.patch(
            url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_article(self):
        # Login with test1 user
        client.login(username='test1', password='test1')
        url = "{0}{1}/".format(reverse('article-list'), self.article_of_user1.pk)
        response = client.patch(
            url,
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_other_user_article(self):
        # Login with test1 user
        client.login(username='test1', password='test1')
        url = "{0}{1}/".format(reverse('article-list'), self.article_of_user2.pk)
        response = client.patch(
            url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DeleteSingleArticleTest(TestCase):
    """ Test module for deleting an existing Article record """

    def setUp(self):
        self.user1 = User.objects.create_user(username='test1', email='test1@gmail.com', password='test1')
        self.user2 = User.objects.create_user(username='test2', email='test2@gmail.com', password='test2')

        self.article_of_user1 = Article.objects.create(
            title='How to learn Flask1',
            description='Ever wonder how1?',
            body='You have to believe1',
            created_by=self.user1
        )
        self.article_of_user2 = Article.objects.create(
            title='How to learn Flask2',
            description='Ever wonder how2?',
            body='You have to believe2',
            created_by=self.user2
        )

    def test_valid_delete_article(self):
        client.login(username='test1', password='test1')
        url = "{0}{1}/".format(reverse('article-list'), self.article_of_user1.pk)
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_article(self):
        client.login(username='test1', password='test1')
        url = "{0}{1}/".format(reverse('article-list'), 50)
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_other_user_article(self):
        client.login(username='test1', password='test1')
        url = "{0}{1}/".format(reverse('article-list'), self.article_of_user2.pk)
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
