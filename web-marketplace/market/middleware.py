import logging
import os
import traceback
import sys


class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file_path = 'logs.txt'

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)
        self.formatter = logging.Formatter('%(asctime)s - %(message)s')

        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, 'w') as f:
                pass

        self.file_handler = logging.FileHandler(self.log_file_path)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def __call__(self, request):
        response = self.get_response(request)

        if sys.exc_info()[0] is not None:
            self.logger.error(''.join(traceback.format_exception(*sys.exc_info())))

        return response

    def process_exception(self, request, exception):
        self.logger.error(''.join(traceback.format_exception(type(exception), exception, exception.__traceback__)))