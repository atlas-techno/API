import pymongo
from pymongo import MongoClient
#import urllib.parse

#username = urllib.parse.quote_plus('Atlas')

#password = urllib.parse.quote_plus('Atlas@132')

cluster = "mongodb+srv://atlas-techno:Atlas132i@cluster0.wts6q.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(cluster)

db = client["atlas"]

collection = db["db"]

data = {"_id":0}

collection.insert_one(data)
