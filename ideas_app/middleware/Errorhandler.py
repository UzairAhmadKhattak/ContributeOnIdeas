from django.http import HttpResponseServerError
import logging
from django.conf import settings

class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        if settings.DEBUG:
                level = logging.DEBUG
        else:
            level = logging.INFO
        logging.basicConfig(level=level,
                                format='%(filename)s - %(asctime)s - %(levelname)s - %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S',
                                handlers=[
                                    logging.StreamHandler(),
                                ]
                                )
        self.logger = logging.getLogger()

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            response = HttpResponseServerError("Oops! Something went wrong.")
            self.logger.debug('Error: '+str(e))
        return response