#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, send_from_directory
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser
from path import path
# from MastodonClass import MastodonClass as Mstdn
import time
from html2text import HTML2Text
from urllib.parse import urlparse
from datetime import datetime
import requests

ROOT = path('.').realpath()
HASHTAGS = ['ironème', 'ironèmes', 'ironeme', 'ironemes']
BLOCKLIST = ['TrendingBot@mastodon.social', ]
# API management
API_URL = 'https://{domain}/api/v1/timelines/tag/{hashtag}?limit={limit}&since_id={since_id}'

path.chdir(ROOT)

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


def save(obj):
    db.session.add(obj)
    db.session.commit()


def save_account(instance_name, content):
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
    if not Instance.query.filter_by(domain=domain).count():
        instance = Instance(creation_date=datetime.now(),
                            domain=domain,
                            lock=False,
                            blacklisted=False)
        save(instance)
    else:
        instance = Instance.query.filter_by(domain=domain).first()
    return instance.id


db.create_all()

# setup mastodon api
# connection = Mstdn(config['Auth']['instance'],
#                    config['Auth']['usermail'],
#                    config['Auth']['userpass'],
#                    ROOT)
# connection.initialize()
# api = connection.mastodon


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


def get_hashtags(hashtags, instance_url):
    """
    fetches all toots for a given hashtag on given instance
    """
    for hashtag in hashtags:
        next_fetch = API_URL.format(domain=instance_url,
                                    hashtag=hashtag,
                                    since_id=0,
                                    limit=40)
        # l'id le plus haut pour une instance donnee
        # last_instance_id = max([y.mastodon_id for y in Toot.query.filter_by(domain=instance).all()])
        while next_fetch is not None:
            try:
                request_url = next_fetch
                local_toots = requests.get(request_url,
                                           timeout=120)
            except:
                # something bad happened, store URL to fetch later
                missed_link = Missed_Link(url=request_url)
                save(missed_link)

            if local_toots:
                print(local_toots.links)
                try:
                    next_fetch = local_toots.links['next']['url']
                    for toot in local_toots.json():
                        account = toot['account']['acct']
                        instance = urlparse(toot['url']).netloc
                        if not Instance.query.filter_by(domain=instance).first():
                            instance_id = add_domain_to_db(instance)
                        else:
                            instance_id = Instance.query.filter_by(domain=instance).first().id
                        # print(instance_id)

                        if '@' not in account:
                            # we got local account.
                            # so, genuine toots, not federated ones.
                            # let's grab it by the user!
                            account = account + '@' + instance_url
                            account = save_account(instance_id, toot['account'])

                            existing_toot = Toot.query.filter_by(mastodon_id=toot['id'], instance_id=instance_id).first()
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

                    time.sleep(1)  # avoid hitting limit rates
                except (KeyError, ):
                    # no more dicts, no scraping left
                    break


if not Instance.query.filter_by(domain=config['Auth']['instance']).first():
    add_domain_to_db(urlparse(config['Auth']['instance']).netloc)

for i in [x.domain for x in Instance.query.all()]:
    print(i)
    get_hashtags(HASHTAGS, i)

app.run()
