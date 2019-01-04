import datetime
import booker
import unittest
from freezegun import freeze_time
import numbers

def get_schedule(english):
    schedule = booker.get_schedule(english)
    assert isinstance(schedule, booker.Schedule)
    assert isinstance(schedule.interval, int)
    assert isinstance(schedule.tts, int)
    assert isinstance(schedule.ttl, numbers.Real)
    return schedule

class ScheduleTest(unittest.TestCase):
    def test_every(self):
        s = get_schedule('every 2 days')
        self.assertIsInstance(s, booker.Schedule)
        self.assertEqual(s.interval, 172800)
        self.assertEqual(s.tts, 0)
        self.assertEqual(s.ttl, 0)

        s = get_schedule('every 2 days 6 hours')
        self.assertEqual(s.interval, 194400)
        self.assertEqual(s.tts, 0)
        self.assertEqual(s.ttl, 0)

        s = get_schedule('every 10 days 3 hours 25 minutes 32 seconds')
        self.assertEqual(s.interval, 876332)
        self.assertEqual(s.tts, 0)
        self.assertEqual(s.ttl, 0)

    def test_in(self):
        s = get_schedule('in 5 minutes')
        self.assertEqual(s.interval, 0)
        self.assertEqual(s.tts, 300)
        self.assertEqual(s.ttl, 0)

        s = get_schedule('in 120 days 600 hours 200 minutes 1 second')
        self.assertEqual(s.interval, 0)
        self.assertEqual(s.tts, 12540001)
        self.assertEqual(s.ttl, 0)

    def test_every_in(self):
        s = get_schedule('every 2 days in 30 minutes')
        self.assertEqual(s.interval, 172800)
        self.assertEqual(s.tts, 1800)
        self.assertEqual(s.ttl, 0)

        s = get_schedule('every 2 days in 1 day 10 hours \
                17 minutes 36 seconds')
        self.assertEqual(s.interval, 172800)
        self.assertEqual(s.tts, 123456) # heh
        self.assertEqual(s.ttl, 0)

        s = get_schedule('every 12 days 15 hours 12 minutes 13 seconds \
                in 30 days 18 hours 25 minutes 10 seconds')
        self.assertEqual(s.interval, 1091533)
        self.assertEqual(s.tts, 2658310)
        self.assertEqual(s.ttl, 0)

    def test_in_every(self):
        s = get_schedule('in 5 minutes every 1 day 15 minutes 20 seconds')
        self.assertEqual(s.interval, 87320)
        self.assertEqual(s.tts, 300)
        self.assertEqual(s.ttl, 0)

        s = get_schedule('in 4 days 4 hours 4 minutes 4 seconds \
                every 4 days 8 hours 5 minutes 30 seconds')
        self.assertEqual(s.interval, 374730)
        self.assertEqual(s.tts, 360244)
        self.assertEqual(s.ttl, 0)

    def test_at(self):
        freezer = freeze_time('2020-12-25 12:00:00')
        freezer.start()

        s = get_schedule('every 5 minutes at 12:30')
        self.assertEqual(s.tts, 1800)

        # Because this task starts at 11AM and it is currently 12PM,
        # the time-to-start (tts) value is adjusted so that it begins
        # tomorrow at 11am.
        # That's 82800 seconds from now.
        s = get_schedule('at 11:00')
        self.assertEqual(s.tts, 82800)

        freezer.stop()

        freezer = freeze_time('2020-12-25 12:00:45')
        freezer.start()

        # This should start in 15 seconds.
        s = get_schedule('at 12:01')
        self.assertEqual(s.tts, 15)

        freezer.stop()

    def test_until(self):
        """
        Using the awesome freezegun library
        so that we can accurately and consistently test
        against predefined datetimes.
        """

        freezer = freeze_time('2020-12-25 12:00:00')
        freezer.start()
        assert datetime.datetime.now() == datetime.datetime(2020, 12, 25, 12, 0, 0)

        s = get_schedule('every 5 minutes until 12-25-2020 12:01')
        self.assertEqual(s.interval, 300)
        self.assertEqual(s.tts, 0)
        self.assertEqual(s.ttl, 60)

        """
        This task should start:
        Start on December 30th, 2020 (because of the 'in 5 days')
        at 1pm (becuase of the 'at 13:00')
        every 2 hours
        until December 31st, 2020, at 2pm
        -----------------------------------------
        Duration between now and start date:
        https://www.timeanddate.com/date/durationresult.html?m1=12&d1=25&y1=2020&m2=12&d2=30&y2=2020&h1=12&i1=0&s1=0&h2=13&i2=0&s2=0

        5 days, 1 hour, 0 minutes, 0 seconds
        435600 seconds (assertion should match this for tts)
        7260 minutes
        121 hours
        -----------------------------------------
        Duration between start date and end date:
        https://www.timeanddate.com/date/durationresult.html?m1=12&d1=30&y1=2020&m2=12&d2=31&y2=2020&h1=13&i1=0&s1=0&h2=14&i2=0&s2=0

        1 day, 1 hour, 0 minutes, 0 seconds
        90000 seconds (+435600(tts) = 525600(ttl))
        """
        s = get_schedule('every 2 hours in 12 minutes until 12-26-2020 16:34')
        self.assertEqual(s.interval, 7200)
        self.assertEqual(s.tts, 720)
        self.assertEqual(s.ttl, 102840)

        s = get_schedule('every 2 hours \
                in 5 days \
                at 13:00 \
                until 12-31-2020 14:00')
        self.assertEqual(s.interval, 7200)
        self.assertEqual(s.tts, 435600)
        self.assertEqual(s.ttl, 525600)

        freezer.stop()

    def test_cancel(self):
        def myfunc():
            print('Hi')

        # In case we created other tasks in other tests
        booker.cancel_all()
        assert len(booker.tasks()) == 0

        # Cancelling by label.
        booker.do(myfunc, 'in 1 second', 'dummy-task')
        booker.do(myfunc, 'in 1 second', 'dummy-task')
        booker.do(myfunc, 'in 1 second', 'dummy-task')
        booker.do(myfunc, 'in 1 second', 'dummy-task')
        assert len(booker.tasks()) == 4
        booker.cancel('dummy-task')
        assert len(booker.tasks()) == 0

        # Using .cancel_all().
        booker.do(myfunc, 'in 1 second')
        booker.do(myfunc, 'in 1 second')
        assert len(booker.tasks()) == 2
        booker.cancel_all()
        assert len(booker.tasks()) == 0

    def test_do_return_types(self):
        def myfunc():
            print('Hi')

        taskinfo = booker.do(myfunc, 'in 10 seconds')
        assert isinstance(taskinfo, booker.SingleTask)
        assert isinstance(taskinfo.task, booker.Task)
        assert isinstance(taskinfo.schedule, booker.Schedule)

        taskinfo = booker.do(myfunc, 'every 10 seconds in 10 seconds')
        assert isinstance(taskinfo, booker.RepeatingTask)
        assert isinstance(taskinfo.task, booker.Task)
        assert isinstance(taskinfo.schedule, booker.Schedule)

        taskinfo = booker.do(myfunc, 'at 12:00')
        assert isinstance(taskinfo, booker.SingleTask)

        taskinfo = booker.do(myfunc, 'every 5 seconds in 15 minutes until 01-30-2020 12:00')
        assert isinstance(taskinfo, booker.RepeatingTask)
        booker.cancel_all()

    def test_has_label(self):
        def myfunc():
            print('Hi')

        taskinfo = booker.do(myfunc, 'in 10 seconds', 'my-label')
        assert taskinfo.task.label == 'my-label'
        booker.cancel_all()

if __name__ == '__main__':
    unittest.main()
