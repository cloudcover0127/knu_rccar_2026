def main():
    print(10 == 100)
    print(10 != 100)
    print(100 <= 100)
    print(type(True))

    print(not True)
    print(not False)
    print(True and True)
    print(False or False)

    a = int(input("100보다 큰 숫자를 넣으세요>"))

    if a > 100:
        print("a는 100보다 큽니다.")
    print("프로그램을 종료 합니다.")