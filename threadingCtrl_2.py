import threading
import queue
import time

class JobScheduler:
    def __init__(self):
        self.job_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.running = threading.Event()
        self.paused = threading.Event()
        self.stopped = threading.Event()
        self.thread = threading.Thread(target=self._process_jobs)

    def add_job(self, task_name, x, y):
        print(f"[任務加入] {task_name}({x}, {y})")
        self.job_queue.put((task_name, x, y))
        

    def task_add(self, x, y):
        return x + y
    def task_multiply(self, x, y):
        return x * y
    def task_power(self, x, y):
        return x ** y
    
    def start_processing(self):
        self.running.set()
        self.paused.clear()
        self.stopped.clear()
        if not self.thread.is_alive():
            self.thread = threading.Thread(target=self._process_jobs)
            self.thread.start()

    def pause_processing(self):
        self.paused.set()

    def resume_processing(self):
        self.paused.clear()

    def stop_processing(self):
        print("[系統] 停止執行")
        self.stopped.set()
        self.running.clear()
        self.resume_processing()
        self.thread.join()

    def _process_jobs(self):
        while self.running.is_set() and not self.stopped.is_set():
            if self.paused.is_set():
                print("[系統] 執行緒暫停")
                time.sleep(0.1)
                continue
            try:
                task_name, x, y = self.job_queue.get(timeout=0.5)
                print(f"[執行任務] {task_name}({x}, {y})")
                if hasattr(self, task_name):
                    func = getattr(self, task_name)
                    result = func(x, y)
                    print(f"[完成任務] {task_name}({x}, {y}) = {result}")
                    self.result_queue.put((task_name, x, y, result))
                else:
                    print(f"[錯誤] 任務 {task_name} 不存在")
                    self.result_queue.put((task_name, x, y, "Invalid Task"))
            except queue.Empty:
                print("[系統] 所有執行緒已結束")
                continue
        print("[系統] 所有執行緒已結束")

if __name__ == '__main__':
    scheduler = JobScheduler()
    scheduler.start_processing()

    scheduler.add_job("task_multiply", 2, 3)
    scheduler.add_job("task_multiply", 2, 3)
    scheduler.add_job("task_multiply", 2, 3)
    scheduler.add_job("task_multiply", 2, 3)
    scheduler.add_job("task_multiply", 2, 3)
    scheduler.add_job("task_multiply", 2, 3)

    time.sleep(3)
    scheduler.pause_processing()

    time.sleep(5)
    scheduler.resume_processing()

    scheduler.job_queue.join()
    scheduler.stop_processing()