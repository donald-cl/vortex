from mongoengine import *
from base import MongoMixin
from bson import ObjectId
import datetime
import bcrypt

class MinPassword(Exception): pass
class MixPassword(Exception):pass

class UserShortInfo(Document, MongoMixin):

    meta = { 'indexes': ['uid'] }
    uid                 = ObjectIdField(required=True)
    name                = StringField()
    small_pic_url       = StringField()
    med_pic_url         = StringField()
    large_pic_url       = StringField()

class User(Document, MongoMixin):

    meta = { 'indexes': ['email'] }

    MIN_PASSWORD_LENGTH = 10

    class Gender(object):
        MALE        = 0
        FEMALE      = 1
        UNKNOWN     = 2
        UNSPECIFIED = 3

    firstname           = StringField()
    lastname            = StringField()
    gender              = IntField()
    password            = StringField(min_length=MIN_PASSWORD_LENGTH)
    short_info          = ObjectIdField()

    email               = StringField(unique=True, required=True, max_length=50)
    fb_uid              = IntField(unique=True, required=False)
    twtr_uid            = IntField(required=False)
    google_uid          = LongField(required=False)
    associated_emails   = ListField(StringField(), default=[])
    verified            = BooleanField(default=False, required=False)
    associated_verify   = ListField(BooleanField(), default=[])

    @property
    def full_name(self):
        return "%s %s" % (self.firstname, self.lastname)

    # Hash and salt it here.
    def _secure_password(self, password):
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        return hashed

    def set_password_and_save(self, new_password):
        if len(new_password) < self.MIN_PASSWORD_LENGTH:
            emsg = "Your password must be at least %d characters in length" % (
                    self.MIN_PASSWORD_LENGTH)
            raise MinPassword(emsg)

        has_num = False
        has_alpha = False

        for c in new_password:
            if c.isalpha():
                has_alpha = True
            if c.isdigit():
                has_num = True

        if not has_num and not has_alpha:
            emsg = "Your password must contain at least 1 alphabet character "\
                    "and 1 numeric character."
            raise MixPassword(emsg)

        self.password = self._secure_password(new_password)
        self.save()

    def validate_password(self, password):
        return self._secure_password(password) == self.password

    @classmethod
    def by_email(cls, email, fields=None):
        if not fields:
            user = cls.objects(__raw__={'email' : email})
            if user:
                return user[0]
        else:
            user = cls.objects(__raw__={'email' : email}).only(*fields)
            if user:
                return user[0]
