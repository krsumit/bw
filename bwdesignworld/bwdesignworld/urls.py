"""bwwellness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import handler404, handler500
from django.conf.urls import include, url, patterns
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from django.views.generic import RedirectView
from magazineisuue import views as magazineissue_view
from community import views as community_view
from homepage import views as homepage_view
from articles import views as article_view
from sponsored import views as sponsoredposts_view
from tags import views as tag_view
from author import views as author_view
from event import views as event_view
from category import views as category_view
from quickbytes import views as QuickBytes_view
from topics import views as topic_view
from columns import views as column_view
from newsletter import views as newsletter_view
from authornewslatter import views as author_newsletter_view
from photoshoot import views as photoshoot_view
from libs import views as libs_view
from businessentertainment import views as businessentertainment_view
from mainnewsletter import views as mainnewsletter_view
from bwdesignworld.feeds import LatestEntriesAllFeed,LatestFooterEntriesAllFeed, LatestEntriesFeed, LatestImportantFeed, LatestColumnistFeed, LatestInterviewsFeed, LatestNewsFeed, LatestWebExclusiveFeed, LatestTodaysArticleFeed, Latest20Articles,CategoryNewsHunt, CategoryFlipboard
from mainvideo import views as mainvideo_view
from bwdesignworld.feeds import StaticViewSitemap
from bwdesignworld.sitemap import LatestTodaysitemap,LatestSponsoredpostssitemap,LatestColumnsitemap,LatestNewssitemap,LatestAuthorsitemap

from bwdesignworld.search_indexes import search_articles, search_author, search_sponsored

sitemaps = {
    'static': StaticViewSitemap,
}

sitemaps1 = {
    'static': LatestTodaysitemap
}
sitemaps6 = {
    'static': LatestNewssitemap
}




urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', cache_page(60 * 15)(homepage_view.homepage)),

    #url(r'^search/', include('haystack.urls')),
    url(r'^search/articles/', search_articles),
    url(r'^search/authors/', search_author),
    url(r'^search/sponsor/', search_sponsored),
    url(r'^robots\.txt/$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

    #RSS feeds
    url(r'^rss/editors-picks-article.xml$', LatestEntriesFeed()),
    url(r'^rss/all-article.xml$', LatestEntriesAllFeed()),
    url(r'^rss/important-articles.xml$', LatestImportantFeed()),
    url(r'^rss/columnist-articles.xml$', LatestColumnistFeed()),
    url(r'^rss/interviews.xml$', LatestInterviewsFeed()),
    url(r'^rss/news-article.xml$', LatestNewsFeed()),
    url(r'^rss/web-exclusive-articles.xml$', LatestWebExclusiveFeed()),
    url(r'^rss/todays-article.xml$', LatestTodaysArticleFeed()),
    url(r'^rss/latest-article.xml$', Latest20Articles()),
    url(r'^rss/channel-feed-articles.xml$', LatestFooterEntriesAllFeed()),
    url(r'^rss/(?P<category_name>[\w$.?!(),:\'+-]+)-(?P<category_id>\d+).xml$', CategoryNewsHunt()),
    url(r'^rss/flipboard/(?P<category_name>[\w$.?!(),:\'+-]+)-(?P<category_id>\d+).xml$', CategoryFlipboard()),
    #Sitemaps
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^all-article\.xml$', sitemap, {'sitemaps': sitemaps1}, name='all-article'),
    #url(r'^sitemap3\.xml$', sitemap, {'sitemaps': sitemaps3}, name='sitemap3'),
    #url(r'^sitemap4\.xml$', sitemap, {'sitemaps': sitemaps4}, name='sitemap4'),
    #url(r'^sitemap5\.xml$', sitemap, {'sitemaps': sitemaps5}, name='sitemap5'),
    url(r'^news\.xml$', sitemap, {'sitemaps': sitemaps6}, name='news'),
    #url(r'^news-sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps,'template_name': 'sitemap7.xml'}),
    
    #communities of content 
    url(r'^communities-content/', community_view.community_content),

    #Article Landing pages

    url(r'^article/(?P<article_title>[\w$.?!(),:\'"+-]+)/(?P<article_published_date>[\w-]+)-(?P<article_id>\d+)/$', article_view.articleLanding),
    url(r'^amp/article/(?P<article_title>[\w$.?!(),:\'"+-]+)/(?P<article_published_date>[\w-]+)-(?P<article_id>\d+)/$', article_view.articleLandingAmp),	
    url(r'^article/comments/(?P<article_title>[\w$.?!(),:\'"+-]+)/(?P<article_published_date>[\w-]+)-(?P<article_id>\d+)/$', cache_page(60 * 1)(article_view.articleLanding)), #Article Comment landing
    url(r'^web-exclusive', article_view.web_exclusivearticle),
    url(r'^events-listing', event_view.event_listing),

    #sponsered landing page start
     url(r'^sponsor/(?P<sponsoredposts_title>[\w$.?!(),:\'+-]+)/(?P<sponsoredposts_published_date>[\w-]+)-(?P<sponsoredposts_id>\d+)/$', cache_page(60 * 15)(sponsoredposts_view.sponserLanding)),

    #end

    # Author Articles Listing and loading
    url(r'^author/(?P<author_type>[\w$.?!(),:\'+-]+)/(?P<author_name>[\w$.?!(),:\'+-]+)-(?P<author_id>\d+)/$', cache_page(60 * 15)(author_view.author_articles_list)),
    url(r'^author-load/(?P<author_type>[\w$.?!(),:\'+-]+)/(?P<author_id>\d+)/$', cache_page(60 * 15)(author_view.author_articles_list)),
    # End

    # Recent Articles Listing and loading
    url(r'^all-articles/$', cache_page(60 * 15)(article_view.recent_articles_listing), name ='recent_articles_listing'),
    url(r'^all-articles-load/$', cache_page(60 * 15)(article_view.recent_articles_listing_load)),
    # End

    # Category Articles Listing and loading
    url(r'^category/(?P<category_name>[\w$.?!(),:\'+-]+)-(?P<category_id>\d+)/$', cache_page(60 * 15)(category_view.category_articles_list)),
    url(r'^category-list/(?P<category_id>\d+)/$', cache_page(60 * 15)(category_view.category_articles_list_load)),
    # End

    #column relate column listing articles
    url(r'^column/(?P<column_name>[\w$.?!(),:\'+-]+)-(?P<column_id>\d+)/$', cache_page(60 * 15)(column_view.column_articles_list)),
    #end

    # Topic Articles Listing and loading
    url(r'^topics/(?P<topic_name>[\w$.?!(),:\'+-]+)-(?P<topic_id>\d+)/$', cache_page(60 * 15)(topic_view.topic_articles_list)),
    url(r'^topics-list/(?P<topic_id>\d+)/$', cache_page(60 * 15)(topic_view.topic_articles_list_load)),
    # End

    # Tags Article Listing and loading
    url(r'^tags/(?P<tag_name>[\w$.?!(),:\'+-]+)-(?P<tag_id>\d+)/$', cache_page(60 * 15)(tag_view.tag_articles_list)),
    url(r'^tags-list/(?P<tag_id>\d+)/$', cache_page(60 * 15)(tag_view.tag_articles_list_load)),
    # End

    #json creation link
    url(r'^create-json/(?P<secret_key>[\w$.?!(),:\'"+-]+)/$', libs_view.createJsonValues),

    #newsletterscb
    url(r'^newsletter_Subscriber_details/$', newsletter_view.get_newsletter_Subscriber_details),
    url(r'^author_newsletter_Subscriber_details/$', author_newsletter_view.get_author_newsletter_Subscriber_details),

    url(r'^exclusive_articles_header/$', cache_page(60 * 15)(libs_view.exclusive_articles), name ='exclusive_articles_header'),
    url(r'^columns_data_header/$', cache_page(60 * 15)(libs_view.columns_data)),
    url(r'^exclusiveonweb/$', libs_view.exclusive_onpagearticles),
    url(r'^bwtv_articles_header/$', cache_page(60 * 15)(libs_view.bwtv_articles)),
    url(r'^popular_articles/$', libs_view.popular_articles),
    url(r'^event_articles_header/$',libs_view.event_articles),
    url(r'^event_listing_by_ajax/$',libs_view.event_listing),
    url(r'^columns/$',article_view.column_articles),
    url(r'^online-exclusive/$',article_view.exclusive_article),
    url(r'^bw-event/$',article_view.event_articles),
    url(r'^business-news/$', cache_page(60 * 15)(article_view.news_articles), name ='news_articles'),
    #url(r'^business-news/$',article_view.news_articles),
    url(r'^business-opinion-analysis/$',article_view.opinion_articles),
    url(r'^interview_articles/$',article_view.Interviews_articles),
    url(r'^business-feature-stories/$',article_view.feature_articles),
    url(r'^date/(?P<article_published_date>[\w-]+)/$',article_view.article_list_time_wise),
    url(r'^main-newsletter/$',mainnewsletter_view.main_news_letter),
    #url(r'^reports-generator/$',libs_view.reports_view),
    #url(r'^reports-generatorhtml/$',libs_view.reportshtml_view),
    #url(r'^reports-generatorajax/$',libs_view.reportsajax_view),
    url(r'^bw-past-event/$',event_view.past_event_articles),

    #Quickbyte landing and loading with individual image
    url(r'^quickbytes/(?P<quick_byte_title>[\w$.?!(),:\'+-]+)/(?P<quick_byte_published_date>[\w-]+)-(?P<quick_byte_id>\d+)/$',cache_page(60 * 1)(QuickBytes_view.quickbyteslanding)),
    url(r'^quickbytes/(?P<quick_byte_title>[\w$.?!(),:\'+-]+)/(?P<quick_byte_id>\d+)/(?P<quick_byte_image_name>[\w$.?!(),:\'+-]+)-(?P<quick_byte_image_id>\d+)/$', cache_page(60 * 1)(QuickBytes_view.quick_bytes_image_load)),
    #url(r'^quickbytes/(?P<quick_byte_title>[\w$.?+-]+)/(?P<quick_byte_published_date>[\w-]+)-(?P<quick_byte_id>\d+)/$',QuickBytes_view.quickbytes_load),
    url(r'^all-quickbytes/$',QuickBytes_view.quickbyte_listing),
    # End
    #magazine-issues pages
    url(r'^magazine-issues/(?P<year>\d+)/(?P<title>[\w$.?+-]+)-(?P<magazine_id>\d+)/web-view/$',article_view.magzine_articles_listing),    
    url(r'^magazine-issues/(?P<year>\d+)/$',magazineissue_view.magazineissue_listing),
    
    #mainvideo_view PAGE    
    url(r'^all-videos/$',mainvideo_view.main_video_listing),
    url(r'^video/(?P<video_title>[\w$.?!(),:\'"+-]+)/(?P<updated_at>[\w-]+)-(?P<video_id>\d+)/$',mainvideo_view.main_video_landing_page),

    #photoshoot PAGE

    url(r'^photoshoot/$',photoshoot_view.photo_shoot ),
    url(r'^all-photo-features/$',photoshoot_view.photo_shoot_listing),
    url(r'^photo-feature/(?P<photo_shoot_title>[\w$.?!(),:\'"+-]+)/(?P<photo_shoot_updated_at>[\w-]+)-(?P<photo_shoot_id>\d+)/$',photoshoot_view.photo_shoot_landing_page),

    #Static pages
    url(r'^google4f73e6c07e7339f8.html/$', cache_page(60 * 15)(libs_view.static_google4f73e6c07e7339f8)),
    url(r'^business-of-entertainment/$', businessentertainment_view.business_entertainment),
    url(r'^rss-feed/$', cache_page(60 * 15)(libs_view.static_rss_feeds)),

    #Redirect Views
    #url(r'^some-page/$', RedirectView.as_view(url='/')),
    url(r'^(?P<category_name>[\w$.?!(),:\'+-]+)/$', category_view.category_redirect),  #Category
    url(r'^tags/(?P<tag_name>[\w$.?!(),:\'+-]+)/$', tag_view.tag_redirect), #Tags
    url(r'^(?P<category_name>[\w$.?!(),:\'+-]+)/(?P<article_title>[\w$.?!(),:\'"+-]+)/$', RedirectView.as_view(url='/')),  #Article
]

#handler404 = 'libs_view.customError'
handler500 = 'libs.views.customError'

'''
if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
    urlpatterns += patterns('',
            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
'''
