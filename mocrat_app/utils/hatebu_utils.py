import logging
import requests

import feedparser

from utils.mocrat_requests_classes import TwitterRequests

from mocrat_config.environ_config import env
from mocrat_config.post_texts import *

logger = logging.getLogger(__name__)

hatebu_it_top_xml_rss = env("HATEBU_IT_TOP_XML_RSS")

def return_tophatebu_itposts():
    '''
    python3 -c "from utils import hatebu_utils; hatebu_utils.return_tophatebu_itposts()"
    '''

    feeds = feedparser.parse(hatebu_it_top_xml_rss)
    ret = []
    for entry in feeds.entries:
        ret.append((entry.title, entry.link))
    
    return ret