def gen1():
    yield 1
    yield 2


def gen2():
    yield 3
    yield 4


def comp_generator():
    yield from gen1()
    yield from gen2()


if __name__ == "__main__":
    for i in comp_generator():
        print(i) # 1,2,3,4