import logging
import threading
import time
import wxStart
import start

l =123



if __name__ == "__main__":
    # global l
    print("main ", l)
    x = threading.Thread(target=start.oglStart)
    x.start()
    time.sleep(2)
    # y = threading.Thread(target=wxStart.wxStart, daemon=True)
    # y.start()
    print("main 2 ", l)
    time.sleep(20)
    print("main 3 ", l)


