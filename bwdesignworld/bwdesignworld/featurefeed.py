from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from featuredbox.models import FeatureBox

class LatestFeatureFeed(Feed):
    title = "featured-article"
    link = "/featured-article/"
    description = "All listed featured article."
    description_template = 'feeds/featured-article.html'

    def items(self):
        return FeatureBox.objects.order_by('-feature_box_create_at')

    def item_title(self, item):
        return item.feature_box_title

    def item_description(self, item):
        return item.feature_box_description

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        #return reverse('news-item', args=[item.pk])
        return item.get_absolute_url()
        #return reverse('article/'+str(item.title_for_url)+'/'+str(item.article_published_date)+'-'+str(item.article_id), args=[])

    def item_publish_date(self, item):
        return item.feature_box_create_at