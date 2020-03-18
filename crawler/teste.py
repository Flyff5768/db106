import multiprocessing as mp
import os


def worker(id,task_queue):
    while True:
        q = task_queue.get()
        print(os.getpid(),id,q)
        task_queue.task_done()



def main():
    # multiprocessing
    # 任務佇列
    task_queue = mp.JoinableQueue()

    for i in range(1000):
        task_queue.put('A')

    # 工作程序1
    worker1 = mp.Process(target=worker, args=(1, task_queue))
    worker1.daemon = True
    worker1.start()

    worker2 = mp.Process(target=worker, args=(2, task_queue))
    worker2.daemon = True
    worker2.start()

    print('wait')
    task_queue.join()  # 確定任務佇列 處理完主程式才離開(主程式結束 任務佇列會繼續
    for i in range(100):
        task_queue.put('B')
    print('exit')
    task_queue.join()  # 確定任務佇列 處理完主程式才離開(主程式結束 任務佇列會繼續
    print('exit')
if __name__ == '__main__' :
    main()


























