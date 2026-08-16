# Code Understanding Journal

## Exercise: Codebase Exploration Challenge

**Language selected:** Python

## Part 1 — Initial Project Observation

Before using AI or examining the code in detail, I looked at the project structure and file names.

Based on the file names, I think this is a command-line Task Management application that allows users to create, update, view and store tasks.

My initial understanding of the files is:

* `cli.py` may handle commands entered by the user.
* `task_manager.py` may contain the main task management logic.
* `models.py` may define the structure of a task, including its status and priority.
* `storage.py` may be responsible for saving and retrieving task information.
* `tests/` may contain tests used to check whether the application works correctly.
* `README.md` provides instructions for using the project.

At this stage, I think the application may work like this:

**User → CLI → Task Manager → Models/Storage**

This is only my initial understanding based on the project structure. I have not yet used AI to verify it.

## Part 1 — Understanding Task Creation and Status Updates

### Main Components Involved

After using Codex to trace the feature through the existing code, I found that four main files are involved:

* `cli.py` handles commands and input from the user.
* `task_manager.py` coordinates the task-management operations.
* `models.py` defines the `Task`, `TaskStatus`, and `TaskPriority` objects.
* `storage.py` handles saving, loading, updating, and retrieving tasks.

### Task Creation Flow

Task creation starts when the user runs the `create` command in the CLI.

The basic flow is:

**User → `cli.py` → `TaskManager.create_task()` → `Task` → `TaskStorage.add_task()` → `TaskStorage.save()` → `tasks.json`**

The CLI collects the title, description, priority, due date, and tags.

The tags are split from a comma-separated string into a list before being passed to the Task Manager.

`TaskManager.create_task()` prepares some of the input before creating the Task. The priority number is converted into a `TaskPriority` value, while the due-date string is converted into a Python `datetime` object.

The new `Task` is then created in `models.py`.

During creation, the Task receives:

* A unique UUID as its ID.
* `TaskStatus.TODO` as its initial status.
* A creation timestamp.
* An initial `updated_at` timestamp equal to the creation time.
* `completed_at = None` because the Task has not yet been completed.

The Task is passed to `TaskStorage.add_task()`. The storage class first places the Task into its in-memory dictionary and then calls `save()`.

`save()` serializes the Task objects and writes them to `tasks.json`.

### How Tasks Are Retrieved

When the application starts again, `TaskStorage.load()` reads the tasks from `tasks.json`.

A custom decoder converts the stored JSON values back into Python objects such as:

* `Task`
* `TaskPriority`
* `TaskStatus`
* `datetime`

The Tasks are then stored in memory and can be retrieved by their IDs.

### Task Status Update Flow

Status updates start with the `status` command in `cli.py`.

The basic flow is:

**User → `cli.py` → `TaskManager.update_task_status()` → Task/Storage → `TaskStorage.save()` → `tasks.json`**

The status entered by the user is converted into a `TaskStatus` enum.

I discovered that there are two different paths.

For normal statuses such as `TODO`, `IN_PROGRESS`, and `REVIEW`, the Task Manager uses the storage update operation. The Task's status is changed and its `updated_at` timestamp is updated.

For `DONE`, the application uses special behaviour. It retrieves the Task and calls `Task.mark_as_done()`.

This changes:

* `status` to `TaskStatus.DONE`
* `completed_at` to the current time
* `updated_at` to the same completion time

The updated Task is then saved back to `tasks.json`.

### Design and Separation of Responsibilities

The application separates different responsibilities between its files.

`cli.py` deals mainly with user interaction and does not directly manipulate JSON data.

`TaskManager` acts as a service layer between the CLI, models, and storage.

The `Task` model owns Task-specific state and behaviour, including updating fields and marking a Task as complete.

`TaskStorage` handles persistence, including loading, saving, finding, updating, and deleting Tasks.

The application also uses enums for statuses and priorities so that only known values can be stored.

Custom JSON encoding and decoding is used to translate Python objects such as `TaskStatus`, `TaskPriority`, and `datetime` into values that JSON can store and then recreate them when loading.

### What I Learned

My original guess that the application followed a flow similar to **User → CLI → Task Manager → Models/Storage** was mostly correct.

However, after using AI, I understood the responsibilities of each layer in much more detail. I also discovered that completing a Task is treated differently from a normal status update because completion needs to update the status, completion time, and modification time together.

## Part 2 — Understanding Task Prioritization

### My Initial Understanding

Before using AI, I looked briefly at the priority-related code.

I think the Task Manager has four priority levels:

