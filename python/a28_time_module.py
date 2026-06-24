import time


def main():
    print(time.asctime())
    print(time.time())
    print(time.clock_gettime_ns(1))

    ptime = time.time()
    cnt = int()
    while time.time() < ptime + 5:
        cnt +=1
    print(f"5초 동안 {cnt:,d}번 반복했습니다.")


if __name__ == "__main__":
    main()