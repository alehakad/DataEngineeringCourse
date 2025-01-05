import time


class InifiniteRange:
    def __init__(self):
        self.cur_num = 0

    def __iter__(self):
        return self

    def __next__(self):
        cur_num = self.cur_num
        self.cur_num += 1
        return cur_num


if __name__ == "__main__":
    a = InifiniteRange()
    for i in a:
        print(i)
        time.sleep(0.5)

    # generator of all even numbers with generator expresson
    even_numbers = (i for i in InifiniteRange() if i % 2 == 0)
