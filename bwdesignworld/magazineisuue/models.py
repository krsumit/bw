from django.db import models
import re
# Create your models here.

class Magazine(models.Model):
    magazine_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    imagepath = models.CharField(max_length=255)
    publish_date_m = models.DateField()
    story1_title = models.CharField(max_length=256)
    story1_url = models.CharField(max_length=256)
    story2_title = models.CharField(max_length=256)
    story2_url = models.CharField(max_length=256)
    story3_title = models.CharField(max_length=256)
    story3_url = models.CharField(max_length=256)
    story4_title = models.CharField(max_length=256)
    story4_url = models.CharField(max_length=256)
    story5_title = models.CharField(max_length=256)
    story5_url = models.CharField(max_length=256)
    valid = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'magazine'

    def get_absolute_url(self):
        #title_for_url = self.topic_name.strip().replace(' ', '-')
        title_for_url = re.sub('[^A-Za-z0-9]+', '-', self.title)
        return str(title_for_url)+'-'+str(self.magazine_id)+'/web-view'
