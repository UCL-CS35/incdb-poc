from __future__ import print_function  # Use print() instead of print
from flask import url_for


def test_pages_url(client):

    # Visit home page
    response = client.get(url_for('home.index'))
    assert b'<h1>Internet Neurocinematics Database</h1>' in response.data

    # Visit guide page
    response = client.get(url_for('home.guide'))
    assert b'<h2>What is INcDb?</h2>' in response.data

    # Visit faq page
    response = client.get(url_for('home.faq'))
    assert b'<h1>Frequently Asked Questions</h1>' in response.data

    # Visit movies page
    response = client.get(url_for('movies.index'))
    assert b'<h2>Movies</h2>' in response.data

    # Visit terms page
    response = client.get(url_for('terms.index'))
    assert b'<h2>Terms</h2>' in response.data
