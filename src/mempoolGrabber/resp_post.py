from src.last_block_tx_simulatore.block_transactions import resp_post_rust


def resp_post(data, blck_num):
    resp = resp_post_rust(data, blck_num)
    print('reeesp')
