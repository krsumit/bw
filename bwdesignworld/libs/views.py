from django.shortcuts import render
from django.http import HttpResponse
import xml.etree.ElementTree as ET
import datetime
from django.utils import timezone
from django.http import HttpResponseRedirect
#from reportlab.lib.pagesizes import letter
import json
import re
import urllib2
from io import BytesIO
from django.conf import settings
#from reportlab.pdfgen import canvas
#from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.defaultfilters import date
#import dateutil.parser
from libs.models import Contactus
from author.models import Author, AuthorType
from articles.models import Articles, ArticleImages, ArticleCategory, ArticleTopics, ArticleView
from bwdesignworld.utils import sidebar_data, category_jump_list
import hashlib
import feedparser
import HTMLParser
from django.utils.html import remove_tags
# Create your views here.

# Exclusive articles header data
def exclusive_articles(request):
    #if request.method == 'POST':
    tree = ET.parse("/opt/python/current/app/bwhr/static/xml/exclusive.xml")
    root = tree.getroot()
    response_data = '<div class="menu-content-inner" style="width:100% !important;">'
    for article in root.findall('exclusive'):
        article_id = article.find('article_id').text
        article_title = article.find('article_title').text
        article_published_date = article.find('article_published_date').text

        image_url = article.find('image_url').text
        #title_for_url = article_title.replace(' ', '-')
        title_for_url = re.sub('[^A-Za-z0-9]+', '-', article_title)

        response_data += '<div class="article-column" style="width:22% !important; margin:0 1.5% !important">'
        response_data += '<a href="/article/'+title_for_url+'/'+article_published_date+'-'+article_id+'"><img src="'+image_url+'" alt="" /></a>'
        response_data += '<h3><a href="/article/'+title_for_url+'/'+article_published_date+'-'+article_id+'">'+article_title+'</a></h3></div>'

    response_data += '</div>'
    return HttpResponse(response_data)
    #else:
        #return HttpResponse()

# Event articles header data
def event_articles(request):
    #if request.method == 'POST':
    tree = ET.parse("/opt/python/current/app/bwhr/static/xml/event_articles.xml")
    root = tree.getroot()
    response_data = '<div class="menu-content-inner" style="width:100% !important;">'
    for event in root.findall('events'):
        event_id = event.find('event_id').text
        title = event.find('title').text
        created_at = event.find('created_at').text

        image_url = event.find('image_url').text
        title_for_url = title.replace(' ', '-')

        response_data += '<div class="article-column" style="width:22% !important; margin:0 1.5% !important">'
        response_data += '<a href="/event/'+title_for_url+'/'+created_at+'-'+event_id+'"><img src="'+image_url+'" alt="" /></a>'
        response_data += '<h3><a href="/event/'+title_for_url+'/'+created_at+'-'+event_id+'">'+title+'</a></h3></div>'

    response_data += '</div>'
    return HttpResponse(response_data)
    #else:
        #return HttpResponse()

# Event Listing page data
def event_listing(request):
    if request.method == 'POST':
        tree = ET.parse("/opt/python/current/app/bwhr/static/xml/events_listing.xml")
        root = tree.getroot()
        response_data = '<div class="block-content item-block-1 split-stuff blocks-3" id="itemblock">'
        for event in root.findall('eventsListing'):
            event_id = event.find('event_id').text
            title = event.find('title').text
            created_at = event.find('created_at').text

            image_url = event.find('image_url').text
            category = event.find('category').text
            title_for_url = title.replace(' ', '-')

            response_data += '<div class="item-block"><div class="item-header">'
            response_data += '<a href="/event/'+title_for_url+'/'+created_at+'-'+event_id+'"><img src="'+image_url+'" alt="" /></a></div>'
            response_data += '<div class="item-content"><h3><a href="/event/'+title_for_url+'/'+created_at+'-'+event_id+'">'+title+'</a>'+created_at+'</h3><div class="item-author">'+category+'</div></div></div>'

        response_data += '</div>'
        return HttpResponse(response_data)
    else:
        return HttpResponse()

