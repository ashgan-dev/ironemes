#!/usr/bin/env python
# -*- coding: utf-8 -*-

# script based on https://github.com/julianaito/mstdntools
# for the kickstart

import json
import time
from configparser import ConfigParser
from operator import itemgetter
from urllib.parse import urlparse
from html2text import HTML2Text


import arrow
import jinja2
from path import path
from natsort import humansorted

from MastodonClass import MastodonClass as Mstdn

HASHTAGS = ['ironème', 'ironèmes', 'ironeme', 'ironemes']
BLOCKLIST = ['TrendingBot@mastodon.social', ]
HTMLTAGS = ['span', 'a', 'html', 'body']
INDEX_TEMPLATE = 'index.tpl'
HTML_TEMPLATE_FILE = 'template.tpl'
ROOT = path('.').realpath()
UPLOAD_DIR = path('to_upload')
JSON_OUTPUT_FILE = UPLOAD_DIR / 'ironemes_json_{year}_{week}.json'
JSON_DUMP_FILE = UPLOAD_DIR / 'ironemes.json'
HTML_INDEX_FILE = UPLOAD_DIR / 'index.html'


def datetimeformat(value, date_format='DD/MM/YYYY à HH:mm:ss'):
    """
    formating date for templates
    """
    return arrow.get(value).format(date_format)


def proper_name(value):
    """
    formating ironemes dates and files
    """
    if 'json' not in value:
        return 'ironemes'
    else:
        x = value.stripext().split('_')
        semaine = x[-2:]
        return 'ironèmes {}, semaine {}'.format(semaine[0], semaine[1])


def render_page():
    """
    render HTML page with toots
    """
    json_files = list()
    for x in UPLOAD_DIR.walkfiles('*.json'):
        json_files.append(x)

    templateloader = jinja2.FileSystemLoader(searchpath=ROOT, encoding='utf-8')
    templateenv = jinja2.Environment(loader=templateloader)
    templateenv.filters['datetimeformat'] = datetimeformat
    templateenv.filters['proper_name'] = proper_name
    template_name = HTML_TEMPLATE_FILE
    template = templateenv.get_template(template_name)

    for i in json_files:
        with open(i, encoding='utf-8') as json_file:
            x = json.load(json_file)
            y = len(x)
        output_html = template.render(toots=x,
                                      nb_toots=y,
                                      json_file=i)

        with open(UPLOAD_DIR / i.namebase + '.html', 'wb') as outfile:
            outfile.write(output_html.encode('utf-8'))

    template = templateenv.get_template(INDEX_TEMPLATE)
    html_files = list()
    for i in UPLOAD_DIR.walkfiles('*.html'):
        html_files.append(i.name)
    html_files.remove('index.html')
    index_html = template.render(html_files=humansorted(html_files))

    with open(HTML_INDEX_FILE, 'wb') as outfile:
        outfile.write(index_html.encode('utf-8'))


def to_text(html, rehtml=False):
    """
    get text only from toot content
    """
    parser = HTML2Text()
    parser.wrap_links = False
    parser.skip_internal_links = True
    parser.inline_links = True
    parser.ignore_anchors = True
    parser.ignore_images = True
    parser.ignore_emphasis = True
    parser.ignore_links = True
    text = parser.handle(html)
    text = text.strip(' \t\n\r')
    if rehtml:
        text = text.replace('\n', '<br/>')
        text = text.replace('\\', '')
    return text


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
        while True: #tootcnt < 20: # True:
            toots = api_endpoint.timeline_hashtag(hashtag, max_id=maxid, limit=40)
            if len(toots) == 0:
                break
            for toot in toots:
                toot_date = arrow.get(toot['account']['created_at'])
                account = toot['account']['acct']
                toot['content'] = to_text(toot['content'], rehtml=True)
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

path.makedirs_p(UPLOAD_DIR)

toots_list = get_hashtags(HASHTAGS, api, config['Auth']['instance'])
split_json(toots_list[0])
render_page()

# quoi faire de ca? utile?
# je verrais bien le toot d'origine,
# et un clic sur "learn more" et bam l'historique qui depile


# toot "remi sans famille", seul au monde
# toot_alone = get_context(99723799065931813, api)
# et un avec du contexte
# moucho_story = get_context(99626644990501540, api)
