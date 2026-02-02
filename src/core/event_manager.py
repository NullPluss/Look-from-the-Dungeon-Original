class EventManager:
    """
    Централизованный менеджер игровых событий.
    """

    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_type, callback):
        """
        Подписка на событие.
        """
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def emit(self, event):
        """
        Отправка события всем подписчикам.
        """
        for callback in self.listeners.get(type(event), []):
            callback(event)