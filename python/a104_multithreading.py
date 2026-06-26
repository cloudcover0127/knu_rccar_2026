import threading
import time


def task(name,duration):
    print("쓰레드 시작",name)
    time.sleep(duration)
    print("쓰레드 종료",name,duration)

def main():
    threading.Thread()



if __name__ == "__main__":
    main()
    