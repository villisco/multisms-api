import pytest
import logging

from application.utils.log_filters import FilterRemoveDateFromWerkzeugLogs, FilterExcludeHEADLogs
from tests.fixtures.log_fixtures import werkzeug_log_before_date_filter, werkzeug_log_after_date_filter, werkzeug_log_filtered_head_req

def test_filter_remove_date_from_werkzeug_logs(werkzeug_log_before_date_filter, werkzeug_log_after_date_filter):
    filter_instance = FilterRemoveDateFromWerkzeugLogs()
    assert filter_instance.filter(werkzeug_log_before_date_filter) is True
    assert werkzeug_log_before_date_filter.msg == werkzeug_log_after_date_filter.msg

def test_filter_exclude_head_logs_filtered(werkzeug_log_filtered_head_req):
    filter_instance = FilterExcludeHEADLogs()
    assert filter_instance.filter(werkzeug_log_filtered_head_req) is False  # HEAD request filtered out

def test_filter_exclude_head_logs_allows_other_requests(werkzeug_log_after_date_filter):
    filter_instance = FilterExcludeHEADLogs()
    assert filter_instance.filter(werkzeug_log_after_date_filter) is True  # GET request allowed