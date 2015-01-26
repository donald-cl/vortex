from base_handlers import BaseHandler
import tornado.web

class SignupHandler(BaseHandler):

    def get(self):
        self.write("hello world")

    def post(self):
        email           = self.get_argument('email')
        password        = self.get_argument('password')
        repeat_pass     = self.get_argument('repeat_pass')
        login_method    = self.get_int_argument('login_method', default=0)

        if password != repeat_pass:
            error = "Passwords do not match."
            raise Exception(error)

        u = User.by_email(email)
        if u:
            return
        elif login_method == 0:
            u = User(email = email)
            u = u.set_password_and_save(password)
            self.set_current_user(u)
        elif login_method == 1:
            #TODO: facebook login (grab fb profile pics and stuff here, upoad to s3)
            pass

        self.redirect('/index')
