# Performance Optimization Challenge

**Language:** Python  
**Scenario:** Slow Data Processing  
**File:** `inventory_analysis.py`

## Step 1 — Initial Performance Analysis

The purpose of this program is to examine a list of products and find pairs whose combined prices are close to a target price.

The function `find_product_combinations()` receives a list of products, a target price and an acceptable price margin.

Before using AI, I think the main performance problem is caused by the nested loops.

The code loops through every product using `i` and then loops through the whole product list again using `j`.

This means that many product combinations are examined repeatedly.

For example, after checking Product A with Product B, the algorithm can later check Product B with Product A.

I also noticed that every time a matching price combination is found, the code uses `any()` to scan the existing results and determine whether the reverse pair already exists.

I think this duplicate-checking process becomes increasingly expensive as the results list becomes larger.

My initial conclusion is that the main bottleneck is the combination of:

- nested loops over the products;
- repeated reversed combinations;
- repeatedly scanning the results list to check for duplicates.

I will use AI to confirm which operations are responsible for the slowdown and investigate better approaches.

## Step 2 — Understanding After Using AI

After analysing the function with AI, I confirmed that the main performance problem is the amount of repeated work performed by the algorithm.

### What the Program Is Supposed to Do

`find_product_combinations()` searches through an inventory and finds pairs of products whose combined prices are within a specified range around a target price.

Matching pairs are stored and finally sorted according to how close their combined price is to the target.

### Primary Bottleneck — Nested Product Loops

The code contains one loop over all products inside another loop over all products.

For each value of `i`, the program goes through the complete product list again using `j`.

The condition:

`if i != j`

prevents a product from being paired with itself.

However, it does not prevent reversed comparisons.

For example, the algorithm may check:

`Product A + Product B`

and later check:

`Product B + Product A`

even though these represent the same product pair.

This creates unnecessary work.

### Secondary Bottleneck — Duplicate Checking

When a matching pair is found, the program checks whether the reversed pair already exists by using:

`any(...)`

over the `results` list.

This means the program may scan many previously discovered results every time another possible match is found.

As the results list grows, this duplicate check becomes more expensive.

Therefore, the program first performs many repeated pair comparisons and then performs additional searches to remove duplication caused by those comparisons.

### Smaller Performance Factors

The progress message that prints every 100 products creates some additional I/O work.

However, it is not the main bottleneck compared with the nested pair comparisons and duplicate-result searching.

### Suggested Improvement 1 — Generate Each Pair Only Once

Instead of comparing every product with every other product in both directions, the algorithm could generate only unique pairs.

Conceptually, after selecting one product, the second loop could begin only with products that come after it.

This would avoid:

- comparing a product with itself;
- checking both `(A, B)` and `(B, A)`;
- needing as much duplicate detection.

This is the easiest and safest improvement because it preserves the idea of comparing product pairs while removing unnecessary work.

### Suggested Improvement 2 — Use Faster Duplicate Tracking

If duplicate tracking is still required, a set or another efficient lookup structure could be used to record combinations that have already been processed.

Checking membership in an appropriate lookup structure is generally more efficient than repeatedly scanning the entire `results` list.

### Suggested Improvement 3 — Use a Better Pair-Finding Algorithm

A more advanced solution could reorganize or sort the product data and search for values that complement each product's price.

This could reduce the need to blindly compare every possible product pair.

However, this approach would be more complex and would need careful testing to ensure that all pairs within the price margin are still found.

## Bottleneck Flow

Product list

↓

Outer loop selects a product

↓

Inner loop examines the entire product list

↓

Many repeated/reversed comparisons

↓

Calculate combined price

↓

Possible match found

↓

Scan existing results using `any(...)`

↓

Results list grows

↓

Duplicate scans become increasingly expensive

↓

Long execution time

## Reflection

Before using AI, I suspected that the nested loops were making the program slow.

After the analysis, I understood that the nested loops are only part of the problem.

The design also creates reversed duplicate comparisons and then compensates for those duplicates by repeatedly scanning the results list.

This means one inefficient design decision creates another expensive operation.

The most useful improvement would be to avoid generating duplicate pairs in the first place.

In my own programs, I will pay more attention to nested loops, repeated searches through growing collections, and situations where the same information is processed multiple times.

I also learned that performance optimization should begin by identifying the bottleneck rather than randomly changing code.