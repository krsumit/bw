# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils import feedgenerator
from django.contrib import sitemaps
from django.core.urlresolvers import reverse
from articles.models import Articles
#from featuredbox.models import FeatureBox
from category.models import ChannelCategory
#from django.core.urlresolvers import reverse
import datetime
import HTMLParser
import re
import string
from django.conf import settings

class LatestEntriesFeedGenerator(Rss201rev2Feed):
    def rss_attributes(self):
        return {u"version": self._version, u"xmlns:dc": u"http://purl.org/dc/elements/1.1/", u"xmlns:slash": "http://purl.org/rss/1.0/modules/slash/", u"xmlns:atom": "http://www.w3.org/2005/Atom", u"xmlns:content": "http://purl.org/rss/1.0/modules/content/", u"xmlns:sy": "http://purl.org/rss/1.0/modules/syndication/"}

    def add_root_elements(self, handler):
        super(LatestEntriesFeedGenerator, self).add_root_elements(handler)
        handler.startElement(u'image', {})
        handler.addQuickElement(u"url", settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + "static_bwdiff/images/BWH-Logo-300x72.jpg")
        handler.addQuickElement(u"title", u"All Articles")
        handler.addQuickElement(u"link", u"http://bwdefence.businessworld.in/all-articles")
        handler.endElement(u'image')
        '''handler.addQuickElement(u"image", '',
            {
                 'url': settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + "static_bwdiff/images/BWH-Logo-300x72.jpg",
                 'title': u"BWcio",
                 'link': u"http://www.bwdefence.businessworld.in/",
             })'''

    def add_item_elements(self, handler, item):
        super(LatestEntriesFeedGenerator, self).add_item_elements(handler, item)
        handler.addQuickElement(u'dc:creator', item['article_author_name'])

#editors-picks-article
class LatestEntriesFeed(Feed):
    #description_template = "feeds/all_articles.html"
    #feed_type = feedgenerator.Rss201rev2Feed
    feed_type = LatestEntriesFeedGenerator
    title = "All Articles"
    link = "http://bwdefence.businessworld.in/all-articles"
    description = "All listed articles."

    def items(self):
        return Articles.objects.order_by('-article_published_date')[:100]

    def item_extra_kwargs(self, item):
        return {'article_author_name':item.get_article_author_name()}

    def item_title(self, item):
        return item.article_title

    def item_description(self, item):
        return item.article_summary

    def item_pubdate(self, item):
        timestamp = item.article_published_date
        timestamp.replace(tzinfo=None)
        return timestamp
    # item_link is only needed if NewsItem has no get_absolute_url method.

    def item_link(self, item):
        #return reverse('news-iteauthor_linkm', args=[item.pk])
        return item.get_absolute_url()

class LatestFeedGeneratorForAll(Rss201rev2Feed): #extra elements for article and quickbytes
    def rss_attributes(self):
        return {u"version": self._version, u"xmlns:dc": u"http://purl.org/dc/elements/1.1/", u"xmlns:slash": "http://purl.org/rss/1.0/modules/slash/", u"xmlns:atom": "http://www.w3.org/2005/Atom", u"xmlns:content": "http://purl.org/rss/1.0/modules/content/", u"xmlns:sy": "http://purl.org/rss/1.0/modules/syndication/"}

#all-article
class LatestEntriesAllFeed(Feed):
    feed_type = LatestFeedGeneratorForAll
    title = "All Articles"
    link = "/all-articles/"
    description = "All listed articles."

    def items(self):
        return Articles.objects.order_by('-article_published_date')[:100]

    def item_title(self, item):
        return item.article_title

    def item_description(self, item):
        return item.article_summary

    def item_pubdate(self, item):
        return item.article_published_date
    # item_link is only needed if NewsItem has no get_absolute_url method.


    def item_link(self, item):
        #return reverse('news-iteauthor_linkm', args=[item.pk])
        return item.get_absolute_url()
        #return reverse('article/'+str(item.article_title.strip().replace(' ', '-'))+'/'+str(item.article_published_date)+'-'+str(item.article_id), args=[])
