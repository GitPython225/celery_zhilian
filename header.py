import random
from fake_useragent import UserAgent
headers = {}
ua = UserAgent()
user_agent = ua.random
headers['User-Agent'] = user_agent