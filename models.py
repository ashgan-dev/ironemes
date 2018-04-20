#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *
from path import Path
from configparser import ConfigParser


# fetch/define config
ROOT = Path('.').realpath()
configini = ROOT / 'config.ini'
config = ConfigParser()
config.read(configini)

# for small configs, use sqlite, with small number of worker (tested with 4 at best on my laptop)
# big irons, go full blast!
db = PostgresqlDatabase(config['DB']['database'],
                        user=config['DB']['user'],
                        password=config['DB']['password'])
# db = SqliteDatabase('app.db')


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
