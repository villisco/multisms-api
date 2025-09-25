import logging
import os
import inspect
from flask.logging import wsgi_errors_stream

# https://luolingchun.github.io/flask-openapi3/v4.x/
from flask_openapi3 import OpenAPI, Info, ExternalDocumentation

from config import APP_NAME, APP_VERSION, Config, AuthSecurity
from application.auth.basic_auth import basic_auth_check
from application.utils.log_filters import FilterRemoveDateFromWerkzeugLogs, FilterExcludeHEADLogs
from application.utils.rate_limiter import limiter
from application.utils.exceptions_handler import register_api_error_handler
from application.utils.config_helper import load_yaml_config

from application.routes.get_index import bp as index_bp
from application.routes.get_health import bp as health_bp
from application.routes.get_config import bp as config_bp
from application.routes.post_sms import bp as post_sms_bp
from application.routes.post_alertmanager import bp as post_sms_alertmanager_bp

def configure_logging():
    formatter = logging.Formatter('%(asctime)s [%(filename)s] [%(levelname)s]: %(message)s')

    wsgi_handler = logging.StreamHandler(stream=wsgi_errors_stream)
    wsgi_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers = []
    root_logger.addHandler(wsgi_handler)

def create_app(config_class = Config):
    info = Info(
        title=APP_NAME, 
        version=APP_VERSION
    )

    external_docs = ExternalDocumentation(
        url="https://www.telia.ee/images/documents/juhendid/eng/MultiSMS_manual_eng.pdf",
        description="Telia MutliSMS service (manual)"
    )

    app = OpenAPI(
        __name__, 
        info = info,
        external_docs = external_docs,
        security_schemes = AuthSecurity.security_schemes
    )

    # load base config
    app.config.from_object(config_class)
    configure_logging()
    app.logger.info("Application config loaded: %s" % os.path.basename((inspect.getfile(config_class))))

    if not app.config["GROUPS_CONFIG_PATH"]:
        raise RuntimeError("Required GROUPS_CONFIG_PATH envvar not configured!")

    # merge user managed config
    yaml_config = load_yaml_config(app.config["GROUPS_CONFIG_PATH"])

    app.config.update(yaml_config)
    app.logger.info("Application receivers config loaded: %s" % app.config["GROUPS_CONFIG_PATH"])

    # flask http request logs
    logging.getLogger("werkzeug").addFilter(FilterRemoveDateFromWerkzeugLogs())
    logging.getLogger("werkzeug").addFilter(FilterExcludeHEADLogs())
    logging.getLogger("werkzeug").setLevel(app.config['LOG_LEVEL_HTTP'])

    # flask application logs
    app.logger.setLevel(eval("logging.%s" % app.config['LOG_LEVEL_APP']))
    app.logger.info('Application started with LOG_LEVEL_GUNICORN: %s' % app.config['LOG_LEVEL_GUNICORN'])
    app.logger.info('Application started with LOG_LEVEL_HTTP: %s' % app.config['LOG_LEVEL_HTTP'])
    app.logger.info('Application started with LOG_LEVEL_APP: %s' % app.config['LOG_LEVEL_APP'])

    if app.config["TESTING"]:
        app.logger.warning('Application is in TESTING mode!')

    # apply blueprints
    app.register_api(index_bp, url_prefix="/")
    app.register_api(health_bp, url_prefix="/api/v1")
    app.register_api(config_bp, url_prefix="/api/v1")
    app.register_api(post_sms_bp, url_prefix="/api/v1")
    app.register_api(post_sms_alertmanager_bp, url_prefix="/api/v1")

    register_api_error_handler(app)

    # by default Flask validates request body before all else
    app.before_request(basic_auth_check)

    # initilize requests rate limiter for api endpoints
    limiter.init_app(app)

    return app