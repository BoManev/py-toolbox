from enum import Enum
from typing import Type


class Event:
    def __init__(self, topic: Type[Enum], data=None) -> None:
        self._topic = topic
        self._data = data

    @property
    def topic(self):
        return self._topic

    @property
    def data(self):
        return self._data

    def __repr__(self) -> str:
        return f"[{self._topic.name} >\n\t{self._data}]"


class Dispatcher:
    def __init__(self) -> None:
        self._events = dict()

    def has_listener(self, topic, listener) -> bool:
        if topic in self._events.keys():
            return listener in self._events[topic]
        return False

    def dispatch(self, event: Event):
        if event.topic in self._events.keys():
            listeners = self._events[event.topic]
            for listener in listeners:
                listener(event)

    def register(self, topic, listener):
        if not self.has_listener(topic, listener):
            listeners = self._events.get(topic, [])
            listeners.append(listener)
            self._events[topic] = listeners

    def remove(self, topic, listener):
        if self.has_listener(topic, listener):
            listeners = self._events.get(topic, [])
            l_count = len(listener)
            if l_count == 1:
                del self._events[topic]
                return
            listeners.remove(listener)
            self._events[topic] = listeners


class DomainEvent(Event):
    CREATED = "CREATED"
    UPDATED = "UPDATED"


class Factory:
    def __init__(self, dispatcher: Type[Dispatcher]) -> None:
        self.dispatcher = dispatcher

    def make(self):
        self.dispatcher.dispatch(Event(DomainEvent.CREATED, "[factory] make"))


class Registry:
    def __init__(self, dispatcher: Type[Dispatcher]) -> None:
        self.dispatcher = dispatcher
        self._registrar = dict()
        dispatcher.register(DomainEvent.CREATED, self.register)

    def register(self, event: Type[Event]):
        events = self._registrar.get(event.topic, [])
        events.append(event.data)
        self._registrar[event.topic] = events
        print(f"[registry] /{event.topic}/\n\t{event.data}")


if __name__ == "__main__":
    d = Dispatcher()
    f = Factory(d)
    r = Registry(d)
    r = Registry(d)

    f.make()
