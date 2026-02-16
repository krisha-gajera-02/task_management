import unittest
from services.task_service import TaskService


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.service = TaskService()
        self.service.tasks = []
        self.service._save()

    def test_create_task(self):
        task_id = self.service.add_task("Test", "Desc", "low")
        self.assertEqual(task_id, 1)

    def test_update_task(self):
        task_id = self.service.add_task("Test", "Desc", "low")
        self.service.update_task(task_id, title="Updated")
        task = self.service.get_task(task_id)
        self.assertEqual(task["title"], "Updated")

    def test_delete_task(self):
        task_id = self.service.add_task("Test", "Desc", "low")
        self.service.delete_task(task_id)
        self.assertEqual(len(self.service.tasks), 0)

    def test_persistence(self):
        self.service.add_task("Persist", "Check", "medium")
        new_service = TaskService()
        self.assertEqual(len(new_service.tasks), 1)

    def test_invalid_priority(self):
        with self.assertRaises(ValueError):
            self.service.add_task("Bad", "Priority", "urgent")


if __name__ == "__main__":
    unittest.main()
