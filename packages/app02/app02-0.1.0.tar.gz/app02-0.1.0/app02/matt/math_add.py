from .show_num import info_num
def add_num(args):
    info_num(args)
    sum = 0
    for i in args:
        sum += int(i)
    return sum
