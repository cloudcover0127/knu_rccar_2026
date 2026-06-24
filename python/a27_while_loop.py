def main():
    i = int()
    while i < 10:
        print(f"{i}번째 실행 중...")
        i+=1
    try:
        while True:
            print('.',end="",flush=True)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("키보드 인터럽트!!")
    list_test = list("jang un ho is student")
    print(list_test)
    while "s" in list_test:
        list_test.remove("s")
    print(list_test)
    
if __name__ == "__main__":
    main()