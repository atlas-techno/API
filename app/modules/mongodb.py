import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://atlas-techno:Atlas@132i@cluster0.wts6q.mongodb.net/?retryWrites=true&w=majority")
db = cluster["atlas"]
collection = db["db"]

