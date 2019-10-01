from django.shortcuts import render
# Create your views here.
import datetime
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import json
from newsletter.models import NewsletterTbl,NewsletterSubscriber
from bwdesignworld.utils import closeDbConnection

def get_newsletter_Subscriber_details(request):
   if request.method == 'POST':
        
        newsletter_type_id=request.POST['newsletter_type_id']
        subscriber_email_id=request.POST['subscriber_email_id']
        subscription_date = datetime.datetime.now().date()
        if(subscriber_email_id!=''):
            subscriber_details = NewsletterSubscriber.objects.raw("SELECT newsletter_subscriber_id FROM newsletter_Subscriber  WHERE newsletter_type_id = "+newsletter_type_id+" AND subscriber_email_id='"+subscriber_email_id+"'")

            closeDbConnection()

            if len(list(subscriber_details)) > 0:
                return HttpResponse(
                    json.dumps({"checkuser": "allready exit this user"}),
                    content_type="application/json"
                )

            else:
                newsletter_Subscriber_details = NewsletterSubscriber(newsletter_type_id=newsletter_type_id, subscription_date=subscription_date,  subscriber_email_id = subscriber_email_id,status='1')
                newsletter_Subscriber_details.save()

                closeDbConnection()

            return HttpResponse(
                json.dumps({"success": "this is happening"}),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                json.dumps({"error": "this isn't happening"}),
                content_type="application/json"
            )


    
