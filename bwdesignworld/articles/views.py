# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
import datetime
from django.http import Http404
from django.template import RequestContext, loader
import pprint
import re
import string
import feedparser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import HTMLParser
import xml.etree.ElementTree as ET
from django.conf import settings
from event.models import Event
from articles.models import Articles, ArticleImages, ArticleCategory, ArticleTopics, ArticleView, ArticleVideo,ArticleTotalView
#from featuredbox.models import FeatureBox
from author.models import Author, AuthorType
#from topics.models import ChannelTopics
from tags.models import ChannelTags
from columns.models import Columns
from category.models import ChannelCategory
#from newsletter.models import NewsletterTbl
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from bwdesignworld.utils import sidebar_data, category_jump_list, closeDbConnection
from sponsored.models import Sponsoredposts, SponsoredpostsCategory, SponsoredpostsImages, SponsoredpostsView
from mastervideo.models import VideoMaster
from magazineisuue.models import Magazine
# Create your views here.

# Article landing page
def articleLanding(request, article_title, article_published_date, article_id):
    global art_description_output

    #Sidebar and other data to be used in base template
    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()

    sidebar_zedo_ad = ''

    url_article_title = article_title
    article_title = article_title.replace('-', ' ')

    article_detail = Articles.objects.raw("SELECT A.*,AI.photopath, AI.image_url, AI.image_title FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN article_images AI ON A.article_id = AI.article_id  WHERE A.article_id = "+article_id+" AND (AI.image_status='enabled' OR AI.image_status is null)")

    if len(list(article_detail)) > 0:

        #view count entry
        view_date = datetime.datetime.now().date()
        view_time = datetime.datetime.now().time()
        new_entry_artcle_view = ArticleView(article_id=article_id, view_date=view_date, view_time=view_time, article_published_date=article_detail[0].article_published_date)
        new_entry_artcle_view.save()
        total_article_view = ArticleTotalView.objects.filter(article_id=article_id).first()
        #return HttpResponse(total_article_view.total_view)
        if(total_article_view):
            total_view = int(total_article_view.total_view) + 1
            total_view = int(total_view)
            total_article_view = ArticleTotalView.objects.get(article_id=article_id)
            total_article_view.total_view = total_view
            total_article_view.save()
        else:
            total_article_view = ArticleTotalView(article_id=article_id, total_view=1)
            total_article_view.save()

        #end

        #video url
        if(article_detail[0].video_type == 'uploadedvideo'):
            #video_master
            video_uploaded = VideoMaster.objects.filter(video_id=article_detail[0].video_Id).first()
            article_video = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + settings.VIDEO_MASTER + video_uploaded.video_name
            article_vid_thumb = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + settings.VIDEO_THUMB + video_uploaded.video_thumb_name
        elif(article_detail[0].video_type == 'embededvideocode'):
            video_embeded = ArticleVideo.objects.filter(article_id=article_id).first()
            article_video = video_embeded.video_embed_code.strip()
            article_vid_thumb = ''
        else:
            article_video = ''
            article_vid_thumb = ''
        #end

        #article image for og_image
        article_first_image = ArticleImages.objects.filter(article_id=article_id)[:1]
        #article_first_image = ''
        #end

        #article images for page slider
        article_all_image_count = ArticleImages.objects.filter(article_id=article_id).filter(image_status='enabled').count()
        article_all_image = ArticleImages.objects.filter(article_id=article_id).filter(image_status='enabled')
        #end

        article_description = article_detail[0].article_description

        article_tags = ChannelTags.objects.raw("SELECT t.* FROM channel_tags t INNER JOIN article_tags at ON t.tag_id = at.tag_id WHERE at.article_id = "+article_id)

        tag_names = ''
        for tag in article_tags:
            tag_names = tag_names+', '+tag.tag_name

        column_details = ''
        author_details = Author.objects.raw("SELECT AU.*, AUTYPE.* FROM author AU INNER JOIN article_author A_A ON A_A.author_id = AU.author_id JOIN author_type AUTYPE ON AU.author_type = AUTYPE.author_type_id WHERE A_A.article_id = "+article_id)
        if len(list(author_details)) > 0:
            author_label = author_details[0].label.replace(' ', '-')
            if author_details[0].author_type == 4:
                column_details = Columns.objects.raw("SELECT C.* FROM columns C LEFT JOIN author AU ON AU.column_id = C.column_id WHERE AU.author_id = "+str(author_details[0].author_id))
        else:
            author_label = ''

        #article_topic = ArticleTopics.objects.raw("SELECT T.* FROM article_topics AT LEFT JOIN channel_topics T ON AT.topic_id = T.topic_id WHERE AT.article_id = " + article_id)

        '''article_topic = ChannelTopics.objects.raw("SELECT t.* FROM channel_topics t INNER JOIN article_topics at ON t.topic_id = at.topic_id WHERE at.article_id = "+article_id)

        cat_regex = ''
        topic_names = ''
        for topic in article_topic:
            topic_names = topic_names+', '+topic.topic_name
            topic_nm = topic.topic_name.replace(' ', '-')
            topicId = str(topic.topic_id)
            topic_url = "/topics/"+topic_nm+"-"+topicId
            article_description = article_description.replace(topic.topic_name, "<a href='"+topic_url+"' style='text-decoration:underline'>"+topic.topic_name+"</a>")
            '''
        html_parser = HTMLParser.HTMLParser()
        article_description = html_parser.unescape(article_description)

        article_categories = ChannelCategory.objects.raw("SELECT C.* FROM channel_category C LEFT JOIN article_category AC ON AC.category_id = C.category_id WHERE AC.article_id = "+article_id)

        category_names = ''
        for category in article_categories:
            category_names = category_names+', '+category.category_name

        #Newsletter
        #newsletter = NewsletterTbl.objects.order_by('?').first()

        #next_article = article_detail.get_recent_article_descending();
        next_article = article_detail[0].get_recent_article_descending()
        previous_article = article_detail[0].get_recent_article_ascending()

        #Meta title and descriptons
        meta_title = article_title+' - BW wellness'
        meta_description = 'News and Updates for wellness in India - ' + category_names + '-' + article_detail[0].article_summary
        meta_keyword = tag_names

        og_title= article_title
        og_url= article_detail[0].get_absolute_url
        if len(list(article_first_image)) > 0:
            if(article_detail[0].is_old == 1):
                og_image= article_first_image[0].image_url
            else:
                og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + settings.ARTICLE_IMAGE_LARGE_PATH + article_first_image[0].photopath
        else:
            og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwdiff/images/BW-wellness-logo.jpg'

        if(article_detail[0].canonical_options == 1):
            canoical_tag = '<link rel="canonical" href="'+article_detail[0].canonical_url+'" />'
        else:
            canoical_tag = '<link rel="canonical" href="http://bwwellness.businessworld.in/article/'+url_article_title+'/'+article_published_date+'-'+article_id+'" />'
	amp_tag = '<link rel="amphtml" href="http://bwwellness.businessworld.in/amp/article/'+url_article_title+'/'+article_published_date+'-'+article_id+'" />'

        closeDbConnection()

        return render(request, 'article/article_landing_with_author.html',{
            'article_detail': article_detail[0],
            'article_description': article_description,
            'article_tags': article_tags,
            'author_details': author_details,
            'author_label': author_label,
            'column_details': column_details,
            'article_video': article_video,
            'article_vid_thumb': article_vid_thumb,
            'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
            'trending_now_topics': sidebar_dta['trending_now_topics'],
            'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
            'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
            'category_jumlist': category_jumlist,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'meta_keyword': meta_keyword,
            'og_title': og_title,
            'og_url': og_url,
            'og_image': og_image,
	    'amp_tag':amp_tag,
            'article_all_image': article_all_image,
            'article_all_image_count': article_all_image_count,
            'next_article': next_article,
            'previous_article': previous_article,
            'sidebar_zedo_ad': sidebar_zedo_ad,
            'canoical_tag': canoical_tag,
        })
    else:
        meta_title = 'Article - BW wellness'
        meta_description = 'Article'
        meta_keyword = 'Article'

        og_title= 'Article - BW wellness'
        #og_url= article_detail[0].get_absolute_url
        og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwdiff/images/BW-wellness-logo.jpg'

        return render(request, 'article/article_not_found.html',{
            'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
            #'related_content':related_articles,
            'trending_now_topics': sidebar_dta['trending_now_topics'],
            'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
            'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
            'category_jumlist': category_jumlist,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'meta_keyword': meta_keyword,
            'og_title': og_title,
            #'og_url': og_url,
            'og_image': og_image,
            'sidebar_zedo_ad': sidebar_zedo_ad,
        })
