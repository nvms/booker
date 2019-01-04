import re
import time
import datetime
import threading

first_epoch = time.time()
verbose = False
daemonize = True


class Task(object):
    def __init__(self, english=None, function=None, label=None):
        self.english = english
        self.function = function
        self.label = label

class Schedule(object):
    def __init__(self, interval=0, tts=0, ttl=0):
        self._interval = interval
        self._tts = tts
        self._ttl = ttl

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = value

    @property
    def tts(self):
        return self._tts

    @tts.setter
    def tts(self, value):
        self._tts = value

    @property
    def ttl(self):
        return self._ttl

    @ttl.setter
    def ttl(self, value):
        self._ttl = value

class Elapsed(object):
    def __init__(self, days=0, hours=0, minutes=0, seconds=0, since_epoch=0):
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.since_epoch = since_epoch

    def __str__(self):
        s = "{} days {} hours {} minutes {} seconds since epoch".format(
                self.days,
                self.hours,
                self.minutes,
                self.since_epoch)
        return s

class Colors:
    LABEL = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    UNDERLINE = "\033[4m"
    ENDC = "\033[0m"

def elapsed_since_epoch():
    """
    Returns the time elapsed since booker was imported.

    :return Elapsed
    """

    current_epoch = time.time()
    since_epoch = current_epoch - first_epoch

    days = int(since_epoch // 86400)
    hours = int(since_epoch // 3600 % 24)
    minutes = int(since_epoch // 60 % 60)
    seconds = int(since_epoch % 60)

    return Elapsed(days, hours, minutes, seconds, since_epoch)

def cancel(label):
    """ Given a label, cancels all tasks that have that label """
    for obj in tasks():
        if obj.task.label is not None:
            if obj.task.label == label:
                obj._cancel()

def cancel_all():
    """ Cancels all tasks. """
    for task in tasks():
        task._cancel()

def tasks():
    return _get_all_tasks()

def _get_all_tasks():
    """
    Returns RepeatingTask and SingleTask objects
    discovered using garbage collection.

    :return A list of RepeatingTask and/or SingleTask objects.
    """

    import gc
    objs = []
    for obj in gc.get_objects():
        t = None
        if isinstance(obj, RepeatingTask) and hasattr(obj, '_timer'):
                if obj._timer.is_alive:
                    objs.append(obj)
        if isinstance(obj, SingleTask) and hasattr(obj, '_timer'):
                if obj._timer.is_alive:
                    objs.append(obj)
    return objs

class SingleTask(object):
    def __init__(self, task, schedule, *args, **kwargs):
        self.task = task
        self.schedule = schedule
        self.args = args
        self.kwargs = kwargs
        self._timer = None
        self.start_time = None
        self.finished = False

        self._register_timer()

    def __str__(self):
        s = "SingleTask: [{mod}.{fun}]".format(
                mod=self.task.function.__module__,
                fun=self.task.function.__name__)
        
        if self.schedule.tts > 0:
            s = s + " [tts: {when}s]".format(
                    when=self.schedule.tts)

            next_run = self._get_time_until_next_run()
            if next_run > 0:
                s = s + " [running in: {0:.2f}s]".format(next_run)
            else:
                s = s + " [finished {0:.2f}s ago]".format(next_run * -1)
        return s

    def _cancel(self):
        """
        This is wrapped in a try/except, because if you try to
        cancell all tasks (for task in booker.tasks(): task.cancel()),
        that may include cancelling the task that calls that method.
        In which case, it has __just__ been cancelled and deleted.
        """
        if hasattr(self, "_timer"):
            try:
                self._timer.cancel()
            except AttributeError:
                if verbose:
                    print("{}Error trying to cancel timer that "
                            "didn't exist for task {}.{}{}".format(
                                Colors.FAIL,
                                self.task.function.__module__,
                                self.task.function.__name__,
                                Colors.ENDC))
            try:
                del self._timer
            except AttributeError:
                if verbose:
                    print("{}Error trying to delete timer that "
                            "didn't exist for task {}.{}{}".format(
                                Colors.FAIL,
                                self.task.function.__module__,
                                self.task.function.__name__,
                                Colors.ENDC))

    def _get_time_until_next_run(self):
        if self.schedule.tts > 0:
            return (self.schedule.tts - (time.time() - self.start_time))
        else:
            return 0

    def _register_timer(self):
        self._timer = threading.Timer(self.schedule.tts, self._run)
        self._timer.daemon = daemonize
        self._timer.start()
        self.start_time = time.time()

    def _run(self):
        self.task.function(*self.args, **self.kwargs)
        self._cancel()
        self.finished = True

class RepeatingTask(object):
    def __init__(self, task, schedule, *args, **kwargs):
        self.task = task
        self.schedule = schedule
        self.args = args
        self.kwargs = kwargs
        self._timer = None
        self.start_time = time.time()
        self.last_run_time = 0
        self.is_first_run = True
        self.finished = False

        self._register_timer()

    def _cancel(self):
        """
        This is wrapped in a try/except, because if you try to
        cancell all tasks (for task in booker.tasks(): task.cancel()),
        that may include cancelling the task that calls that method.
            booker.do(my_cancel_func, '...')
        You might end up attempting to cancel that ^^ task, but it
        has already been cancelled because the timers automatically
        cancel when the task is run.
        """
        if hasattr(self, "_timer"):
            try:
                self._timer.cancel()
            except AttributeError:
                if verbose:
                    print("Error trying to cancel timer that "
                            "didn't exist for task {}.{}".format(
                                self.task.function.__module__,
                                self.task.function.__name__))
            try:
                del self._timer
            except AttributeError:
                if verbose:
                    print("Error trying to delete timer that "
                            "didn't exist for task {}.{}".format(
                                self.task.function.__module__,
                                self.task.function.__name__))

    def _get_time_until_next_run(self):
        if self.last_run_time:
            return ((time.time() - self.last_run_time) - self.schedule.interval) * -1
        else:
            return ((time.time() - self.start_time) - self.schedule.interval) * -1

    def __str__(self):
        s = "RepeatingTask: [{mod}.{fun}]".format(
                mod=self.task.function.__module__,
                fun=self.task.function.__name__)
        s = s + " [interval: {interval}s]".format(
                interval=self.schedule.interval)
        s = s + " [tts: {tts}s]".format(tts=self.schedule.tts)

        next_run = self._get_time_until_next_run()
        if next_run > 0:
            s = s + " [running in: {0:.2f}s]".format(next_run)
        
        if self.schedule.ttl:
            s = s + " [until: {sec}s has passed]".format(
                    sec=self.schedule.ttl)
            remaining = self.last_run_time + self.schedule.ttl
        else:
            s = s + " [until: indefinitely]"

        if self.task.label is not None:
            s = s + " [label: {}]".format(self.task.label)

        return s


    def _register_timer(self):
        # If this should not start immediately
        if self.schedule.tts > 0:
            self._timer = threading.Timer(self.schedule.tts, self._run)
            self._timer.daemon = daemonize
            self._timer.start()
        # If this should run immediately
        else:
            # First run? Start now.
            if self.is_first_run:
                self._run()
                self.is_first_run = False
            # Not first run? Start time = schedule.interval
            else:
                self._timer = threading.Timer(self.schedule.interval, self._run)
                self._timer.daemon = daemonize
                self._timer.start()

    def _run(self):
        # Was this task given an end date?
        if self.schedule.ttl:
            elapsed = elapsed_since_epoch()
            if int(elapsed.since_epoch) >= int(self.schedule.ttl):
                return False
        self._funcrunner()

    def _funcrunner(self):
        # Run the task.
        self.task.function(*self.args, **self.kwargs)

        # Schedule next run.
        self._timer = threading.Timer(self.schedule.interval, self._run)
        self._timer.daemon = daemonize
        self._timer.start()
        self.last_run_time = time.time()

def _unpack_expression(found):
    val = 0
    if found:
        if found[0]:
            if found[0][0]:
                val = found[0][0]
            if found[0][1]:
                val = found[0][1]
    return val
    

def _english_to_seconds(english):
    """
    Parses your syntax.

    :param english: Your syntax
    :type english: str
    :return interval, tts (time-to-start), ttl (time-to-live)
    """
    interval = 0
    tts = 0
    ttl = 0

    english = str(english).lower()

    # -----------------------------------------------------
    # mo 08:00 we 08:00 fr 08:00
    # -----------------------------------------------------
    re_sched = '(mo|tu|we|th|fr|sa|su)\s(\d{2,2})\:(\d{2,2})'

    # -----------------------------------------------------------------------
    # keyword: `until`
    # -----------------------------------------------------------------------
    re_until = ".*until\s(\d{2,2})[\/]?[-]?(\d{2,2})[\/]?[-]?(\d{4,4})\s(\d{2,2})\:(\d{2,2})"
    until_match = re.match(re_until, english)
    until_month = None
    until_day = None
    until_year = None
    until_hour = None
    until_minute = None
    if until_match:
        matches = until_match.groups()
        until_month = int(matches[0])
        until_day = int(matches[1])
        until_year = int(matches[2])
        until_hour = int(matches[3])
        until_minute = int(matches[4])

        # datetime() wants a minute value of 0..59
        if until_minute == 60:
            until_minute = 0

        now = datetime.datetime.now()

        # Current YYYY-MM-DD HH:MM:SS
        a = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
        # Desired stop time YYYY-MM-DD HH:MM:SS
        # With `until`, we want to stop on the minute.
        b = datetime.datetime(until_year, until_month, until_day, until_hour, until_minute, 0)

        ttl = (b - a).total_seconds()

    # -----------------------------------------------------------------------
    # keyword: `at`
    # -----------------------------------------------------------------------
    re_at = ".*at\s(\d{2,2})\:(\d{2,2})"
    at_match = re.match(re_at, english)
    if at_match:
        matches = at_match.groups()
        start_hours = int(matches[0])
        start_mins = int(matches[1])

        now = datetime.datetime.now()

        # Current YYYY-MM-DD HH:MM:SS
        a = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
        # Desired start time YYYY-MM-DD HH:MM
        # With `at`, we want to start on the minute.
        b = datetime.datetime(now.year, now.month, now.day, start_hours, start_mins, 0)

        tts = (b - a).seconds

    # -----------------------------------------------------------------------
    # keyword: `in`
    # -----------------------------------------------------------------------
    re_in_days = ".*in\s(\d+)\sdays*.*?(?=every\s\d+)|.*in(?!<=every|u)(?:(?!every\s).)*(?:\s)(\d+)\sdays*"
    re_in_hours = ".*in\s(\d+)\shours*.*?(?=every\s\d+)|.*in(?!<=every|u)(?:(?!every\s).)*(?:\s)(\d+)\shours*"
    re_in_hrs = ".*in\s(\d+)\shrs*.*?(?=every\s\d+)|.*in(?!<=every|u)(?:(?!every\s).)*(?:\s)(\d+)\shrs*"
    re_in_minutes = ".*in\s(\d+)\sminutes*.*?(?=every\s\d+)|.*in(?!<=every|u)(?:(?!every\s).)*(?:\s)(\d+)\sminutes*"
    re_in_seconds = ".*in\s(\d+)\sseconds*.*?(?=every\s\d+)|.*in(?!<=every|u)(?:(?!every\s).)*(?:\s)(\d+)\sseconds*"

    in_days = re.findall(re_in_days, english)
    in_hours = re.findall(re_in_hours, english)
    in_hrs = re.findall(re_in_hrs, english)
    in_minutes = re.findall(re_in_minutes, english)
    in_seconds = re.findall(re_in_seconds, english)

    _id = _unpack_expression(in_days)
    ih = _unpack_expression(in_hours)
    ihrs = _unpack_expression(in_hrs)
    im = _unpack_expression(in_minutes)
    _is = _unpack_expression(in_seconds)

    if _id:
        tts += int(_id) * 86400
    if ih:
        tts += int(ih) * 3600
    if ihrs:
        tts += int(ihrs) * 3600
    if im:
        tts += int(im) * 60
    if _is:
        tts += int(_is)

    # -----------------------------------------------------------------------
    # keyword: `every`
    # -----------------------------------------------------------------------
    re_every_days = ".*every\s(\d+)\sdays*.*?(?=in\s\d+)|.*every(?!<=in\s)(?:(?!in\s).)*(?:\s)(\d+)\sdays*"
    re_every_hours = ".*every\s(\d+)\shours*.*?(?=in\s\d+)|.*every(?!<=in\s)(?:(?!in\s).)*(?:\s)(\d+)\shours*"
    re_every_hrs = ".*every\s(\d+)\shrs*.*?(?=in\s\d+)|.*every(?!<=in\s)(?:(?!in\s).)*(?:\s)(\d+)\shrs*"
    re_every_minutes = ".*every\s(\d+)\sminutes*.*?(?=in\s\d+)|.*every(?!<=in\s)(?:(?!in\s).)*(?:\s)(\d+)\sminutes*"
    re_every_seconds = ".*every\s(\d+)\sseconds*.*?(?=in\s\d+)|.*every(?!<=in\s)(?:(?!in\s).)*(?:\s)(\d+)\sseconds*"

    every_days = re.findall(re_every_days, english)
    every_hours = re.findall(re_every_hours, english)
    every_hrs = re.findall(re_every_hrs, english)
    every_minutes = re.findall(re_every_minutes, english)
    every_seconds = re.findall(re_every_seconds, english)

    ed = _unpack_expression(every_days)
    eh = _unpack_expression(every_hours)
    ehrs = _unpack_expression(every_hrs)
    em = _unpack_expression(every_minutes)
    es = _unpack_expression(every_seconds)

    if ed:
        interval += int(ed) * 86400
    if eh:
        interval += int(eh) * 3600
    if ehrs:
        interval += int(ehrs) * 3600
    if em:
        interval += int(em) * 60
    if es:
        interval += int(es)

    return interval, tts, ttl


def get_schedule(english):
    """
    Given a string, attempts to parse it and return
    a Schedule.

    :param english: An English-syntax string.
    :type english: str
    :return: Schedule
    """
    interval, tts, ttl = _english_to_seconds(english)

    return Schedule(interval,
            tts,
            ttl)

def _handle(task, schedule):
    """
    Assigns tasks.
    If the task has an interval, a RepeatingTask is registered.
    Otherwise, a SingleTask is registered.
    """

    if verbose:

        task_info = "Task: {}.{}".format(
            Colors.OKBLUE + str(task.function.__module__) + Colors.ENDC,
            Colors.OKGREEN + str(task.function.__name__) + Colors.ENDC)

        # Don't judge me.
        sched_info = Colors.UNDERLINE + "Schedule:" + Colors.ENDC \
                + Colors.UNDERLINE + " interval: " + Colors.ENDC \
                    + (Colors.OKGREEN + Colors.UNDERLINE + str(schedule.interval) + Colors.ENDC if schedule.interval else Colors.UNDERLINE + str(schedule.interval) + Colors.ENDC) \
                + Colors.UNDERLINE + " time-to-start: " + Colors.ENDC \
                    + (Colors.OKGREEN + Colors.UNDERLINE + str(schedule.tts) + Colors.ENDC if schedule.tts else Colors.UNDERLINE + str(schedule.tts) + Colors.ENDC) \
                + Colors.UNDERLINE + " time-to-live: " + Colors.ENDC \
                    + (Colors.OKGREEN + Colors.UNDERLINE + str(schedule.ttl) + Colors.ENDC if schedule.ttl else Colors.UNDERLINE + str(schedule.ttl) + Colors.ENDC)
                                # Schedule: interval:                                             time-to-start:                                        time-to-live: 
        print(Colors.UNDERLINE + "                    " + (" " * len(str(schedule.interval))) + "                " + (" " * len(str(schedule.tts))) + "               " + (" " * len(str(schedule.ttl))) + Colors.ENDC)
        print(task_info)
        if task.label is not None:
            print("Label: " + Colors.LABEL + task.label + Colors.ENDC)
        print(sched_info)

    if schedule.ttl > 0 and schedule.ttl < schedule.tts:
        print(Colors.WARNING + "Warning: Task '" + str(task.function.__name__) + "' will never run because it ends {}s before it starts.".format(schedule.tts - schedule.ttl) + Colors.ENDC)

    if schedule.interval > 0:
        return RepeatingTask(task, schedule)
    else:
        return SingleTask(task, schedule)

def task(regex=None, label=None):
    """
    The @task() decorator
    :param regex: English string representation of desired schedule.
    :type regex: str
    :param label: A label for this task.
    :type label: str
    :return: decorator function
    """

    def decorator(function):
        task = Task(function=function, label=label)
        _handle(task, get_schedule(regex))
        return function

    return decorator

def do(func=None, sched=None, label=None):
    """
    booker.do(mycallable, 'every 5 seconds in 10 seconds', 'my-task')
    booker.do(mycallable, booker.Schedule(5, 10, 0), 'my-task')

    :param func: What you want to call.
    :type func: callable
    :param sched: Either a str that can be parsed using expressions,
                  or a Schedule object.
    :type sched: EITHER str OR Schedule
    :param label: A label for this task.
    :type label: str
    """

    if func is None:
        return

    if isinstance(sched, Schedule):
        schedule = sched
    else:
        schedule = get_schedule(sched)

    task = Task(sched, func, label)
    return _handle(task, schedule)

