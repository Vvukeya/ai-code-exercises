# Code Documentation Challenge

**Language:** Python  
**Selected Algorithm:** Task Priority Sorting  
**Source File:** `task_priority.py`

## Step 1 — Initial Observation Before Using AI

For this exercise I selected the Task Priority Sorting algorithm because I already explored it during the Algorithm Deconstruction Challenge.

The file contains three main functions:

- `calculate_task_score(task)`
- `sort_tasks_by_importance(tasks)`
- `get_top_priority_tasks(tasks, limit=5)`

Before using AI, the parts I think would be most confusing to a developer seeing this code for the first time are:

1. The purpose of the different numerical priority weights.
2. Why the priority weight is multiplied by 10.
3. How due dates affect the final score.
4. Why DONE and REVIEW tasks lose points.
5. Why only certain tags add points.
6. What `key=lambda x: x[0]` means during sorting.
7. Why `reverse=True` is required.
8. How `sorted_tasks[:limit]` selects the final tasks.

The existing functions have short docstrings, but they do not fully explain the parameters, return values, scoring rules, assumptions, or detailed intent of the algorithm.

## Step 3 — Checking the AI Documentation

I compared the AI-generated documentation with the original `task_priority.py` implementation.

The documentation is accurate when it explains that:

- priority provides the starting score;
- due dates add urgency bonuses;
- DONE and REVIEW statuses reduce the score;
- special tags add a bonus;
- recently updated tasks receive an additional bonus;
- tasks are sorted by calculated score from highest to lowest;
- the top-priority function returns only the requested number of tasks.

One important point when checking AI documentation is that the source code does not explicitly raise custom exceptions.

Therefore, the documentation should not claim that specific exceptions are deliberately raised by these functions unless the implementation actually contains a `raise` statement.

Invalid objects or incompatible field values could still cause normal Python runtime errors, but these are assumptions or possible failures rather than explicitly defined behaviour.

This checking step helped me understand that AI-generated documentation must always be compared with the actual implementation before it is accepted.

## Final Reflection

The original code was already functional, but its documentation was minimal.

Prompt 1 helped me document the public behaviour of each function, including its purpose, parameters, return values, assumptions, and possible failure conditions.

Prompt 2 helped me understand what information belongs in inline comments. Instead of commenting obvious Python syntax, useful comments should explain decisions that may not immediately be clear, such as the scoring strategy and the sorting key.

The final documented version combines both approaches: docstrings explain how each function should be used, while inline comments explain the reasoning behind the less obvious algorithmic decisions.

The most important lesson from this exercise is that AI-generated documentation should not be accepted automatically. I need to compare every statement with the implementation, especially claims about errors, edge cases, and behaviour.

Good documentation should make the code easier to understand without changing what the code does.