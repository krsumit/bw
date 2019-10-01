from django.db import models
import re
# Create your models here.
'''
class ChannelQuote(models.Model):
    quote_id = models.AutoField(primary_key=True)
    quote_description = models.TextField()
    quote_category = models.TextField()
    quote_author_name = models.TextField()
    quote_update_at = models.DateTimeField(db_column='quote_update-at')  # Field renamed to remove unsuitable characters.
    quote_created_at = models.DateTimeField()
    quote_status = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'channel_quote'


    def quote_author_name_for_url(self):
        return self.quote_author_name.strip().replace(' ', '-')
'''

class ChannelQuote(models.Model):
    quote_id = models.AutoField(primary_key=True)
    quote = models.TextField()
    quote_description = models.TextField()
    q_author_id = models.IntegerField()
    q_tags = models.CharField(max_length=100)
    quote_author_name = models.TextField()
    valid = models.IntegerField()
    quote_update_at = models.DateTimeField()
    quote_created_at = models.DateTimeField()
    quote_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'channel_quote'

    def get_next(self):
        next = ChannelQuote.objects.filter(quote_id__gt=self.quote_id)
        if next:
            return next[0]
        else:
            next_new = ChannelQuote.objects.first()
            return next_new
        return False

    def quote_author_name_for_url(self):
        tag_name = Quotetags.objects.filter(tag_id=self.q_tags).first()
        if tag_name:
            return tag_name.tag.strip().replace(' ', '-')
        else:
            return ''

    def quote_author_name_for_display(self):
        tag_name = Quotetags.objects.filter(tag_id=self.q_tags).first()
        if tag_name:
            return tag_name.tag
        else:
            return ''



class Quotesauthor(models.Model):
    author_id = models.AutoField(primary_key=True)
    author_name = models.CharField(max_length=255)
    valid = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'quotesauthor'

    def quote_author_name_for_url(self):
        return self.author_name.strip().replace(' ', '-')


class Quotetags(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=255)
    valid = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'quotetags'
