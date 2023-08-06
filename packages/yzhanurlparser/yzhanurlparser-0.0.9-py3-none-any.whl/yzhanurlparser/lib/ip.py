import re, IP2Location, os, warnings

def is_ip(ip):
  compile_ip = re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
  return True if compile_ip.match(ip) else False

def get_info(ip):
  warnings.simplefilter('ignore', ResourceWarning)
  current_path = os.path.abspath(__file__)
  database = IP2Location.IP2Location(os.path.join(os.path.dirname(current_path), '..', 'data', 'IP2LOCATION-LITE-DB1.BIN'))
  return database.get_all(ip)

def get_country(ip):
  o = get_info(ip)
  return o.country_short