#footer-article
class LatestFooterEntriesAllFeed(Feed):
    feed_type = LatestFeedGeneratorForAll
    title = "channel feed Articles"
    link = "/channel-articles/"
    description = "Channel listed articles."

    def items(self):
        return Articles.objects.order_by('-article_published_date')[:3]

    def item_title(self, item):
        return item.article_title

    def item_description(self, item):
        return item.article_summary

    def item_pubdate(self, item):
        return item.article_published_date
    # item_link is only needed if NewsItem has no get_absolute_url method.


    def item_link(self, item):
        #return reverse('news-iteauthor_linkm', args=[item.pk])
        return item.get_absolute_url()
        #return reverse('article/'+str(item.article_title.strip().replace(' ', '-'))+'/'+str(item.article_published_date)+'-'+str(item.article_id), args=[])

#columnist-articles
class LatestColumnistFeed(Feed):
    feed_type = LatestFeedGeneratorForAll
    title = "Columnist Post"
    link = "/columnist articles/"
    description = "All listed columnist articles."
    description_template = 'feeds/columnist-articles.html'

    def items(self):
        return  Articles.objects.raw("SELECT A.*, AU.*, AI.image_url FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id JOIN article_images AI ON AI.article_id = A.article_id WHERE A_A.author_type='4' GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 9")

    def item_title(self, item):
        return item.article_title

    def item_description(self, item):
        return item.article_summary

    def item_pubdate(self, item):
        return item.article_published_date
    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        #return reverse('news-item', args=[item.pk])
        return item.get_absolute_url()
        #return reverse('article/'+str(item.title_for_url)+'/'+str(item.article_published_date)+'-'+str(item.article_id), args=[])

#important-articles
class LatestImportantFeed(Feed):
    feed_type = LatestFeedGeneratorForAll
    title = "Important Articles"
    link = "/Important Articles/"
    description = "All listed Important Articles."

    def items(self):
        return  Articles.objects.raw("SELECT * FROM articles WHERE important_article ='1' GROUP BY article_id ORDER BY article_published_date DESC LIMIT 6")

    def item_title(self, item):
        return item.article_title

    def item_description(self, item):
        return item.article_summary

    def item_pubdate(self, item):
        return item.article_published_date
    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        #return reverse('news-item', args=[item.pk])
        return item.get_absolute_url()
        #return reverse('article/'+str(item.title_for_url)+'/'+str(item.article_published_date)+'-'+str(item.article_id), args=[])

#interviews
class LatestInterviewsFeed(Feed):
    feed_type = LatestFeedGeneratorForAll
    title = "Interviews"
    link = "/Interviews/"
    description = "All listed Interviews."

    def items(self):
        return  Articles.objects.raw("SELECT * FROM articles WHERE article_type ='Interviews' GROUP BY article_id ORDER BY article_published_date DESC LIMIT 10")

    def item_title(self, item):
        return item.article_title

    def item_description(self, item):
        return item.article_summary

    def item_pubdate(self, item):
        return item.article_published_date
    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        #return reverse('news-item', args=[item.pk])
        return item.get_absolute_url()
        #return reverse('article/'+str(item.title_for_url)+'/'+str(item.article_published_date)+'-'+str(item.article_id), args=[])

#news-article
class LatestNewsFeed(Feed):
    feed_type = LatestFeedGeneratorForAll
    title = "News"
    link = "/News/"
    description = "All listed News."

    def items(self):
        return  Articles.objects.raw("SELECT * FROM articles WHERE article_type ='news' GROUP BY article_id ORDER BY article_published_date DESC LIMIT 10")

    def item_title(self, item):
        return item.article_title

    def item_description(self, item):
        return item.article_summary

    def item_pubdate(self, item):
        return item.article_published_date
    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        #return reverse('news-item', args=[item.pk])
        return item.get_absolute_url()
        #return reverse('article/'+str(item.title_for_url)+'/'+str(item.article_published_date)+'-'+str(item.article_id), args=[])

#web-exclusive-articles
class LatestWebExclusiveFeed(Feed):
    feed_type = LatestFeedGeneratorForAll
    title = "Web Exclusive "
    link = "/Web Exclusive /"
    description = "All listed Web Exclusive ."

    def items(self):
        return  Articles.objects.raw("SELECT * FROM articles WHERE article_type ='news' GROUP BY article_id ORDER BY article_published_date DESC LIMIT 10")

    def item_title(self, item):
        return item.article_title

    def item_description(self, item):
        return item.article_summary

    def item_pubdate(self, item):
        return item.article_published_date
    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        #return reverse('news-item', args=[item.pk])
        return item.get_absolute_url()
        #return reverse('article/'+str(item.title_for_url)+'/'+str(item.article_published_date)+'-'+str(item.article_id), args=[])

