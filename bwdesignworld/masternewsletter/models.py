from django.db import models
from django.db import models
import datetime
import re
from django.template.defaultfilters import date
from django.conf import settings
# Create your models here.

class MasterNewsletter(models.Model):
    title = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'master_newsletter'


class MasterNewsletterArticles(models.Model):
    master_newsletter_id = models.IntegerField()
    article_id = models.IntegerField()
    is_deleted = models.IntegerField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'master_newsletter_articles'

