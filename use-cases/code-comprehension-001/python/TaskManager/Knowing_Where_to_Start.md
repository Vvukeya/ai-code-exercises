# Knowing Where to Start

**Language:** Python  
**Project:** Task Manager

## Introduction

The purpose of this exercise is to practise identifying the correct place to begin when making changes to an unfamiliar codebase.

Instead of immediately changing code, I will first study the structure of the application, identify the responsibilities of the important files, and determine which areas would be affected by new requirements.

## Part 1 — Initial Understanding of the Project Structure

Before using AI, I examined the files in the Python Task Manager project.

My initial understanding is:

- `cli.py` handles commands entered by the user.
- `task_manager.py` coordinates the main application operations.
- `models.py` defines the Task object and related enums such as task status and priority.
- `storage.py` is responsible for storing and retrieving tasks.
- `tests/` contains automated tests for the application.

I believe the general flow of the application is:

User
↓
CLI
↓
Task Manager
↓
Task Models / Storage

My goal is to confirm this structure before deciding where new functionality should be implemented.

### Understanding After Using AI

After using Codex, my initial understanding of the architecture was confirmed.

The project follows a layered structure:

User → `cli.py` → `task_manager.py` → `models.py` / `storage.py` → JSON storage.

`cli.py` is responsible for command-line interaction and argument parsing.

`task_manager.py` acts as the application/service layer and coordinates task operations.

`models.py` contains the domain model, including `Task`, `TaskStatus`, and `TaskPriority`.

`storage.py` handles persistence by loading, saving, updating, and querying tasks.

The tests verify the behaviour of the Task Manager and its interaction with the other components.

This investigation showed me that understanding the responsibility of each layer makes it easier to identify where a new feature should begin.

## Part 2 — Finding Where a CSV Export Feature Should Go

### My Initial Thinking

The new requirement is to allow the user to export tasks to a CSV file.

Before using AI, I think the feature would probably begin in `cli.py` because the user needs a command to request the export.

I think `task_manager.py` may be responsible for coordinating the export because it contains the application's task-related workflows.

The task data itself comes from the existing Task objects defined in `models.py`, while `storage.py` already knows how to retrieve stored tasks.

I am not yet sure whether the CSV-writing logic should be placed directly inside `task_manager.py`, inside `storage.py`, or in a new separate module.

My goal is to determine the best starting point without changing the existing code.

### Understanding After Using AI

After using Codex, I confirmed that the CSV export feature should begin in `cli.py`, where the user would enter an `export` command and provide a filename.

`task_manager.py` should coordinate the export operation because it acts as the service layer.

The existing tasks can be retrieved through `TaskStorage`, and fields such as ID, title, description, priority, status, dates, and tags can then be converted into CSV-compatible values.

The CSV-writing logic could be placed in `task_manager.py` for a small application, but a separate module such as `csv_exporter.py` would provide better separation of responsibilities if the export functionality became larger.

The main files that would likely change are:

- `cli.py`
- `task_manager.py`
- the test files

`models.py` and `storage.py` may not require changes because the required Task data and retrieval functionality already exist.

The planned flow is:

User → `cli.py` → `TaskManager` → `TaskStorage` → Task data → CSV file


## Part 3 — Understanding the Domain Model

### My Initial Understanding

Before using AI, I believe the main domain object is the `Task` class inside `models.py`.

A Task contains information such as its title, description, priority, status, due date, tags, and timestamps.

`TaskPriority` represents the importance of a task, while `TaskStatus` represents the current stage of the task.

I also believe that some task-specific behaviour belongs inside the Task model itself, such as checking whether a task is overdue and marking a task as completed.

My goal is to understand which data and behaviour belong to the domain model and why this matters when deciding where future changes should be implemented.

## Part 3 — Understanding the Domain Model

### My Initial Understanding

Before using AI, I believe the main domain object is the `Task` class inside `models.py`.

A Task contains information such as its title, description, priority, status, due date, tags, and timestamps.

`TaskPriority` represents the importance of a task, while `TaskStatus` represents the current stage of the task.

I also believe that some task-specific behaviour belongs inside the Task model itself, such as checking whether a task is overdue and marking a task as completed.

My goal is to understand which data and behaviour belong to the domain model and why this matters when deciding where future changes should be implemented.

### Understanding After Using AI

After examining the domain model, I understood that `models.py` represents the core business objects of the application.

`TaskPriority` represents the importance of a task, while `TaskStatus` represents its current state.

The `Task` class stores information including the task ID, title, description, priority, status, creation time, update time, due date, completion time, and tags.

The Task model also contains behaviour that belongs to an individual task. For example, `mark_as_done()` changes the task's state and completion information, while `is_overdue()` determines whether the task has passed its due date.

`TaskManager` does not replace the Task model. Instead, it coordinates operations involving tasks and storage.

The relationship can be represented as:

TaskManager  
↓  
Task → TaskPriority / TaskStatus  
↓  
TaskStorage

Understanding the domain model is important because business rules that describe the state or behaviour of an individual Task may require changes to `models.py`, while workflows involving multiple tasks usually belong in `task_manager.py`.

## Part 4 — Planning a New Business Rule

### Requirement

Tasks that are overdue by more than 7 days should automatically be marked as abandoned unless they are high priority.

### My Initial Thinking

This requirement affects the business rules of the application.

I think `models.py` may need to change because the Task status system may need an `ABANDONED` state.

The existing `is_overdue()` behaviour may also be useful when determining how long a task has been overdue.

I think `task_manager.py` should coordinate the automatic checking of tasks because the rule may need to be applied across multiple stored tasks.

`storage.py` would then persist any changed task status.

I am not yet certain when the automatic check should run or exactly which existing methods should be changed.

### Final Implementation Plan

The business rule affects both the domain model and the application workflow.

If `ABANDONED` is not already part of `TaskStatus`, it should be introduced in `models.py`.

The application must examine each task's due date and determine whether it has been overdue for more than seven days.

Before abandoning the task, the application must check its priority. A HIGH priority task should be excluded from automatic abandonment.

`task_manager.py` is the most appropriate place to coordinate this automatic process across multiple tasks, while `models.py` should continue to contain task-specific state and behaviour.

After a Task is changed, `storage.py` can persist the updated state using its existing save/update functionality.

Tests should cover:

- a task overdue by more than seven days;
- a task overdue by less than seven days;
- exactly seven days overdue;
- a HIGH priority overdue task;
- a non-high-priority overdue task;
- a task without a due date;
- persistence of the changed status.

The overall planned flow is:

Stored Tasks  
↓  
Check due date  
↓  
More than 7 days overdue?  
↓  
Check priority  
↓  
HIGH → keep current status  
Not HIGH → mark ABANDONED  
↓  
Save updated Task

## Final Reflection

This exercise showed me that the correct place to begin a change depends on the responsibility of each layer.

Instead of immediately editing code, I can first identify whether a requirement affects user interaction, application workflow, domain behaviour, persistence, or several layers together.

For the CSV feature, the change begins at the CLI and is coordinated by the Task Manager.

For the overdue business rule, the domain model and Task Manager are more important because the requirement changes task state and business behaviour.

Understanding the architecture first makes it easier to make changes without placing logic in the wrong part of the application.