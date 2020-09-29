from django.contrib.auth.models import User
from django.test import Client, TestCase

from api.models import Article

# Create your tests here.

class ArticleTest(TestCase):
    """ Test module for Article model """

    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@gmail.com', password='test')
        Article.objects.create(
            title='How to learn Flask',
            description='Ever wonder how?',
            body='You have to believe',
            created_by=self.user
        )

    def test_article_model(self):
        article = Article.objects.get(title='How to learn Flask')
        self.assertEqual( str(article), "{0}:How to learn Flask".format(article.id))
