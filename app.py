#!/usr/bin/env python
# -*- coding: utf-8 -*-

# forked from https://github.com/Meewan/MercrediFiction

# from MastodonClass import MastodonClass as Mstdn
import time
from configparser import ConfigParser
from datetime import datetime
from pprint import pprint
from urllib.parse import urlparse

import requests
from flask import Flask  # , render_template, request, send_from_directory
# from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from html2text import HTML2Text
from path import Path

from multiprocessing.pool import Pool

ROOT = Path('.').realpath()
HASHTAGS = ['ironème', 'ironèmes', 'ironeme', 'ironemes']
BLOCKLIST = ['TrendingBot@mastodon.social', ]
# API management
API_URL = 'https://{domain}/api/v1/timelines/tag/{hashtag}?limit={limit}&since_id={since_id}'

Path.chdir(ROOT)

# fetch/define config
configini = ROOT / 'config.ini'
config = ConfigParser()
config.read(configini)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ironemes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Toot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mastodon_id = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime)
    sensitive = db.Column(db.Boolean)
    content = db.Column(db.String(4095))
    favourite_count = db.Column(db.Integer)
    reblog_count = db.Column(db.Integer)
    url = db.Column(db.String(4095))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    instance_id = db.Column(db.Integer, db.ForeignKey('instance.id'))
    blacklisted = db.Column(db.Boolean)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mastodon_id = db.Column(db.Integer)
    username = db.Column(db.String(1024))
    display_name = db.Column(db.String(4095))
    creation_date = db.Column(db.DateTime)
    note = db.Column(db.String(4095))
    url = db.Column(db.String(4095))
    avatar = db.Column(db.String(4095))
    instance_id = db.Column(db.Integer, db.ForeignKey('instance.id'))
    toots = db.relationship('Toot', backref='account', lazy='dynamic')
    blacklisted = db.Column(db.Boolean)


class Instance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime)
    domain = db.Column(db.String(1024))
    toots = db.relationship('Toot', backref='instance', lazy='dynamic')
    accounts = db.relationship('Account', backref='instance', lazy='dynamic')
    lock = db.Column(db.Boolean)
    blacklisted = db.Column(db.Boolean)


class Missed_Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(4095))
    time_misses = db.Column(db.Integer)


class Hashtags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(4095))
    last_seen_id = db.Column(db.Integer)
    instance_id = db.Column(db.Integer, db.ForeignKey('instance.id'))


def save(obj):
    """
    commit change to DB
    """
    db.session.add(obj)
    db.session.commit()


def save_account(instance_name, content):
    """
    record account on DB and return id
    """
    acct = content['username']
    if not Account.query.filter_by(username=acct).count():
        account = Account(mastodon_id=content['id'],
                          username=content['username'],
                          display_name=to_text(content['display_name']),
                          creation_date=datetime.strptime(content['created_at'],
                                                          '%Y-%m-%dT%H:%M:%S.%fZ'),
                          note=to_text(content['note']),
                          url=content['url'],
                          avatar=content['avatar'],
                          instance_id=instance_name,
                          blacklisted=False)
        save(account)
    else:
        account = Account.query.filter_by(username=acct).first()
    return account.id


def add_domain_to_db(domain):
    """
    record instance on DB and return id
    """
    if not Instance.query.filter_by(domain=domain).count():
        instance = Instance(creation_date=datetime.now(),
                            domain=domain,
                            lock=False,
                            blacklisted=False)
        save(instance)
    else:
        instance = Instance.query.filter_by(domain=domain).first()
    return instance.id


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
    ref_id = 0
    next_fetch = instance_url
    local_instance_url = urlparse(instance_url).netloc
    instance_details = Instance.query.filter_by(domain=local_instance_url).first()
    # l'id le plus haut pour l'instance en cours:
    try:
        hastag_detail = Hashtags.query.filter_by(instance_id=instance_details.id).first()
        last_instance_toot_id = hastag_detail.last_seen_id
    except:
        last_instance_toot_id = 0

    while True:
        try:
            local_toots = requests.get(next_fetch,
                                       timeout=120)
        except:
            # something bad happened, store URL to fetch later
            missed_link = Missed_Link(url=next_fetch)
            save(missed_link)

        if local_toots:
            try:
                for toot in local_toots.json():
                    account = toot['account']['acct']
                    instance = urlparse(toot['url']).netloc
                    if not Instance.query.filter_by(domain=instance).first():
                        instance_id = add_domain_to_db(instance)
                    else:
                        instance_id = Instance.query.filter_by(domain=instance).first().id

                    if '@' not in account:
                        # we got local account.
                        # so, genuine toots, not federated ones.
                        # let's grab it by the user!
                        account = account + '@' + instance_url
                        account = save_account(instance_id, toot['account'])

                        existing_toot = Toot.query.filter_by(mastodon_id=toot['id'],
                                                             instance_id=instance_id).first()
                        if not existing_toot:
                            db_toot = Toot(mastodon_id=toot['id'],
                                           creation_date=datetime.strptime(toot['created_at'],
                                                                           '%Y-%m-%dT%H:%M:%S.%fZ'),
                                           sensitive=toot['sensitive'],
                                           account_id=account,
                                           content=to_text(toot['content'], rehtml=True),
                                           instance_id=instance_id,
                                           url=toot['url'],
                                           favourite_count=toot['favourites_count'],
                                           reblog_count=toot['reblogs_count'],
                                           blacklisted=False)
                            save(db_toot)
                next_fetch = local_toots.links['next']['url']
                id_to_fetch = int(next_fetch.split('=')[-1])
                if id_to_fetch > ref_id:
                    ref_id = id_to_fetch

                if last_instance_toot_id > id_to_fetch:
                    break

                time.sleep(1)  # avoid hitting limit rates
            except (KeyError, ):
                # no more dicts, no scraping left
                # oui did it \o/
                break
        else:
            missed_link = Missed_Link(url=next_fetch)
            save(missed_link)
    # houla, cuila y pique!
    tag_name = instance_url.split('?')[0].split('/')[-1]
    # no update for now -> bug!!!!
    hastag_detail = Hashtags.query.filter_by(instance_id=instance_details.id).first()
    try:
        hastag_detail.tag = tag_name
        hastag_detail.last_seen_id = ref_id
        save(hastag_detail)
    except:
        hastag_detail = Hashtags(tag=tag_name,
                                 last_seen_id=ref_id,
                                 instance_id=instance_details.id)
        save(hastag_detail)




db.create_all()

if not Instance.query.filter_by(domain=config['Auth']['instance']).first():
    add_domain_to_db(urlparse(config['Auth']['instance']).netloc)
if __name__ == '__main__':
    to_fetch = list()
    for k in HASHTAGS:
        for i in [x.domain for x in Instance.query.all()]:
            to_fetch.append(API_URL.format(domain=i,
                                           hashtag=k,
                                           since_id=0,
                                           limit=40))
            # get_hashtags(to_fetch)
    with Pool(8) as p:
        result = p.map(get_hashtags, to_fetch)
        # result.get(timeout=360)

    # app.run()