# Article landing page
def articleLandingAmp(request, article_title, article_published_date, article_id):
    global art_description_output

    #Sidebar and other data to be used in base template
    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()

    sidebar_zedo_ad = ''

    url_article_title = article_title
    article_title = article_title.replace('-', ' ')

    article_detail = Articles.objects.raw("SELECT A.*,AI.photopath, AI.image_url, AI.image_title FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN article_images AI ON A.article_id = AI.article_id  WHERE A.article_id = "+article_id+" AND (AI.image_status='enabled' OR AI.image_status is null)")

    if len(list(article_detail)) > 0:

        #video url
        if(article_detail[0].video_type == 'uploadedvideo'):
            #video_master
            video_uploaded = VideoMaster.objects.filter(video_id=article_detail[0].video_Id).first()
            article_video = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + settings.VIDEO_MASTER + video_uploaded.video_name
            article_vid_thumb = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + settings.VIDEO_THUMB + video_uploaded.video_thumb_name
        elif(article_detail[0].video_type == 'embededvideocode'):
            video_embeded = ArticleVideo.objects.filter(article_id=article_id).first()
            article_video = video_embeded.video_embed_code.strip()
            article_vid_thumb = ''
        else:
            article_video = ''
            article_vid_thumb = ''
        #end

        #article image for og_image
        article_first_image = ArticleImages.objects.filter(article_id=article_id)[:1]
        #article_first_image = ''
        #end

        #article images for page slider
        article_all_image_count = ArticleImages.objects.filter(article_id=article_id).filter(image_status='enabled').count()
        article_all_image = ArticleImages.objects.filter(article_id=article_id).filter(image_status='enabled')
        #end

        article_description = article_detail[0].article_description

        article_tags = ChannelTags.objects.raw("SELECT t.* FROM channel_tags t INNER JOIN article_tags at ON t.tag_id = at.tag_id WHERE at.article_id = "+article_id)

        tag_names = ''
        for tag in article_tags:
            tag_names = tag_names+', '+tag.tag_name

        column_details = ''
        author_details = Author.objects.raw("SELECT AU.*, AUTYPE.* FROM author AU INNER JOIN article_author A_A ON A_A.author_id = AU.author_id JOIN author_type AUTYPE ON AU.author_type = AUTYPE.author_type_id WHERE A_A.article_id = "+article_id)
        if len(list(author_details)) > 0:
            author_label = author_details[0].label.replace(' ', '-')
            if author_details[0].author_type == 4:
                column_details = Columns.objects.raw("SELECT C.* FROM columns C LEFT JOIN author AU ON AU.column_id = C.column_id WHERE AU.author_id = "+str(author_details[0].author_id))
        else:
            author_label = ''

       
        
        html_parser = HTMLParser.HTMLParser()
        article_description = html_parser.unescape(article_description)

        article_categories = ChannelCategory.objects.raw("SELECT C.* FROM channel_category C LEFT JOIN article_category AC ON AC.category_id = C.category_id WHERE AC.article_id = "+article_id)

        category_names = ''
        for category in article_categories:
            category_names = category_names+', '+category.category_name

        #Newsletter
        #newsletter = NewsletterTbl.objects.order_by('?').first()

        #next_article = article_detail.get_recent_article_descending();
        next_article = article_detail[0].get_recent_article_descending()
        previous_article = article_detail[0].get_recent_article_ascending()

        #Meta title and descriptons
        meta_title = article_title+' - BW wellness'
        meta_description = 'News and Updates for wellness in India - ' + category_names + '-' + article_detail[0].article_summary
        meta_keyword = tag_names

        og_title= article_title
        og_url= article_detail[0].get_absolute_url
        if len(list(article_first_image)) > 0:
            if(article_detail[0].is_old == 1):
                og_image= article_first_image[0].image_url
            else:
                og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + settings.ARTICLE_IMAGE_LARGE_PATH + article_first_image[0].photopath
        else:
            og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwdiff/images/BW-wellness-logo.jpg'

        if(article_detail[0].canonical_options == 1):
            canoical_tag = '<link rel="canonical" href="'+article_detail[0].canonical_url+'" />'
        else:
            canoical_tag = '<link rel="canonical" href="http://bwwellness.businessworld.in/article/'+url_article_title+'/'+article_published_date+'-'+article_id+'" />'

        closeDbConnection()

        return render(request, 'article/article_amp_landing_with_author.html',{
            'article_detail': article_detail[0],
            'article_description': article_description,
            'article_tags': article_tags,
            'author_details': author_details,
            'author_label': author_label,
            'column_details': column_details,
            'article_video': article_video,
            'article_vid_thumb': article_vid_thumb,
            'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
            'trending_now_topics': sidebar_dta['trending_now_topics'],
            'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
            'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
            'category_jumlist': category_jumlist,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'meta_keyword': meta_keyword,
            'og_title': og_title,
            'og_url': og_url,
            'og_image': og_image,
            'article_all_image': article_all_image,
            'article_all_image_count': article_all_image_count,
            'next_article': next_article,
            'previous_article': previous_article,
            'sidebar_zedo_ad': sidebar_zedo_ad,
            'canoical_tag': canoical_tag,
        })
    else:
        meta_title = 'Article - BW wellness'
        meta_description = 'Article'
        meta_keyword = 'Article'

        og_title= 'Article - BW wellness'
        #og_url= article_detail[0].get_absolute_url
        og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwdiff/images/BW-wellness-logo.jpg'

        return render(request, 'article/article_not_found.html',{
            'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
            #'related_content':related_articles,
            'trending_now_topics': sidebar_dta['trending_now_topics'],
            'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
            'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
            'category_jumlist': category_jumlist,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'meta_keyword': meta_keyword,
            'og_title': og_title,
            #'og_url': og_url,
            'og_image': og_image,
            'sidebar_zedo_ad': sidebar_zedo_ad,
        })

