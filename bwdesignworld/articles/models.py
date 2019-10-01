from django.db import models
import datetime
import re
from django.template.defaultfilters import date
from django.conf import settings
#from django.apps import apps
#category_app = apps.get_app_config('category')

from category.models import ChannelCategory
from author.models import Author

# Create your models here.

class ArticleAuthor(models.Model):
    article_id = models.IntegerField()
    author_type = models.IntegerField()
    author_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'article_author'

class ArticleCategory(models.Model):
    article_id = models.ForeignKey('Articles', blank='true', null='true')
    #category = models.ForeignKey('ChannelCategory')
    category_id = models.ForeignKey('category.ChannelCategory', blank='true', null='true')
    category_level = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'article_category'

class ArticleImages(models.Model):
    id = models.AutoField(primary_key=True)
    #article_id = models.ForeignKey('Articles', related_name='image_for_article', blank='true', null='true')
    article_id = models.IntegerField()
    photopath = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    image_title = models.CharField(max_length=255)
    image_source_name = models.CharField(max_length=100)
    image_source_url = models.CharField(max_length=255)
    photo_by = models.CharField(max_length=256)
    image_status = models.CharField(max_length=8)

    class Meta:
        managed = True
        db_table = 'article_images'

class ArticleTags(models.Model):
    article_id = models.ForeignKey('Articles', blank='true', null='true')
    tag_id = models.ForeignKey('tags.ChannelTags', blank='true', null='true')

    class Meta:
        managed = True
        db_table = 'article_tags'

class ArticleTopics(models.Model):
    article_id = models.ForeignKey('Articles', blank='true', null='true')
    topic_id = models.ForeignKey('topics.ChannelTopics', blank='true', null='true')

    class Meta:
        managed = True
        db_table = 'article_topics'

class ArticleVideo(models.Model):
    article_id = models.ForeignKey('Articles', blank='true', null='true')
    video_url = models.CharField(max_length=255)
    video_embed_code = models.TextField()
    video_title = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'article_video'

class ArticleView(models.Model):
    article_id = models.IntegerField()
    view_date = models.DateField()
    view_time = models.TimeField()
    article_published_date = models.DateField()

    class Meta:
        managed = True
        db_table = 'article_view'

class ArticleTotalView(models.Model):
    article_id = models.IntegerField()
    total_view = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'article_total_view'

