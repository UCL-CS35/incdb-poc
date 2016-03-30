from __future__ import print_function  # Use print() instead of print
from app.models.users import User
from app import db
from app.initializers.create_users import find_or_create_user


def test_user_management(client):

    # allows user to register
    user = find_or_create_user(u'User2', u'Example', u'Mr', u'user2@example.com', 'Password1')
    assert user

    # allows user to reset password 
    new_user = find_or_create_user(u'User2', u'Example', u'Mr', u'user2@example.com', 'Password1')
    new_user.password = u'Password2'
    db.session.commit()
    user = User.query.filter(User.email == u'user2@example.com').first()
    assert user.password == 'Password2'

    # allow user to edit title
    new_user = find_or_create_user(u'User2', u'Example', u'Mr', u'user2@example.com', 'Password1')
    new_user.title = u'Dr'
    db.session.commit()
    user = User.query.filter(User.email == u'user2@example.com').first()
    assert user.title == 'Dr'

    # allow user to edit first_name and last_name
    new_user = find_or_create_user(u'User2', u'Example', u'Mr', u'user2@example.com', 'Password1')
    new_user.first_name = u'Jeremy'
    new_user.last_name = u'Skipper'
    db.session.commit()
    user = User.query.filter(User.email == u'user2@example.com').first()
    assert (user.first_name == 'Jeremy' and user.last_name == 'Skipper')
