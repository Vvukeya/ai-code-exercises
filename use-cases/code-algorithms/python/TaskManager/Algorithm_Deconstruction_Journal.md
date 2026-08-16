# Algorithm Deconstruction Challenge

## Selected Algorithm

**Language:** Python  
**Algorithm:** Task Priority Sorting  
**File:** `task_priority.py`

## Step 1 — Initial Understanding Before Using AI

Before using AI, I read through the function names, comments, and general structure of `task_priority.py`.

My initial understanding is that the algorithm tries to decide which tasks are more important by giving each task a numerical score.

I think `calculate_task_score()` calculates the score of an individual task using information such as its priority, due date, status, tags, and when it was last updated.

I think `sort_tasks_by_importance()` calculates the scores for multiple tasks and then sorts the tasks so that the most important task appears first.

I think `get_top_priority_tasks()` uses the sorted list and returns only a limited number of the highest-priority tasks.

At this stage, I understand the general purpose of the algorithm, but I am not yet completely sure how each condition affects the final score or how the sorting works internally.

## Step 2 — Understanding After Using AI

After using Codex, I understood that the algorithm does more than simply use the TaskPriority value.

`calculate_task_score()` creates one numerical importance score by combining several factors.

### Priority Score

The priority weights are:

- LOW = 1
- MEDIUM = 2
- HIGH = 4
- URGENT = 6

The selected weight is multiplied by 10.

This means the starting scores are:

- LOW = 10
- MEDIUM = 20
- HIGH = 40
- URGENT = 60

### Due-Date Adjustment

Tasks become more important when their due dates are close.

The algorithm adds:

- +35 if overdue
- +20 if due today
- +15 if due within two days
- +10 if due within seven days

Tasks due later than seven days do not receive a due-date bonus.

### Status Adjustment

A completed Task receives a penalty of -50.

A Task in REVIEW receives a penalty of -15.

This reduces the likelihood that completed or review Tasks appear above unfinished work.

### Tag Adjustment

If at least one tag is `blocker`, `critical`, or `urgent`, the Task receives +8.

### Recently Updated Adjustment

If the Task was updated less than one day ago, it receives +5.

### Sorting

`sort_tasks_by_importance()` calculates a score for every Task.

It temporarily creates pairs containing:

`(score, task)`

The function then sorts these pairs using the first value, which is the score.

`reverse=True` causes the highest score to appear first.

The function finally removes the score values and returns only the sorted Task objects.

### Selecting the Top Tasks

`get_top_priority_tasks()` first sorts all Tasks and then uses:

`sorted_tasks[:limit]`

This means it returns only the first number of Tasks requested by the limit.

The default limit is five.

## Edge Cases I Identified

After studying the algorithm, I identified several possible edge cases:

1. **Empty Task list**  
   Sorting an empty list returns an empty list.

2. **Tasks with equal scores**  
   Two different Tasks may receive the same importance score. Their relative order depends on the existing ordering and Python's stable sorting behaviour.

3. **Task without a due date**  
   A Task with no due date receives no due-date bonus.

4. **Unknown priority**  
   The priority lookup uses a default score of zero if the Task priority is not present in the priority weight dictionary.

5. **Completed but urgent Task**  
   A completed Task loses 50 points, but other bonuses can still contribute to its final score.

6. **Tags are case-sensitive**  
   A tag such as `Critical` would not match the lowercase string `critical`.

7. **Time-dependent results**  
   The score can change depending on the current date and time because the function uses `datetime.now()`.

8. **Limit larger than the list**  
   If the requested limit is greater than the number of Tasks, slicing simply returns all available Tasks.

   ## Reflection

### How did my understanding change after using AI?

Initially, I understood only that the code calculated a score and sorted Tasks.

After using AI, I understood exactly how each part of a Task contributes to the final score and how all of those values are combined.

I also learned how `sorted()`, a lambda function, tuples, `reverse=True`, and list slicing work together to rank the Tasks.

### How would I explain this algorithm to a classmate?

I would describe it like a points system.

Each Task starts with points based on its priority. The algorithm then adds points when the Task is urgent because of its due date, tags, or recent activity. It removes points when a Task is already done or in review.

Once every Task has a score, the program places the highest-scoring Tasks first.

### What was most challenging?

The most challenging part was understanding that priority is only one factor. A Task's final position depends on several conditions working together.

The AI examples helped me understand how the score changes one step at a time.

### What did I learn from this exercise?

I learned that complex-looking algorithms become easier to understand when I break them into smaller decisions, calculate one example manually, and then follow how the result is used by the next function.
