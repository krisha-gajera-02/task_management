from datetime import datetime


class Task:
    def __init__(self, task_id, title, description, priority):
        self.id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.status = "pending"
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return self.__dict__
