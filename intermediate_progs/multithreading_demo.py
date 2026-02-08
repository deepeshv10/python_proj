# multi-threadin example in python


from threading import Thread, Lock
import time

db_value = 0

def increase(lock):
    global db_value
    lock.acquire()
    local_db_value = db_value
    local_db_value += 1
    time.sleep(0.1)
    db_value = local_db_value
    lock.release()

    ## Or use below context manager way as well, 
    ## where we don't need to manage lock acquire & release
    # global db_value
    # with lock:
    #     local_db_value = db_value
    #     local_db_value += 1
    #     time.sleep(0.1)
    #     db_value = local_db_value
    

if __name__ == "__main__":
    print('start value ', db_value)
    lock = Lock()

    t1 = Thread(target=increase, args=(lock,))
    t2 = Thread(target=increase, args=(lock,))
    
    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print('end value ', db_value)
    print('end main')
