from datetime import datetime

from models import TaskStatus, TaskPriority

def calculate_task_score(task):
    """Calculate and return a task's numerical importance score.

    The score combines the task's priority with adjustments for due-date
    proximity, workflow status, urgency tags, and recent activity. Because the
    calculation uses the current time, the same task can receive a different
    score when evaluated later.

    Args:
        task: A task with ``priority``, ``due_date``, ``status``, ``tags``, and
            ``updated_at`` attributes.

    Returns:
        The task's calculated importance score as an integer.
    """
    priority_weights = {
        TaskPriority.LOW: 1,
        TaskPriority.MEDIUM: 2,
        TaskPriority.HIGH: 4,
        TaskPriority.URGENT: 6
    }

    # Multiplication leaves room for smaller bonuses to adjust each priority band.
    score = priority_weights.get(task.priority, 0) * 10

    # Only the nearest matching due-date band contributes a bonus.
    if task.due_date:
        days_until_due = (task.due_date - datetime.now()).days
        if days_until_due < 0:
            score += 35
        elif days_until_due == 0:
            score += 20
        elif days_until_due <= 2:
            score += 15
        elif days_until_due <= 7:
            score += 10

    # Deprioritize work that is complete or already in review.
    if task.status == TaskStatus.DONE:
        score -= 50
    elif task.status == TaskStatus.REVIEW:
        score -= 15

    # Multiple urgency tags still produce a single bonus.
    if any(tag in ["blocker", "critical", "urgent"] for tag in task.tags):
        score += 8

    # Keep tasks updated within the last day more visible.
    days_since_update = (datetime.now() - task.updated_at).days
    if days_since_update < 1:
        score += 5

    return score

def sort_tasks_by_importance(tasks):
    """Return tasks ordered from highest to lowest importance score.

    Each score is calculated once. Tasks with equal scores retain their input
    order because Python's sort is stable.

    Args:
        tasks: An iterable of tasks accepted by :func:`calculate_task_score`.

    Returns:
        A new list containing the supplied task objects in importance order.
    """
    task_scores = [(calculate_task_score(task), task) for task in tasks]
    # Compare only scores so tied task objects are never compared directly.
    sorted_tasks = [task for _, task in sorted(task_scores, key=lambda x: x[0], reverse=True)]
    return sorted_tasks

def get_top_priority_tasks(tasks, limit=5):
    """Return up to ``limit`` tasks with the highest importance scores.

    Args:
        tasks: An iterable of tasks accepted by :func:`calculate_task_score`.
        limit: Maximum number of sorted tasks to return. Defaults to 5.

    Returns:
        A list containing the leading slice of the importance-ordered tasks.
    """
    sorted_tasks = sort_tasks_by_importance(tasks)
    return sorted_tasks[:limit]