- LOW = 1
- MEDIUM = 2
- HIGH = 3
- URGENT = 4

My initial understanding is that each task stores one priority value.

I think the priority may affect which tasks are considered more important and possibly the order in which tasks are displayed.

I also think users can filter tasks by priority and change the priority of an existing task.

I am not yet sure whether the application automatically sorts tasks from URGENT to LOW or whether priority is mainly used for storing, filtering, and displaying task information.

 ## Part 2 — Understanding Task Prioritization

### My Initial Understanding

Before using AI, I understood that the Task Manager has four priority levels:

- LOW = 1
- MEDIUM = 2
- HIGH = 3
- URGENT = 4

I understood that every Task stores a priority and that users can select, filter, and update priorities.

However, I initially thought that tasks might automatically be sorted from highest to lowest priority when they are listed.

### Guided Investigation

Instead of asking Codex to explain the whole priority system, I asked it to guide me with one question at a time.

I examined the code myself before answering each question.

I discovered that `TaskPriority` is an Enum defined in `models.py`.

A Task that is created without an explicitly supplied priority defaults to:

`TaskPriority.MEDIUM`

During task creation, the integer received from the CLI is converted into a TaskPriority using:

`TaskPriority(priority_value)`

For example, a value of 3 becomes `TaskPriority.HIGH`.

The converted value is passed into the `Task` constructor and stored using:

`self.priority = priority`

### Filtering Tasks by Priority

The CLI allows the user to supply a priority filter when listing tasks.

The priority is passed into `TaskManager.list_tasks()`, converted into a `TaskPriority`, and then sent to `TaskStorage.get_tasks_by_priority()`.

The storage method examines the Tasks stored in memory and returns Tasks where:

`task.priority == priority`

### Updating Priority

When the user changes the priority of an existing Task, the CLI calls `TaskManager.update_task_priority()`.

The new integer value is converted into a `TaskPriority` and passed to `TaskStorage.update_task()`.

The existing Task is retrieved and its priority is updated through `Task.update()`.

The `updated_at` timestamp is also changed to the current time, and the updated Task is saved.

### Automatic Priority Sorting

My biggest misconception was that Tasks were automatically ordered according to priority.

After examining the listing code, I found that there is no `sorted()` call or other priority-ordering logic.

Therefore, the application does not automatically display URGENT Tasks before HIGH, MEDIUM, or LOW Tasks.

Priority is used for:

- representing importance;
- filtering Tasks;
- updating Task priority;
- storing Task priority.

It is not currently used for automatic ordering.

### Saving and Loading Priority

When a Task is saved to JSON, `TaskEncoder` converts the TaskPriority enum into its numeric value using:

`obj.priority.value`

For example:

`TaskPriority.HIGH` becomes `3`.

When the application loads Tasks again, `TaskDecoder` converts the saved number back into a TaskPriority using:

`TaskPriority(obj['priority'])`

Therefore, a stored value of `3` becomes `TaskPriority.HIGH` again.

### Initial Understanding vs Final Understanding

Initially, I correctly understood the four priority levels and that priority could be selected and changed.

However, I incorrectly assumed that higher-priority Tasks might automatically be displayed first.

The guided questions helped me discover that this implementation stores, filters, updates, and persists priorities, but does not automatically sort Tasks by priority.

This exercise also helped me understand how the same value moves through different representations:

CLI integer → TaskPriority enum → Task object → JSON number → TaskPriority enum

## Part 3 — Mapping Task Completion Data Flow

### Entry Point

Task completion starts when the user uses the `status` command in `cli.py` and supplies `done` as the new status.

The CLI passes the task ID and status to:

`TaskManager.update_task_status()`

### Completion Flow

The data flow is:

User enters status command  
↓  
`cli.py`  
↓  
`TaskManager.update_task_status()`  
↓  
Convert `"done"` to `TaskStatus.DONE`  
↓  
`TaskStorage.get_task(task_id)`  
↓  
`Task.mark_as_done()`  
↓  
Set `status = DONE`  
↓  
Set `completed_at = current time`  
↓  
Set `updated_at = completion time`  
↓  
`TaskStorage.save()`  
↓  
Write changes to `tasks.json`

### State Changes

Before completion:

- The status may be `TODO`, `IN_PROGRESS`, or `REVIEW`.
- `completed_at` is normally `None`.

After completion:

- `status` becomes `TaskStatus.DONE`.
- `completed_at` stores the current date and time.
- `updated_at` is updated to the same completion time.

### Persistence

After `mark_as_done()` changes the Task, `TaskStorage.save()` serializes the Task information and writes the collection to `tasks.json`.

