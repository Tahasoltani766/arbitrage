import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
blockchain_db = client['blockchain']
