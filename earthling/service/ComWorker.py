import time, threading, yaml, json
from .Com import Com
from .Logging import log
from multiprocessing import Process, Value

class ComWorker(Com):
    
    def __init__(self, worker_no, is_working, action):
        super().__init__()
        self.worker_no = worker_no
        self.is_working = is_working
        self.action = action

    def lock(self):
        self.is_working.value = 1

    def unlock(self):
        self.is_working.value = 0

    def work(self, task):
        
        worker_meta = {
            "no": self.worker_no.value,
            "thread_no": threading.get_native_id(),
            "state": "working",
            "task": task
        }
        date_desc = json.loads(task["message"])
        data_type = date_desc["data_type_name"]

        self.monitor.write_worker(worker_meta)
        log.debug(f"Worker-[{self.worker_no.value}]가 task-[{task['task_no']}]의 '{data_type}'(을)를 시작합니다. (Thread: {threading.get_native_id()})")
        log.debug(f"Worker-[{self.worker_no.value}]가 task-[{task['task_no']}]의 '{data_type}'(을)를 처리중입니다.")

        self.action(task)
        self.is_working.value = 0
        log.debug(f"Worker-[{self.worker_no.value}]가 task-[{task['task_no']}]의 '{data_type}'(을)를 완료하였습니다.")

        worker_meta["state"] = "idle"
        self.monitor.write_worker(worker_meta)
        self.unlock()

        WorkerPool.getInstance().terminate(self.worker_no.value)

class WorkerPool:    
    __instance = None

    def default_action(self, task): 
        log.debug("Default Action으로 처리합니다.")
        time.sleep(10)

    def __init__(self, action=None):
        self.workers = []
        self.proc_map = {}
        self.task_queue = None
        self.work_procs = []
        self.action = self.default_action if action is None else action
        if not WorkerPool.__instance:
            compose = None
            with open(f'earth-compose.yml') as f:
                compose = yaml.load(f, Loader=yaml.FullLoader)
                compose = compose['rpc']
            host_addr = compose['host']['address']

            assistant = compose['assistant']
            for target_ass in assistant:
                if target_ass['address'] == host_addr:
                    target_workers = target_ass['workers']
                    for worker_no in target_workers:
                        worker = ComWorker(Value('i', worker_no), Value('i', 0), self.action)
                        self.workers.append(worker)


    @classmethod
    def getInstance(cls, action=None):
        if not cls.__instance:
            cls.__instance = WorkerPool(action)
        return cls.__instance

    def set_task_queue(self, queue):
        self.task_queue = queue

    def push_task(self, task):
        self.task_queue.put(task) #append(task)
    
    def pop_work(self):
        task_count = self.task_queue.qsize()
        if task_count > 0:
            task = self.task_queue.get() #pop(0)
            self.work(task)
            return True
        
        # 테스트가 필요한 코드: Process Terminate
        for p in self.work_procs:
            p.terminate()
        self.work_procs = []

        return False

    def work(self, task):
        for worker in self.workers:
            if worker.is_working.value == 0:
                worker.lock()
                p = Process(target=worker.work, args=(task, ))
                self.work_procs.append(p) # 테스트가 필요한 코드: Process Save
                p.start()

                self.proc_map[worker.worker_no] = p
                break

    def terminate(self, worker_no):
        if self.proc_map.get(worker_no) is not None:
            p = self.proc_map[worker_no]
            p.terminate()