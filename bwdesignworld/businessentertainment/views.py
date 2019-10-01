from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.http import Http404
from django.template import RequestContext, loader
import pprint
import string
# Create your views here.
from articles.models import Articles, ArticleImages, ArticleCategory, ArticleTopics, ArticleView
from bwdesignworld.utils import closeDbConnection

def business_entertainment(request):
    recent_entertainment_list = Articles.objects.raw("SELECT A.*, AU.*,AI.photopath, AI.image_url FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON A.article_id = AI.article_id LEFT JOIN  article_category AC ON A.article_id = AC.article_id WHERE AC.category_id = '64' GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 1, 6")

    recent_entertainment = Articles.objects.raw("SELECT A.*, AU.*, AI.photopath,AI.image_url FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON A.article_id = AI.article_id LEFT JOIN  article_category AC ON A.article_id = AC.article_id WHERE AC.category_id = '64' GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 1")

    closeDbConnection()

    return render(request, 'businessentertainment/business-of-entertainment.html', {
        'recent_entertainment_list':recent_entertainment_list,
        'recent_entertainment':recent_entertainment

    })
