# README Documentation Exercise

**Language:** Python  
**Project:** Task Manager

## Step 1 — Project Details and Initial Understanding

The Task Manager is a command-line Python application that allows users to create, view, update, prioritise, complete, and delete tasks.

The project is organised into several main components:

- `cli.py` — command-line interface and user input.
- `task_manager.py` — application/service logic.
- `models.py` — Task, TaskStatus and TaskPriority domain models.
- `storage.py` — JSON persistence and retrieval.
- `tests/` — automated tests.

### Main Features

The application supports:

- Creating tasks
- Listing tasks
- Assigning priorities
- Changing task status
- Setting due dates
- Adding tags
- Finding overdue tasks
- Deleting tasks
- Viewing task statistics

My goal is to produce documentation that allows a new user to understand, install and use the Task Manager without needing to read the source code.

## Documentation Produced

### README

The AI-generated README explains the Task Manager's purpose, main features, project structure, installation process, CLI usage, data storage and troubleshooting.

I checked the generated commands against `cli.py` to make sure the documentation reflects the actual application rather than invented functionality.

### User Guide

For the step-by-step user guide, I selected the task creation feature.

The guide is written for a beginner and explains how to navigate to the project, execute the create command, provide task information and confirm that the task was created successfully.

### FAQ

The FAQ focuses on questions that a new Task Manager user may ask, including priorities, statuses, due dates, tags, persistence, filtering and tests.

## Reflection

This exercise showed me that project documentation serves different purposes.

A README gives an overall introduction to the project.

A user guide focuses on completing one specific task step by step.

An FAQ provides quick answers to common questions and problems.

AI made it faster to create the first drafts, but the important part was checking the generated documentation against the actual source code. Commands and features should not be included simply because they sound reasonable; they must actually exist in the application.