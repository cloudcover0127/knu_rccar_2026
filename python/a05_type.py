def main():
    # 파이썬에서는 변수 선언을 따로 하지않는다.
    int_a = 123
    print(int_a, type(int_a))
    int_a = "123 숫자" # 파이썬은 동적 타이핑이다.
    print(int_a, type(int_a))
    int_a = 3.141592
    print(int_a, type(int_a)) #컨트롤 슬래쉬 하면 주석처리된다.
   
if __name__ == "__main__":
    main()