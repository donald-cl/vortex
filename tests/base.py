import mongoengine
import unittest

class BaseTest(unittest.TestCase):

    MONGO_DB = 'test_db'

    def setUp(self):
        mongoengine.connect(self.MONGO_DB, host='localhost')