# Exclusive articles page data
def exclusive_onpagearticles(request):
    if request.method == 'POST':
        tree = ET.parse("/opt/python/current/app/bwhr/static/xml/exclusive.xml")
        root = tree.getroot()
        response_data = '<div class="block-content item-block-1 split-stuff blocks-3" id="itemblock">'
        for article in root.findall('exclusive'):
            article_id = article.find('article_id').text
            article_title = article.find('article_title').text
            article_published_date = article.find('article_published_date').text

            image_url = article.find('image_url').text
            #title_for_url = article_title.replace(' ', '-')
            title_for_url = re.sub('[^A-Za-z0-9]+', '-', article_title)
        
            response_data += '<div class="item-block"><div class="item-header"><a href="/article/'+title_for_url+'/'+article_published_date+'-'+article_id+'"><img src="'+image_url+'" alt="" width="371px"height="210px"/></a></div>'
            response_data += '<div class="item-content"><h3><a href="/article/'+title_for_url+'/'+article_published_date+'-'+article_id+'">'+article_title+'</a></h3></div></div>'
              
        response_data += '</div>'
        return HttpResponse(response_data)
    else:
        return HttpResponse()

## Popular Post data
def popular_articles(request):
    if request.method == 'POST':
        day_name = request.POST['day_nm']
        tree = ET.parse("/opt/python/current/app/bwhr/static/xml/popular_"+day_name+".xml")
        root = tree.getroot()
        response_data = '<div class="photo-gallery-grid" id="populardata">'
        for article in root.findall('popularArticles'):
            article_id = article.find('article_id').text
            article_title = article.find('article_title').text
            article_published_date = article.find('article_published_date').text

            image_url = article.find('image_url').text
            #title_for_url = article_title.replace(' ', '-')
            title_for_url = re.sub('[^A-Za-z0-9]+', '-', article_title)

            response_data += '<div class="item"><div style="box-shadow: inset 0 0 0 7px #999999;" class="item-header">'
            response_data += '<a href="/article/'+title_for_url+'/'+article_published_date+'-'+article_id+'"><img src="'+image_url+'" alt="" style="width:160px !important; height:105px !important;" /></a>'
            response_data += '</div><h3><a href="/article/'+title_for_url+'/'+article_published_date+'-'+article_id+'">'+article_title+'</a></h3></div>'

        response_data += '</div>'
        return HttpResponse(response_data)
    else:
        return HttpResponse()

# Columns header data
def columns_data(request):
    #if request.method == 'POST':

    columnist_label = AuthorType.objects.filter(author_type_id = '4').first()
    author_label = str(columnist_label.label.replace(' ', '-'))

    tree = ET.parse("/opt/python/current/app/bwhr/static/xml/columnist.xml")
    root = tree.getroot()
    response_data = ''
    for columnist in root.findall('columnist'):
        author_id = columnist.find('author_id').text
        author_name = columnist.find('author_name').text
        author_image_url = columnist.find('author_image_url')
        image_url = ''
        if author_image_url is None:
            image_url = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwhr/images/author_dummy.png'
        else:
            image_url = author_image_url.text
        response_data += '<a style="line-height:30px;" href="/author/'+author_label+'/'+author_name+'-'+author_id+'"><img src="'+image_url+'" width="50px" height="30px"  />  '+author_name+'</a>'
            #/author/{{recent_article_author_label}}/{{recent_article_author.0.author_name_for_url|urlencode}}-{{recent_article_author.0.author_id}}

    tree = ET.parse("/opt/python/current/app/bwhr/static/xml/column_articles.xml")
    root = tree.getroot()
    response_data += '<div class="menu-content-inner">'
    for article in root.findall('columnArticles'):
        article_id = article.find('article_id').text
        article_title = article.find('article_title').text
        article_published_date = article.find('article_published_date').text
        image_url = article.find('image_url').text
        #title_for_url = article_title.replace(' ', '-')
        title_for_url = re.sub('[^A-Za-z0-9]+', '-', article_title)

        response_data += '<div class="article-column" style="width:22% !important; margin:0 1.5% !important">'
        response_data += '<a href="/article/'+title_for_url+'/'+article_published_date+'-'+article_id+'"><img src="'+image_url+'" alt="" /></a>'
        response_data += '<h3><a href="/article/'+title_for_url+'/'+article_published_date+'-'+article_id+'">'+article_title+'</a></h3></div>'

    response_data += '</div>'
    return HttpResponse(response_data)
    #else:
        #return HttpResponse()

