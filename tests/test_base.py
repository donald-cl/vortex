__author__ = 'donaldhui@gmail.com'

from mongoengine import *
from base import *

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model import *
import unittest

class mock_db_object(Document, MongoMixin):
    uid  = IntField()
    name = StringField()

class TestMongoMixin(BaseTest):

    def setUp(self):
        super(TestMongoMixin, self).setUp()
        self.test_obj = mock_db_object(name="test", uid=1)
        self.test_obj.save()

    def test_find_find_all(self):
        objs = self.test_obj.find({})
        self.assertEqual(len(objs), 1)

    def test_find_one(self):
        obj = mock_db_object(name="test2", uid=2).save()
        obj = mock_db_object.find_one({ "uid" : 2, "name" : "test2" })
        self.assertTrue(obj is not None)

    def test_by_id(self):
        obj = mock_db_object(uid=4, name="blah").save()
        obj_id = obj.id
        obj2 = mock_db_object.by_id(obj_id)
        self.assertEqual(obj, obj2)

    def test_by_ids(self):
        obj = mock_db_object(uid=4, name="blah").save()
        obj2 = mock_db_object(uid=5, name="blah").save()
        result = mock_db_object.by_ids([obj.id, obj2.id])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].id, obj.id)
        self.assertEqual(result[0].name, obj.name)
        self.assertEqual(result[1].id, obj2.id)

    def test_get_or_create(self):
        obj = mock_db_object.get_or_create_by_uid(uid=4, name="test3")
        self.assertTrue(obj is not None)
        obj = mock_db_object.find({ "name" : "test3", "uid" :4 })
        self.assertEqual(len(obj), 1)

        # Should not create second time, should find existing.
        obj = mock_db_object.get_or_create_by_uid(uid=4, name="test3")
        obj = mock_db_object.find({ "name" : "test3", "uid" :4 })
        self.assertEqual(len(obj), 1)

    def test_to_dict(self):
        obj = mock_db_object(uid=4, name="blah")
        expected = { "id" : None, "uid" : 4, "name" : "blah"}
        self.assertEqual(expected, obj.to_dict())

    def tearDown(self):
        objs = self.test_obj.find({})
        for o in objs:
            o.delete()
        objs = self.test_obj.find({})
        self.assertEqual(len(objs), 0)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMongoMixin)
    unittest.TextTestRunner(verbosity=2).run(suite)
