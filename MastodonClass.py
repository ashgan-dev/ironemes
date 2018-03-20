#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from mastodon import Mastodon

class MastodonClass:

    def __init__(self, instance, email, password, rootdir):
        self.mastodon = None
        self.instance_url = instance
        self.email = email
        self.password = password
        safeinstance = os.path.basename(instance)
        self.clientcred = os.path.join(
            rootdir,
            'creds/{}_{}_mstdn_clientcred.txt'.format(safeinstance, email))
        self.usercred = os.path.join(
            rootdir,
            'creds/{}_{}_mstdn_usercred.txt'.format(safeinstance, email))
        if not os.path.isdir('creds'):
            os.mkdir(os.path.join(rootdir, 'creds'), 0o700)

    def initialize(self):
        if not os.path.isfile(self.clientcred):
            print("Creating app")
            self.mastodon = Mastodon.create_app(
                'mstdntagslurper',
                to_file = self.clientcred,
                api_base_url=self.instance_url)
            os.chmod(self.clientcred, 0o600)

        # Fetch access token if I didn't already
        if not os.path.isfile(self.usercred):
            print("Logging in")
            self.mastodon = Mastodon(
                client_id = self.clientcred,
                api_base_url=self.instance_url)
            self.mastodon.log_in(self.email, self.password, to_file = self.usercred)
            os.chmod(self.usercred, 0o600)

        self.mastodon = Mastodon(
            client_id = self.clientcred,
            access_token = self.usercred,
            api_base_url=self.instance_url
        )



