# https://flask-limiter.readthedocs.io/en/stable/
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

"""
Example usage:
@limiter.limit("100/day")
@limiter.limit("10/hour")
@limiter.limit("1/minute")
@limiter.limit("10/second")
"""
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://", # replace this with redis for persistence
)