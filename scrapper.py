#!/usr/bin/env python
# -*- coding: utf-8 -*-

from path import Path
from configparser import ConfigParser
from models import *
from html2text import HTML2Text
from urllib.parse import urlparse
from datetime import datetime
from multiprocessing.pool import Pool
from models import *

ROOT = Path('.').realpath()
API_URL = 'https://{domain}/api/v1/timelines/tag/{hashtag}?limit={limit}&since_id={since_id}'
HASHTAGS = ['ironème', 'ironèmes', 'ironeme', 'ironemes']

Path.chdir(ROOT)

# fetch/define config
configini = ROOT / 'config.ini'
config = ConfigParser()
config.read(configini)


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
    # current instance URL
    next_fetch = instance_url
    # current instance DB details already on DB
    local_instance_url = urlparse(instance_url).netloc
    instance_details = Instance.get(domain=local_instance_url)

    # hashtags details:
    # houla, cuila y pique!
    tag_name = instance_url.split('?')[0].split('/')[-1]
    # we don't have any id,
    # so let's set it to 0 for the 1st pass
    ref_id = int(instance_url.split('=')[-1])

    # did we have already parsed someting?
    hashtag_detail, _ = Hashtags.get_or_create(instance_id=instance_details.id,
                                               tag=tag_name,
                                               defaults={'last_seen_id': 0})

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

                # next URL to fetch
                next_fetch = local_toots.links['next']['url']
                id_to_fetch = int(next_fetch.split('=')[-1])
                # we want to keep biggest id ever seen on the whole loop
                # so we pass it from loop to loop
                if id_to_fetch > ref_id:
                    ref_id = id_to_fetch

                #
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

    # at last, we update the hashtags id with the biggest one!
    query = Hashtags.update(last_seen_id=ref_id).where((Hashtags.instance_id == instance_details.id) &
                                                       (Hashtags.tag == hashtag_detail.tag))
    query.execute()


if __name__ == '__main__':
    # db.connect()
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
    with Pool(64) as p:
        result = p.map(get_hashtags, to_fetch)
