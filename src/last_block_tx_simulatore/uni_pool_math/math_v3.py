import math
from src.last_block_tx_simulatore.uni_pool_math.math_v2 import math_delta_y, math_delta_x
from old.web3_instances import w3
from old.web3_instances import abi_pool_v3

min_tick = -887272
max_tick = 887272

q96 = 2 ** 96
eth = 10 ** 18


def price_to_tick(p):
    return math.floor(math.log(p, 1.0001))


def price_to_sqrtp(p):
    return int(math.sqrt(p) * q96)


def sqrtp_to_price(sqrtp):
    return (sqrtp / q96) ** 2


def tick_to_sqrtp(t):
    return int((1.0001 ** (t / 2)) * q96)


def liquidity0(amount, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return (amount * (pa * pb) / q96) / (pb - pa)


def liquidity1(amount, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return amount * q96 / (pb - pa)


def calc_amount0(liq, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return int(liq * q96 * (pb - pa) / pb / pa)


def calc_amount1(liq, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return int(liq * (pb - pa) / q96)


def get_liq_sqrtp(item, block_num):
    contract = w3.eth.contract(address=item, abi=abi_pool_v3)
    liq = contract.functions.liquidity().call(block_identifier=int(block_num) - 1)
    sqr = contract.functions.slot0().call(block_identifier=int(block_num) - 1)
    sqrtp = sqr[0]
    return sqrtp, liq


def swap_t1_in(liq, sqrtp_cur, amount_in, blnc_bfr_0, blnc_bfr_1):
    price_diff = (amount_in * q96) // liq
    price_next = sqrtp_cur + price_diff
    new_price = (price_next / q96) ** 2
    new_tick = price_to_tick((price_next / q96) ** 2)
    delta_x = calc_amount0(liq, price_next, sqrtp_cur)
    delta_y = calc_amount1(liq, price_next, sqrtp_cur)
    new_price_v3 = sqrtp_to_price(tick_to_sqrtp(new_tick))
    return new_price_v3, int(blnc_bfr_0) + int(delta_x), int(blnc_bfr_1) + int(delta_y)


def swap_t0_in(liq, sqrtp_cur, amount_in, blnc_bfr_1, blnc_bfr_0):
    price_next = int((liq * q96 * sqrtp_cur) // (liq * q96 + amount_in * sqrtp_cur))
    new_price = (price_next / q96) ** 2
    new_tick = price_to_tick((price_next / q96) ** 2)
    calc_amount1(liq, price_next, sqrtp_cur)
    new_price_v3 = sqrtp_to_price(tick_to_sqrtp(new_tick))
    delta_y = calc_amount1(liq, price_next, sqrtp_cur)
    delta_x = calc_amount0(liq, price_next, sqrtp_cur)

    return new_price_v3, int(blnc_bfr_0) + int(delta_x), int(blnc_bfr_1) + int(delta_y)
