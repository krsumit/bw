# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import datetime
from django.http import Http404
from django.template import RequestContext, loader
import pprint
import string
import re
import datetime
from django.template.defaultfilters import date
from django.utils import timezone
from django import forms
from haystack.forms import FacetedSearchForm, ModelSearchForm
from magazineisuue.models import Magazine
from articles.models import Articles, ArticleImages, ArticleVideo,ArticleCategory, ArticleTopics
from author.models import Author, AuthorType
from category.models import ChannelCategory
from django.utils import timezone
from mastervideo.models import VideoMaster
from libs import templatetags
from quickbytes.models import QuickBytes, QuickBytesPhotos, QuickBytesTags
from bwdesignworld.utils import sidebar_data, category_jump_list

# Create your views here.

def homepage(request):
    #index 1
    recent_articles = Articles.objects.raw("SELECT A.article_id,A.article_title, A.article_description,A.article_summary,C.category_id, C.category_name, AI.image_url, AI.photopath FROM articles A  LEFT JOIN article_category AC ON A.article_id = AC.article_id  LEFT JOIN channel_category C ON C.category_id = AC.category_id  JOIN article_images AI ON AI.article_id = A.article_id  WHERE A.display_to_homepage = '1' AND AI.photopath !='' GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 21")
    recent_articles_rightsidebar = Articles.objects.raw("SELECT A.*, AU.*, AI.image_url, AI.photopath, AV.video_embed_code FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id JOIN article_images AI ON AI.article_id = A.article_id LEFT JOIN article_video AV ON A.article_id = AV.article_id WHERE A.display_to_homepage = '1' AND AI.photopath !='' GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 8")
    recent_important_article = Articles.objects.raw("SELECT A.article_id,A.article_title, A.article_description,A.article_summary, AU.*, AI.image_url, AI.photopath FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON A.article_id = AI.article_id WHERE A.display_to_homepage = '1'  AND A.important_article = 1 AND AI.photopath !='' GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 1")
    
    bwtv_articles = VideoMaster.objects.raw("SELECT * FROM video_master ORDER BY video_id DESC LIMIT 7")
    form = ModelSearchForm(searchqueryset=None, load_all=True)
   
    from django.db import connection

    connection.close()

    return render(request, 'homepage/onepage_index.html', {
        'recent_articles': recent_articles,
        'current_date_n_time': datetime.datetime.now(),
        'bwtv_articles':bwtv_articles,
        'recent_important_article': recent_important_article,
        'form': form,
        
    })

def robt(request):
    return render(request, './robots.txt',{

    })
