import logging
import sys

class ConsoleHandlerNoTraceback(logging.StreamHandler):
    """Handler que solo muestra el mensaje sin traceback en consola"""
    def emit(self, record):
        exc_info_original = record.exc_info
        record.exc_info = None
        try:
            super().emit(record)
        finally:
            record.exc_info = exc_info_original