# Recent article listing
def recent_articles_listing(request):
    recent_articles = Articles.objects.raw("SELECT A.*, AU.*, AI.image_url,AI.photopath FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON AI.article_id = A.article_id WHERE (AI.image_status='enabled' OR AI.image_status is null) GROUP BY A.article_id ORDER BY A.article_published_date DESC")

    paginator = Paginator(list(recent_articles), 10) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)
    pg_url = page

    try:
        recent_articles = paginator.page(page)
        page_no = int(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        recent_articles = paginator.page(1)
        pg_url = 1
        page_no = 1

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_no = 1
        recent_articles = paginator.page(paginator.num_pages)


    adjacent_pages = 5

    #page_numbers = [n for n in \ range(paginator.num_pages - adjacent_pages, paginator.num_pages + adjacent_pages + 1) \ if n > 0 and n <= paginator.num_pages]
    page_numbers = [n for n in \
                    range(page_no - adjacent_pages, page_no + adjacent_pages + 1) \
                    if n > 0 and n <= page_no]

    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()

    meta_title = 'BW wellness - News and Updates for  wellness in India'
    meta_description = 'BW wellness - News and Updates for wellness in India'
    meta_keyword = 'Recent Articles,  BW wellness'

    og_title= 'BW wellness | Recent Articles'
    og_url= '/all-articles'
    og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwdiff/images/BW-wellness-logo.jpg'

    sidebar_zedo_ad = ''

    closeDbConnection()

    return render(request, 'article/listing.html', {
        "news_articles": recent_articles,
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'no_of_pages': no_of_pages,
        'page_title_h1': 'Latest Articles',
        'listing_page_url': '/all-articles-load',
        'view_page_url': '/all-articles',
        'category_jumlist': category_jumlist,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keyword': meta_keyword,
        'og_title': og_title,
        'og_url': og_url,
        'og_image': og_image,
        'sidebar_zedo_ad': sidebar_zedo_ad,
        'page_numbers':page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
        'last_page': paginator.num_pages
    })

def recent_articles_listing_load(request):
    recent_articles = Articles.objects.raw("SELECT A.*, AU.*,AI.photopath, AI.image_url FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON AI.article_id = A.article_id WHERE (AI.image_status='enabled' OR AI.image_status is null) GROUP BY A.article_id ORDER BY A.article_published_date DESC")

    paginator = Paginator(list(recent_articles), 6) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)
    sidebar_dta = sidebar_data()

    sidebar_zedo_ad = ''

    closeDbConnection()

    return render(request, 'article/listing_load.html', {
        "recent_articles": articles,
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'no_of_pages': no_of_pages,
        'sidebar_zedo_ad': sidebar_zedo_ad,
    })

