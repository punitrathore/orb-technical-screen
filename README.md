# Orb Debugging Interview

## Interview Format

1. Intros + discuss the debugging problem (15 minutes)
2. Debug issues in the existing code (40 minutes)
3. Discuss bringing our solution [to production](./PRODUCTION.md) (15 minutes)
   - This document will mainly cover the Debugging portion and we'll talk through the productionizing portion later
4. Wrap-up and time to ask the interviewer questions (5 minutes)

In this interview, your goal is to take an existing codebase (with associated tests) and determine the reason for the test failures.
These test failures may be related to the code or the tests themselves.
To resolve these bugs, you may add, remove, or change code as you see fit, provided the requirements below are still met.

The are _multiple_ bugs, so we may or may not choose to cover all of them during our time.
After working through the bugs, we'll talk about how we can take the problem discussed below to production to support a real product.

Below, we've provided a requirements docs that was used to build the functionality in this exercise.
Unfortunately, our team has failed to build a fully working product; we could use your help fixing our remaining bugs!

### What we're looking for

In order of importance, we’re looking for the following in this interview:

1. During the debugging portion
   - An understanding of the code and ability to debug issues
   - An ability to narrow down affected components and code
2. During the production discussion
   - An ability to talk through SQL database schema design
   - An ability to talk through scaling a SQL database

## Introduction

Imagine you’re building a service called ClassCredits, where you buy credits upfront that you can later use to pay for classes.
You can think of these credits like a “balance” to be used to sign up and pay for classes online like workout classes, cooking classes, and more.

For example, here’s a sequence of actions a user could take:

1. Buy 20 credits (“Credit Block A”) effective at time 1 and expiring at time 60
2. Use 10 credits (“Credit Deduction #1”) for a class at time 10
3. Buy 10 credits (“Credit Block B”) effective on time 20 and expiring at time 90
4. Use 15 credits (“Credit Deduction #2”) for a class at time 25

The above would result in the following credit balances at different times.
Note that this service is tied to a single user, so you don't need to worry about multiple users.

| Time       | Total Credit Balance |
| ---------- | -------------------- |
| _time_: 2  | 20                   |
| _time_: 11 | 10                   |
| _time_: 21 | 20                   |
| _time_: 26 | 5                    |
| _time_: 61 | 5                    |
| _time_: 91 | 0                    |

## Requirements

### Summary

Our implementation must do the following (details expanded upon below):

1. Satisfy the interface below to:
   - Support for adding and deducting credits
   - Support for getting the current credit balance at a given time
2. When deducting credits, ensure we deduct them from the soonest expiring credit block
3. Ensure correct handlings of operations arriving in _any_ order (explained more below)

### Details

For simplicity, we’ll represent all timestamps as seconds since the process started.
You will never see the same timestamp twice when adding or deducting credits, so you don’t need to worry about conflict resolution (e.g. adding and deducting credits at the same time).
In addition, we'll only consider one user, so you don't need to worry about multiple credit balances.

You may assume that deductions will never try to deduct more credits than are available, so there’s no need to perform any input validation.

The interface we want to satisfy is:

- add_credits(amount: int, effective_at: int, expires_at: int)
- deduct_credits(amount: int, effective_at: int)
- get_balance_at(timestamp: int) -> int

In our implementation, we want to deduct from the soonest expiring credit block first.
In our example above, for “Credit Deduction #2,” there were two credit blocks eligible for deduction: “Credit Block A” and “Credit Block B.”
This means the credit deduction first took 10 credits from “Credit Block A” and then 5 from “Credit Block B.”

In addition, note that operations can come in **any** order, so the implementation must account for that. For example, operations could arrive in the following sequence in our system (i.e. in code).

```python
add_credits(amount=5, effective_at=15, expires_at=23) # Credit Block A
deduct_credits(amount=4, effective_at=17)
get_balance_at(timestamp=20) # Returns: 1

# If we add a block in the past with an earlier `expires_at` time, use it instead

add_credits(amount=8, effective_at=3, expires_at=19) # Credit Block B
get_balance_at(timestamp=20) # Returns: 5
```

In this example, the second call to `get_balance_at(timestamp: 20)` should return `5` because the deduction now takes entirely from Credit Block B.
**Please make sure you fully understand this example or ask your interviewer for clarification.**

## Running the first test

While debugging, please remember that you **may add, remove, or change code as you see fit** -- when in doubt, add a print statement!

We'll be walking through tests in a test file that are failing starting from the top of the file to the bottom.
To get start, run the following command:

```terminal
# Go

go test -run TestGetBalance

# Java (Linux or Mac)
./gradlew test --tests 'org.credits.ClassCreditsTest.getBalanceTest'

# Java (Windows)
gradlew.bat test --tests 'org.credits.ClassCreditsTest.getBalanceTest'

# Python

pip3 install -r requirements.txt
pytest test_credits.py -k test_get_balance

# Typescript

npm install
npm test -- credits.test.ts -t "test get balance"
```