# Exclusive articles header data
def bwtv_articles(request):
    #if request.method == 'POST':
    tree = ET.parse("/opt/python/current/app/bwhr/static/xml/bwtv_articles.xml")
    root = tree.getroot()
    response_data = '<div class="menu-content-inner" style="width:100% !important;">'
    for article in root.findall('bwtvArticles'):
        article_id = article.find('article_id').text
        article_title = article.find('article_title').text
        article_published_date = article.find('article_published_date').text

        image_url = article.find('image_url').text
        #title_for_url = article_title.replace(' ', '-')
        title_for_url = re.sub('[^A-Za-z0-9]+', '-', article_title)

        response_data += '<div class="article-column" style="width:22% !important; margin:0 1.5% !important">'
        response_data += '<a href="/article/'+title_for_url+'/'+article_published_date+'-'+article_id+'"><img src="'+image_url+'" alt="" /></a>'
        response_data += '<h3><a href="/article/'+title_for_url+'/'+article_published_date+'-'+article_id+'">'+article_title+'</a></h3></div>'

    response_data += '</div>'
    return HttpResponse(response_data)
    #else:
        #return HttpResponse()

def static_google4f73e6c07e7339f8(request):
    return render(request, 'static_pages/google4f73e6c07e7339f8.html', {
        
    })

def static_rss_feeds(request):

    sidebar_dta = sidebar_data()
    category_jumlist = category_jump_list()

    meta_title = 'RSS Feeds, Latest Feeds, Latest XML Feeds - News and Updates for HR Professional in India - BW people'
    meta_description = "Latest RSS Feeds, Latest XML Feeds for News and Updates for HR Professional in India, News and Updates for HR Professional in India from BW people"
    meta_keyword = 'RSS Feeds,  BW people'

    og_title= 'RSS Feeds, Latest Feeds, Latest XML Feeds - News and Updates for HR Professional in India - BW people'
    og_url= '/rss-feed'
    og_image= settings.AWS_S3_BASE_URL + settings.BUCKET_PATH +'static_bwhr/images/BW-people-logo.jpg'

    return render(request, 'static_pages/rss-feed.html', {
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
    })

