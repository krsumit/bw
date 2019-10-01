from django.db import models
import re
# Create your models here.

class ChannelCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    category_parent = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'channel_category'

    def category_name_for_url(self):
        #return self.category_name.strip().replace(' ', '-')
        return re.sub('[^A-Za-z0-9]+', '-', self.category_name)

    def category_self_url(self):
        category_name = re.sub('[^A-Za-z0-9]+', '-', self.category_name)
        return '/category/' + category_name + '-' + str(self.category_id)