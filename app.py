#!/usr/bin/env python
# -*- coding: utf-8 -*-

# forked from https://github.com/Meewan/MercrediFiction

from configparser import ConfigParser
from datetime import datetime
from multiprocessing.pool import Pool
from urllib.parse import urlparse

import arrow
import requests
from flask import Flask, render_template
from html2text import HTML2Text
from path import Path
from peewee import *

ROOT = Path('.').realpath()
HASHTAGS = ['ironème', 'ironèmes', 'ironeme', 'ironemes']
BLOCKLIST = ['TrendingBot@mastodon.social', ]
# API management
API_URL = 'https://{domain}/api/v1/timelines/tag/{hashtag}?limit={limit}&since_id={since_id}'
POSTGRESQL_URL = 'postgresql://{user}:{password}@{DB_host}:{port}/{database}'

Path.chdir(ROOT)

# fetch/define config
configini = ROOT / 'config.ini'
config = ConfigParser()
config.read(configini)


app = Flask(__name__)
# for small configs, use sqlite, with small number of worker (tested with 4 at best on my laptop)
# big irons, go full blast!
# db = PostgresqlDatabase(config['DB']['database'],
#                         user=config['DB']['user'],
#                         password=config['DB']['password'])
db = SqliteDatabase('app.db')


class Instance(Model):
    """instance db model"""
    creation_date = DateTimeField()
    domain = CharField(1024, unique=True)
    lock = BooleanField()
    blacklisted = BooleanField()

    class Meta:
        """related db"""
        database = db


class Account(Model):
    """account db model"""
    mastodon_id = IntegerField()
    username = CharField(1024)
    display_name = CharField(4095)
    creation_date = DateTimeField()
    note = CharField(4095)
    url = CharField(4095)
    avatar = CharField(4095)
    instance = ForeignKeyField(Instance, backref='accounts')
    blacklisted = BooleanField()

    class Meta:
        """related db"""
        database = db


class Toot(Model):
    """toots db model"""
    mastodon_id = BigIntegerField()
    creation_date = DateTimeField()
    sensitive = BooleanField()
    content = CharField(4095)
    favourite_count = IntegerField()
    reblog_count = IntegerField()
    url = CharField(4095)
    account = ForeignKeyField(Account, backref='toots')
    instance = ForeignKeyField(Instance, backref='toots')
    blacklisted = BooleanField()

    class Meta:
        """related db"""
        database = db


class MissedLink(Model):
    """missed links db model"""
    url = CharField(4095, unique=True)
    time_misses = IntegerField()

    class Meta:
        """related db"""
        database = db


class Hashtags(Model):
    """Hashtags db model"""
    tag = CharField(4095)
    last_seen_id = BigIntegerField(default=0)
    instance = ForeignKeyField(Instance, backref='hashtags')

    class Meta:
        """related db"""
        database = db


def datetimeformat(value, date_format='DD/MM/YYYY à HH:mm:ss'):
    """
    formating date for templates
    """
    return arrow.get(value).format(date_format)


def to_text(html, rehtml=False):
    """
    get text from HTML
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


def get_hashtags(instance_url):
    """
    fetches all toots for a given hashtag on given instance
    """
    print(instance_url)
    # last toot ID seen on the current instance
    ref_id = 0
    # current instance URL
    next_fetch = instance_url
    # current instance DB details already on DB
    local_instance_url = urlparse(instance_url).netloc
    instance_details = Instance.get(domain=local_instance_url)

    # hashtags details:
    # houla, cuila y pique!
    tag_name = instance_url.split('?')[0].split('/')[-1]

    # did we have already parsed someting?
    hashtag_detail, _ = Hashtags.get_or_create(instance_id=instance_details.id,
                                               last_seen_id=0,
                                               tag=tag_name)

    local_toots = None
    while True:
        try:
            local_toots = requests.get(next_fetch,
                                       timeout=120)
        except:
            # something bad happened, store URL to fetch later
            MissedLink.get_or_create(url=next_fetch,
                                     defaults={'time_misses': 0})
            break

        if local_toots:
            try:
                for toot in local_toots.json():
                    account = toot['account']['acct']
                    instance = urlparse(toot['url']).netloc
                    # get instance ID or get a new one
                    instance_id, _ = Instance.get_or_create(domain=instance,
                                                            defaults={'creation_date': datetime.now(),
                                                                      'lock': False,
                                                                      'blacklisted': False})

                    if '@' not in account:
                        # we got local account.
                        # so, genuine toots, not federated ones.
                        # let's grab it by the user!
                        account = account + '@' + instance_url
                        account_saved, _ = Account.get_or_create(mastodon_id=toot['account']['id'],
                                                        defaults={'username': toot['account']['username'],
                                                                  'display_name': to_text(toot['account']['display_name']),
                                                                  'creation_date': datetime.strptime(toot['account']['created_at'],
                                                                                                   '%Y-%m-%dT%H:%M:%S.%fZ'),
                                                                  'note': to_text(toot['account']['note']),
                                                                  'url': toot['account']['url'],
                                                                  'avatar': toot['account']['avatar'],
                                                                  'instance_id': instance_id.id,
                                                                  'blacklisted': False})

                        toot_saved, _ = Toot.get_or_create(url=toot['url'],
                                                           defaults={'creation_date': datetime.strptime(toot['created_at'],
                                                                                                        '%Y-%m-%dT%H:%M:%S.%fZ'),
                                                                     'sensitive': toot['sensitive'],
                                                                     'account_id': account_saved.id,
                                                                     'content': to_text(toot['content'], rehtml=True),
                                                                     'instance_id': instance_id.id,
                                                                     'mastodon_id': toot['id'],
                                                                     'favourite_count': toot['favourites_count'],
                                                                     'reblog_count': toot['reblogs_count'],
                                                                     'blacklisted': False})

                next_fetch = local_toots.links['next']['url']
                id_to_fetch = int(next_fetch.split('=')[-1])
                if id_to_fetch > ref_id:
                    ref_id = id_to_fetch

                if hashtag_detail.last_seen_id > id_to_fetch:
                    break

                # time.sleep(1)  # avoid hitting limit rates
            except (KeyError, ):
                # no more dicts, no scraping left
                # oui did it \o/
                break
        else:
            missed_link = MissedLink.get_or_create(url=next_fetch,
                                                   defaults={'time_misses': 0})

    query = Hashtags.update(last_seen_id=ref_id).where((Hashtags.instance_id == instance_details.id) &
                                                       (Hashtags.tag == hastag_detail.tag))
    query.execute()


app.add_template_filter(datetimeformat)


@app.route('/')
def start_page():
    """main page"""
    return render_template('template.tpl',
                           toots=Toot.select().order_by(Toot.creation_date))


if __name__ == '__main__':
    db.connect()
    db.create_tables([Instance, Account, Toot, MissedLink, Hashtags])

    domain = urlparse(config['Auth']['instance']).netloc
    query = Instance.get_or_create(domain=domain,
                                   defaults={'creation_date': datetime.now(),
                                             'lock': False,
                                             'blacklisted': False})

    to_fetch = list()
    for k in HASHTAGS:
        for i in [x.domain for x in Instance.select()]:
            to_fetch.append(API_URL.format(domain=i,
                                           hashtag=k,
                                           since_id=0,
                                           limit=40))
    # we're *not really* CPU/mem/HDD bound. so yepekai!
    # for info, with 32 workers, on average:
    # <2Mbits/s download, 25-50% CPU, 1.5/2Go Ram, <10% HDD use on my core I7-4710 laptop
    with Pool(4) as p:
        result = p.map(get_hashtags, to_fetch)

    app.run(debug=True)
