import datetime

def main():
    now = datetime.datetime.now()

    if 9 < now.hour < 12:
        print(f"현재 시각은 {now.hour}로 오전 입니다.")
    elif now.hour < 9:
        print(f"현재 시각은 {now.hour}로 새벽 입니다.")
    else:
        print(f"현재 시각은 {now.hour}로 오후 입니다.")

    
    print(now.month, type(now.month))
    # 봄,여름,가을,겨울 을 출력하세요
    # 12,1,2,3 -> 겨울
    # 4,5 -> 봄
    # 6,7,8 -> 여름
    # 9,10,11 -> 가을
    if now.month < 3:
        print(f"이번달은 {now.month}로 겨울입니다.")
    elif now.month <= 5:
        print(f"이번달은 {now.month}로 봄입니다.")
    elif now.month <= 8:
        print(f"이번달은 {now.month}로 여름입니다.")
    elif now.month <= 11:
        print(f"이번달은 {now.month}로 가을입니다.")
    else:
        print(f"이번달은 {now.month}로 겨울입니다.")



if __name__ == "__main__":
    main()