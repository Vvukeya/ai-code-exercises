# Error Diagnosis Challenge

**Language:** Python  
**Scenario:** Off-by-One Error  
**File:** `stock_manager.py`

## Step 1 — Initial Error Interpretation

The program is supposed to print every item in an inventory report.

From reading the code, I expect the program to eventually produce an error similar to:

`IndexError: list index out of range`

My initial understanding is that the problem is connected to the loop:

`for i in range(len(items) + 1)`

Python lists use indexes starting from zero.

For example, if a list contains three items, its valid indexes are:

- 0
- 1
- 2
 
However, `range(len(items) + 1)` allows the loop to continue one extra time.

This means the program eventually tries to access an item that does not exist.

At this stage I believe this is an off-by-one error, but I will use AI to confirm exactly how the error develops.

## Step 2 — Error Explanation After Using AI

The error occurs because the program attempts to access a list position that does not exist.

When `main()` runs, it creates three inventory items.

Therefore:

`len(items) = 3`

The valid indexes are:

`0, 1, 2`

However, the loop uses:

`range(len(items) + 1)`

This becomes:

`range(4)`

Therefore the loop produces:

`0, 1, 2, 3`

The first three iterations are valid:

- `items[0]` accesses Laptop.
- `items[1]` accesses Mouse.
- `items[2]` accesses Keyboard.

On the final iteration:

`i = 3`

The program evaluates:

`items[3]`

There is no fourth item in the list, so Python raises:

`IndexError: list index out of range`

## Root Cause

The root cause is not the inventory data itself.

The problem is the loop boundary.

The programmer used the number of elements in the list as though it were also a valid final index.

For a list containing `n` elements, valid indexes range from:

`0` to `n - 1`

The current loop continues to `n`, creating one additional iteration.

This is why the problem is classified as an off-by-one error.

## Chain of Events

`main()`

↓

Creates 3 inventory items

↓

Calls `print_inventory_report(items)`

↓

`len(items)` returns 3

↓

`len(items) + 1` becomes 4

↓

`range(4)` produces 0, 1, 2, 3

↓

Indexes 0, 1 and 2 succeed

↓

Loop reaches index 3

↓

`items[3]` is requested

↓

Index does not exist

↓

`IndexError: list index out of range`

## How the Test Helps Diagnose the Problem

The test `test_print_inventory_report()` provides two test items and calls the function.

The test specifically catches `IndexError` and fails with the message:

`print_inventory_report raised IndexError unexpectedly!`

This confirms that an IndexError is considered incorrect behaviour.

The test expects both inventory items and their quantities to be printed successfully without the function crashing.

## Conceptual Fix

The loop should only iterate across valid list indexes.

The important principle is that if a list contains `n` elements, its final valid index is `n - 1`.

Another safer approach in Python is often to iterate directly over the objects instead of manually managing indexes when an index is not actually required.

For this exercise I did not modify the source code because the goal was to diagnose and understand the error.

## Preventing Similar Errors

To avoid off-by-one errors in future code, I should always distinguish between:

- the number of elements in a collection; and
- the highest valid index.

I should also carefully check the start and end boundaries of `range()` and remember that the stop value is excluded.

## Reflection

Before using AI, I suspected that the `+ 1` in the loop caused the problem.

After tracing the program step by step, I understood exactly why it fails.

The key insight is that a list with three elements does not have an index 3. Its indexes are only 0, 1 and 2.

AI was most useful for tracing the complete chain of events from `main()` to the failing expression instead of simply identifying the incorrect line.

This exercise also showed me that an error message usually identifies the symptom, while root-cause analysis explains the decisions and program state that created that symptom.