When the application starts again, `TaskStorage.load()` reads the JSON file and `TaskDecoder` reconstructs the stored Task, including its DONE status and timestamps.

### Potential Failure Points

Possible failure points include:

- The Task ID does not exist.
- An invalid status is supplied.
- The JSON file contains invalid or corrupted data.
- The application cannot write to the JSON file.
- Stored date or enum values cannot be reconstructed correctly.

### What I Learned

I initially thought completing a Task would only change its status to DONE.

After tracing the code, I learned that completion has special behaviour. The application also records when the Task was completed, updates its modification timestamp, and then persists all of those changes.

## Part 4 — Final Reflection

### High-Level Architecture

The Python Task Manager is organised into separate layers:

User  
↓  
`cli.py` — handles user commands and input  
↓  
`task_manager.py` — coordinates application logic  
↓  
`models.py` — defines Task, status, priority and Task behaviour  
↓  
`storage.py` — handles saving and retrieving Tasks  
↓  
`tasks.json` — persistent storage

### Task Creation

Task creation starts in the CLI. The information is passed to `TaskManager.create_task()`, which prepares values such as priority and due date.

A `Task` object is created with a unique ID, TODO status and timestamps before `TaskStorage` saves it.

### Task Prioritization

The application uses four priorities:

- LOW
- MEDIUM
- HIGH
- URGENT

Priority can be selected, filtered and updated.

My original misconception was that Tasks were automatically sorted by priority. After examining the code, I discovered that the application does not perform automatic priority sorting.

### Task Completion

When a Task becomes DONE, the application uses `Task.mark_as_done()`.

This updates the status, completion timestamp and modification timestamp before the Task is persisted.

### Interesting Design Approach

The most interesting design approach was the separation of responsibilities.

The CLI does not directly save Tasks, the Task Manager does not directly manipulate JSON, and the Task model contains behaviour related specifically to a Task.

This makes the application easier to understand because each component has a specific responsibility.

### Most Challenging Part

The most challenging part was understanding how information moves between the CLI, TaskManager, Task model and TaskStorage.

The AI prompts helped because I could trace one feature at a time instead of trying to understand the whole project at once.

The guided-question approach was particularly useful because it made me inspect the code myself before receiving confirmation from AI.

### Final Reflection

This exercise taught me that when exploring an unfamiliar codebase, I should first inspect the structure, identify the entry point, trace one feature at a time and follow how data moves between components.

AI is most useful when it helps validate and deepen my understanding rather than replacing the process of reading the code myself.

## Part 4 — 3–5 Minute Presentation

Good day everyone. My presentation is about the Python Task Manager codebase exploration challenge.

The application is a command-line Task Management System. Its main structure is separated into four important files. `cli.py` handles the user commands, `task_manager.py` controls the application logic, `models.py` defines the Task, TaskStatus and TaskPriority, and `storage.py` saves and loads tasks using JSON.

For task creation, the process starts when the user runs the `create` command. The CLI collects the title, description, priority, due date and tags. This information is sent to `TaskManager.create_task()`. The priority number is converted into a `TaskPriority`, the due date is converted into a datetime value, and then a new `Task` object is created. The Task receives a unique ID, TODO status and timestamps. After that, `TaskStorage.add_task()` saves the task to `tasks.json`.

For task prioritization, I discovered that the application has four priority levels: LOW, MEDIUM, HIGH and URGENT. I first thought that tasks were automatically sorted by priority, but after using guided AI questions, I found that this is not true. Priority is used for storing, filtering and updating tasks, but the list is not automatically sorted from urgent to low.

For task completion, the process starts when the user changes a task status to `done`. The CLI sends the task ID and status to `TaskManager.update_task_status()`. The string `done` is converted to `TaskStatus.DONE`. The existing task is retrieved, and `Task.mark_as_done()` is called. This changes the status to DONE, records the completion time and updates the modified time. The changes are then saved back to `tasks.json`.

One interesting design approach I found is separation of responsibilities. The CLI does not directly save data. The Task Manager coordinates the work. The Task model stores task behaviour, and the Storage class handles persistence. This makes the project easier to understand.

The most challenging part was following how data moves between the files. The AI prompts helped me by allowing me to trace one feature at a time. The guided-question prompt was especially useful because it made me inspect the code myself before confirming my understanding.

In conclusion, this exercise taught me how to explore an unfamiliar codebase by first checking the structure, then tracing important features, and finally using AI to validate my understanding instead of depending on it completely.



[Prompt Output](Screenshots)