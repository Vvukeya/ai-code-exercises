# Learning How to Test Code with AI

**Language:** Python
**Project:** Task Manager
**Functions:** `calculate_task_score`, `sort_tasks_by_importance`, `get_top_priority_tasks`

## Part 1 — Initial Behaviour Analysis

The `calculate_task_score()` function calculates a numeric importance score for a task.

Before using AI, I identified these behaviours that should be tested:

1. Different priority levels should produce different base scores.
2. Overdue tasks should receive the correct due-date bonus.
3. Tasks due today should receive the correct bonus.
4. DONE and REVIEW tasks should receive score penalties.
5. Tags such as `blocker`, `critical`, and `urgent` should increase the score.
6. Recently updated tasks should receive a recency bonus.
7. Tasks without a due date should still be scored correctly.
8. Sorting should place tasks with higher calculated scores first.
9. `get_top_priority_tasks()` should respect its limit.
10. Empty task lists should be handled correctly.

I also want the tests to isolate individual scoring rules where possible so that one modifier does not accidentally affect another test.
## Part 2 — Unit Testing

I created a simple LOW-priority test and a due-date test.

The LOW-priority test expects a score of 10.

The due-date test expects a MEDIUM task due within two days to score 35.

I used controlled timestamps so the tests are predictable.

## Part 3 — TDD Current User Feature

The new requirement was for tasks assigned to the current user to receive a +12 score boost.

I first wrote the test before changing the production code.

The test failed because calculate_task_score() did not support current_user.

I then added the smallest required change and ran the same test again.

The test passed.

This demonstrated the RED and GREEN stages of TDD.

## Part 3 — TDD Bug Fix

I tested the recent-update calculation using a future timestamp.

The original condition considered negative days to be less than one and therefore incorrectly awarded the +5 bonus.

I wrote a failing test first.

I then changed the condition so only values between 0 and less than 1 qualify.

The test then passed.

## Part 4 — Integration Test

I tested calculate_task_score(), sort_tasks_by_importance() and get_top_priority_tasks() together.

The test confirmed that the functions produce a consistent ranking and return the correct highest-priority tasks.

## Reflection

Testing showed me that a failing test can be useful because it proves that a missing feature or bug has been detected.

I also learned that time-based tests should use fixed timestamps.

AI helped me think about edge cases and verify my test plan, but I still needed to understand what each test was proving.
