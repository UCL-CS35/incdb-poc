from app import manager
from app import app


@manager.command
def list_routes():
    """ List all routes defined """
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = "{:40s} {:20s} {}".format(rule.endpoint, methods, rule)
        line = urllib.unquote(line)
        output.append(line)

    for line in sorted(output):
        print(line)


@manager.command
def init_db():
    """ Run to setup database """
    from app.initializers.setup_database import setup_database
    setup_database()
