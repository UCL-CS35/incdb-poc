from datetime import datetime
from app import app, db
from app.core.models import User, Role


def create_users():
    """ Create users when app starts """
    from app.core.models import User, Role, Collection

    # Create all tables
    db.create_all()

    # Adding roles
    admin_role = find_or_create_role('admin', u'Admin')

    # Add users
    jeremy = find_or_create_user(u'Jeremy', u'Skipper', u'Dr', u'jeremy@incdb.com', 'Password1', admin_role)
    ong = find_or_create_user(u'Yong Lin', u'Ong', u'Mr', u'ong@incdb.com', 'Password1')
    johnson = find_or_create_user(u'Johnson', u'Cheung', u'Mr', u'johnson@incdb.com', 'Password1')
    rajind = find_or_create_user(u'Rajind', u'Karunaratne', u'Mr', u'rajind@incdb.com', 'Password1')

    # Save to DB
    db.session.commit()


def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_create_user(first_name, last_name, title, email, password, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    title=title,
                    password=app.user_manager.hash_password(password),
                    active=True,
                    confirmed_at=datetime.utcnow())
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user

    