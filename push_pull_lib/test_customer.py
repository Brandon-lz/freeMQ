
from threading import Thread

import zmq

import zmq,logging


# importeer de modules
from logging import handlers
import logging
from pathlib import Path

logpath = Path('.') / 'logs'

logpath.mkdir(parents = True, exist_ok = True)




# create logger
logger = logging.getLogger('zmq_customer')
logger.setLevel(logging.INFO)

# 如果是根logger设置这个
logger.propagate = False

ch = handlers.TimedRotatingFileHandler(
    str(logpath/'recvmesg.log'), when='midnight', backupCount=180, encoding='utf-8')
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)




def consume(url):
    """Consume messages"""
    ctx = zmq.Context.instance()
    s = ctx.socket(zmq.PULL)
    # s.connect(url)
    s.bind(url)
    print("Consuming")
    # for i in range(MSGS * PRODUCERS):
    msg_count = 0
    while True:
        msg = s.recv()
        msg_count+=1
        if msg.decode()=='_None':
            continue
        logger.info(msg.decode())        # 打开日志
        print(msg.decode())
        print(msg_count)
    print("Consumer done")
    s.close()


def proxy(in_url, out_url):
    ctx = zmq.Context.instance()
    in_s = ctx.socket(zmq.PULL)
    in_s.bind(in_url)
    out_s = ctx.socket(zmq.PUSH)
    # out_s.bind(out_url)
    out_s.connect(out_url)
    try:
        zmq.proxy(in_s, out_s)
    # except zmq.ContextTerminated:
    except KeyboardInterrupt:
        print("proxy terminated")
        in_s.close()
        out_s.close()


if __name__ == '__main__':
    in_url = 'tcp://*:5555'
    to_custom_url = 'tcp://127.0.0.1:5556'
    to_custom_url = "inproc://prox_to_custom"

    
    consumer = Thread(target=consume, args=(to_custom_url,),daemon=True)
    proxy_thread = Thread(target=proxy, args=(in_url, to_custom_url),daemon=True)

    consumer.start()
    proxy_thread.start()


    consumer.join()
    # proxy_thread.join()
    zmq.Context.instance().term()
