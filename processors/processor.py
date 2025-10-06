from event_emitter import EventEmitter

class Processor(EventEmitter):
    def __init__(self):
        super().__init__()