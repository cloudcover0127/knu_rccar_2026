def call_10_times(func):
    for _ in range(10):
        func()


def print_hello():
    print("Hello")


def main():
    temp_f = print_hello
    print(type(print_hello))
    call_10_times(temp_f)


if __name__ == "__main__":
    main()