from __future__ import print_function  # Use print() instead of print
from flask import url_for


def test_user_managment_url(client):

    # Login as user and visit User Account page
    response = client.post(url_for('user.login'), follow_redirects=True,
                           data=dict(email='jeremy@incdb.com', password='Password1'))
    assert b'<h1>Internet Neurocinematics Database</h1>' in response.data
    response = client.get(url_for('user.user_account'))
    assert b'<h1>Account</h1>' in response.data

    # Edit User Account
    response = client.get(url_for('user.user_account'))
    assert b'<h1>Account</h1>' in response.data
    response = client.post(url_for('user.user_account'), follow_redirects=True,
                           data=dict(first_name='new first name', last_name='User'))
    response = client.get(url_for('user.user_account'))
    assert b'new first name' in response.data

    # Logout
    response = client.get(url_for('user.logout'), follow_redirects=True)
    assert b'<h1>Internet Neurocinematics Database</h1>' in response.data

    # Login as admin and visit Manage INcDb page
    response = client.post(url_for('user.login'), follow_redirects=True,
                           data=dict(email='jeremy@incdb.com', password='Password1'))
    assert b'<h1>Internet Neurocinematics Database</h1>' in response.data
    response = client.get(url_for('admin.index'))
    assert b'<h1>Manage INcDb</h1>' in response.data

    # Logout
    response = client.get(url_for('user.logout'), follow_redirects=True)
    assert b'<h1>Internet Neurocinematics Database</h1>' in response.data
