from mongoengine import *
from base import *

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model import *
import unittest

class TestUserModel(BaseTest):

    def setUp(self):
        super(TestUserModel, self).setUp()

    def _create_user(self):
        test_user = User(
                firstname="Donald",
                lastname="Hui",
                gender=User.Gender.MALE,
                email="donaldhui2@gmail.com",
                fb_uid=2).save()
        usi = UserShortInfo(
                uid=test_user.id,
                name=test_user.full_name)
        return test_user, usi

    def test_find_find_all(self):
        _, _ = self._create_user()
        users = User.find({})
        self.assertEqual(len(users), 1)

    def test_set_password(self):
        user, _ = self._create_user()

        try:
            user.set_password_and_save('test')
        except MinPassword, e:
            pass
        try:
            user.set_password_and_save('1234567890')
        except MixPassword, e:
            pass

        self.assertNotEqual(user.password, '123456789a')
        user.validate_password('123456789a')

    def tearDown(self):
        objs = User.find({})
        self.assertTrue(len(objs) > 0)
        for o in objs:
            o.delete()
        objs = User.find({})
        self.assertEqual(len(objs), 0)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUserModel)
    unittest.TextTestRunner(verbosity=2).run(suite)
