#!/usr/bin/env python
# -*- coding: utf-8 -*-

# script based on https://github.com/julianaito/mstdntools
# for the kickstart

import json
import time
from configparser import ConfigParser
from ftplib import FTP
from urllib.parse import urlparse
from operator import itemgetter

import arrow
import jinja2
from bs4 import BeautifulSoup
from path import path

from MastodonClass import MastodonClass as Mstdn

HASHTAGS = ['ironème', 'ironèmes', 'ironeme', 'ironemes']
BLOCKLIST = ['TrendingBot@mastodon.social', ]
HTMLTAGS = ['span', 'a', 'html', 'body']
JSON_OUTPUT_FILE = 'ironemes_json_{year}_{week}.json'
JSON_DUMP_FILE = 'ironemes.json'
HTML_INDEX_FILE = 'index.html'
INDEX_TEMPLATE = 'index.tpl'
HTML_TEMPLATE_FILE = 'template.tpl'
ROOT = path('.').realpath()


def datetimeformat(value, date_format='DD/MM/YYYY à HH:mm:ss'):
    """
    formating date for templates
    """
    return arrow.get(value).format(date_format)


def render_page():
    """
    render HTML page with toots
    """
    json_files = ROOT.files('*.json')

    templateloader = jinja2.FileSystemLoader(searchpath=ROOT, encoding='utf-8')
    templateenv = jinja2.Environment(loader=templateloader)
    templateenv.filters['datetimeformat'] = datetimeformat
    template_name = HTML_TEMPLATE_FILE
    template = templateenv.get_template(template_name)

    for i in json_files:
        with open(i, encoding='utf-8') as json_file:
            x = json.load(json_file)
            y = len(x)
        output_html = template.render(toots=x,
                                      nb_toots=y,
                                      json_file=i)

        with open(i.namebase + '.html', 'wb') as outfile:
            outfile.write(output_html.encode('utf-8'))

    template = templateenv.get_template(INDEX_TEMPLATE)
    html_files = ROOT.files('*.html')
    index_html = template.render(html_files=html_files)

    with open(HTML_INDEX_FILE, 'wb') as outfile:
        outfile.write(index_html.encode('utf-8'))


def clean_html(content):
    """
    remove unwanted html tags from toot content
    """
    content_to_parse = BeautifulSoup(content, "html.parser")
    # gently remove tags and CSS stuff, keeping content
    # only <p> and <br> should remain.
    for i in HTMLTAGS:
        for j in content_to_parse.find_all(i):
            j.unwrap()
    # bruteforce anihilation of iframe/script tags.
    # should not exist because of API cleaning,
    # but who knows?!?
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
    get the whole conversation fot a toot
    not used at this time
    """
    toot_context = api_endpoint.status_context(toot_id)
    return toot_context


def split_json(toot_list):
    """
    split toots by year and week
    """
    out_string = dict()
    b = dict()
    for i in toot_list:
        toot_date = arrow.get(i['created_at'])
        out_string['year'], out_string['week'], _ = toot_date.isocalendar()
        tuple_key = (out_string['year'], out_string['week'])
        if tuple_key not in b.keys():
            b[tuple_key] = []
            b[tuple_key].append(i)
        else:
            b[tuple_key].append(i)
    for i in b.keys():
        json_filename = JSON_OUTPUT_FILE.format(year=i[0], week=i[1])
        with open(json_filename, 'w', encoding='utf8') as out_file:
            json.dump(b[i],
                      out_file,
                      sort_keys=True,
                      indent=4,
                      ensure_ascii=False)


def get_hashtags(hashtags, api_endpoint, instance_url):
    """
    fetches all toots for a given <hashtag> using an <api> established connection,
    and we're connected on the <instance_url>
    """
    id_list = list()
    toot_list = list()
    tooters = dict()
    for hashtag in hashtags:
        maxid = None  # latest toot id we've fetched
        tootcnt = 0
        # get @local.instance because local toots are returned only with the
        # account name
        localinstance = '@' + urlparse(instance_url).netloc
        while True:
            toots = api_endpoint.timeline_hashtag(hashtag, max_id=maxid, limit=40)
            if len(toots) == 0:
                break
            for toot in toots:
                toot_date = arrow.get(toot['account']['created_at'])
                account = toot['account']['acct']
                toot['content'] = clean_html(toot['content'])
                toot['account']['created_at'] = toot_date.for_json()
                toot['created_at'] = arrow.get(toot['created_at']).for_json()

                if '@' not in account:  # local instance toot
                    account += localinstance
                if account not in BLOCKLIST:
                    if toot['id'] not in id_list:
                        id_list.append(toot['id'])
                        toot_list.append(toot)

                maxid = toot['id']
                tootcnt += 1

            time.sleep(1)  # avoid hitting limit rates
    for i in toot_list:
        account = i['account']['acct']
        if account not in tooters.keys():
            tooters[account] = 1
        else:
            tooters[account] += 1
    sorted_toots = sorted(toot_list, key=itemgetter('created_at'), reverse=True)

    with open(JSON_DUMP_FILE, 'w', encoding='utf8') as out_file:
        json.dump(sorted_toots,
                  out_file,
                  sort_keys=True,
                  indent=4,
                  ensure_ascii=False)

    return sorted_toots, len(sorted_toots)


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

toots_list = get_hashtags(HASHTAGS, api, config['Auth']['instance'])
split_json(toots_list[0])
render_page()
# print(get_context(99723799065931813, api))
# print(get_context(99626644990501540, api))

# ftp = FTP(config['FTP']['host'],
#           config['FTP']['user'],
#           config['FTP']['password'])
# f_name = HTML_OUPUT_FILE
# f = open(f_name, 'rb')
# ftp.storbinary('STOR ' + f_name, f)
# f.close()
