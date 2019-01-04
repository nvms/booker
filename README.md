# Booker
Tested on Python 2.7, 3.5, 3.6 and 3.7.

Cron-esque, in-script task scheduler with an incredibly easy to use
English syntax. Booker can make calls (tasks) with specific intervals,
start times and end times.

```python
booker.do(mycallable, 'every 7 days at 12:00 until 01-30-2020')
```

## Table of contents

* [Basic usage](#basic-usage)
* [Using the function decorator](#using-the-function-decorator)
   * [Tasks that do not repeat](#tasks-that-do-not-repeat)
      * [Starting immediately](#starting-immediately)
      * [Starting at a specific time](#starting-at-a-specific-time)
      * [Starting in 5 minutes](#starting-in-5-minutes)
      * [Combining at and in](#combining-at-and-in)
   * [Tasks that repeat with the every keyword](#tasks-that-repeat-with-the-every-keyword)
      * [Starting now](#starting-now)
      * [Starting at a specific time](#starting-at-a-specific-time-1)
      * [Starting in a while](#starting-in-a-while)
      * [Combining every with at and in.](#combining-every-with-at-and-in)
      * [Running until a specific date and time](#running-until-a-specific-date-and-time)
* [Using the do() method](#using-the-do-method)
* [Task labels](#task-labels)
   * [Assigning labels with the decorator](#assigning-labels-with-the-decorator)
   * [Assigning labels using do()](#assigning-labels-using-do)
* [Cancelling tasks](#cancelling-tasks)
   * [All](#all)
   * [By label](#by-label)
* [Why?](#why)
* [Q&amp;A](#qa)


## Tests

Please inspect and run tests.py yourself. All tests are passing. You
will need the (awesome) [freezegun](https://github.com/spulec/freezegun) library
to run the tests.

## Why?
There are other job scheduling libraries out there that work well,
such as [schedule](https://github.com/dbader/schedule) or the 
more feature-packed [APScheduler](https://github.com/agronholm/apscheduler).
However, as far as I know, there are none that employ the English language
as the syntax for constructing schedules. Maybe there's a good reason
for that. ¯\\\_(ツ)_/¯

__Again, why!__
1. It's cool.
2. Forgetting how to use it is nearly impossible.
3. More reasons.

## Basic usage
```bash
$ pip install booker
```
The keywords `every`, `in`, `at` and `until` are explained below. They
work how you might expect them to work.
```python
import booker
import time

def myfunc():
    print('Task has been run')

# Runs daily at noon until a long, long time from now.
booker.do(myfunc, 'every 1 day at 12:00 until 01-30-2030 12:00')

# Runs at 2PM. If the current time is past 2PM, it will run tomorrow at 2PM.
booker.do(myfunc, 'at 14:00')

# Runs every 15 minutes, starting an hour from now, indefinitely.
booker.do(myfunc, 'every 15 minutes in 1 hour')

try:
    while True:
        time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)
```
## Using the function decorator
### Tasks that do not repeat
#### Starting immediately
This is identical to just calling the method yourself.
```python
@booker.task()
def myfunc():
    print('Hello')
```
#### Starting `at` a specific time
Use the `at` keyword for this. This keyword expects time to be in 24 hour format (HH:MM). Seconds are not given.
```python
@booker.task('at 14:00')
def myfunc():
    print('It is 2PM.')
```
#### Starting `in` 5 minutes
Use the `in` keyword for this. The task below runs 3 days and 5 minutes from now.
```python
@booker.task('in 3 days 5 minutes')
def myfunc():
    print('Hello')
```
#### Combining `at` and `in`
You can combine `at` and `in` to define a task that, `at` a specific time,
will do something `in` a certain amount of time. It does not matter what
order you put these phrases in.
```python
@booker.task('in 30 minutes at 12:00')
def myfunc():
    print('It is 12:30')
```
### Tasks that repeat with the `every` keyword
When you use the `every` keyword, booker looks for additional keywords,
prefixed by a number. Those keywords are `day[s]`, `hour[s]` or `hr[s]`,
`minute[s]`, and `second[s]` and they should be following a number, e.g.:

`7 days, 1 hour, 30 minutes, 1 second`

The commas in the syntax above aren't necessary, but you can throw them
in there. They have no effect.
#### Starting now
Like the commas above, the `and` below is not required, but you can add
it for readability. Booker will ignore what it does not understand.
```python
@booker.task('every 3 days and 12 hours')
@booker.task('every 15 minutes 15 seconds')
```
#### Starting `at` a specific time
You can combine `every` with `at`.
```python
@booker.task('every 12 hours at 12:00')
@booker.task('at 16:30, do this every 30 minutes')
```
#### Starting `in` a while
Using `every` with `in`, you can define a task that runs
__in__ in a certain amount of time after the first epoch.
```python
@booker.task('every 1 day in 3 hours')
@booker.task('in 30 minutes, do this every 5 seconds')
```
#### Combining `every` with `at` and `in`.
Combining all of the above, the task below runs daily at 12:30. It does not
matter what order you put these phrases in.
```python
@booker.task('in 30 minutes at 12:00 every 1 day')
```
#### Running `until` a specific date and time
Using the `until` keyword, you can tell booker when to end
a task.

You need to provide the month, day, year, hour, and minute that
you want the task to end in `MM-DD-YYYY HH:MM` format.

The task below would run at noon, every week, until 6PM on January 2nd
of the year 2020. Unless you had a power outage before then, or something.
```python
@booker.task('every 7 days at 12:00 until 01-02-2020 18:00')
```
## Using the `do()` method
You can use the `booker.do()` method to register a task with booker just as you
would do with the function decorator.
```python
def myfunc(): ...

booker.do(myfunc, 'every 1 day starting at 12:00')
```
If you build an `booker.Schedule` using `booker.get_schedule()`, you can pass
that Schedule object to `booker.do()`. The example below is indentical to the
example above.
```python
def myfunc(): ...

schedule = booker.get_schedule('every 1 day starting at 12:00')
booker.do(myfunc, schedule)
```
## Task labels
You can assign labels to tasks. Giving a task a label means that you can
cancel it at any time.
### Assigning labels with the decorator
```python
@booker.task('every 5 seconds', 'my-label')
def myfunc(): ...
```
### Assigning labels using `do()`
```python
def myfunc(): ...

booker.do(myfunc, 'every 5 seconds', 'my-label')
```
## Cancelling tasks
### By label
```python
booker.cancel('my-label') # cancel all tasks with the label 'my-label'
```
### All
```python
booker.cancel_all()
```
## Q&A
### __Q__: What exactly is a task?
__A__: A `threading.Timer` object.

<hr/>

### __Q__: Will booker block my main thread?
__A__: No. Booker doesn't have its own thread, or control loop,
or anything like that. It just spawns `threading.Timer` objects
for you when you create a task. It's up to you to keep your program
alive throughout the duration of task execution (unless you set
`booker.daemonize` to `False`). Usually you would do this with a
typical `while True: time.sleep(1)` loop.

The example below would quit immediately
and the task that was defined would never run because, by default,
booker daemonizes all of its tasks. You can disable this by setting
`booker.daemonize` to `False`.
```python
# This example quits immediately
import booker

def myfunc():
    ...

booker.do(myfunc, 'in 10 seconds')
```
This example, on the other hand, would block your main thread
and prevent the program from exiting until the task has finished.
```python
# This example quits after 10 seconds has passed
import booker

booker.daemonize = False

def myfunc():
    ...

booker.do(myfunc, 'in 10 seconds')
```

<hr/>

### __Q__: It is 6PM. What happens with this task?
```python
booker.do(myfunc, 'at 12:00')
```
__A__: It will run, once, tomorrow at noon.

<hr/>

### __Q__: I have a string: `2 hours, 59 minutes, 40 seconds`, and I want to run a task 5 minutes after that. How?

__A__: Use `booker.get_schedule` to get an `booker.Schedule` and add 300 seconds to its `tts` (time-to-start) property.
```python
schedule = booker.get_schedule('in 2 hours, 59 minutes, 40 seconds')
schedule.tts = schedule.tts + 300

booker.do(myfunc, schedule)
```

<hr/>

### __Q__: How do I pass arguments to a task?

__A__: Use a lambda.
```python
def myfunc(myarg):
    print('Hello, {}'.format(myarg))

booker.do(lambda: myfunc('world!'), 'in 5 seconds')
```

<hr/>

### __Q__: Can I view the status of a task?

__A__: From `example.py`:
```python
for task in booker.tasks():
    print(task)
```
__output:__
```bash
RepeatingTask: [__main__.pong] [interval: 1s] [tts: 2s] [running in: 0.00s] [until: indefinitely] [label: my-pong-task]
SingleTask: [__main__.print_task_status] [tts: 3s] [finished 0.00s ago]
SingleTask: [__main__.<lambda>] [tts: 12s] [running in: 9.00s]
SingleTask: [__main__.<lambda>] [tts: 19s] [running in: 16.00s]
SingleTask: [booker.cancel_all] [tts: 20s] [running in: 17.00s]
RepeatingTask: [__main__.print_time] [interval: 1s] [tts: 0s] [running in: 0.00s] [until: indefinitely]
RepeatingTask: [__main__.never_run] [interval: 1s] [tts: 5s] [until: 3s has passed]
SingleTask: [__main__.<lambda>] [tts: 7s] [running in: 4.00s]
RepeatingTask: [__main__.ping] [interval: 1s] [tts: 0s] [running in: 0.00s] [until: indefinitely] [label: my-ping-task]
SingleTask: [__main__.in_five_seconds] [tts: 5s] [running in: 2.00s]
SingleTask: [__main__.in_ten_seconds] [tts: 10s] [running in: 7.00s]
```
