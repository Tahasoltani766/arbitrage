uniswap_router2 = '0x7a250d5630b4cf539739df2c5dacb4c659f2488d'.lower()
zerox = '0xdef1c0ded9bec7f1a1670819833240f027b25eff'.lower()
oneinch = '0x1111111254fb6c44bAC0beD2854e76F90643097d'.lower()
sushiswap = '0xd9e1ce17f2641f24ae83637ab66a2cca9c378b9f'.lower()
universal_router = '0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD'.lower()
swap_router02 = '0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45'.lower()
swap_router01 = '0xE592427A0AEce92De3Edee1F18E0157C05861564'.lower()
regex_list = [r'', r'\[31m', r'\[32m', r'\[2;49;39m', r'\[0m', r'\[33', r'\[36m']
combined_regex = '|'.join(regex_list)
list_address_router = [uniswap_router2, zerox, oneinch, sushiswap, universal_router, swap_router02]
combined_pattern = r'^\[\d+\]\s*|' \
                           r'.*::[0-9A-Za-z]*swap[0-9A-Za-z]*.*|├─|\[\d+\]\s*|←|\(\)|└─|│|\[\d+(\.\d+)?e\d+\]| |true|\bm\b'