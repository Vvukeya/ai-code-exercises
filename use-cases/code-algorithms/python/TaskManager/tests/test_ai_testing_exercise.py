import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from models import Task, TaskPriority
from task_priority import (
    calculate_task_score,
    sort_tasks_by_importance,
    get_top_priority_tasks,
)


class TaskPriorityAITestingExercise(unittest.TestCase):

    def setUp(self):
        self.now = datetime(2026, 8, 17, 12, 0, 0)

    @patch("task_priority.datetime")
    def test_basic_low_priority_score(self, mock_datetime):
        mock_datetime.now.return_value = self.now

        task = Task("Basic Task", priority=TaskPriority.LOW)
        task.updated_at = self.now - timedelta(days=2)

        score = calculate_task_score(task)

        self.assertEqual(score, 10)

    @patch("task_priority.datetime")
    def test_due_in_two_days_adds_expected_bonus(self, mock_datetime):
        mock_datetime.now.return_value = self.now

        task = Task("Due Soon", priority=TaskPriority.MEDIUM)
        task.updated_at = self.now - timedelta(days=2)
        task.due_date = self.now + timedelta(days=2)

        score = calculate_task_score(task)

        self.assertEqual(score, 35)


    @patch("task_priority.datetime")
    def test_current_user_gets_12_point_boost(self, mock_datetime):
        mock_datetime.now.return_value = self.now

        task = Task("Assigned Task", priority=TaskPriority.MEDIUM)
        task.updated_at = self.now - timedelta(days=2)
        task.assigned_to = "current-user"

        mine = calculate_task_score(task, current_user="current-user")
        other = calculate_task_score(task, current_user="other-user")

        self.assertEqual(mine, other + 12)


    @patch("task_priority.datetime")
    def test_future_timestamp_does_not_get_recency_bonus(self, mock_datetime):
        mock_datetime.now.return_value = self.now

        task = Task("Future Update", priority=TaskPriority.LOW)
        task.updated_at = self.now + timedelta(hours=1)

        score = calculate_task_score(task)

        self.assertEqual(score, 10)


    @patch("task_priority.datetime")
    def test_all_priority_functions_work_together(self, mock_datetime):
        mock_datetime.now.return_value = self.now

        urgent = Task("Urgent", priority=TaskPriority.URGENT)
        high = Task("High", priority=TaskPriority.HIGH)
        medium = Task("Medium", priority=TaskPriority.MEDIUM)

        for task in [urgent, high, medium]:
            task.updated_at = self.now - timedelta(days=2)

        tasks = [medium, urgent, high]

        sorted_tasks = sort_tasks_by_importance(tasks)
        top_two = get_top_priority_tasks(tasks, limit=2)

        self.assertEqual(sorted_tasks[0].title, "Urgent")
        self.assertEqual(sorted_tasks[1].title, "High")
        self.assertEqual(top_two[0].title, "Urgent")
        self.assertEqual(top_two[1].title, "High")
        self.assertEqual(len(top_two), 2)


if __name__ == "__main__":
    unittest.main()
