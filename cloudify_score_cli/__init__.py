import logging
import ConfigParser
import collections
from cloudify_rest_client import CloudifyClient

_logger = None

CONFIGFILE = '.score'
SECTION = 'Openstack'

USER = 'user'
PASSWORD = 'password'
HOST = 'host'
TOKEN = 'token'
SCORE_HOST = 'score_host'
DEFAULT_PROTOCOL = 'http'
SECURED_PROTOCOL = 'https'


Configuration = collections.namedtuple('Configuration', 'user, password, host, token, score_host')

def get_logger():
    global _logger
    if _logger is not None:
        return _logger
    log_format = '%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s'
    _logger = logging.getLogger("score_cli_logger   ")
    _logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
    return _logger


def save_config(service_parameters):
    _save_openstack_config(service_parameters)


def load_config(logger):
    return _load_openstack_config(logger)


def _save_openstack_config(openstack):
    config = ConfigParser.RawConfigParser()
    config.add_section(SECTION)
    config.set(SECTION, USER, openstack.user)
    config.set(SECTION, PASSWORD, openstack.password)
    config.set(SECTION, HOST, openstack.host)
    config.set(SECTION, TOKEN, openstack.token)
    config.set(SECTION, SCORE_HOST, openstack.score_host)       
    
    with open(CONFIGFILE, 'wb') as configfile:
        config.write(configfile)    


def _load_openstack_config(logger):
    openstack = Configuration
    try:
        config = ConfigParser.ConfigParser()
        config.read(CONFIGFILE)
        openstack.user = config.get(SECTION, USER, None)
        openstack.password = config.get(SECTION, PASSWORD, None)
        openstack.host = config.get(SECTION, HOST, None)
        openstack.token = config.get(SECTION, TOKEN, None)
        openstack.score_host = config.get(SECTION, SCORE_HOST, None)       
    except ConfigParser.NoSectionError as e:
        logger.info(e)
    return openstack


def _get_headers(config):
    return None

def get_score_client(config):
    headers = _get_headers(config)
    return CloudifyClient(host=config.score_host, protocol=DEFAULT_PROTOCOL, headers=headers)

