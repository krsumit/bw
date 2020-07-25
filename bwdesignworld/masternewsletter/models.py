from django.db import models
from django.db import models
import datetime
import re
from django.template.defaultfilters import date
from django.conf import settings
# Create your models here.

class MainNewsletter(models.Model):
    title = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'main_newsletter'


class MainNewsletterArticles(models.Model):
    main_newsletter_id = models.IntegerField()
    article_id = models.IntegerField()
    is_deleted = models.IntegerField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'main_newsletter_articles'

