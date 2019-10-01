from django.db import models

# Create your models here.

class NewsletterTbl(models.Model):
    newsletter_id = models.AutoField(primary_key=True)
    newsletter_type = models.IntegerField()
    newsletter_title = models.CharField(max_length=255)
    newsletter_description = models.TextField()
    newsletter_image = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'newsletter_tbl'

class NewsletterSubscriber(models.Model):
    newsletter_subscriber_id = models.AutoField(primary_key=True)
    newsletter_type_id = models.IntegerField()
    subscriber_email_id = models.CharField(max_length=100)
    subscription_date = models.DateField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'newsletter_Subscriber'