#todays-article
class LatestTodaysArticleFeed(Feed):
    feed_type = LatestFeedGeneratorForAll
    title = "Today article "
    link = "/Today article/"
    description = "All listed Todays article ."

    def items(self):
        return  Articles.objects.raw("SELECT * FROM articles WHERE article_published_date = CURDATE() GROUP BY article_id ORDER BY article_published_date DESC LIMIT 10")

    def item_title(self, item):
        return item.article_title

    def item_description(self, item):
        return item.article_summary

    def item_pubdate(self, item):
        return item.article_published_date
    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        #return reverse('news-item', args=[item.pk])
        return item.get_absolute_url()
        #return reverse('article/'+str(item.title_for_url)+'/'+str(item.article_published_date)+'-'+str(item.article_id), args=[])

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'hourly'

    def items(self):
         return ['news', 'all-article']

    def lastmod(self, item):
        return datetime.datetime.now()

    def location(self, item):
        return reverse(item)

class LatestItemsFeedGenerator(Rss201rev2Feed): #extra elements for article and quickbytes
    def rss_attributes(self):
        return {u"version": self._version, u"xmlns:dc": u"http://purl.org/dc/elements/1.1/", u"xmlns:slash": "http://purl.org/rss/1.0/modules/slash/", u"xmlns:atom": "http://www.w3.org/2005/Atom", u"xmlns:content": "http://purl.org/rss/1.0/modules/content/", u"xmlns:sy": "http://purl.org/rss/1.0/modules/syndication/"}

    def add_root_elements(self, handler):
        super(LatestItemsFeedGenerator, self).add_root_elements(handler)
        handler.startElement(u'image', {})
        handler.addQuickElement(u"url", settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + "static_bwdiff/images/BWH-Logo-300x72.jpg")
        handler.addQuickElement(u"title", u"Latest 20 Articles")
        handler.addQuickElement(u"link", u"http://bwdefence.businessworld.in/all-articles/")
        handler.endElement(u'image')
        '''handler.addQuickElement(u"image", '',
            {
                 'url': settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + "static_bwdiff/images/BWH-Logo-300x72.jpg",
                 'title': u"BWHotelier",
                 'link': u"http://www.bwdefence.businessworld.in/",
             })'''

    def add_item_elements(self,  handler, item):
        super(LatestItemsFeedGenerator, self).add_item_elements(handler, item)
        handler.addQuickElement(u'dc:creator', item['article_author_name'])
        handler.addQuickElement(u'image', item['article_image'])
        handler.addQuickElement(u'comments', item['article_comment'])
        for item_category in item['article_category']:
            handler.addQuickElement(u'category', item_category)
        #handler.addQuickElement(u'comments', item['article_comment'])

#Latest 20 Articles -- By Ankita
class Latest20Articles(Feed):
    #description_template = "feeds/all_articles.html"
    #feed_type = feedgenerator.Rss201rev2Feed
    feed_type = LatestItemsFeedGenerator
    title = "Latest 20 Articles"
    link = "http://bwdefence.businessworld.in/all-articles/"
    description = "Latest 20 articles."
    #image = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + "static_bwhotelier/images/BW-logo.png"

    def items(self):
        return Articles.objects.order_by('-article_published_date')[:20]

    def item_extra_kwargs(self, item):
        
        return {
            'article_author_name':item.get_article_author_name(),
            'article_image':item.get_image_for_feed(),
            'article_comment':item.get_comment_url(),
            'article_category':item.get_article_category_listing()
        }

    def item_title(self, item):
        return item.article_title

    def item_description(self, item):
        return item.article_summary

    def item_pubdate(self, item):
        return item.article_published_date
    # item_link is only needed if NewsItem has no get_absolute_url method.

    def item_link(self, item):
        #return reverse('news-iteauthor_linkm', args=[item.pk])
        return item.get_absolute_url()

