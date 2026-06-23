def main():
    print(range(10))
    print(range(0,10,1))
    a = range(10)
    print(list(a))
    print(list(range(5,10,3)))
    a =[]
    for i in range(100):
        a.append(i+1)
    print(a)

    list_b = ["a","b","c","d","e","f"]
    for a,ele in enumerate(list_b):
        print(ele+"원소",a)




if __name__ == "__main__":
    main()