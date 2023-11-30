from typing import Callable
import enum


class EventType(enum.Enum):
    PART_CONFIG_UPDATED = 1


__registry: dict[EventType, set[Callable[[any], None]]] = dict()


def subscribe(event_type: EventType, func: Callable[[any], None]) -> None:
    if event_type not in __registry:
        __registry[event_type] = set()
    __registry[event_type].add(func)


def unsubscribe(event_type: EventType, func: Callable[[any], None]) -> None:
    if event_type in __registry:
        __registry[event_type].remove(func)


def send(event_type: EventType, payload: any = None) -> None:
    if event_type in __registry:
        for subscriber in __registry[event_type]:
            subscriber(payload)
