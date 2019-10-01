from django.db import models

# Create your models here.


class AuthorNewsletterSubscriber(models.Model):
    author_newsletter_subscriber_id = models.AutoField(primary_key=True)
    author_newsletter_type_id = models.IntegerField()
    subscriber_email_id = models.CharField(max_length=100)
    subscription_date = models.DateField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'author_newsletter_Subscriber'