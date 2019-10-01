from django.db import models
from django.template.defaultfilters import date
from articles.models import Articles, ArticleImages, ArticleCategory, ArticleTopics, ArticleView
# Create your models here.
class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    imagepath = models.CharField(max_length=255)
    image_url = models.CharField(max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    state = models.IntegerField()
    country = models.IntegerField()
    category = models.CharField(max_length=100)
    valid = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'event'
    def get_article_author_name(self):
        arcticleall_event = Articles.objects.raw("SELECT article_id,article_title,article_published_date from  articles  where event_id = '"+str(self.event_id)+"' " )

        return arcticleall_event

