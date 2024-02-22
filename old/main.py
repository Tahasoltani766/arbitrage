import asyncio
import filter_transactions as f_tx
import filter_pool as f_pl
from balanceOf import get_pool_address
from uni_pool_math.math_v3 import adr_pool_v3

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(f_tx.main())
    f_pl.main()
    get_pool_address()
    adr_pool_v3()

