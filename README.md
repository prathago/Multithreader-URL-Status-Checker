# Multithreaded URL Status Checker

## Objective
Check the availability of multiple URLs concurrently using Python threading, demonstrating Global Interpreter Lock (GIL) and synchronization.

## Features
- Reads URLs from a text file
- Validates URL format using RegEx
- Checks status codes using multithreading
- Uses thread-safe lock to store shared results
- Logs invalid and failed requests
- Displays how work is distributed across threads

## Global Interpreter Lock (GIL)
	•	Python’s GIL ensures only one thread runs Python bytecode at a time, even on multi-core systems.
	•	This limits true parallelism for CPU-bound tasks.
	•	However, for I/O-bound tasks (like HTTP requests), threads can release the GIL while waiting on I/O — making multithreading useful.

## Threading
	•	Threads run concurrently within the same Python process.
	•	Each thread in this project pulls a URL from a shared Queue, makes a request, and logs the result.
	•	Python’s threading.Lock is used to prevent race conditions when writing shared data (like results.csv and logs).

## Requirements
Install dependencies:
```bash
pip install -r requirements.txt