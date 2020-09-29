from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Convert tags to lower case
        """
        self.name = self.name.lower()
        super(Tag, self).save(*args, **kwargs)


class Article(models.Model):
    title = models.CharField(max_length=100, help_text='Title for your Article')
    description = models.CharField(max_length=200, help_text='Description for your Article')
    body = models.TextField()
    tags = models.ManyToManyField(
        Tag,
        verbose_name='tags',
        blank=True
    )
    featuredImage = models.ImageField(null=True, blank=True, upload_to='images/')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    favorited = models.BooleanField(default=False)
    favoritesCount = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.pk}:{self.title}'

    @classmethod
    def abc(cls, aa):
        pass
