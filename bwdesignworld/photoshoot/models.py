from django.db import models
import datetime
import re
from django.template.defaultfilters import date
# Create your models here.


class PhotoShoot(models.Model):
    photo_shoot_id = models.AutoField(primary_key=True)
    
    photo_shoot_title = models.TextField()
    photo_shoot_description = models.TextField()
    photo_shoot_photo = models.CharField(max_length=256)
    photo_shoot_photo_name_nm = models.CharField(max_length=256)
    photo_shoot_sponsered = models.IntegerField()
    photo_shoot_published_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'photo_shoot'

    def get_image_credit(self):
        photoshoot_pic = PhotoShootPhotos.objects.filter(photo_shoot_id=self.photo_shoot_id).all()
        photo_credit = ''
        if photoshoot_pic:
            for image in photoshoot_pic:
                if image.photo_by:
                    photo_credit += image.photo_by+', '
        return photo_credit

    def get_absolute_url(self):
        photo_shoot_title_for_url = re.sub('[^A-Za-z0-9]+', '-', self.photo_shoot_title)
        return '/photo-feature/'+str(photo_shoot_title_for_url)+'/'+str(date(self.photo_shoot_published_date, "d-m-Y"))+'-'+str(self.photo_shoot_id)

    def photo_shoot_title_for_url(self):
        return re.sub('[^A-Za-z0-9]+', '-', self.photo_shoot_title)


class PhotoShootPhotos(models.Model):
    photo_shoot_image_id = models.AutoField(primary_key=True)
    photo_shoot_id = models.IntegerField()
    photo_shoot_photo_name = models.CharField(max_length=100)
    photo_shoot_photo_url = models.TextField()
    photo_shoot_photo_title = models.TextField()
    photo_by = models.CharField(max_length=256)
    photo_shoot_photo_description = models.TextField()

    class Meta:
        managed = False
        db_table = 'photo_shoot_photos'


class PhotoShootTags(models.Model):
    photo_shoot_id = models.IntegerField()
    tag_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'photo_shoot_tags'


