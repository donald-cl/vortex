from base_handlers import BaseHandler
from model import *
import tornado.web

class SignupHandler(BaseHandler):

    def get(self):
        self.render('admin.html')

    def post(self):
        email           = self.get_argument('email')
        password        = self.get_argument('password')
        repeat_pass     = self.get_argument('repeat_pass')
        login_method    = self.get_int_argument('login_method', default=0)

        if password != repeat_pass:
            error = "Passwords do not match."
            raise Exception(error)
        if not email or not password:
            error = "You must provide a valid email and password"
            raise Exception(error)

        if self.get_current_user() is None:
            u = User.by_email(email)
            if u and login_method == 0 and u.validate_password(password):
                self.set_current_user(u)
            elif login_method == 0:
                user = User(email = email)
                user.set_password_and_save(password)
                user = str(user.to_dict())
                self.set_current_user(user)

        self.redirect('/feed')

class FeedHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('feed.html')
