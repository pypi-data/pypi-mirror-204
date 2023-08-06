from urllib.parse import urlparse
from .ip import get_info as get_info_by_ip, get_country as get_country_by_ip
import socket

def get_hostname(url):
  o = urlparse(url)
  return o.hostname

def get_ip(url):
  hostname = get_hostname(url)
  return socket.gethostbyname(hostname)

def get_info(url):
  return get_info_by_ip(get_ip(url))

def get_country(url):
  return get_country_by_ip(get_ip(url))