class LatestFlipboardFeedGenerator(Rss201rev2Feed):
    def rss_attributes(self):
        return {u"version": self._version, u"xmlns:dc": u"http://purl.org/dc/elements/1.1/", u"xmlns:slash": "http://purl.org/rss/1.0/modules/slash/", u"xmlns:atom": "http://www.w3.org/2005/Atom", u"xmlns:content": "http://purl.org/rss/1.0/modules/content/", u"xmlns:sy": "http://purl.org/rss/1.0/modules/syndication/"}

    def add_root_elements(self, handler):
        super(LatestFlipboardFeedGenerator, self).add_root_elements(handler)
        handler.startElement(u'image', {})
        handler.addQuickElement(u"url", settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + "static_bwdiff/images/BWH-Logo-300x72.jpg")
        handler.addQuickElement(u"title", u"Latest 30 Articles")
        handler.addQuickElement(u"link", u"http://bwdefence.businessworld.in/all-articles/")
        handler.endElement(u'image')

    def add_item_elements(self,  handler, item):
        super(LatestFlipboardFeedGenerator, self).add_item_elements(handler, item)
        handler.addQuickElement(u'dc:creator', item['article_author_name'])
        '''handler.startElement(u'figure', {})
        handler.startElement(u'img', {
            'src': item['article_image']
        })
        handler.endElement(u'img')
        handler.endElement(u'figure')'''
        #handler.addQuickElement(u'image', item['article_image'])
        handler.addQuickElement(u'content:encoded', item['article_summary'])

#Category wise feed for newshunt

class CategoryNewsHunt(Feed):
    feed_type = LatestItemsFeedGenerator

    #image = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + "static_bwhotelier/images/BWH-Logo-300x72.jpg"

    def get_object(self, request, category_name, category_id):
        #return HttpResponse(category_id)
        category_details = ChannelCategory.objects.filter(category_id=category_id).first()
        self.title = "Latest Articles in "+str(category_details.category_name)
        self.link = "http://bwdefence.businessworld.in/category/"+category_name+"-"+category_id
        self.description = "Latest 10 Articles in "+str(category_details.category_name)
        return category_id
        ##st_name = category_name.upper()
         ## return HttpResponse(st_name)
        ##return CountryStates.objects.filter(name__exact=st_name).get()


    def items(self, obj):
        category_id = obj
        #title = category_id+"Latest BW Smarticities Category Articles"
        #return Articles.objects.filter(article_location_state=state_id).order_by('-article_published_date')[:10]
        return Articles.objects.raw("SELECT A.* FROM articles A inner join article_category AC on A.article_id=AC.article_id WHERE  AC.category_id="+str(category_id)+" GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 10")

        #return obj.items.all()
        #return Articles.objects.filter(article_type='3').order_by('-article_published_date')[:10]


    def item_extra_kwargs(self, item):
        if(item.get_image_for_feed()):
            article_img = item.get_image_for_feed()
        else:
            article_img = ''
        
        return {
            'article_author_name':item.get_article_author_name(),
            'article_image':article_img,
            'article_comment':item.get_comment_url(),
            'article_category':item.get_article_category_listing()
        }

    def item_title(self, item):
        return item.article_title

    def item_description(self, item):
        return item.article_summary

    def item_pubdate(self, item):
        return item.article_published_date
    # item_link is only needed if NewsItem has no get_absolute_url method.

    def item_link(self, item):
        #return reverse('news-iteauthor_linkm', args=[item.pk])
        return item.get_absolute_url()


#Category wise feed for flipboard

class CategoryFlipboard(Feed):
    feed_type = LatestFlipboardFeedGenerator
    title = "Latest 30 Article cateogry"
    link = "http://bwdefence.businessworld.in/all-articles"
    description = "Latest 30 Review."

    def get_object(self, request, category_name, category_id):
            category_details = ChannelCategory.objects.filter(category_id=category_id).first()
            self.title = "Latest Articles in "+str(category_details.category_name)
            self.link = "http://bwdefence.businessworld.in/category/"+category_name+"-"+category_id
            self.description = "Latest 30 Articles in "+str(category_details.category_name)
            return category_id



    def items(self, obj):
         category_id = obj

         return Articles.objects.raw("SELECT A.* FROM articles A  join article_category AC on A.article_id=AC.article_id WHERE  AC.category_id="+str(category_id)+" GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 30")


    def item_extra_kwargs(self, item):
        if(item.get_image_for_feed()):
            article_img = item.get_image_for_feed()
        else:
            article_img = ''
        image_content = '<figure><img src="'+article_img+'"></figure>'
        #image_content = '<figure><img src="'+item.get_image_for_feed()+'"></figure>'
        article_desc = self.item_content_encoded(item)+image_content
        return {
            'article_author_name':item.get_article_author_name(),
            'article_image':item.get_image_for_feed(),
            'article_summary':article_desc
        }


    def item_title(self, item):
        return item.article_title

    def item_description(self, item):
        return item.article_summary

    def item_pubdate(self, item):
        return item.article_published_date

    def item_content_encoded(self, item):
        html_parser = HTMLParser.HTMLParser()
        article_description = html_parser.unescape("<![CDATA[%s]]>" % item.article_description)
        return article_description

