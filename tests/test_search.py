from __future__ import print_function  # Use print() instead of print
from flask import url_for


def test_search(client):

    # Search Movie (empty database)
    url = url_for('movies.search', movie="Harry Potter")
    response = client.get(url)
    assert b'<h2>We have found 0 movie that matches your search.</h2>' in response.data

    # Search Terms (empty database)
    url = url_for('terms.search', term="emotional")
    response = client.get(url)
    assert b'<h2>We have found 0 term that matches your search.</h2>' in response.data
