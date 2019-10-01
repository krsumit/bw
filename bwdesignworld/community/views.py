from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.http import Http404
from django.template import RequestContext, loader
import pprint
import string
import feedparser
# Create your views here.
def community_content (request):
    feeds_cric = feedparser.parse('http://bwcio.com/feed/')
    feeds_bws = feedparser.parse('http://bwsmartcities.com/feed')
    feeds_bwh = feedparser.parse('http://bwhotelier.com/feed/')
    return render(request, 'community/community.html', {
        'feeds_cric':feeds_cric,
        'feeds_bws':feeds_bws,
        'feeds_bwh':feeds_bwh
    })
    