# freeMQ

Multiple message publishers and multiple message subscribers,  flexible publish of messages
base zmq

![The topology](src.jpg)

## usage

see example.py

## base PUSH-PULL mode

all of PUSH side's messaes will send to all aviliable PULL sider

test:

```shell
cd push_pull_lib
python test_customer.py
python test_producer.py
```
