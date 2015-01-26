from mongoengine import *
from bson.objectid import ObjectId
import datetime

# The interface for common mongodb / redis read/write operations.
class AbstractDAO(object):

    @classmethod
    def get_or_create(cls, _id, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def by_id(cls, _id, fields=None):
        raise NotImplementedError

    @classmethod
    def by_ids(cls, ids, fields=None):
        raise NotImplementedError

    @classmethod
    def by_uid(cls, uid, limit=10):
        raise NotImplementedError

    @classmethod
    def get_latest(cls, hours=1):
        raise NotImplementedError

class MongoMixin(AbstractDAO):

    DFLT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    @classmethod
    def find(cls, query_dict):
        return cls.objects(__raw__=query_dict)

    @classmethod
    def find_one(cls, query_dict):
        objs = cls.find(query_dict)
        return objs[0] if objs and len(objs) > 0 else None

    @classmethod
    def get_or_create_by_uid(cls, uid, *args, **kwargs):
        obj = cls.objects(__raw__={'uid' : uid})
        if obj:
            return obj[0]
        else:
            obj = cls(uid=uid, *args, **kwargs)
            obj.save()
            return obj

    @classmethod
    def by_id(cls, _id, fields=None):
        if type(_id) == str:
            _id = ObjectId(_id)
        if ObjectId.is_valid(_id):
            user = None
            if not fields:
                user = cls.objects(__raw__={'_id' : _id})
            else:
                user = cls.objects(__raw__={'_id' : _id}).only(*fields)
            if user:
                return user[0]

    @classmethod
    def by_ids(cls, ids, fields=None):
        if type(ids) != list:
            error = "by_ids must be passed a list. Got %s instead" % type(ids)
            raise Exception(error)
        ids = [i for i in ids if ObjectId.is_valid(i)]
        ids = [ObjectId(i) for i in ids]
        if not fields:
            users = cls.objects(__raw__={'_id' : { '$in' : ids }})
            return [u for u in users] if users else None
        else:
            users = cls.objects(__raw__={'_id' : { '$in' : ids }}).only(*fields)
            return [u for u in users] if users else None

    @classmethod
    def by_uid(cls, uid, limit=10):
        if type(uid) == str:
            uid = ObjectId(uid)
        if ObjectId.is_valid(uid):
            objs = cls.objects(__raw__={'uid' : uid}).limit(limit)
            objs = [o for o in obs]
            return obs

    @classmethod
    def by_uids(cls, ids, fields=None):
        if type(ids) != list:
            error = "by_ids must be passed a list. Got %s instead" % type(ids)
            raise Exception(error)
        ids = [i for i in ids if ObjectId.is_valid(i)]
        ids = [ObjectId(i) for i in ids]
        if not fields:
            users = cls.objects(__raw__={'uid' : { '$in' : ids }})
            return [u for u in users] if users else None
        else:
            users = cls.objects(__raw__={'uid' : { '$in' : ids }}).only(*fields)
            return [u for u in users] if users else None

    @classmethod
    def get_latest(cls, hours=1):
        now = datetime.datetime.utcnow()
        hour_ago = now - datetime.timedelta(hours=hours)
        start_oid = ObjectId.from_datetime(hour_ago)
        end_oid = ObjectId.from_datetime(now)
        query = {
            '$and' : [
                { '_id' : { '$gte' : start_oid }},
                { '_id' : { '$lte' : end_oid }},
                ]
            }
        results = cls.objects(__raw__ = query)
        return [r for r in results]

    def generation_time(self, time_format=None):
        time_format = self.DFLT_DATE_FORMAT if not time_format else time_format
        return self.id.generation_time.strftime(time_format)

    def to_dict(cls, fields=None):
        if not fields:
            return cls.__dict__.get('_data')
        else:
            default_dict = cls.__dict__.get('_data')
            filtered_dict = {}
            for f in fields:
                if f in default_dict:
                    filtered_dict[f] = default_dict[f]
            return filtered_dict
