import atexit
import valkey
from settings import env
import time

r = valkey.from_url(env.REDDIS_URL)
p = None
THREADS = []
# def setValue(key: str, value: str) -> str: 
#     r.set(key, value)

# def getValue(key: str):
#     return r.get(key).decode('utf-8')




def main():
    global p, THREADS
    p = r.pubsub()

    def user_tracking_handler(message):
        data = message['data'].decode('utf-8')
        print(data)

    def tracking_handler(message):
        # get the uid from data and create new thread that watches it
        uid = message['data'].decode('utf-8')
        p.subscribe(**{uid: user_tracking_handler})
        thread = p.run_in_thread(sleep_time=0.01)
        THREADS.append(thread)



    p.subscribe(**{'tracking_tasks': tracking_handler})
    thread = p.run_in_thread(sleep_time=0.01)
    THREADS.append(thread)

    r.publish('tracking_tasks', 'test11')
    r.publish('test11', 'newLocData')


def exit_handler():
    print('Exiting')
    for thread in THREADS:
        thread.stop()
    p.close()
    print('Proccesses stopped')

atexit.register(exit_handler)

if __name__ == "__main__":
    main()
