import datetime


def main():
    ptime = datetime.datetime.now()
    list_a = [0,1,2,3,4,5,6]
    list_b = ["a","b","c","d","e","f"]
    del list_a[0]
    del list_b[2]
    print(list_a)
    print(list_b)
    del list_a
    print(list_a)

if __name__ == "__main__":
    main()