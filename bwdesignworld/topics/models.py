from django.db import models

# Create your models here.

class ChannelTopics(models.Model):
    topic_id = models.AutoField(primary_key=True)
    topic_name = models.CharField(max_length=255)
    topic_url = models.CharField(max_length=255)
    category_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'channel_topics'

    def topic_name_for_url(self):
        return self.topic_name.strip().replace(' ', '-')

    def __unicode__(self):
        return unicode(self.topic_id)