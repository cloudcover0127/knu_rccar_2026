def test():
    print("함수가 호출 되었습니다.")
    yield "re"

def main():
    ge = test()
    print(ge)
    #print(ge.__next__())
    print(next(ge))
    print(next(ge))