# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import datetime
from django.http import Http404
from django.template import RequestContext, loader
import pprint
import string
import datetime
from django.template.defaultfilters import date
from django.utils import timezone
from django import forms
from haystack.forms import FacetedSearchForm, ModelSearchForm
import feedparser
from articles.models import Articles, ArticleImages, ArticleVideo
from masternewsletter.models import MasterNewsletter, MasterNewsletterArticles
import re

from django.apps import apps




# Create your views here.

def master_news_letter(request):
    #index 1
    recent_articles = Articles.objects.raw("SELECT A.*, AI.image_url, AI.photopath, AV.video_embed_code FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id  JOIN article_images AI ON AI.article_id = A.article_id LEFT JOIN article_video AV ON A.article_id = AV.article_id JOIN master_newsletter_articles MNL ON A.article_id = MNL.article_id  GROUP BY A.article_id ORDER BY  MNL.sequence, A.article_published_date DESC ")
  
    return render(request, 'static_pages/master_newsletter.html', {
        'recent_articles': recent_articles,
       


    })

