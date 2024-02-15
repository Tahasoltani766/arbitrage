from mongo_handler import get_data_pool_mongo, pool_coloction


# {'_id': ObjectId('65c9e248f3edcb7796379409'), 'TYPE POOL': 'v2', 'POOL':
# '0x73A86455888902108bC88F5831919e23098b9B04', 'Dex': '0x7a250d5630b4cf539739df2c5dacb4c659f2488d',
# 'Hash': '0x1835a6f1972c6fb6d142443f38f6e6532d856db80d152523cbaeafc0cb2ce6ef', 'token':
# '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'balance': '109971641174899333072', 'blockNumber': '19210990',
# 'Balance Token0 before': '751874628252885451832249', 'Balance Token1 before': '111248495546914444530'}

# def calc():
#     data: list = get_data_pool_mongo()
#     for item in data:
#         if item['Type Pool'] == 'v2':
#             if item['Token'] == item['Token0']:
#                 delta_tk1 = int(item['Balance Token0 before']) - int(item['Balance'])
#                 math_delta_y(int(item['Balance Token0 before']), int(item['Balance Token1 before']), delta_tk1,
#                              item['_id'])
#             elif item['Token'] == item['Token1']:
#                 delta_tk0 = int(item['Balance Token1 before']) - int(item['Balance'])
#                 math_delta_x(int(item['Balance Token0 before']), int(item['Balance Token1 before']), delta_tk0,
# #                              item['_id'])
#         else:
#             break


# def trs_v3(item):
#     return item


def math_k(x, y):
    k = x * y
    return k


def math_delta_y(x, y, delta_y, _id):
    delta_x = (-x * delta_y) / (delta_y + y)
    result = x + delta_x
    p = result / (y + delta_y)
    m_query = {"_id": _id}
    new_q = {'$set': {"After tk0": str(int(result)), "newPrice": str(p)}}
    rename_q = {"$rename": {'Balance': 'After tk1'}}
    try:
        pool_coloction.update_one(m_query, new_q)
        pool_coloction.update_one(m_query, rename_q)
        pool_coloction.update_one(m_query, {'$unset': {'Token': 1}}, False, True)
        print('Updated')
    except KeyError:
        pass

def math_delta_x(x, y, delta_x, _id):
    delta_y = (-y * delta_x) / (delta_x + x)
    result = y + delta_y
    p = result / (x + delta_x)
    m_query = {"_id": _id}
    new_q = {'$set': {"After tk1": str(int(result)), "newPrice": p}}
    rename_q = {"$rename": {'Balance': 'After tk0'}}
    try:
        pool_coloction.update_one(m_query, new_q)
        pool_coloction.update_one(m_query, rename_q)
        # pool_coloction.update_one(m_query, {'$unset': {'Token': 1}}, False, True)
        print('Updated')
    except KeyError:
        pass
#
#
