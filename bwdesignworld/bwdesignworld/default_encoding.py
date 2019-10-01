import sys

class DefaultEncodingMiddleware(object):
    def process_response(self, request, response):
        reload(sys)
        sys.setdefaultencoding("utf-8")
        return response