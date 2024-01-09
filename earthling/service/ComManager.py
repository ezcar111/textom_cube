
'''
pip3 install grpcio
pip3 install grpcio-tools
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./proto/EarthlingProtocol.proto
# ProtoBuf 생성 후 패키지 경로 조정이 필요함 => EarthlingProtocol_pb2_grpc.py from proto.. 로 수정하기
'''

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import time, json
from earthling.proto.ManagerEarthling import ManagerEarthlingDecorator
from earthling.handler.earthling_dao import *
from multiprocessing import Process
from earthling.service.Com import Com
from earthling.service.Logging import log

class ComManager(Com):

    def __init__(self):
        super().__init__()
        self.decorator = ManagerEarthlingDecorator()

    def serve(self):
        compose = self.monitor.get_compose()['manager']
        port = compose['port']
        self.decorator.serve(port)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        EarthlingProtocol_pb2_grpc.add_EarthlingServicer_to_server(Earthling(), server)
        server.add_insecure_port(f'[::]:{port}')
        server.start()
        server.wait_for_termination()

    def loop(self):
        while True:
            result = select_wait_task()
            # log.debug(result)
            for message in result:
                channel = message['channel']
                task_no = message['idx']
                data_type_names = message['data_type_names']

                assistant = self.monitor.get_compose()['assistant']
                assistant = assistant if assistant is not None else []
                random.shuffle(assistant)
                for ass in assistant:
                    addr, port = ass['address'], ass['port']

                    try:
                        idle_count = self.decorator.getIdleWorkerCount(addr, port)
                        time.sleep(1)  # 트래픽 제한을 위한 딜레이
                    except Exception as err: 
                        # log.debug(err)
                        log.debug(f"Assistant 서버[{addr}:{port}]를 연결할 수 없습니다. (1)")
                        idle_count = 0
                        time.sleep(5)

                    if idle_count > 0:
                        log.debug(f"Request task-{task_no} to Assistant Domain: {addr}:{port}")
                        try:
                            data_exec = 'N'
                            # data_type_names = [ 'web_data', 'news_data', 'facebook_data' ]
                            for data_type_name in data_type_names:
                                # log.debug(message)
                                data_type_key_name = f"{data_type_name}_data"
                                data_exec = message[data_type_key_name]
                                if data_exec == 'Y':
                                    data_desc = { "channel": channel, "data_type_name": data_type_name, "state": data_exec }
                                    update_state_to_start(task_no, data_type_name, channel)
                                    result = self.decorator.notifyTaskToAss(addr, port, task_no, json.dumps(data_desc))
                                    result_message = json.loads(result.message)
                                    is_success = result_message["is_success"]
                                    err_message = result_message["err_message"]

                                    if not is_success:
                                        update_state_to_wait(task_no, data_type_name, channel)
                                    break
                        except Exception as err: 
                            log.debug(err)
                            log.debug(f"Assistant 서버[{addr}:{port}]를 연결할 수 없습니다. (2)")
                            time.sleep(5)

                        break
                    

            time.sleep(5)  # 이 딜레이는 반드시 필요한 딜레이



def run():
    mng = ComManager()
    p = Process(target=mng.loop, args=())
    p.start()

    compose = mng.monitor.get_compose()['manager']
    addr, port = compose['address'], compose['port']
    log.debug(f"Started Manager Server From {addr}:{port}")
    mng.serve()


if __name__ == '__main__':
    run()