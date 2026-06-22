class A_test:
    def __repr__(self):
        return "A_test 객체이다."


def main():
    print(12345)
    print(123,"jang", "un", "ho")
    print(3.1415)
    a = A_test()
    print(a)

    print("this is", "python", "class!!",sep="-", end="")
    print("this is", "python", "class!!",sep="-")



if __name__ == "__main__":
    main()