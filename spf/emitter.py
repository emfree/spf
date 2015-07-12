import abc
import json
import sys
import time
import requests


class Emitter(object):
    def __init__(self, sampler, client_id=None, interval=60, handlers=None):
        self.sampler = sampler
        # TODO(emfree): better name?
        self.client_id = client_id
        self.interval = interval
        self.handlers = set()
        if handlers is not None:
            self.handlers = set(handlers)

    def add_handler(self, handler):
        self.handlers.add(handler)

    def remove_handler(self, handler):
        self.handlers.remove(handler)

    def publish(self):
        stats = self.sampler.stats()
        self.sampler.reset()
        data = json.dumps({
            'client_id': self.client_id,
            'stats': stats
        })
        for handler in self.handlers:
            handler.publish(data)

    def run(self):
        self.sampler.start()
        while True:
            time.sleep(self.interval)
            self.publish()


class Handler(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def publish(self, data):
        raise NotImplementedError


class StreamHandler(Handler):
    def __init__(self, stream=None):
        self.stream = stream or sys.stderr

    def publish(self, data):
        self.stream.write(data + '\n')


class HTTPHandler(Handler):
    def __init__(self, url, timeout=5):
        self.url = url
        self.timeout = timeout

    def publish(self, data):
        requests.post(self.url, data=data,
                      headers={'Content-Type: application/json'},
                      timeout=self.timeout)


class FileHandler(Handler):
    def __init__(self, filename, mode='a'):
        self.filename = filename
        self.mode = mode

    def publish(self, data):
        with open(self.filename, self.mode) as f:
            f.write(data + '\n')
