from django.contrib import sitemaps
from django.core.urlresolvers import reverse
import datetime
import re
from django.template.defaultfilters import date

from articles.models import Articles
from author.models import Author, AuthorType
from sponsored.models import Sponsoredposts
from columns.models import Columns

class LatestTodaysitemap(sitemaps.Sitemap):

    priority = 0.8
    changefreq = 'hourly'

    def items(self):
        return Articles.objects.order_by('-article_published_date')[:50]

    def item_title(self, item):
        return item.article_title

    def item_description(self, item):
        return item.article_summary

    def lastmod(self, item):
        return item.article_published_date

    def location(self, item):
        #title_for_url_article = item.article_title.replace(' ', '-')
        title_for_url_article = re.sub('[^A-Za-z0-9]+', '-', item.article_title)

        return '/article/'+str(title_for_url_article)+'/'+str(date(item.article_published_date, "d-m-Y"))+'-'+str(item.article_id)

    def item_pubdate(self, item):
        return item.article_published_date

class LatestSponsoredpostssitemap(sitemaps.Sitemap):

    priority = 0.8
    changefreq = 'hourly'

    def items(self):
        return Sponsoredposts.objects.order_by('-sponsoredposts_published_date')[:50]

    def item_title(self, item):
        return item.sponsoredposts_title

    def item_description(self, item):
        return item.sponsoredposts_description

    def lastmod(self, item):
        return item.sponsoredposts_published_date

    def location(self, item):
        sponsoredposts_title_for_url = item.sponsoredposts_title.replace(' ', '-')
        return '/sponser/'+str(sponsoredposts_title_for_url)+'/'+str(date(item.sponsoredposts_published_date, "d-m-Y"))+'-'+str(item.sponsoredposts_id)

class LatestColumnsitemap(sitemaps.Sitemap):

    priority = 0.8
    changefreq = 'hourly'

    def items(self):
        return list(Articles.objects.raw("SELECT A.*, AU.*, AI.image_url FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id JOIN article_images AI ON AI.article_id = A.article_id WHERE A_A.author_type='4' GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 50"))

    def item_title(self, item):
        return item.article_title

    def item_description(self, item):
        return item.article_summary

    def lastmod(self, item):
        return item.article_published_date

    def location(self, item):
        #title_for_url_article = item.article_title.replace(' ', '-')
        title_for_url_article = re.sub('[^A-Za-z0-9]+', '-', item.article_title)
        return '/article/'+str(title_for_url_article)+'/'+str(date(item.article_published_date, "d-m-Y"))+'-'+str(item.article_id)

class LatestColumnsitemap(sitemaps.Sitemap):

    priority = 0.8
    changefreq = 'hourly'

    def items(self):
        return list(Articles.objects.raw("SELECT A.*, AU.*, AI.image_url FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id JOIN article_images AI ON AI.article_id = A.article_id WHERE A_A.author_type='4' GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 50"))

    def item_title(self, item):
        return item.article_title

    def item_description(self, item):
        return item.article_summary

    def lastmod(self, item):
        return item.article_published_date

    def location(self, item):
        #title_for_url_article = item.article_title.replace(' ', '-')
        title_for_url_article = re.sub('[^A-Za-z0-9]+', '-', item.article_title)
        return '/article/'+str(title_for_url_article)+'/'+str(date(item.article_published_date, "d-m-Y"))+'-'+str(item.article_id)

class LatestNewssitemap(sitemaps.Sitemap):

    priority = 0.8
    changefreq = 'hourly'

    def items(self):
        return list(Articles.objects.raw("SELECT A.*, AU.*, AI.image_url FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id LEFT JOIN author AU ON A_A.author_id = AU.author_id LEFT JOIN article_images AI ON A.article_id = AI.article_id WHERE A.article_type = '3'  OR A.article_type = '1' GROUP BY A.article_id ORDER BY A.article_published_date DESC "))[:50]

    def item_title(self, item):
        return item.article_title

    def item_description(self, item):
        return item.article_summary

    def lastmod(self, item):
        return item.article_published_date

    def location(self, item):
        #title_for_url_article = item.article_title.replace(' ', '-')
        title_for_url_article = re.sub('[^A-Za-z0-9]+', '-', item.article_title)
        return '/article/'+str(title_for_url_article)+'/'+str(date(item.article_published_date, "d-m-Y"))+'-'+str(item.article_id)

class LatestAuthorsitemap(sitemaps.Sitemap):

    priority = 0.8
    changefreq = 'hourly'

    def items(self):
        return list(Author.objects.raw("SELECT * FROM (SELECT AU.*, AR.article_published_date FROM author AU INNER JOIN article_author ARU ON AU.author_id = ARU.author_id INNER JOIN articles AR ON ARU.article_id = AR.article_id WHERE AU.author_type='4' ORDER BY AR.article_published_date DESC) AS tem GROUP BY tem.author_id "))

    def item_title(self, item):
        return item.author_name

    def item_author_label(self, item):
        return item.author_label

    def lastmod(self, item):
        return item.article_published_date

    def location(self, item):
        columnist_label = AuthorType.objects.filter(author_type_id = '4').first()
        author_label = columnist_label.author_type_for_url
        author_name_for_url = item.author_name.replace(' ', '-')
        return '/author/'+str(author_label)+'/'+str(author_name_for_url)+'-'+str(item.author_id)



