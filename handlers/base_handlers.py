'''
    Author: Donald Hui
    Description: Base / Abstract classes for Request Handlers should go here.
'''
from tornado.options import options
import tornado.web
import tornado.websocket
import redis
from fluent import sender
from fluent import event
import random
import time
import os.path

class BaseHandler(tornado.web.RequestHandler):

    CUR_DIR = os.path.dirname(os.path.realpath(__file__))
    ROOT_DIR = "/".join(CUR_DIR.split("/")[:-1])
    debug = True

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get_current_uid(self):
        current_user = self.get_current_user
        return current_user.uid if current_user else None

    def set_current_user(self, user):
        self.set_secure_cookie("user", user)

    def get_int_argument(self, arg_name, default_val=None, strip=True):
        arg_val = self.get_argument(arg_name, default=default_val, strip=strip)
        return int(arg_val) if arg_val else None

    def get_bool_argument(self, arg_name, default_val=None, strip=True):
        arg_val = self.get_argument(arg_name, default=default_val, strip=strip)
        return bool(arg_val) if arg_val else None

    def api_resp(self, code, message=None, data=None):
        data = data if data else None
        messsage = meessage if message else None
        ret = { 'code' : code, 'data' : data, 'message' : message }
        self.set_status(code)
        self.write(ret)

    #==========================================================================#

    def log(self, log_type, data, uid=None):
        data['time'] = data['time'] if data.get('time') else int(time.time())
        log_map = { 'request'   : 'vortex_requests' }
        td_db = log_map[log_type]
        print "[Logged to TD [%s] ] : %s" % (td_db, data)
        sender.setup('td.sbf', host='localhost', port=24224)
        event.Event(td_db, data)

    def success(self, success_msg):
        if self.debug:
            print "[SUCCESS] : %s" % success_msg
        self.set_status(200)
        self.finish(success_msg)

    def failure(self, error_msg):
        if self.debug:
            print "[ERROR] : %s" % error_msg
        self.set_status(400)
        self.finish(error_msg)
