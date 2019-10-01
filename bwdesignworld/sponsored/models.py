from django.db import models
from django.template.defaultfilters import date

# Create your models here.


class Sponsoredposts(models.Model):
    sponsoredposts_id = models.AutoField(primary_key=True)
    sponsoredposts_title = models.TextField()
    sponsoredposts_description = models.TextField()
    sponsoredposts_summary = models.TextField()
    sponsoredposts_type = models.CharField(max_length=255)
    sponsoredposts_published_date = models.DateTimeField()
    sponsoredposts_slug = models.TextField()
    sponsoredposts_status = models.CharField(max_length=9)
    important_sponsoredposts = models.IntegerField()
    display_to_homepage = models.IntegerField()
    magzine_issue_name = models.CharField(max_length=255)
    sponsoredposts_location_country = models.CharField(max_length=255)
    sponsoredposts_location_state = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'sponsoredposts'

    def __str__(self):
        return self.sponsoredposts_title

    def title_for_url(self):
        return self.sponsoredposts_title.strip().replace(' ', '-')

    def get_listing_image(self):
        article_pic = SponsoredpostsImages.objects.filter(article_id=self.article_id).first()
        return article_pic.image_url

    def get_absolute_url(self):
        title_for_url = self.sponsoredposts_title.strip().replace(' ', '-')
        return '/sponsor/'+str(title_for_url)+'/'+str(date(self.sponsoredposts_published_date, "d-m-Y"))+'-'+str(self.sponsoredposts_id)


class SponsoredpostsCategory(models.Model):
    sponsoredposts_id = models.IntegerField()
    category_id = models.IntegerField()
    category_level = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'sponsoredposts_category'


class SponsoredpostsImages(models.Model):
    sponsoredposts_id = models.IntegerField()
    image_url = models.CharField(max_length=255)
    image_title = models.CharField(max_length=255)
    image_source_name = models.CharField(max_length=100)
    image_source_url = models.CharField(max_length=255)
    image_status = models.CharField(max_length=8)
    sponsoredposts_id_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sponsoredposts_images'


class SponsoredpostsNameCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    category_parent = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'sponsoredposts_name_category'


class SponsoredpostsVideo(models.Model):
    sponsoredposts_id = models.IntegerField()
    sponsoredposts_url = models.CharField(max_length=255)
    video_embed_code = models.TextField()
    video_title = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'sponsoredposts_video'


class SponsoredpostsView(models.Model):
    sponsoredposts_id = models.IntegerField()
    view_date = models.DateField()
    view_time = models.TimeField()
    sponsoredposts_published_date = models.DateField()

    class Meta:
        managed = True
        db_table = 'sponsoredposts_view'
