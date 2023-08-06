from .lib.ip import is_ip as _is_ip, get_info as _get_info_by_ip, get_country as _get_country_by_ip
from .lib.url import get_info as _get_info_by_url, get_country as _get_country_by_url

def is_ip(ip):
  return _is_ip(ip)

def get_info_by_ip(ip):
  return _get_info_by_ip(ip)

def get_country_by_ip(ip):
  return _get_country_by_ip(ip)

def get_info_by_url(url):
  return _get_info_by_url(url)

def get_country_by_url(url):
  return _get_country_by_url(url)
