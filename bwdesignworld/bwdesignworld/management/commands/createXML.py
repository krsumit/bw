from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
import xml.etree.cElementTree as ET
from django.template.defaultfilters import date
from django.conf import settings
import re
from tags.models import ChannelTags
from articles.models import Articles, ArticleImages, ArticleCategory, ArticleTopics, ArticleView
from quickbytes.models import QuickBytes, QuickBytesPhotos, QuickBytesTags
import feedparser
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Command(BaseCommand):
    help = 'Create XML for header'
    reload(sys)
    sys.setdefaultencoding('utf8')
    #sys.setdefaultencoding("latin-1")
    def handle(self, *args, **options):
        recent_exclusive_article = Articles.objects.raw("SELECT A.*, AI.image_url, AI.photopath FROM articles A LEFT JOIN article_images AI ON A.article_id = AI.article_id WHERE A.is_exclusive = '1' GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 4")

        root = ET.Element("root")

        for article in recent_exclusive_article:
            doc = ET.SubElement(root, "exclusive")
            ET.SubElement(doc, "article_id").text = str(article.article_id)
            ET.SubElement(doc, "article_title").text = str(article.article_title)
            ET.SubElement(doc, "article_published_date").text = str(date(article.article_published_date, 'd-m-Y'))
            if article.is_old == 1:
                imag_url = str(article.image_url)
            else:
                imag_url = settings.AWS_S3_BASE_URL + settings.BUCKET_PATH + settings.ARTICLE_IMAGE_LARGE_PATH + str(article.photopath)
            ET.SubElement(doc, "image_url").text = imag_url

        tree = ET.ElementTree(root)
        tree.write("/var/www/html/bw_hr/bwhr/static/xml/exclusive.xml")

        recent_publish_article = Articles.objects.order_by('-article_published_date')[:500]

        urlset = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        urlset.set('xmlns:news', "http://www.google.com/schemas/sitemap-news/0.9")


        for article in recent_publish_article:
            title_for_url = re.sub('[^A-Za-z0-9]+', '-', article.article_title)
            article_tags = ChannelTags.objects.raw("SELECT t.* FROM channel_tags t INNER JOIN article_tags at ON t.tag_id = at.tag_id WHERE at.article_id = "+str(article.article_id))

            tag_names = ''
            for tag in article_tags:
                tag_names = tag.tag_name+', '+tag_names

            doc = ET.SubElement(urlset, "url")
            ET.SubElement(doc, "loc").text = 'http://bwpeople.businessworld.in/article/'+str(title_for_url)+'/'+str(date(article.article_published_date, "d-m-Y"))+'-'+str(article.article_id)
            news=ET.SubElement(doc, "news:news")
            newsp=ET.SubElement(news, "news:publication")
            ET.SubElement(newsp,"news:name").text='BWHotelier'
            ET.SubElement(newsp,"news:language").text='en'
            ET.SubElement(news, "news:publication_date").text = str(date(article.article_published_date, 'Y-m-d'))
            ET.SubElement(news, "news:title").text = str(article.article_title)
            ET.SubElement(news, "news:keywords").text = str(tag_names)

        quickbytes_detail = QuickBytes.objects.order_by('-quick_byte_published_date')[:100]

        for quickbytes_article in quickbytes_detail:
            title_for_url_qucikbyte = re.sub('[^A-Za-z0-9]+', '-', quickbytes_article.quick_byte_title)
            quickbytes_tags = ChannelTags.objects.raw("SELECT t.* FROM channel_tags t INNER JOIN quick_bytes_tags qt ON t.tag_id = qt.tag_id WHERE qt.quick_byte_id = "+str(quickbytes_article.quick_byte_id))
            tag_namesq = ''
            for tag in quickbytes_tags:
                tag_namesq = tag.tag_name+', '+tag_namesq

            doc = ET.SubElement(urlset, "url")
            ET.SubElement(doc, "loc").text = 'http://bwpeople.businessworld.in/quickbytes/'+str(title_for_url_qucikbyte)+'/'+str(date(quickbytes_article.quick_byte_published_date, "d-m-Y"))+'-'+str(quickbytes_article.quick_byte_id)
            news=ET.SubElement(doc, "news:news")
            newsp=ET.SubElement(news, "news:publication")
            ET.SubElement(newsp,"news:name").text='BWHotelier'
            ET.SubElement(newsp,"news:language").text='en'
            ET.SubElement(news, "news:publication_date").text = str(date(quickbytes_article.quick_byte_published_date, 'Y-m-d'))
            ET.SubElement(news, "news:title").text = str(quickbytes_article.quick_byte_title)
            ET.SubElement(news, "news:keywords").text = str(tag_namesq)
        tree = ET.ElementTree(urlset)
        tree.write("/var/www/html/bw_hr/bwhr/templates/sitemap7.xml")

        #astrology xml
        feeds_cric = feedparser.parse('http://feeds.ganeshaspeaks.com/BusinessWorld/BWWeeklyMoney.xmlfeed')
        root = ET.Element("root")

        for entry in feeds_cric.entries:
            doc = ET.SubElement(root, "astrology")
            ET.SubElement(doc, "link").text = str(entry.link)
            ET.SubElement(doc, "title").text = str(entry.title)
            ET.SubElement(doc, "description").text = str(entry.description)

        tree = ET.ElementTree(root)
        tree.write("/var/www/html/bw_hr/bwhr/static/xml/astrology.xml")


        #Dow Jones XML generation
        #urlset = ET.Element('xml', version="1.0", encoding="UTF-8")
        nodes = ET.Element('nodes')

        html_parser = HTMLParser.HTMLParser()

        #50 article list without BW Online for yahoo and dow jones
        article_list = Articles.objects.raw("SELECT A.* FROM articles A LEFT JOIN article_author A_A ON A.article_id = A_A.article_id WHERE A_A.author_type != 1 GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 50")

        for article in article_list:
            node = ET.SubElement(nodes, "node")
            ET.SubElement(node, "link").text = 'http://bwpeople.businessworld.in/' + article.get_absolute_url()
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
        out = open('/var/www/html/bw_hr/bwhr/static/xml/dow_jones_article.xml', 'w+')
        out.write(tree)
        out.close()

