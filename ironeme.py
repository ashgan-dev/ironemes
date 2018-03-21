#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
from configparser import ConfigParser
from urllib.parse import urlparse
import jinja2

from bs4 import BeautifulSoup
from path import path

from MastodonClass import MastodonClass as Mstdn

HASHTAGS = ['ironème', ]  # , 'ironèmes', 'ironeme', 'ironemes']
BLOCKLIST = ['TrendingBot@mastodon.social', ]
HTMLTAGS = ['span', 'a', 'html', 'body']
JSON_OUTPUT_FILE = 'out.json'
HTML_OUPUT_FILE = 'index.html'
HTML_TEMPLATE = 'template.tpl'
ROOT = path('.').realpath()


def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)


def render_page(toots):
    """
    render HTML page with toots
    """
    templateloader = jinja2.FileSystemLoader(searchpath=ROOT, encoding='utf-8')
    templateenv = jinja2.Environment(loader=templateloader)
    templateenv.filters['datetimeformat'] = datetimeformat
    template_name = HTML_TEMPLATE
    html_output_path = ROOT / HTML_OUPUT_FILE

    template = templateenv.get_template(template_name)
    output_html = template.render(toots=toots[0],
                                  nb_toots=toots[1],
                                  now=time.strftime(u'%d/%m/%Y à %H:%M:%S', time.localtime()))

    with open(html_output_path, 'wb') as outfile:
        outfile.write(output_html.encode('utf-8'))


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


def get_context(toot_id, api_endpoint):
    """
    get the whole conversation
    """
    pass


def get_hashtags(hashtags, api_endpoint, instance_url):
    """
    fetches all toots for a given <hashtag> using an <api> established connection,
    and we're connected on the <instance_url>
    """
    id_list = list()
    toot_list = list()
    tootcnt = 0  # fetched toot counter
    for hashtag in hashtags:
        maxid = None  # latest toot id we've fetched
        # get @local.instance because local toots are returned only with the
        # account name
        localinstance = '@' + urlparse(instance_url).netloc
        while True: #tootcnt < 20:  # True
            toots = api_endpoint.timeline_hashtag(hashtag, max_id=maxid)
            if len(toots) == 0:
                break
            for toot in toots:
                account = toot['account']['acct']
                toot['content'] = clean_html(toot['content'])
                toot['account']['created_at'] = toot['account']['created_at'].strftime(u'%Y-%m-%dT%H:%M:%SZ')
                toot['created_at'] = toot['created_at'].strftime(u'%d/%m/%Y à %H:%M:%S')

                if '@' not in account:  # local instance toot
                    account += localinstance
                if account not in BLOCKLIST:
                    if toot['id'] not in id_list:
                        id_list.append(toot['id'])
                        toot_list.append(toot)
                maxid = toot['id']
                tootcnt += 1

            time.sleep(1)  # avoid hitting limit rates
        with open(JSON_OUTPUT_FILE, 'w', encoding='utf8') as out_file:
            json.dump(toot_list, out_file, sort_keys=True, indent=4, ensure_ascii=False)
        print(time.strftime(u'%d/%m/%Y à %H:%M:%S', time.localtime()))
    return toot_list, tootcnt


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

print(time.strftime(u'%d/%m/%Y à %H:%M:%S', time.localtime()))
toots_list = get_hashtags(HASHTAGS, api, config['Auth']['instance'])
render_page(toots_list)