def web_exclusivearticle(request):

    tree = ET.parse("/static/xml/exclusive.xml")
    root = tree.getroot()
    response_data = '<div class="block-content item-block-1 split-stuff blocks-3" id="itemblock">'
    for article in root.findall('exclusive')[:3]:
        article_id = article.find('article_id').text
        article_title = article.find('article_title').text
        article_published_date = article.find('article_published_date').text

        image_url = article.find('image_url').text
        #title_for_url = article_title.replace(' ', '-')
        title_for_url = re.sub('[^A-Za-z0-9]+', '-', article_title)

        response_data += '<div class="item-block"><div class="item-header"><a href="/article/'+title_for_url+'/'+article_published_date+'-'+article_id+'"><img src="'+image_url+'" alt="" width="100%" /></a></div>'
        response_data += '<div class="item-content"><h3><a href="/article/'+title_for_url+'/'+article_published_date+'-'+article_id+'">'+article_title+'</a></h3></div></div>'
    response_data += '</div>'

    meta_title = 'Web Exclusive Stories - BW wellness'
    meta_description = 'wellness'
    meta_keyword = 'Web Exclusive, News and Updates for wellness in India'

    return render(request, 'article/web-exclusive.html', {
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keyword': meta_keyword,
        'web_exclusive_dta': response_data,
    })







