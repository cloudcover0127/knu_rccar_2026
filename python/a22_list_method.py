class Mylist:
    def __init__(self):
        self.myVariable = "jang"
        self.myVariable2 = "un"
        self.mylist = list()

    def append(self,ele):
        self.mylist.append(ele)

def main():
    list_a = [1,2,3]
    list_b = [4,5,6]
    print(list_a + list_b)
    print(list_a)
    list_a.extend(list_b)
    print(list_a)

    list_b.append(7)
    list_b.append(8)
    print(list_b)
    list_b.insert(1,4.5)
    print(list_b)
    myList_a = Mylist()
    myList_a.append("jang un ho")
    print(myList_a.myVariable,myList_a.myVariable2,myList_a.mylist)



if __name__ == "__main__":
    main()