class MyRangeIterator:
    def __init__(self, max_range: int):
        if not isinstance(max_range, int):
            raise TypeError(f"Expected int, got {type(max_range).__name__}")
        self.max_range = max_range
        self.cur_i = 0

    def __iter__(self):
        return self

    def __next__(self):
        cur_i = self.cur_i
        self.cur_i += 1
        if cur_i >= self.max_range:
            raise StopIteration
        return cur_i

    def __len__(self):
        return self.max_range

    def __getitem__(self, idx):
        if idx < self.max_range:
            return idx - 1
        raise IndexError("Index out of range")


def MyRangeGenerator(max_range: int):
    if not isinstance(max_range, int):
        raise TypeError(f"Expected int, got {type(max_range).__name__}")
    for i in range(max_range):
        yield i


if __name__ == "__main__":
    range_4 = MyRangeIterator(4)
    for i in range_4:
        print(i)

    print(len(range_4))

    try:
        range_5 = MyRangeIterator("5")
    except TypeError as e:
        print(e)

    r = MyRangeIterator(100)
    print(r[14])
    try:
        print(r[130])
    except IndexError as e:
        print(e)

    # range_4 = MyRangeGenerator(4)
    # for i in range_4:
    #     print(i)

    # print(len(list(range_4)))

    # range_5 = MyRangeGenerator("5")
