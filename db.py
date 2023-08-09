from pymongo import MongoClient,DESCENDING
from datetime import datetime
import redis
import json

client=MongoClient("mongodb+srv://test:test@cluster0.ysvwtpx.mongodb.net/")


chat_db=client.get_database("ChatDB")
messages_collection=chat_db.get_collection("messages")

redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

def save_message(room_id,text,sender):
    messages_collection.insert_one({'room_id':room_id,'text':text,'sender':sender,'created_at':datetime.now()})
    redis_client.delete(room_id)


def get_messages(room_id):
    cached_messages = redis_client.get(room_id)
    if cached_messages:
        return json.loads(cached_messages)
    else:
        messages = list(messages_collection.find({'room_id': room_id}).sort('_id', DESCENDING))
        messages = messages[::-1]
        for message in messages:
            message['_id'] = str(message['_id'])
            message['created_at'] = message['created_at'].isoformat()

        redis_client.setex(room_id, 3600, json.dumps(messages))

        return messages