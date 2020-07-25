from django.db import models
import datetime
import re
from django.template.defaultfilters import date
# Create your models here.
from tags.models import ChannelTags
from category.models import ChannelCategory

class VideoMain(models.Model):
    video_id = models.AutoField(primary_key=True)
    video_title = models.TextField()
    video_summary = models.TextField()
    video_name = models.CharField(max_length=256)
    video_thumb_name = models.CharField(max_length=256)
    tags = models.CharField(max_length=256)
    video_status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'video_main'


    def get_absolute_url(self):
      
       video_main_title_for_url = re.sub('[^A-Za-z0-9]+', '-', self.video_title)
       return '/video/'+str(video_main_title_for_url)+'/'+str(date(self.updated_at, "d-m-Y"))+'-'+str(self.video_id)
    def photo_shoot_title_for_url(self):
        
        return re.sub('[^A-Za-z0-9]+', '-', self.video_title)
    def get_video_tags_listing(self):
        video_tags = ChannelTags.objects.raw("SELECT t.* FROM channel_tags t Left JOIN video_tags at ON t.tag_id = at.tags_id WHERE at.video_id = "+str(self.video_id))
        tag_names = ''
        for tag in video_tags:
            tag_names = tag.tag_name+','+tag_names
        return tag_names 
    def get_video_category_listing(self):
        categories = ChannelCategory.objects.raw("SELECT CC.* FROM channel_category CC LEFT JOIN video_category AC ON AC.category_id = CC.category_id WHERE AC.video_id="+str(self.video_id)+" AND  AC.level=1")
        category_array = []
        if len(list(categories)) > 0:
            for cat in categories:
                category_array.append(cat.category_name)
        else:
            category_array = []

        return category_array    


class VideoCategory(models.Model):
    v_category_id = models.AutoField(primary_key=True)
    video_id = models.IntegerField()
    category_id = models.IntegerField()
    level = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'video_category'
    def get_video_category_listing(self):
        categories = ChannelCategory.objects.raw("SELECT CC.* FROM channel_category CC LEFT JOIN video_category AC ON AC.category_id = CC.category_id WHERE AC.video_id="+str(self.video_id)+" AND  AC.category_level=1")
        category_array = []
        if len(list(categories)) > 0:
            for cat in categories:
                category_array.append(cat.category_name)
        else:
            category_array = []

        return category_array    

class VideoTags(models.Model):
    v_tags_id = models.AutoField(primary_key=True)
    video_id = models.IntegerField()
    tags_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'video_tags'
    
  
            
    