class Articles(models.Model):
    article_id = models.AutoField(primary_key=True)
    article_title = models.TextField()
    article_description = models.TextField()
    article_summary = models.TextField()
    article_type = models.CharField(max_length=255)
    article_published_date = models.DateTimeField()
    article_slug = models.TextField()
    article_status = models.CharField(max_length=9)
    important_article = models.IntegerField()
    hide_image = models.IntegerField()
    video_Id = models.CharField(max_length=100)
    canonical_url = models.CharField(max_length=100)
    canonical_options = models.IntegerField()
    video_type = models.CharField(max_length=100)
    display_to_homepage = models.IntegerField()
    magzine_issue_name = models.CharField(max_length=255)
    article_location_country = models.CharField(max_length=255)
    article_location_state = models.CharField(max_length=255)
    is_old = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'articles'

    def __str__(self):
        return self.article_title

    def title_for_url(self):
        #return self.article_title.strip().replace(' ', '-')
        return re.sub('[^A-Za-z0-9]+', '-', self.article_title)

    def get_absolute_url(self):
        #title_for_url = self.article_title.strip().replace(' ', '-')
        title_for_url = re.sub('[^A-Za-z0-9]+', '-', self.article_title)
        return '/article/'+str(title_for_url)+'/'+str(date(self.article_published_date, "d-m-Y"))+'-'+str(self.article_id)

    def get_comment_url(self):
        #title_for_url = self.article_title.strip().replace(' ', '-')
        title_for_url = re.sub('[^A-Za-z0-9]+', '-', self.article_title)
        return '/article/'+'/comments/'+str(title_for_url)+'/'+str(date(self.article_published_date, "d-m-Y"))+'-'+str(self.article_id)

    '''
    def id_n_timestamp_for_url(self):
        published_date = datetime(self.article_published_date)
        id_n_date = published_date+self.article_id
        return id_n_date

    def get_recent_article_descending(self):
        next = Articles.objects.filter(article_id__lt=self.article_id).order_by('-article_id')
        if next:
            return next[0]
        else:
            return False
    '''

    def get_recent_article_descending(self):
        next = Articles.objects.filter(article_id__gt=self.article_id)[0:1]
        if next:
            return next[0]
        else:
            next_new = Articles.objects.first()
            return next_new
        return False

    def get_recent_article_ascending(self):
        prev = Articles.objects.filter(article_id__lt=self.article_id).order_by('-article_id')[0:1]
        if prev:
            return prev[0]
        else:
            prev_new = Articles.objects.order_by('-article_id').first()
            return prev_new
        return False

    def get_article_author_url(self):
        #article_author = ArticleAuthor.objects.filter(article_id=self.article_id).first()
        #author_details = Author.objects.filter(author_id=article_author.author_id)
        author_details = Author.objects.raw("SELECT AU.*, AUTYPE.* FROM author AU INNER JOIN article_author A_A ON A_A.author_id = AU.author_id JOIN author_type AUTYPE ON AU.author_type = AUTYPE.author_type_id WHERE A_A.article_id = "+str(self.article_id))
        if len(list(author_details)) > 0:
            author_label = author_details[0].label.replace(' ', '-')
            author_name_for_url = author_details[0].author_name.strip().replace(' ', '-')
            author_url = '/author/'+str(author_label)+'/'+str(author_name_for_url)+'-'+str(author_details[0].author_id)
            #return '/author/'+str(author_label)+'/'+str(author_name_for_url)+'-'+str(author_details[0].author_id)
        else:
            author_url = '#'
        return author_url

    def get_article_category_data(self):
        categories = ChannelCategory.objects.raw("SELECT CC.* FROM channel_category CC LEFT JOIN article_category AC ON AC.category_id = CC.category_id WHERE AC.article_id="+str(self.article_id))
        if len(list(categories)) > 0:
            return_val = ''
            for cat in categories:
                cat_name = cat.category_name.strip().replace(' ', '-')
                return_val += '<a href="/category/'+str(cat_name)+'-'+str(cat.category_id)+'"><span style="color:#A00707">'+cat.category_name+'</span></a>'
        else:
            return_val = ''

        return return_val

    def get_article_category_listing(self):
        categories = ChannelCategory.objects.raw("SELECT CC.* FROM channel_category CC LEFT JOIN article_category AC ON AC.category_id = CC.category_id WHERE AC.article_id="+str(self.article_id)+" AND  AC.category_level=1")
        category_array = []
        if len(list(categories)) > 0:
            for cat in categories:
                category_array.append(cat.category_name)
        else:
            category_array = []

        return category_array

    def get_listing_image(self):
        article_detail = Articles.objects.filter(article_id=self.article_id).first()
        article_pic = ArticleImages.objects.filter(article_id=self.article_id).filter(image_status='enabled').first()
        if article_pic:
            if article_detail.is_old == 1:
                return article_pic.image_url
            else:
                return settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + settings.ARTICLE_IMAGE_LARGE_PATH + article_pic.photopath
        else:
            return False

    def get_image_for_feed(self):
        article_detail = Articles.objects.filter(article_id=self.article_id).first()
        article_pic = ArticleImages.objects.filter(article_id=self.article_id).filter(image_status='enabled').first()
        if article_pic:
            if article_detail.is_old == 1:
                return article_pic.image_url
            else:
                return settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + settings.ARTICLE_IMAGE_EXTRA_LARGE_PATH + article_pic.photopath
        else:
            return False

    def get_image_credit(self):
        article_pic = ArticleImages.objects.filter(article_id=self.article_id).filter(image_status='enabled').all()
        photo_credit = ''
        if article_pic:
            for image in article_pic:
                if image.photo_by:
                    photo_credit += image.photo_by+', '
        return photo_credit

    def get_homepage_list_image(self):
        article_detail = Articles.objects.filter(article_id=self.article_id).first()
        article_pic = ArticleImages.objects.filter(article_id=self.article_id).filter(image_status='enabled').first()
        if article_pic:
            if article_detail.is_old == 1:
                return article_pic.image_url
            else:
                return settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + settings.ARTICLE_IMAGE_THUMB_PATH + article_pic.photopath
        else:
            return False

    def get_article_author_name(self):
        author_details = Author.objects.raw("SELECT AU.* FROM author AU INNER JOIN article_author A_A ON A_A.author_id = AU.author_id WHERE A_A.article_id = "+str(self.article_id))
        if len(list(author_details)) > 0:
            author_name = author_details[0].author_name
        else:
            author_name = ''
        return author_name

    def get_magzine_issue_title(self):
        magzine_isse = Magazine.objects.filter(magazine_id=self.magzine_issue_name).first()
        if len(list(magzine_isse)) > 0:
            magzine_isse_title = magzine_isse.title
        else:
            magzine_isse_title = ''
        return magzine_isse_title

    def get_article_video(self):
        article_video = ArticleVideo.objects.filter(article_id=self.article_id).first()
        if len(list(article_video)) > 0:
            video_embed_code = article_video.video_embed_code.strip()
        else:
            video_embed_code = ''
        return video_embed_code

class Magazine(models.Model):
    magazine_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    imagepath = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue = models.CharField(max_length=255)
    valid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'magazine'

class ArticleTotalView(models.Model):
    article_id = models.IntegerField()
    total_view = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'article_total_view'




