from __future__ import unicode_literals

from django.db import models


class Post(models.Model):
    """
    A model for dealing with all the Post objects.
    """
    SCIENCE = 1
    AIML = 2
    NATURE = 3
    PHILOSOPHY = 4
    CATEGORIES = (
        (SCIENCE, 'Science'),
        (AIML, 'Artificial Intelligence / Machine Learning'),
        (NATURE, 'Nature'),
        (PHILOSOPHY, 'Philosophy'))

    title = models.CharField(
        help_text='Title of the post. Max 255 chars.',
        max_length=255)
    category = models.IntegerField(
        help_text='Selectable category for the post.',
        choices=CATEGORIES,
        blank=True,
        null=True)
    body = models.TextField(
        help_text='The actual body of the post.',
        blank=True)
    is_active = models.BooleanField(
        help_text='If the post is active or not.')
    added_on = models.DateTimeField(
        help_text='Creation timestamp.',
        auto_now_add=True)
    updated_on = models.DateTimeField(
        help_text='Last updation timestamp.',
        auto_now=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __unicode__(self):
        return self.title
