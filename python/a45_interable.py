from collections.abc import Iterable

class Simpleiter:
    def __init__(self,start,end):
        self.current = start
        self.end = end

def main():
    iter = Simpleiter(0,10)
    print(isinstance(iter, Iterable))


if __name__ == "__main__":
    main()