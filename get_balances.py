from mongo_handler import *


def get_data_pool_mongo():
    loaded_data = pool_cooloction.find({})
    for data in loaded_data:
        yield data


def balance_tk0():
    data = get_data_pool_mongo()
    while 1:
        try:
            datum = next(data)
            blnc_tk0 = datum['Balance Token0 before']
            yield blnc_tk0
        except StopIteration:
            break

def balance_tk1():
    data = get_data_pool_mongo()
    while 1:
        try:
            datum = next(data)
            blnc_tk1 = datum['Balance Token1 before']
            print(blnc_tk1)
            yield blnc_tk1
        except StopIteration:
            break
