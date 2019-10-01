from django.db import models

# Create your models here.

class ChannelTags(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'channel_tags'

    def title_for_url(self):
        return self.tag_name.strip().replace(' ', '-')
