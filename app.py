#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arrow
from flask import Flask, render_template, request

from models import *


def datetimeformat(value, date_format='DD/MM/YYYY à HH:mm'):
    """
    formating date for templates
    """
    return arrow.get(value).format(date_format)


def datetimeformat2(value, date_format='DD/MM/YYYY'):
    """
    formating date for templates
    """
    return arrow.get(value).format(date_format)


app = Flask(__name__)

app.add_template_filter(datetimeformat)
app.add_template_filter(datetimeformat2)


@app.route('/', methods=['POST', 'GET'])
def start_page():
    """main page"""
    # some needed infos
    instances_names = Instance.select().order_by(Instance.domain.asc())
    selected_toots = Toot.select().join(Account).order_by(Toot.creation_date.desc())

    if request.method == 'POST':
        requested_date = request.form['date']
        requested_instance = int(request.form['instance'])
        if requested_instance != 0:
            requested_instance_name = Instance.get(Instance.id == requested_instance).domain
        else:
            requested_instance_name = 0

        # nice, we can filter more afterward!
        # let's go.
        if requested_date is not '':
            # okay, *THIS* is a joke.
            # no direct date filter/comparaison on a datetime?
            # seriously?!? even MYSQL has a date() damn fonction!!!
            a = arrow.get(requested_date, 'YYYY-MM-DD')
            selected_toots = selected_toots.where((Toot.creation_date.year == a.year),
                                                  (Toot.creation_date.month == a.month),
                                                  (Toot.creation_date.day == a.day))
        if requested_instance is not 0:
            selected_toots = selected_toots.where(Toot.instance_id == requested_instance)

        return render_template('template.tpl',
                               toots=selected_toots,
                               instances_names=instances_names,
                               chosen_instance=requested_instance_name,
                               requested_date=requested_date)
    else:
        return render_template('template.tpl',
                               toots=selected_toots.limit(30),
                               instances_names=instances_names,
                               chosen_instance=0,
                               requested_date='')


@app.route('/search', methods=['POST', 'GET'])
def search():
    """
    search toots content
    """
    if request.method == 'POST':
        searched_text = request.form['search']
        selected_toots = Toot.select().where(Toot.content.contains(searched_text)).join(Account).order_by(Toot.creation_date.desc())
        return render_template('search.tpl',
                               toots=selected_toots)
    else:
        return render_template('search.tpl')


if __name__ == '__main__':
    app.run(debug=True)
