# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.http import Http404
from django.template import RequestContext, loader
import pprint
import re
import string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from articles.models import Articles, ArticleImages,ArticleCategory, ArticleTopics, ArticleView
#from featuredbox.models import FeatureBox
from author.models import Author, AuthorType
from topics.models import ChannelTopics
from tags.models import ChannelTags
from columns.models import Columns
from category.models import ChannelCategory
from sponsored.models import Sponsoredposts,SponsoredpostsCategory,SponsoredpostsImages,SponsoredpostsView

from bwdesignworld.utils import sidebar_data, category_jump_list, closeDbConnection

# Create your views here.

def sponserLanding(request,sponsoredposts_title, sponsoredposts_published_date, sponsoredposts_id):
    global art_description_output

    sponsoredposts_title = sponsoredposts_title.replace('-', ' ')

    sponsoredposts_detail = Sponsoredposts.objects.raw("SELECT S.*, SI.image_url FROM sponsoredposts S LEFT JOIN sponsoredposts_images SI ON SI.sponsoredposts_id = S.sponsoredposts_id WHERE S.sponsoredposts_id = "+sponsoredposts_id+" AND S.sponsoredposts_title = '"+sponsoredposts_title+"' AND SI.image_status='enabled' GROUP BY S.sponsoredposts_id ORDER BY S.sponsoredposts_published_date DESC")

    #view count entry
    view_date = datetime.datetime.now().date()
    view_time = datetime.datetime.now().time()
    new_entry_sponsoredposts_view = SponsoredpostsView(sponsoredposts_id=sponsoredposts_id, view_date=view_date, view_time=view_time, sponsoredposts_published_date=sponsoredposts_detail[0].sponsoredposts_published_date)
    new_entry_sponsoredposts_view.save()
    #end

    sponsoredposts_description = sponsoredposts_detail[0].sponsoredposts_description


    related_articles = Articles.objects.raw("SELECT T.article_id ,COUNT(T.article_id), A.*,  AI.image_url FROM articles A JOIN article_images AI ON AI.article_id = A.article_id LEFT JOIN article_tags T ON T.article_id = A.article_id GROUP BY T.article_id HAVING COUNT(T.article_id)<=(SELECT MAX(mycount) FROM  (SELECT article_id, COUNT(article_id) mycount FROM article_tags GROUP BY article_id ) as temp ) ")

    #maximum_used_tags = ChannelTags.objects.raw("SELECT T . * , COUNT( A.article_id ) AS count FROM channel_tags T LEFT JOIN article_tags AT ON AT.tag_id = T.tag_id LEFT JOIN articles A ON AT.article_id = A.article_id GROUP BY T.tag_id ORDER BY count DESC")

    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()
    sponsored_detail = Sponsoredposts.objects.raw("SELECT S.*, SI.image_url FROM sponsoredposts S LEFT JOIN sponsoredposts_images SI ON SI.sponsoredposts_id = S.sponsoredposts_id  ORDER BY S.sponsoredposts_published_date DESC LIMIT 2")

    sidebar_zedo_ad = ''

    closeDbConnection()

    return render(request, 'sponsor/sponsor_landing_view.html',{
        'sponsoredposts_detail': sponsoredposts_detail[0],
        'sponsoredposts_description': sponsoredposts_description,
        'quick_bytes_listing':sidebar_dta['quick_bytes_listing'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'related_content':related_articles,
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'category_jumlist': category_jumlist,
        'sponsored_detail':sponsored_detail,
        'sidebar_zedo_ad': sidebar_zedo_ad,
    })

