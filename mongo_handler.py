import pymongo

client = pymongo.MongoClient()
blockchain_db = client['blockchain']

trx_collection = blockchain_db['Transactions']
pool_coloction = blockchain_db['FilterPool']


def get_data_pool_mongo():
    list_data = []
    loaded_data = pool_coloction.find({})
    for data in loaded_data:
        list_data.append(data)
    return list_data


get_data_pool_mongo()
