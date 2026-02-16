from models.task import Task
from storage.json_storage import JSONStorage
from utils.logger import logger
from utils.validators import validate_priority, validate_status


class TaskService:
    def __init__(self):
        self.storage = JSONStorage()
        self.tasks = self.storage.load()

    def _save(self):
        self.storage.save(self.tasks)

    def _generate_id(self):
        if not self.tasks:
            return 1
        return max(task["id"] for task in self.tasks) + 1

    def add_task(self, title, description, priority):
        # Normalize priority to lowercase
        priority = priority.lower()

        validate_priority(priority)

        task = Task(
            task_id=self._generate_id(),
            title=title,
            description=description,
            priority=priority
        )

        self.tasks.append(task.to_dict())
        self._save()

        logger.info(f"Task created: {task.id}")
        return task.id

    def list_tasks(self):
        return self.tasks

    def get_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        raise ValueError("Task not found")

    def update_task(self, task_id, **kwargs):
        task = self.get_task(task_id)

        if "priority" in kwargs and kwargs["priority"] is not None:
            kwargs["priority"] = kwargs["priority"].lower()
            validate_priority(kwargs["priority"])

        if "status" in kwargs and kwargs["status"] is not None:
            validate_status(kwargs["status"])

        for key, value in kwargs.items():
            if value is not None:
                task[key] = value

        self._save()
        logger.info(f"Task updated: {task_id}")

    def complete_task(self, task_id):
        self.update_task(task_id, status="completed")

    def delete_task(self, task_id):
        task = self.get_task(task_id)
        self.tasks.remove(task)
        self._save()

        logger.info(f"Task deleted: {task_id}")
