import abc
from models import *


class Observer(metaclass=abc.ABCMeta):
    def __init__(self):
        self._subject = None
        self._observer_state = None

    @abc.abstractmethod
    def update(self, arg):
        pass


class Subject(metaclass=abc.ABCMeta):
    def __init__(self):
        self._observers = set()
        self._subject_state = None

    def attach(self, observer):
        observer._subject = self
        self._observers.add(observer)

    def detach(self, observer):
        observer._subject = None
        self._observers.discard(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._subject_state)
