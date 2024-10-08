def math_k(x, y):
    k = x * y
    return k


def math_delta_y(x, y, delta_y, balance):
    delta_x = (-x * delta_y) / (delta_y + y)
    after_tk0 = x + delta_x
    new_price = after_tk0 / (y + delta_y)
    after_tk1 = balance
    return new_price, after_tk0, after_tk1


def math_delta_x(x, y, delta_x, balance):
    delta_y = (-y * delta_x) / (delta_x + x)
    after_tk1 = y + delta_y
    new_price = after_tk1 / (x + delta_x)
    after_tk0 = balance
    return new_price, after_tk0, after_tk1
