'''
    Author: Donald Hui
    Description: Entry point for the entire Web App. Server is started here.
    Purpose: Main server file - starting point for all http request handling.
    Date started: Jan 13 2015
'''
from tornado.options import define, options
from pymongo.read_preferences import ReadPreference
from handlers import mapping
import mongoengine
import redis
import tornado.ioloop
import tornado.web
import tornado.autoreload
import os

PY_PORT = 9000
MONGO_DB = "vortex"
REPLICA_SET = "rs0"

""" Tornado command-line arguments """
define("port", default=PY_PORT, help="The port the app starts on")
define("redis_host", default="localhost", help="Redis DB host")
define("mongo_host", default="localhost", help="Mongo DB host")
define("replica_set", default=REPLICA_SET, help="Mongo DB replica set")
define("name", default="vortex1", help="Name of the sfeeder instance.")
define("env", default="dev", help="[dev, local, stage, prod]")

def get_db_pref(instance_name):

    preference_map = {
            'vortex1' : ReadPreference.PRIMARY_PREFERRED,
            'vortex2' : ReadPreference.SECONDARY_PREFERRED,
            }

    return preference_map.get(instance_name, ReadPreference.PRIMARY_PREFERRED)

""" Vroom Vroom Start it up """
if __name__ == '__main__':
    tornado.options.parse_command_line()

    """ Standard tornado application intialization """
    settings = dict(
        debug=True,
        autoreload=True,
        login_url="/login",
        cookie_secret="VORTEX",
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        template_path=os.path.join(os.path.dirname(__file__), "static"),
        env=options.env,
        redis_host=options.redis_host,
        port=options.port,
        instance_name=options.name,
    )

    """ Make sure we autoreload templates """
    for (path, dirs, files) in os.walk(settings["template_path"]):
        for item in files:
            tornado.autoreload.watch(os.path.join(path, item))

    """ Instantiate the web server ... """
    application = tornado.web.Application(
            mapping.mappings,
            **settings
            )

    """ Tell the server which port to listen on """
    application.listen(options.port)
    print "Application listening on port : [%d]" % options.port

    try:
        if options.env == 'dev':
            mongoengine.connect(
                    MONGO_DB,
                    host=options.mongo_host,
                    )
        elif options.env == 'prod':
            mongoengine.connect(
                    MONGO_DB,
                    host=options.mongo_host,
                    replicaSet=options.replica_set,
                    read_preference=get_db_pref(options.name),
                    )
    except Exception, e:
        print str(e)
        quit()

    print "Application connected to mongo db: [%s]" % MONGO_DB
    print "Connected to mongo host: [%s]" % options.mongo_host
    print "Environment is [%s]" % options.env
    tornado.ioloop.IOLoop.instance().start()
