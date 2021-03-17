import asyncio
import json
import os
import queue
import base64
import sys
import threading


from nats.aio.client import Client as NATS
from nats.aio.errors import NatsError
from iotedgeapplicationlinksdk import _app_name, getLogger, _product_sn, _device_sn, _appInfo

_logger = getLogger()


def exit_handler(signum, frame):
    sys.exit(0)


_msg_cb = None
_msg_rrpc_cb = None

_nat_publish_queue = queue.Queue()


class _natsClientPub(object):
    def __init__(self):
        self.url = os.environ.get(
            'IOTEDGE_NATS_ADDRESS') or 'tcp://127.0.0.1:4222'
        self.nc = NATS()
        self.loop = asyncio.new_event_loop()

    async def _publish(self):
        global _nat_publish_queue
        try:
            await self.nc.connect(servers=[self.url], loop=self.loop)
        except Exception as e1:
            _logger.error(e1)
            sys.exit(1)

        while True:
            try:
                msg = _nat_publish_queue.get()
                bty = json.dumps(msg['payload'])
                await self.nc.publish(subject=msg['subject'],
                                      payload=bty.encode('utf-8'))
                await self.nc.flush()
            except NatsError as e:
                _logger.error(e)
            except Exception as e:
                _logger.error(e)

    def start(self):
        self.loop.run_until_complete(self._publish())
        # self.loop.run_forever()


class _natsClientSub(object):
    def __init__(self):
        self.url = os.environ.get(
            'IOTEDGE_NATS_ADDRESS') or 'tcp://127.0.0.1:4222'
        self.nc = NATS()
        self.loop = asyncio.new_event_loop()

    async def _connect(self):
        try:
            await self.nc.connect(servers=[self.url], loop=self.loop)
        except Exception as e1:
            _logger.error(e1)
            sys.exit(1)

        async def message_handler(msg):
            global _msg_rrpc_cb
            global _msg_cb
            _logger.debug("recv message:{} " .format(str(msg)))
            try:
                js = json.loads(msg.data.decode())
                topic = js['topic']
                data = base64.b64decode(js['payload'])
                if isinstance(topic, str) and topic.startswith("/$system/") and topic.count('/rrpc/request/') > 0:
                    topic = topic.replace("/request/", "/response/", 1)
                    _msg_rrpc_cb(topic, data)
                else:
                    _msg_cb(topic, data)
            except Exception as e:
                _logger.error('handle msg error {}'.format(str(e)))

        await self.nc.subscribe("edge.app."+_app_name, queue=_app_name, cb=message_handler, is_async=True)
        await self.nc.flush()

    def start(self):
        self.loop.run_until_complete(self._connect())
        self.loop.run_forever()


def register_callback(cb, rrpc_cb):
    global _msg_cb
    _msg_cb = cb

    global _msg_rrpc_cb
    _msg_rrpc_cb = rrpc_cb


def get_gateway_product_sn():
    return _product_sn


def get_gateway_device_sn():
    return _device_sn


def get_application_name():
    return _app_name


def get_application_config():
    return _appInfo


def publish(topic: str, msg: bytes):
    global _nat_publish_queue
    payload_encode = base64.b64encode(msg)
    payload = {
        'src': "app",
        'topic': topic,
        "identity": _app_name,
        'payload': str(payload_encode, encoding='utf-8')
    }
    data = {
        'subject': 'edge.router.'+_app_name,
        'payload': payload
    }
    _nat_publish_queue.put(data)


def _start_pub():
    _natsClientPub().start()


def _start_sub():
    _natsClientSub().start()


_t_nats_pub = threading.Thread(target=_start_pub)
_t_nats_pub.setDaemon(True)
_t_nats_pub.start()

_t_nats_sub = threading.Thread(target=_start_sub)
_t_nats_sub.setDaemon(True)
_t_nats_sub.start()
