# class a():
#     def __init__(self):
#         pass
#
#     def plus(self, *args, **kwargs):
#         list_arg = []
#         for arg in args:
#             list_arg.append(arg)
#         print(list_arg)
#
#
# x = ('sia', 'jdo', 'sia', 'jdo', 'sia', 'hsu')
# for i in x:
#     print(i)


def a(aq, b, *args):
    return aq + b


def f(*args):
    return a(*args)


p = f(1, 2, 3, 4, 5, 6, 7, 8, 9)
print(p)
