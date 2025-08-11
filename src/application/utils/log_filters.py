import logging
import re

class FilterRemoveDateFromWerkzeugLogs(logging.Filter): # NOSONAR: safe static filter
    """
    Custom filter to clean up logs by removing date strings.
    """
    # '192.168.0.102 - - [30/Jun/2024 01:14:03] "%s" %s %s' ---> '192.168.0.102 - "%s" %s %s'
    pattern: re.Pattern = re.compile(r' - - \[.+?] "')

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = self.pattern.sub(' - "', record.msg)
        return True

# shared by gunicorn + werkzeug (flask dev)
class FilterExcludeHEADLogs(logging.Filter): # NOSONAR: safe static filter
    """
    Custom filter to clean up logs by removing HEAD requests.
    """
    # Health check logs:
    # '192.168.0.102 - "HEAD / HTTP/1.0" 200 -'
    def filter(self, record: logging.LogRecord):
        return 'HEAD / HTTP' not in record.getMessage()