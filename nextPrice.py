from mongo_handler import get_data_pool_mongo
from uni_pool_math.math_v2 import math_delta_y, math_delta_x


def analyze():
    dt = get_data_pool_mongo()
    for item in dt:
        if item['Type Pool'] == 'v2':
            if item['Token'] == item['Token0']:
                delta_tk1 = int(item['Balance Token0 before']) - int(item['Balance'])
                math_delta_y(int(item['Balance Token0 before']), int(item['Balance Token1 before']), delta_tk1,
                             item['_id'])
            elif item['Token'] == item['Token1']:
                delta_tk0 = int(item['Balance Token1 before']) - int(item['Balance'])
                math_delta_x(int(item['Balance Token0 before']), int(item['Balance Token1 before']), delta_tk0,
                             item['_id'])
        elif item['Type Pool'] == 'v3':
            print(item)

analyze()