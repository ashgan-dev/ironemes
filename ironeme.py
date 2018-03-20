#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
from configparser import ConfigParser
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from path import path

from MastodonClass import MastodonClass as Mstdn

HASHTAGS = ['ironème', ]  # , 'ironèmes', 'ironeme', 'ironemes']
BLOCKLIST = ['TrendingBot@mastodon.social', ]
HTMLTAGS = ['span', 'a', 'html', 'body']
JSON_FILE = 'out.json'


def clean_html(content):
    """
    remove unwanted html tags from toot content
    """
    content_to_parse = BeautifulSoup(content, "html.parser")
    for i in HTMLTAGS:
        for j in content_to_parse.find_all(i):
            j.unwrap()
    try:
        content_to_parse.iframe.extract()
    except AttributeError:
        pass
    try:
        content_to_parse.script.extract()
    except AttributeError:
        pass
    return str(content_to_parse)


def get_hashtags(hashtags, api_endpoint, instance_url):
    """
    fetches all toots for a given <hashtag> using an <api> established connection,
    and we're connected on the <instance_url>
    """
    id_list = list()
    toot_list = list()
    for hashtag in hashtags:
        maxid = None  # latest toot id we've fetched
        tootcnt = 0  # fetched toot counter
        # get @local.instance because local toots are returned only with the
        # account name
        localinstance = '@' + urlparse(instance_url).netloc
        while tootcnt < 20:  # True
            toots = api_endpoint.timeline_hashtag(hashtag, max_id=maxid)
            if len(toots) == 0:
                break
            for toot in toots:
                account = toot['account']['acct']
                toot['content'] = clean_html(toot['content'])
                toot['account']['created_at'] = toot['account']['created_at'].strftime(u'%Y-%m-%dT%H:%M:%SZ')
                toot['created_at'] = toot['created_at'].strftime(u'%Y-%m-%dT%H:%M:%SZ')

                if '@' not in account:  # local instance toot
                    account += localinstance
                if account not in BLOCKLIST:
                    if toot['id'] not in id_list:
                        id_list.append(toot['id'])
                        toot_list.append(toot)
                maxid = toot['id']
                tootcnt += 1

            time.sleep(1)  # avoid hitting limit rates
        with open(JSON_FILE, 'w', encoding='utf8') as out_file:
            json.dump(toot_list, out_file, sort_keys=True, indent=4, ensure_ascii=False)


ROOT = path('.').realpath()
path.chdir(ROOT)

# fetch/define config
configini = ROOT / 'config.ini'
config = ConfigParser()
config.read(configini)

# setup mastodon api
connection = Mstdn(config['Auth']['instance'],
                   config['Auth']['usermail'],
                   config['Auth']['userpass'],
                   ROOT)
connection.initialize()
api = connection.mastodon

get_hashtags(HASHTAGS, api, config['Auth']['instance'])