def createJsonValues(request, secret_key):

    now = datetime.datetime.now()
    today_dt = now.strftime("%d%m%Y")
    mystring = 'businessworld'
    new_string = today_dt+mystring
    #return HttpResponse(new_string)
    hash_object = hashlib.md5(new_string.encode())
    my_secret_key = hash_object.hexdigest()

    if(my_secret_key == secret_key):

        recent_articles = Articles.objects.raw("SELECT A.*, AU.*, AI.image_url, AI.photopath, AV.video_embed_code FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id JOIN article_images AI ON AI.article_id = A.article_id LEFT JOIN article_video AV ON A.article_id = AV.article_id WHERE A.display_to_homepage = '1' AND AI.photopath !='' GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 8")
        recent_articles_json = []
        for article in recent_articles:
            art_elem = {}
            art_elem['article_title'] = article.article_title
            art_elem['article_published_date'] = str(article.article_published_date)
            art_elem['article_id'] = article.article_id
            art_elem['photopath'] = article.photopath
            art_elem['video_type'] = article.video_type
            art_elem['important_article'] = article.important_article
            art_elem['absolute_url'] = article.get_absolute_url()
            recent_articles_json.append(art_elem)

        bwtv_articles = VideoMaster.objects.raw("SELECT * FROM video_master ORDER BY video_id DESC LIMIT 6")
        bwtv_articles_json = []
        for article in bwtv_articles:
            art_elem = {}
            art_elem['video_title'] = article.video_title
            art_elem['video_thumb_name'] = article.video_thumb_name
            art_elem['absolute_url'] = article.get_absolute_url()
            bwtv_articles_json.append(art_elem)
        
        recent_important_article = Articles.objects.raw("SELECT A.*, AU.*, AI.image_url, AI.photopath FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON A.article_id = AI.article_id WHERE A.display_to_homepage = '1' AND A.important_article = '1' GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 1")
        recent_important_article_json = []
        for article in recent_important_article:
            art_elem = {}
            art_elem['article_title'] = article.article_title
            art_elem['article_published_date'] = str(article.article_published_date)
            art_elem['article_id'] = article.article_id
            art_elem['photopath'] = article.photopath
            art_elem['video_type'] = article.video_type
            art_elem['article_summary'] = article.article_summary
            art_elem['author_name'] = article.author_name
            author_url = article.get_article_author_url()
            art_elem['author_url'] = author_url
            art_elem['absolute_url'] = article.get_absolute_url()
            recent_important_article_json.append(art_elem)

        recent_exclusive_article = Articles.objects.raw("SELECT A.*, AI.image_url, AI.photopath FROM articles A LEFT JOIN article_images AI ON A.article_id = AI.article_id WHERE A.is_exclusive = '1' GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 4")
        recent_exclusive_article_json = []
        for article in recent_exclusive_article:
            art_elem = {}
            art_elem['article_title'] = article.article_title
            art_elem['article_published_date'] = str(article.article_published_date)
            art_elem['article_id'] = article.article_id
            art_elem['photopath'] = article.photopath
            art_elem['video_type'] = article.video_type
            art_elem['article_summary'] = article.article_summary
            author_url = article.get_article_author_url()
            art_elem['author_url'] = author_url
            art_elem['absolute_url'] = article.get_absolute_url()
            recent_exclusive_article_json.append(art_elem)

        column_articles = Articles.objects.raw("SELECT A.*, AU.*, AI.image_url, AI.photopath FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON A.article_id = AI.article_id WHERE A_A.author_type='4' GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 4")
        column_articles_json = []
        for article in column_articles:
            art_elem = {}
            art_elem['article_title'] = article.article_title
            art_elem['article_published_date'] = str(article.article_published_date)
            art_elem['article_id'] = article.article_id
            art_elem['photopath'] = article.photopath
            art_elem['video_type'] = article.video_type
            art_elem['article_summary'] = article.article_summary
            art_elem['author_name'] = article.author_name
            author_url = article.get_article_author_url()
            art_elem['author_url'] = author_url
            art_elem['absolute_url'] = article.get_absolute_url()
            column_articles_json.append(art_elem)

        columnist = Author.objects.raw("SELECT * FROM (SELECT AU.*, AR.article_published_date FROM author AU INNER JOIN article_author ARU ON AU.author_id = ARU.author_id INNER JOIN articles AR ON ARU.article_id = AR.article_id WHERE AU.author_type='4' ORDER BY AR.article_published_date DESC) AS tem GROUP BY tem.author_id ORDER BY article_published_date DESC LIMIT 9")
        columnist_json = []
        for article in columnist:
            art_elem = {}
            art_elem['author_photo'] = article.author_photo
            art_elem['author_name'] = article.author_name
            art_elem['absolute_url'] = article.get_absolute_url()
            columnist_json.append(art_elem)

        sidebar_recent_articles = Articles.objects.raw("SELECT A.*, AU.*, AI.image_url, AI.photopath, AV.video_embed_code FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id JOIN article_images AI ON AI.article_id = A.article_id LEFT JOIN article_video AV ON A.article_id = AV.article_id WHERE A.display_to_homepage = '1' AND AI.photopath !='' GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 10")
        sidebar_recent_articles_json = []
        for article in sidebar_recent_articles:
            art_elem = {}
            art_elem['article_title'] = article.article_title
            art_elem['article_published_date'] = str(article.article_published_date)
            art_elem['article_id'] = article.article_id
            art_elem['photopath'] = article.photopath
            art_elem['absolute_url'] = article.get_absolute_url()
            sidebar_recent_articles_json.append(art_elem)

        recent_articles_interview = Articles.objects.raw("SELECT A.*, AU.*, AI.image_url, AI.photopath FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON A.article_id = AI.article_id WHERE A.display_to_homepage = '1' AND A.article_type = 3  AND AI.photopath !='' GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 1, 6")
        recent_articles_interview_json = []
        for article in recent_articles_interview:
            art_elem = {}
            art_elem['article_title'] = article.article_title
            art_elem['article_published_date'] = str(article.article_published_date)
            art_elem['article_id'] = article.article_id
            art_elem['photopath'] = article.photopath
            art_elem['video_type'] = article.video_type
            art_elem['absolute_url'] = article.get_absolute_url()
            recent_articles_interview_json.append(art_elem)

        recent_important_article_interview = Articles.objects.raw("SELECT A.*, AU.*, AI.image_url, AI.photopath FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON A.article_id = AI.article_id WHERE A.display_to_homepage = '1'  AND A.article_type = 3 AND AI.photopath !='' GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 1")
        recent_important_article_interview_json = []
        for article in recent_important_article_interview:
            art_elem = {}
            art_elem['article_title'] = article.article_title
            art_elem['article_published_date'] = str(article.article_published_date)
            art_elem['article_id'] = article.article_id
            art_elem['photopath'] = article.photopath
            art_elem['video_type'] = article.video_type
            art_elem['article_summary'] = article.article_summary
            art_elem['author_name'] = article.author_name
            author_url = article.get_article_author_url()
            art_elem['author_url'] = author_url
            art_elem['absolute_url'] = article.get_absolute_url()
            recent_important_article_interview_json.append(art_elem)

        category_jumlist = ChannelCategory.objects.filter(category_parent='0')
        category_jumlist_json = []
        for article in category_jumlist:
            art_elem = {}
            art_elem['category_name'] = article.category_name
            art_elem['absolute_url'] = article.category_self_url()
            category_jumlist_json.append(art_elem)

        author_list_on_home_page = Author.objects.raw("SELECT * FROM (SELECT AU.*, AR.article_published_date, NWS.newsletter_counts FROM author AU INNER JOIN article_author ARU ON AU.author_id = ARU.author_id INNER JOIN articles AR ON ARU.article_id = AR.article_id LEFT JOIN (SELECT author_newsletter_type_id, COUNT(author_newsletter_type_id) AS newsletter_counts FROM author_newsletter_Subscriber GROUP BY author_newsletter_type_id)NWS ON AU.author_id = NWS.author_newsletter_type_id WHERE AU.author_type='4'  OR AU.author_type='3'  ORDER BY AR.article_published_date DESC) AS tem GROUP BY tem.author_id ORDER BY article_published_date desc LIMIT 6")
        author_list_on_home_page_json = []
        for article in author_list_on_home_page:
            art_elem = {}
            art_elem['author_name'] = article.author_name
            art_elem['newsletter_counts'] = str(article.newsletter_counts)
            art_elem['author_photo'] = article.author_photo
            art_elem['absolute_url'] = article.get_absolute_url()
            author_list_on_home_page_json.append(art_elem)

        bwtv_articles = Articles.objects.raw("SELECT A.*, AC.*, AI.image_url, AI.photopath FROM articles A LEFT JOIN  article_category AC ON A.article_id = AC.article_id LEFT JOIN article_images AI ON A.article_id = AI.article_id  WHERE  AC.category_id = '156' ORDER BY A.article_published_date DESC LIMIT 10")
        bwtv_articles_json = []
        for article in bwtv_articles:
            art_elem = {}
            art_elem['video_title'] = article.video_title
            art_elem['article_published_date'] = str(article.article_published_date)
            art_elem['video_thumb_name'] = article.video_thumb_name
            art_elem['absolute_url'] = article.get_absolute_url()
            bwtv_articles_json.append(art_elem)

        magazine_image = Magazine.objects.raw("SELECT *,YEAR(publish_date_m) as years FROM magazine ORDER BY publish_date_m DESC LIMIT 1")
        magazine_image_json = []
        for article in magazine_image:
            art_elem = {}
            art_elem['description'] = article.description
            art_elem['imagepath'] = article.imagepath
            art_elem['story1_url'] = article.story1_url
            art_elem['story1_title'] = article.story1_title
            art_elem['story2_url'] = article.story2_url
            art_elem['story2_title'] = article.story2_title
            art_elem['story3_url'] = article.story3_url
            art_elem['story3_title'] = article.story3_title
            art_elem['story4_url'] = article.story4_url
            art_elem['story4_title'] = article.story4_title
            art_elem['story5_url'] = article.story5_url
            art_elem['story5_title'] = article.story5_title
            art_elem['flipbook_url'] = article.flipbook_url
            art_elem['absolute_url'] = article.get_absolute_url()
            art_elem['years'] = article.years
            magazine_image_json.append(art_elem)

       

        photoshoot_listing = PhotoShoot.objects.raw("SELECT count(*) as counts, ps.*,psp.photo_shoot_photo_url, psp.photo_shoot_image_id , psp.photo_shoot_photo_name FROM photo_shoot_photos psp join photo_shoot ps on  psp.photo_shoot_id=ps.photo_shoot_id group by psp.photo_shoot_id ORDER BY  ps.photo_shoot_id DESC  LIMIT 0,5")
        photoshoot_listing_json = []
        for article in photoshoot_listing:
            art_elem = {}
            art_elem['photo_shoot_title'] = article.photo_shoot_title
            art_elem['photo_shoot_photo_name'] = article.photo_shoot_photo_name
            art_elem['counts'] = article.counts
            art_elem['absolute_url'] = article.get_absolute_url()
            photoshoot_listing_json.append(art_elem)
       
        #Rest of the site Sidebar data

        client = storage.Client()
        bucket = client.get_bucket('bwmedia')
        blob_homepage = bucket.get_blob('json-files/bwdiff/homepage_site_data.json')
        #print(blob_homepage.download_as_string())
        blob_homepage.upload_from_string(json.dumps({
           'recent_articles':recent_articles_json,
            'sidebar_recent_articles':sidebar_recent_articles_json,
            'bwtv_articles': bwtv_articles_json,
            'recent_important_article': recent_important_article_json,
            'column_articles': column_articles_json,
            'columnist': columnist_json,
            'recent_articles_interview': recent_articles_interview_json,
            'recent_important_article_interview': recent_important_article_interview_json,
            'category_jumlist': category_jumlist_json,
            'author_list_on_home_page': author_list_on_home_page_json,
            'bw_corporate_movement': bw_corporate_movement_json,
            'magazine_image': magazine_image_json,
            'featured_boxs': featured_boxs_json,
            'recent_exclusive_article':recent_exclusive_article_json,
            'photoshoot_listing':photoshoot_listing_json,
        }))

        blob_sidebar = bucket.get_blob('json-files/bw-bwdiff/sidebar_site_data.json')
        blob_sidebar.upload_from_string(json.dumps({
            'sidebar_recent_articles':sidebar_recent_articles_json[:6],
            'bwtv_articles': bwtv_articles_json[:6],
            'category_jumlist': category_jumlist_json,
        }))


        feeds_bwcio = feedparser.parse('http://bwcio.businessworld.in/rss/all-article.xml')
        feeds_bws = feedparser.parse('http://bwsmartcities.businessworld.in/rss/channel-feed-articles.xml')
        feeds_bwh = feedparser.parse('http://businessworld.in/rss/latest-article.xml')
        feeds_bwd = feedparser.parse('http://bwdisrupt.businessworld.in/rss/channel-feed-articles.xml')
        feeds_ever = feedparser.parse('http://everythingexperiential.businessworld.in/rss/channel-feed-articles.xml')
        feeds_bwwh = feedparser.parse('http://bwwealth.businessworld.in/rss/all-article.xml')
        feeds_bma = feedparser.parse('http://www.digitalmarket.asia/feed/')

        feeds_bwcio_json = []
        feeds_bws_json = []
        feeds_bwh_json = []
        feeds_bwd_json = []
        feeds_ever_json = []
        feeds_bwwh_json = []
        feeds_bma_json = []


        for entry in feeds_bwcio.entries:
            #return HttpResponse(entry.link)
            json_feed = {}
            json_feed['link'] = entry.link
            json_feed['title'] = entry.title
            feeds_bwcio_json.append(json_feed)

        for entry in feeds_bws.entries:
            json_feed = {}
            json_feed['link'] = entry.link
            json_feed['title'] = entry.title
            feeds_bws_json.append(json_feed)

        for entry in feeds_bwh.entries:
            json_feed = {}
            json_feed['link'] = entry.link
            json_feed['title'] = entry.title
            feeds_bwh_json.append(json_feed)

        for entry in feeds_bwd.entries:
            json_feed = {}
            json_feed['link'] = entry.link
            json_feed['title'] = entry.title
            feeds_bwd_json.append(json_feed)

        for entry in feeds_ever.entries:
            json_feed = {}
            json_feed['link'] = entry.link
            json_feed['title'] = entry.title
            feeds_ever_json.append(json_feed)

        for entry in feeds_bwwh.entries:
            json_feed = {}
            json_feed['link'] = entry.link
            json_feed['title'] = entry.title
            feeds_bwwh_json.append(json_feed)

        for entry in feeds_bma.entries:
            json_feed = {}
            json_feed['link'] = entry.link
            json_feed['title'] = entry.title
            feeds_bma_json.append(json_feed)

        blob_footer_community = bucket.get_blob('json-files/bw-bwdiff/footer_community_site_data.json')
        blob_footer_community.upload_from_string(json.dumps({
            'feeds_bwcio':feeds_bwcio_json,
            'feeds_bws':feeds_bws_json,
            'feeds_bwh':feeds_bwh_json,
            'feeds_bwd':feeds_bwd_json,
            'feeds_ever':feeds_ever_json,
            'feeds_bwwh':feeds_bwwh_json,
            'feeds_bma':feeds_bma_json,
            'recent_exclusive_article':recent_exclusive_article_json,
            'column_articles': column_articles_json,
        }))

        #Dow Jones XML generation
        #urlset = ET.Element('xml', version="1.0", encoding="UTF-8")
        nodes = ET.Element('nodes')

        html_parser = HTMLParser.HTMLParser()

        #50 article list without BW Online for yahoo and dow jones
        article_list = Articles.objects.raw("SELECT A.* FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id WHERE A_A.author_type != 1 GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 50")

        for article in article_list:
            node = ET.SubElement(nodes, "node")
            ET.SubElement(node, "link").text = 'http://bwhotelier.businessworld.in/' + article.get_absolute_url()
            ET.SubElement(node, "title").text = html_parser.unescape(article.article_title)

            categories = article.get_article_category_listing()
            if len(list(categories)) > 0:
                categories_list = ET.SubElement(node, "categories")
                for category in categories:
                    ET.SubElement(categories_list, "category").text = category
            ET.SubElement(node, "description").text = html_parser.unescape(article.article_summary)
            ET.SubElement(node, "author").text = html_parser.unescape(article.get_article_author_name())
            article_desc = remove_tags(article.article_description, "p")
            ET.SubElement(node, "body").text = article_desc
            ET.SubElement(node, "post-date").text = str(article.article_published_date.strftime('%a, %Y %b %d %H:%M:%S %Z'))

        tree = ET.tostring(nodes)
        tree = re.sub(r'&lt;','<',tree)
        tree = re.sub(r'&gt;','>',tree)
        out = open('static/xml/dow_jones_article.xml', 'w+')
        out.write(tree)
        out.close()
        

        return HttpResponse(json.dumps({'result':'completed'}))
    else:
        return HttpResponseRedirect("/")