def column_articles(request):
    sidebar_zedo_ad = ''
    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()

    column_articles = Articles.objects.raw("SELECT A.*, AI.image_url, AI.photopath FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN article_images AI ON A.article_id = AI.article_id WHERE A_A.author_type='4' GROUP BY A.article_id ORDER BY A.article_published_date DESC ")

    paginator = Paginator(list(column_articles), 10) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)
    pg_url = page

    try:
        column_articles = paginator.page(page)
        page_no = int(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        column_articles = paginator.page(1)
        pg_url = 1
        page_no = 1

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_no = 1
        column_articles = paginator.page(paginator.num_pages)


    adjacent_pages = 5

    #page_numbers = [n for n in \ range(paginator.num_pages - adjacent_pages, paginator.num_pages + adjacent_pages + 1) \ if n > 0 and n <= paginator.num_pages]
    page_numbers = [n for n in \
                    range(page_no - adjacent_pages, page_no + adjacent_pages + 1) \
                    if n > 0 and n <= page_no]

    meta_title = 'Exclusive articles by Columnists - BW wellness - Page'+str(page_no)
    meta_description = 'Columnists at BW wellness analysis, dissects and opinionate on the latest financial situations and developments in India and world. Page '+str(page_no)+' of the list.'

    og_title = 'Exclusive articles by Columnists - BW wellness - Page'+str(page_no)
    og_url = '/columns'
    og_image='http://d1s8mqgwixvb29.cloudfront.net/static_bwdiff/images/BW-wellness-logo.jpg'


    return render(request, 'column/listing_column.html', {
        'column_articles': column_articles,
        'category_jumlist': category_jumlist,
        'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'sidebar_zedo_ad': sidebar_zedo_ad,
        'meta_title': meta_title,
        'meta_description': meta_description,

        'og_title': og_title,
        'og_url': og_url,
        'og_image':og_image,
        'page_numbers':page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
        'last_page': paginator.num_pages
    })

def exclusive_article(request):
    sidebar_zedo_ad = ''

    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()
    recent_exclusive_article = Articles.objects.raw("SELECT A.*, AI.image_url, AI.photopath FROM articles A LEFT JOIN article_images AI ON A.article_id = AI.article_id WHERE A.is_exclusive = '1' GROUP BY A.article_id ORDER BY A.article_published_date DESC ")
    paginator = Paginator(list(recent_exclusive_article), 10) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)
    pg_url = page

    try:
        recent_exclusive_article = paginator.page(page)
        page_no = int(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        recent_exclusive_article = paginator.page(1)
        pg_url = 1
        page_no = 1

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_no = 1
        recent_exclusive_article = paginator.page(paginator.num_pages)


    adjacent_pages = 5

    #page_numbers = [n for n in \ range(paginator.num_pages - adjacent_pages, paginator.num_pages + adjacent_pages + 1) \ if n > 0 and n <= paginator.num_pages]
    page_numbers = [n for n in \
                    range(page_no - adjacent_pages, page_no + adjacent_pages + 1) \
                    if n > 0 and n <= page_no]
    meta_title = 'Web Exclusive Stories - BW wellness - Page '+str(page_no)
    meta_description = 'Web Exclusive stories from News and Updates for wellness in India from BW wellness. Page '+str(page_no)+' of the list.'

    og_title = 'Web Exclusive Stories - BW wellness - Page '+str(page_no)
    og_url = '/online-exclusive'
    og_image = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwdiff/images/BW-wellness-logo.jpg'
    closeDbConnection()

    return render(request, 'webexclusive/webexclusivelisting.html', {
        'recent_exclusive_article': recent_exclusive_article,
        'category_jumlist': category_jumlist,
        'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'sidebar_zedo_ad': sidebar_zedo_ad,
        'meta_title': meta_title,
        'meta_description': meta_description,

        'og_title': og_title,
        'og_url': og_url,
        'og_image':og_image,
        'page_numbers':page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
        'last_page': paginator.num_pages
    })

def event_articles(request):
    sidebar_zedo_ad = ''

    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()
    event_articles = Event.objects.raw("SELECT *, datediff(start_date,CURDATE()) as datedi FROM event  where  end_date >=  CURDATE() AND valid=1 ORDER BY  datedi  asc ")
    paginator = Paginator(list(event_articles), 10) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)
    pg_url = page

    try:
        event_articles = paginator.page(page)
        page_no = int(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        event_articles = paginator.page(1)
        pg_url = 1
        page_no = 1

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_no = 1
        event_articles = paginator.page(paginator.num_pages)


    adjacent_pages = 5

    #page_numbers = [n for n in \ range(paginator.num_pages - adjacent_pages, paginator.num_pages + adjacent_pages + 1) \ if n > 0 and n <= paginator.num_pages]
    page_numbers = [n for n in \
                    range(page_no - adjacent_pages, page_no + adjacent_pages + 1) \
                    if n > 0 and n <= page_no]

    meta_title = 'BW Events - Events hosted and managed by BW wellness '
    meta_description = 'List upcoming and past Business Events hosted and Managed by BW wellness Media Pvvt. Ltd. '
    og_title = 'BW Events - Events hosted and managed by BW wellness'
    og_url = '/bw-events'
    og_image = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwdiff/images/BW-wellness-logo.jpg'
    eventpast_articles = Event.objects.raw("SELECT *, datediff(end_date,CURDATE()) as datedi FROM event where  end_date <=  CURDATE() AND  valid = 1 ORDER BY  datedi  desc")

    closeDbConnection()

    return render(request, 'event/event_listing.html', {
        'event_articles': event_articles,
        'eventpast_articles':eventpast_articles,
        'category_jumlist': category_jumlist,
        'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'sidebar_zedo_ad': sidebar_zedo_ad,
        'meta_title': meta_title,
        'meta_description': meta_description,

        'og_title': og_title,
        'og_url': og_url,
        'og_image':og_image,
        'page_numbers':page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
        'last_page': paginator.num_pages
    })

def news_articles(request):
    sidebar_zedo_ad = ''

    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()
    news_articles = Articles.objects.raw("SELECT A.*, AI.image_url, AI.photopath FROM articles A LEFT JOIN article_images AI ON A.article_id = AI.article_id WHERE A.article_type = '1' GROUP BY A.article_id ORDER BY A.article_published_date DESC ")
    paginator = Paginator(list(news_articles), 10) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)
    pg_url = page

    try:
        news_articles = paginator.page(page)
        page_no = int(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news_articles = paginator.page(1)
        pg_url = 1
        page_no = 1

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_no = 1
        news_articles = paginator.page(paginator.num_pages)


    adjacent_pages = 5

    #page_numbers = [n for n in \ range(paginator.num_pages - adjacent_pages, paginator.num_pages + adjacent_pages + 1) \ if n > 0 and n <= paginator.num_pages]
    page_numbers = [n for n in \
                    range(page_no - adjacent_pages, page_no + adjacent_pages + 1) \
                    if n > 0 and n <= page_no]
    meta_title = 'News and Updates for wellness in India and World - BW wellness'
    meta_description = 'News and Updates for wellness in India and around the world'
    meta_keyword = 'News and Updates for wellness in India'
    og_title = 'News and Updates for wellness in India and World - BW wellness'
    og_url = '/business-news'
    og_image = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwhr/images/BW-wellness-logo.jpg'
    closeDbConnection()

    return render(request, 'article/listing.html', {

        'news_articles': news_articles,
        'category_jumlist': category_jumlist,
        'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'sidebar_zedo_ad': sidebar_zedo_ad,
        'page_title_h1': 'Business News',
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keyword': meta_keyword,
        'og_title': og_title,
        'og_url': og_url,
        'og_image':og_image,
        'page_numbers':page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
        'last_page': paginator.num_pages
    })

def opinion_articles(request):
    sidebar_zedo_ad = ''

    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()
    opinion_articles = Articles.objects.raw("SELECT A.*, AI.image_url, AI.photopath FROM articles A LEFT JOIN article_images AI ON A.article_id = AI.article_id WHERE A.article_type = '2' GROUP BY A.article_id ORDER BY A.article_published_date DESC")
    paginator = Paginator(list(opinion_articles), 10) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)
    pg_url = page

    try:
        opinion_articles = paginator.page(page)
        page_no = int(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        opinion_articles = paginator.page(1)
        pg_url = 1
        page_no = 1

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_no = 1
        opinion_articles = paginator.page(paginator.num_pages)


    adjacent_pages = 5

    #page_numbers = [n for n in \ range(paginator.num_pages - adjacent_pages, paginator.num_pages + adjacent_pages + 1) \ if n > 0 and n <= paginator.num_pages]
    page_numbers = [n for n in \
                    range(page_no - adjacent_pages, page_no + adjacent_pages + 1) \
                    if n > 0 and n <= page_no]
    meta_title = 'Opinion and Analysis of latest News and Updates for wellness in India by Experts - BW wellness'
    meta_description = 'Opinion and Analysis of latest News and Updates for wellness in India by Experts, Columnists and Comments - BW wellness'
    meta_keyword = 'News and Updates for wellness Opinion and Analysis in India, News and Updates for wellness in India Interviews'
    og_title = 'Opinion and Analysis of latest News and Updates for wellness in India News by Experts - BW wellness'
    og_url = '/business-opinion-analysis'
    og_image = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwhr/images/BW-wellness-logo.jpg'
    closeDbConnection()
    return render(request, 'article/listing.html', {

        'news_articles': opinion_articles,
        'category_jumlist': category_jumlist,
        'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'sidebar_zedo_ad': sidebar_zedo_ad,
        'meta_title': meta_title,
        'page_title_h1': 'Opinion & Analysis',
        
        'meta_description': meta_description,
        'meta_keyword': meta_keyword,
        'og_title': og_title,
        'og_url': og_url,
        'og_image':og_image,
        'page_numbers':page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
        'last_page': paginator.num_pages
    })

def Interviews_articles(request):
    sidebar_zedo_ad = ''

    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()
    interview_articles = Articles.objects.raw("SELECT A.*, AU.*, AI.image_url, AI.photopath FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON A.article_id = AI.article_id WHERE  A.article_type = 3 GROUP BY A.article_id ORDER BY A.article_published_date DESC")
    paginator = Paginator(list(interview_articles), 10) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)
    pg_url = page

    try:
        interview_articles = paginator.page(page)
        page_no = int(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        interview_articles = paginator.page(1)
        pg_url = 1
        page_no = 1

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_no = 1
        interview_articles = paginator.page(paginator.num_pages)


    adjacent_pages = 5

    #page_numbers = [n for n in \ range(paginator.num_pages - adjacent_pages, paginator.num_pages + adjacent_pages + 1) \ if n > 0 and n <= paginator.num_pages]
    page_numbers = [n for n in \
                    range(page_no - adjacent_pages, page_no + adjacent_pages + 1) \
                    if n > 0 and n <= page_no]
    meta_title = 'Opinion and Analysis of latest News and Updates for wellness in India by Experts - BW wellness'
    meta_description = 'Opinion and Analysis of latest News and Updates for wellness in India by Experts, Columnists and Comments - BW wellness'
    meta_keyword = 'News and Updates for wellness Business Opinion and Analysis in India, Hotel Industry and Hospitality Interviews'
    og_title = 'Opinion and Analysis of latest News and Updates for wellness in India Business News by Experts - BW wellness'
    og_url = '/business-opinion-analysis'
    og_image = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwhr/images/BW-wellness-logo.jpg'
    closeDbConnection()
    return render(request, 'article/listing.html', {

        'news_articles': interview_articles,
        'category_jumlist': category_jumlist,
        'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'sidebar_zedo_ad': sidebar_zedo_ad,
        'meta_title': meta_title,
        'page_title_h1': 'Interviews Articles',
        'meta_description': meta_description,
        'meta_keyword': meta_keyword,
        'og_title': og_title,
        'og_url': og_url,
        'og_image':og_image,
        'page_numbers':page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
        'last_page': paginator.num_pages
    })



def feature_articles(request):
    sidebar_zedo_ad = ''

    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()
    feature_articles = Articles.objects.raw("SELECT A.*, AI.image_url, AI.photopath FROM articles A LEFT JOIN article_images AI ON A.article_id = AI.article_id WHERE A.article_type = '5' GROUP BY A.article_id ORDER BY A.article_published_date DESC")
    paginator = Paginator(list(feature_articles), 10) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)
    pg_url = page

    try:
        feature_articles = paginator.page(page)
        page_no = int(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        feature_articles = paginator.page(1)
        pg_url = 1
        page_no = 1

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_no = 1
        feature_articles = paginator.page(paginator.num_pages)


    adjacent_pages = 5

    #page_numbers = [n for n in \ range(paginator.num_pages - adjacent_pages, paginator.num_pages + adjacent_pages + 1) \ if n > 0 and n <= paginator.num_pages]
    page_numbers = [n for n in \
                    range(page_no - adjacent_pages, page_no + adjacent_pages + 1) \
                    if n > 0 and n <= page_no]

    meta_title = 'News and Updates for wellness in India Business Features of BW wellness'
    meta_description = 'Feature stories around News and Updates for wellness in India Business. BW wellness'
    og_image = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwhr/images/BW-wellness-logo.jpg'
    meta_keyword = 'News and Updates for wellness  Business in India, News and Updates for wellness in India Interviews'
    og_title = 'News and Updates for wellness in India Business Features covered by inhouse reporters of BW wellness'
    og_url = '/business-feature-stories'
    closeDbConnection()
    return render(request, 'article/article_feature_type_listing.html', {

        'feature_articles': feature_articles,
        'category_jumlist': category_jumlist,
        'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'sidebar_zedo_ad': sidebar_zedo_ad,
        'meta_title': meta_title,
        'page_title_h1': 'Feature Articles',
        'meta_description': meta_description,
        'meta_keyword': meta_keyword,
        'og_title': og_title,
        'og_url': og_url,
        'og_image':og_image,
        'page_numbers':page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
        'last_page': paginator.num_pages
    })

import datetime
def article_list_time_wise(request,article_published_date):
    sidebar_zedo_ad = ''
    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()

    today = datetime.datetime.strptime(article_published_date, "%d-%B-%Y")
    todays =str(today)[:10]
    article_list_time = Articles.objects.raw("SELECT A.*, AI.image_url, AI.photopath FROM articles A LEFT JOIN article_images AI ON A.article_id = AI.article_id WHERE DATE_FORMAT(article_published_date, '%%Y-%%m-%%d')= '"+str(todays)+"' GROUP BY A.article_id ORDER BY A.article_published_date DESC")
    paginator = Paginator(list(article_list_time), 10) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)
    pg_url = page

    try:
        article_list_time = paginator.page(page)
        page_no = int(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        article_list_time = paginator.page(1)
        pg_url = 1
        page_no = 1

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_no = 1
        article_list_time = paginator.page(paginator.num_pages)


    adjacent_pages = 5

    #page_numbers = [n for n in \ range(paginator.num_pages - adjacent_pages, paginator.num_pages + adjacent_pages + 1) \ if n > 0 and n <= paginator.num_pages]
    page_numbers = [n for n in \
                    range(page_no - adjacent_pages, page_no + adjacent_pages + 1) \
                    if n > 0 and n <= page_no]

    meta_title = 'News and Updates for wellness Business in India on' +todays
    meta_description = 'List of news, opinion and analysis stories published on  '+todays+'  on BW wellness. Page 1 of list'
    og_image = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwhr/images/BW-wellness-logo.jpg'
    og_title = 'News and Updates for wellness in India Business in India on'+todays
    og_url = '/date/ '+str(today)
    closeDbConnection()
    return render(request, 'article/article_listing_time_wise.html', {

        'article_list_time': article_list_time,
        'category_jumlist': category_jumlist,
        'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'sidebar_zedo_ad': sidebar_zedo_ad,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'og_image':og_image,
        'og_title': og_title,
        'og_url': og_url,
        'today':today,
        'page_numbers':page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
        'last_page': paginator.num_pages

    })
# magzine issue article listing
def magzine_articles_listing(request,year,magazine_id,title):
    magazinshow = Magazine.objects.raw("SELECT * FROM magazine  where magazine_id ="+magazine_id+"")
    magzine_articles = Articles.objects.raw("SELECT A.*, AU.*, AI.image_url,AI.photopath FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON AI.article_id = A.article_id WHERE (AI.image_status='enabled' OR AI.image_status is null)  AND magzine_issue_name = "+magazine_id+"  GROUP BY A.article_id ORDER BY A.article_published_date DESC")

    paginator = Paginator(list(magzine_articles), 10) # Show 6 articles per page

    page = request.GET.get('page')
    no_of_pages = range(1, paginator.num_pages+1)
    pg_url = page

    try:
        magzine_articles = paginator.page(page)
        page_no = int(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        magzine_articles = paginator.page(1)
        pg_url = 1
        page_no = 1

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_no = 1
        magzine_articles = paginator.page(paginator.num_pages)


    adjacent_pages = 5

    #page_numbers = [n for n in \ range(paginator.num_pages - adjacent_pages, paginator.num_pages + adjacent_pages + 1) \ if n > 0 and n <= paginator.num_pages]
    page_numbers = [n for n in \
                    range(page_no - adjacent_pages, page_no + adjacent_pages + 1) \
                    if n > 0 and n <= page_no]


    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()

    meta_title = 'Magazine- '+ str(magazinshow[0].title) +' -'+ str(magazinshow[0].publish_date_m)+' BW wellness'
    meta_description = 'BW wellness Magazine published on '+ str(magazinshow[0].publish_date_m)+' with cover story '+ str(magazinshow[0].title) +'. Read all stories from the'
    meta_keyword = 'magazine issue,  BW wellness'

    og_title= 'Magazine- '+ str(magazinshow[0].title) +' -'+ str(magazinshow[0].publish_date_m)+' BW wellness'
    og_url= '/magazine-issues/'+str(year)+'/'+str(magazinshow[0].title)+'-'+str(magazine_id)+'/web-view'
    if (magazinshow[0].imagepath ==''):
        og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwhr/images/BW-wellness-logo.jpg'
       
    else:
        og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + settings.MAGAZINE_IMAGE_PATH_URL + magazinshow[0].imagepath

    sidebar_zedo_ad = '<!-- Javascript tag  --><!-- begin ZEDO for channel:  Internal Pages , publisher:  wellness , Ad Dimension: Medium Rectangle-300x250-IP - 300 x 250 --><script language="JavaScript">var zflag_nid="3336"; var zflag_cid="4"; var zflag_sid="1"; var zflag_width="300"; var zflag_height="250"; var zflag_sz="22"; </script><script language="JavaScript" src="http://xp2.zedo.com/jsc/xp2/fo.js"></script><!-- end ZEDO for channel:  Internal Pages , publisher: BW Hotelier , Ad Dimension: Medium Rectangle-300x250-IP - 300 x 250 -->'

    closeDbConnection()

    return render(request, 'article/article_feature_type_listing.html', {
        'feature_articles': magzine_articles,
        'category_jumlist': category_jumlist,
        'quick_bytes_listing': sidebar_dta['quick_bytes_listing'],
        'bwtv_cat_details': sidebar_dta['bwtv_cat_details'],
        'sidebar_recent_articles': sidebar_dta['sidebar_recent_articles'],
        'trending_now_topics': sidebar_dta['trending_now_topics'],
        'sidebar_zedo_ad': sidebar_zedo_ad,
        'page_title_h1': 'Magazine Articles',
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keyword': meta_keyword,
        'og_title': og_title,
        'og_url': og_url,
        'og_image':og_image,
        'page_numbers':page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
        'last_page': paginator.num_pages
    })

