import pymongo

client = pymongo.MongoClient()
blockchain_db = client['blockchain']
