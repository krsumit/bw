from django.shortcuts import render
# Create your views here.
import datetime
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import json
from authornewslatter.models import AuthorNewsletterSubscriber

def get_author_newsletter_Subscriber_details(request):
    if request.method == 'POST':
        newsletter_type_id=request.POST['newsletter_type_id']
        subscriber_email_id=request.POST['subscriber_email_id']
        subscription_date = datetime.datetime.now().date()
        if(subscriber_email_id!=''):
            subscriber_details = AuthorNewsletterSubscriber.objects.raw("SELECT author_newsletter_subscriber_id FROM author_newsletter_Subscriber  WHERE author_newsletter_type_id = "+newsletter_type_id+" AND subscriber_email_id='"+subscriber_email_id+"'")


            if len(list(subscriber_details)) > 0:
                return HttpResponse(
                    json.dumps({"checkuser": "allready exit this user"}),
                    content_type="application/json"
                )

            else:
                newsletter_Subscriber_details = AuthorNewsletterSubscriber(author_newsletter_type_id=newsletter_type_id, subscription_date=subscription_date,  subscriber_email_id = subscriber_email_id,status='1')
                newsletter_Subscriber_details.save()



            return HttpResponse(
                json.dumps({"success": "this is happening"}),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                json.dumps({"error": "this isn't happening"}),
                content_type="application/json"
            )







