import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import time, proto
from multiprocessing import Process, Value, Queue
from .Com import Com
from .ComWorker import WorkerPool
from .Logging import log
from .Monitor import Monitor

class ComAssistant(Com):
    def __init__(self, decorator):
        super().__init__()
        self.decorator = decorator
        self.procs = []

    def serve(self):
        compose = self.monitor.get_compose()
        host_addr = compose['host']['address']
        assistant = compose['assistant']
        for ass in assistant:
            if ass['address'] == host_addr:
                port = str(ass['port'])
                self.decorator.serve(port)
                break

    def loop(self):
        while True:
            try:
                idle_count = 0
                workers = WorkerPool.getInstance().workers #self.decorator.get_workers()
                for worker in workers:
                    is_working = True if worker.is_working.value > 0 else False

                    # task가 있다면 유휴한 Worker를 실행
                    if not is_working: 
                        is_working = WorkerPool.getInstance().pop_work()
                        
                    # 처리할 task가 없다면 idle_count + 1
                    if not is_working: 
                        idle_count = idle_count + 1

                # if idle_count > 0:
                #     self.monitor.monit_idle_count(idle_count)

                # idle count를 독립적으로 집계하여 업데이트함
                self.decorator.set_idle_count(idle_count)                    

            except Exception as err:
                log.debug(err)
                log.debug("Can't connect remote...")
                time.sleep(1)
                pass    

            time.sleep(3)


def action(task):
    log.debug("Undefined Action")

def run(action):
    compose = Monitor().get_compose()

    mng_addr, mng_port   =  compose['manager']['address'], compose['manager']['port']
    host_addr, host_port =  compose['host']['address'], compose['host']['port']
    
    task_queue = Queue() # Shared Queue

    WorkerPool.getInstance(action).set_task_queue(task_queue)  # Shared Queue 설정

    shared_idle_count = Value('i', 0) # Shared Variable
    earthling = proto.AssistantEarthling(shared_idle_count, WorkerPool.getInstance()) # Shared Variable 설정
    decorator = proto.AssistantEarthlingDecorator(earthling) # Decorate Target 객체 설정
    ass = ComAssistant(decorator) # Decorator 객체 설정

    # Manager Server 연결 확인
    message = str(host_port) if 'int' in str(type(host_port)) else host_port
    # log.debug(mng_addr, mng_port, message)
    try:
        echoed = ass.decorator.echo(mng_addr, mng_port, message)
        log.debug(f"Manager로부터 받은 echo 메시지: {echoed}")
    except Exception as err:
        log.debug(err)
        log.debug("Manager 서버에 연결할 수 없습니다.")

    p = Process(target=ass.loop, args=())
    p.start()

    log.debug(f"Started Assistant Server From {host_addr}:{host_port}")
    ass.serve()


# if __name__ == '__main__':
#     run(action)