import logging

class RequestIDFilter(logging.Filter):
    """
    Logging filter that injects the current request ID (if available) into the log record.
    """
    def filter(self, record):
        # We can fetch the request ID from the thread context, or just default to empty.
        # For simplicity, we default to "N/A" unless explicit extra parameters are passed.
        # But we can try to inspect current requests via django-crs or a simple local thread.
        # Let's keep it safe.
        record.request_id = getattr(record, 'request_id', '-')
        return True
