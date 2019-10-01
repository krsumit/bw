from articles.models import Articles, ArticleImages,ArticleCategory, ArticleTopics
#from featuredbox.models import FeatureBox
from author.models import Author, AuthorType
from topics.models import ChannelTopics
from tags.models import ChannelTags
from columns.models import Columns
from category.models import ChannelCategory
from mastervideo.models import VideoMaster
from quickbytes.models import QuickBytes, QuickBytesPhotos, QuickBytesTags
def sidebar_data():
    sidebar_recent_articles = Articles.objects.raw("SELECT A.*, AI.image_url, AI.photopath FROM articles A LEFT JOIN article_images AI ON AI.article_id = A.article_id WHERE (AI.image_status='enabled' OR AI.image_status is null) GROUP BY A.article_id ORDER BY A.article_published_date DESC LIMIT 6")

    trending_now_topics = ChannelTopics.objects.raw("SELECT T.*, A.article_published_date FROM channel_topics T LEFT JOIN article_topics AT ON AT.topic_id = T.topic_id LEFT JOIN articles A ON AT.article_id = A.article_id GROUP BY T.topic_id ORDER BY A.article_published_date DESC LIMIT 5")

    bwtv_articles = Articles.objects.raw("SELECT A.*, AC.*, AI.image_url, AI.photopath FROM articles A LEFT JOIN  article_category AC ON A.article_id = AC.article_id JOIN article_images AI ON AI.article_id = A.article_id  WHERE AC.category_id = '110' ORDER BY A.article_published_date DESC LIMIT 3")
    #videomaster_listing = VideoMaster.objects.raw("SELECT * FROM video_master ORDER BY updated_at DESC LIMIT 6")
   
    bwtv_cat_details = ChannelCategory.objects.filter(category_id='110').first()
    quick_bytes_listing = QuickBytes.objects.raw("SELECT Q.*, QP.quick_byte_photo_url as image_url, QP.quick_byte_photo_name FROM quick_bytes Q LEFT JOIN quick_bytes_photos QP ON Q.quick_byte_id = QP.quick_byte_id WHERE QP.quick_byte_photo_name !='' GROUP BY Q.quick_byte_id ORDER BY Q.quick_byte_published_date DESC LIMIT 0,5 ")
    return {'sidebar_recent_articles': sidebar_recent_articles, 'trending_now_topics': trending_now_topics, 'bwtv_articles':bwtv_articles, 'bwtv_cat_details':bwtv_cat_details,'quick_bytes_listing':quick_bytes_listing}
    
def category_jump_list():
    category_jumlist = ChannelCategory.objects.filter(category_parent='0')
    return category_jumlist

def closeDbConnection():
    from django.db import connection
    connection.close()
    return
