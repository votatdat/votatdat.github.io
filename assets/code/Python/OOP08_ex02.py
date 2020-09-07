from datetime import datetime


class TimeUTC:
    def __get__(self, instance, owner_class):
        return datetime.utcnow().isoformat()


class Logger:
    current_time = TimeUTC()
