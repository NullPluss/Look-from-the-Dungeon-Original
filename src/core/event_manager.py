import pygame
from collections import defaultdict

class EventManager:
    def __init__(self):
        self.listeners = defaultdict(list)

    def subscribe(self, event_type, callback):
        if callback not in self.listeners[event_type]:
            self.listeners[event_type].append(callback)

    def unsubscribe(self, event_type, callback):
        if callback in self.listeners[event_type]:
            self.listeners[event_type].remove(callback)

    def emit(self, event_type, **data):
        for callback in self.listeners[event_type]:
            callback(**data)

    def process_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.emit("QUIT")
            elif event.type == pygame.KEYDOWN:
                self.emit("KEYDOWN", event=event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.emit("MOUSE_DOWN", event=event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.emit("MOUSE_UP", event=event)
            elif event.type == pygame.MOUSEMOTION:
                self.emit("MOUSE_MOVE", event=event)
            elif event.type == pygame.MOUSEWHEEL:
                self.emit("MOUSEWHEEL", event=event)