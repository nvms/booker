from __future__ import print_function
import booker
import time
import sys
import datetime
import threading

def hour(): return datetime.datetime.now().hour
def minute(): return datetime.datetime.now().minute
def second(): return datetime.datetime.now().second
def ms(): return datetime.datetime.now().microsecond

booker.verbose = True

# ---
# Using the decorator.
@booker.task('in 2 seconds')
def hello_world(thing='world'):
    print('- Hello, {}!'.format(thing))

# ---
# Using the decorator.
@booker.task('in 5 seconds')
def in_five_seconds():
    print('- It\'s been 5 seconds.')

@booker.task('in 10 seconds')
def in_ten_seconds():
    print('- It\'s been 10 seconds.')
    print(booker.elapsed_since_epoch())

# ---
# Using the decorator, with a label.
@booker.task('every 1 second', 'my-ping-task')
def ping():
    print('- Ping')

# ---
# Using .do().
def pong():
    print('- Pong')

booker.do(pong, 'every 1 second in 2 seconds', 'my-pong-task')

def print_task_status():
    print('- Printing the status of all tasks:')
    for task in booker.tasks():
        print(task)
booker.do(print_task_status, 'in 3 seconds')

# ---
# Using .do().
def cancel_by_label(label):
    print('- Cancelling tasks with label: \'{}\'...'.format(label))
    booker.cancel(label)

booker.do(lambda: cancel_by_label('my-ping-task'), 'in 12 seconds')

# ---
# Using .do().
booker.do(lambda: print('- Cancelling all tasks in 1 second...'), 'in 19 seconds')
booker.do(booker.cancel_all, 'in 20 seconds')

# ---
# Using the decorator.
@booker.task('every 1 second')
def print_time():
    sys.stdout.write('{:02d}:{:02d}:{:02d}:{:02d}\n'.format(hour(), minute(), second(), ms()))

# ---
# Using .do().
def never_run():
    print('This should never be run and instead will produce a warning.')

schedule = booker.Schedule(interval=1, tts=5, ttl=3)
booker.do(never_run, schedule, 'task-that-never-runs')

# ---
# An alternative way to build a schedule.
mystr = '6 seconds'
schedule = booker.get_schedule('in ' + mystr)
schedule.tts = schedule.tts + 1 # Add 1 second to the start time.
booker.do(lambda: print('- It\'s been 7 seconds'), schedule)

# ---
# Keep alive.
def main():
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    main()

