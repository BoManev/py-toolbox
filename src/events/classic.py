import enum
from typing import List, Type
import uuid
from .simple_event_dispatch import Dispatcher, Event


class Issue:
    class InvalidTransition(Exception):
        pass

    class _ETopic(enum.Enum):
        OPENED = "OPENED"
        CLOSED = "CLOSED"
        START_PROGRESS = "START_PROGRESS"
        STOP_PROGRESS = "STOP_PROGRESS"
        RESOLVED = "RESOLVED"
        REOPENED = "REOPENED"

    class State(enum.Enum):
        OPEN = "OPEN"
        RESOLVED = "RESOLVED"
        CLOSED = "CLOSED"
        REOPENED = "REOPENED"
        IN_PROGRESS = "IN_PROGRESS"

    def __init__(self, dispatcher: Type[Dispatcher], events: List[Event] = None) -> None:
        self.dispatcher = dispatcher
        if not events:
            self.state: Issue.State = Issue.State.OPEN
            self.id = uuid.uuid4()
            self.version = 1
            dispatcher.dispatch(Event(Issue._ETopic.OPENED.name, str(id)))
        else:
            self.

    def can_start(self):
        return self.state in [Issue.State.OPEN, Issue.State.REOPENED]

    def start(self):
        if not self.can_start():
            raise Issue.InvalidTransition()
        self.dispatcher.dispatch(Event(Issue._ETopic.START_PROGRESS, self.id))
        self.state = Issue.State.IN_PROGRESS
        self.version += 1

    def can_stop(self):
        return self.state in [Issue.State.IN_PROGRESS]

    def stop(self):
        if not self.can_stop():
            raise Issue.InvalidTransition()
        self.dispatcher.dispatch(Event(Issue._ETopic.STOP_PROGRESS, self.id))
        self.state = Issue.State.OPEN
        self.version += 1

    def can_close(self):
        return self.state in [
            Issue.State.OPEN,
            Issue.State.IN_PROGRESS,
            Issue.State.REOPENED,
            Issue.State.RESOLVED,
        ]

    def close(self):
        if not self.can_close():
            raise Issue.InvalidTransition()
        self.dispatcher.dispatch(Event(Issue._ETopic.CLOSED, self.id))
        self.state = Issue.State.CLOSED
        self.version += 1

    def can_reopen(self):
        return self.state in [Issue.State.CLOSED, Issue.State.RESOLVED]

    def reopen(self):
        if not self.can_reopen():
            raise Issue.InvalidTransition()
        self.dispatcher.dispatch(Event(Issue._ETopic.REOPENED, self.id))
        self.state = Issue.State.REOPENED
        self.version += 1

    def can_resolve(self):
        return self.state in [
            Issue.State.OPEN,
            Issue.State.IN_PROGRESS,
            Issue.State.REOPENED,
        ]

    def resolve(self):
        if not self.can_resolve():
            raise Issue.InvalidTransition()
        self.dispatcher.dispatch(Event(Issue._ETopic.RESOLVED, self.id))
        self.state = Issue.State.RESOLVED
        self.version += 1
        
    
    @classmethod
    def from_events(cls, events: List[Event]):
        isssue = None
        for event in events:
            if event.topic == Issue._ETopic.OPENED:
                isssue = cls(dis)
            elif event_type == IssueProgressStarted:
                issue.start()
            elif event_type == IssueProgressStopped:
                issue.stop()
            elif event_type == IssueReopened:
                issue.reopen()
            elif event_type == IssueResolved:
                issue.resolve()
            elif event_type == IssueClosed:
                issue.close()

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} "
            f"id={self.id!s} "
            f"state={self.state and self.state.name}"
            f">"
        )


if __name__ == "__main__":
    d = Dispatcher()
    for topic in Issue._ETopic:
        d.register(topic, print)
    i = Issue(d)
    i.start()
    i.stop()
    i.resolve()
    i.reopen()
    i.start()
    i.close()
    print(i)
