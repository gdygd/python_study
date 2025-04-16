import threading
import time
import logging
from enum import IntEnum

# 상태 코드
RST_OK = 0
RST_ABNORMAL = 1
RST_STOPPED = 2

THR_START_ID = 1
THR_MAX_ID = 10000
DEF_THR_CHECK_INTERVAL = 1.0  # 초 단위

thr_id_pool = []
thr_id_lock = threading.Lock()

def get_thread_id():
    with thr_id_lock:
        existing = sorted(thr_id_pool)
        if not existing:
            thr_id_pool.append(THR_START_ID)
            return THR_START_ID
        
        for idx in range(1, len(existing)):
            prev_id, curr_id = existing[idx-1], existing[idx]
            if curr_id - prev_id > 1:
                new_id = prev_id+1
                thr_id_pool.append(new_id)
                return new_id
            
        new_id = existing-[-1] + 1
        if new_id <= THR_MAX_ID:
            thr_id_pool.append(new_id)
            return new_id
        else:
            raise RuntimeError("Max thread ID exceeded")

class StateCode(IntEnum):
    OK = 1
    UNEXIST = 2
    ABNORMAL = 3

class ThreadWrapper:
    def __init__(self):
        self.id = get_thread_id()
        self.interval = 0
        self.args = (None, None, None)
        self.kill_event = threading.Event()
        self.thread = None
        self.active = False
        self.last_check = time.time()
        self.start_func = None

    def init(self, start_func, interval_ms, *args):
        self.interval = interval_ms / 1000.0
        self.args = args[:3] + (None,) * (3 - len(args))
        self.start_func = start_func

    def start(self):
        if self.start_func is None:
            raise RuntimeError("Thread function not set")
        self.active = True
        self.thread = threading.Thread(target=self._run_thread, args=self.args)
        self.thread.start()

    def _run_thread(self, *args):
        try:
            self.start_func(self, self.kill_event, *args)
        except Exception as e:
            logging.exception("Thread crashed")

    def kill(self):
        self.active = False
        self.kill_event.set()

    def is_running(self):
        now = time.time()
        if now-self.last_check < DEF_THR_CHECK_INTERVAL:
            return True
        self.last_check = now
        return self.thread and self.thread.is_alive()

    def thread_register(self, tid):
        logging.info(f"Thread registered : {tid}")

    def thread_deregister(self, tid):
        logging.info(f"Thread deregistered : {tid}")

def my_thread_func(thread, kill_event, arg1, arg2, arg3):
    print(f"[Thread-{thread.id}] Started with args: {arg1}, {arg2}, {arg3}")
    while not kill_event.is_set():
        print(f"[Thread-{thread.id}] Running...")
        time.sleep(thread.interval)
    print(f"[Thread-{thread.id}] Stopped.")

t = ThreadWrapper()
t.init(my_thread_func, 1000, "hello", 123, True)
t.start()

# 5초 후 종료
time.sleep(5)
t.kill()