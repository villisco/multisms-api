import logging
from gunicorn.glogging import Logger
from application.utils.log_filters import FilterExcludeHEADLogs

class CustomGunicornLogger(Logger):
    def setup(self, cfg):
        super().setup(cfg)

        filters = [FilterExcludeHEADLogs()]

        for log in [self.error_log, self.access_log]:
            for f in filters:
                log.addFilter(f)