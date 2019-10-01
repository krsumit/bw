from django.db import models
import datetime
import re
from django.template.defaultfilters import date

from author.models import Author

# Create your models here.

class QuickBytes(models.Model):
    quick_byte_id = models.AutoField(primary_key=True)
    quick_byte_author_type = models.IntegerField()
    quick_byte_author_id = models.IntegerField()
    quick_byte_title = models.TextField()
    quick_byte_photo_url_tbl = models.CharField(max_length=256)
    quick_byte_photo_name_tbl = models.CharField(max_length=256)
    quick_byte_description = models.TextField()
    quick_byte_sponsered = models.IntegerField()
    quick_byte_published_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'quick_bytes'

    def quick_byte_title_for_url(self):
        #return self.quick_byte_title.strip().replace(' ', '-')
        return re.sub('[^A-Za-z0-9]+', '-', self.quick_byte_title)

    def get_next(self):
        next = QuickBytes.objects.filter(quick_byte_id__gt=self.quick_byte_id)[0:1]
        if next:
            return next[0]
        else:
            next_new = QuickBytes.objects.first()
            return next_new
        return False

    def get_prev(self):
        prev = QuickBytes.objects.filter(quick_byte_id__lt=self.quick_byte_id).order_by('-quick_byte_id')[0:1]
        if prev:
            return prev[0]
        else:
            prev_new = QuickBytes.objects.order_by('-quick_byte_id').first()
            return prev_new
        return False

    def get_absolute_url(self):
        #quick_byte_title_for_url = self.quick_byte_title.strip().replace(' ', '-')
        quick_byte_title_for_url = re.sub('[^A-Za-z0-9]+', '-', self.quick_byte_title)
        return '/quickbytes/'+str(quick_byte_title_for_url)+'/'+str(date(self.quick_byte_published_date, "d-m-Y"))+'-'+str(self.quick_byte_id)

    def get_listing_image(self):
        quick_byte_pic = QuickBytesPhotos.objects.filter(quick_byte_id=self.quick_byte_id).first()
        return quick_byte_pic.quick_byte_photo_name

    def get_article_author_url(self):
        #article_author = ArticleAuthor.objects.filter(article_id=self.article_id).first()
        #author_details = Author.objects.filter(author_id=article_author.author_id)
        author_details = Author.objects.raw("SELECT AU.*, AUTYPE.* FROM author AU JOIN author_type AUTYPE ON AU.author_type = AUTYPE.author_type_id WHERE AU.author_id = "+str(self.quick_byte_author_id))
        if len(list(author_details)) > 0:
            author_label = author_details[0].label.replace(' ', '-')
            author_name_for_url = author_details[0].author_name.strip().replace(' ', '-')
            author_url = '/author/'+str(author_label)+'/'+str(author_name_for_url)+'-'+str(author_details[0].author_id)
            #return '/author/'+str(author_label)+'/'+str(author_name_for_url)+'-'+str(author_details[0].author_id)
        else:
            author_url = '#'
        return author_url

    def get_article_author_name(self):
        author_details = Author.objects.filter(author_id=self.quick_byte_author_id).first()
        if author_details:
            author_name = author_details.author_name
        else:
            author_name = ''
        return author_name

    def get_image_credit(self):
        quickbyte_pic = QuickBytesPhotos.objects.filter(quick_byte_id=self.quick_byte_id).all()
        photo_credit = ''
        if quickbyte_pic:
            for image in quickbyte_pic:
                if image.photo_by:
                    photo_credit += image.photo_by+', '
        return photo_credit

class QuickBytesPhotos(models.Model):
    quick_byte_image_id = models.AutoField(primary_key=True)
    quick_byte_id = models.IntegerField()
    quick_byte_photo_name = models.CharField(max_length=100)
    quick_byte_photo_url = models.TextField()
    quick_byte_photo_title = models.TextField()
    quick_byte_photo_description = models.TextField()
    photo_by = models.TextField()
    sequence = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'quick_bytes_photos'

    def get_next_pic_sequence(self):
        next = QuickBytesPhotos.objects.filter(sequence__gt=self.sequence).filter(quick_byte_id=self.quick_byte_id)
        if next:
            return next[0]
        '''
        else:
            next_new = QuickBytesPhotos.objects.filter(quick_byte_id=self.quick_byte_id).first()
            return next_new
        '''
        return False

    def get_prev_pic_sequence(self):
        prev = QuickBytesPhotos.objects.filter(sequence__lt=self.sequence).filter(quick_byte_id=self.quick_byte_id).order_by('-sequence')
        if prev:
            return prev[0]
        '''
        else:
            prev_new = QuickBytesPhotos.objects.filter(quick_byte_id=self.quick_byte_id).order_by('-quick_byte_image_id').first()
            return prev_new
        '''
        return False

    def get_next_pic_quick_byte(self):
        next = QuickBytesPhotos.objects.filter(quick_byte_image_id__gt=self.quick_byte_image_id).filter(quick_byte_id=self.quick_byte_id)
        if next:
            return next[0]
        '''
        else:
            next_new = QuickBytesPhotos.objects.filter(quick_byte_id=self.quick_byte_id).first()
            return next_new
        '''
        return False

    def get_prev_pic_quick_byte(self):
        prev = QuickBytesPhotos.objects.filter(quick_byte_image_id__lt=self.quick_byte_image_id).filter(quick_byte_id=self.quick_byte_id).order_by('-quick_byte_image_id')
        if prev:
            return prev[0]
        '''
        else:
            prev_new = QuickBytesPhotos.objects.filter(quick_byte_id=self.quick_byte_id).order_by('-quick_byte_image_id').first()
            return prev_new
        '''
        return False

    def quick_byte_image_title_for_url(self):
        return self.quick_byte_photo_name.strip().replace(' ', '-')

class QuickBytesTags(models.Model):
    quick_byte_id = models.IntegerField()
    tag_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'quick_bytes_tags'

class QuickBytesTopic(models.Model):
    quick_byte_id = models.IntegerField()
    topic_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'quick_bytes_topic'

