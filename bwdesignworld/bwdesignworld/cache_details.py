from django.conf import settings

# default 30 days
#MAX_AGE = getattr(settings, 'CACHE_CONTROL_MAX_AGE', 2592000)

class MaxCacheAgeMiddleware(object):
    def process_response(self, request, response):
        response['Cache-Control'] = 'max-age=300, public, must-revalidate, proxy-revalidate'
        return response