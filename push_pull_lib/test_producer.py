import zmq,time
from threading import Thread

MSGS = 2000


class ZMQSender(object):
    def __init__(self, zmq_s:zmq.sugar.socket.Socket) -> None:
        self.zmq_s = zmq_s

    def send(self, data, **kwargs):
        ret = self.zmq_s.send(data,**kwargs,flags=zmq.NOBLOCK)    # 不阻塞的模式，但是如果接收方不存在会报错
        # ret = self.zmq_s.send(data,**kwargs,flags=zmq.DONTWAIT)                   # 阻塞发送，接收方不存在会一直等待接收方上线
        # return ret
    
    def close(self,linger=None):
        return self.zmq_s.close(linger)


def zmq_produce(url):
    """Produce messager"""
    ctx = zmq.Context.instance()
    s = ctx.socket(zmq.PUSH)
    s.connect(url)
    time.sleep(2)            # 等待网络拓扑结构形成
    s = ZMQSender(s)
    return s


def produce(in_url,ident):
    zmq_s = zmq_produce(in_url)
    send = True

    if send:            
        for i in range(int(100)):        # 发送100个消息

            zmq_s.send(f'produce{ident+1} send a {i}'.encode('utf-8'))
            # zmq_s.send(f'produce{ident+1} send a {1}'.encode('utf-8'))
            # zmq_s.send(f'122213produce{ident} send a {i+1}'.encode('utf-8'))
            time.sleep(0.002)
            # print(f'produce{ident} send a {i}')

    zmq_s.close()



if __name__ == '__main__':
    # 注意要点
    PRODUCERS = 1          # 生产者数量,越大，越能测试出性能

    to_url = 'tcp://127.0.0.1:5555'

    producers = [Thread(target=produce, args=(to_url, i)) for i in range(PRODUCERS)]

    for p in producers:
        p.start()

