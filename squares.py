def squares():
    yield(x*x for x in range(1, 10))
    print (x*x for x in range(1, 10))


if __name__ == '__main__':
    squares()