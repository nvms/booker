import sys, os
import curses
import booker
import time

def draw_menu(stdscr):
    key = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Color pairs
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Loop where key is the last char pressed
    # while (key != ord('q')):
    while True:

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Create the left window
        left_x = 0
        left_y = 0
        left_h = height
        left_w = int((width // 2) - 1)
        left = curses.newwin(left_h, left_w, left_y, left_x)
        left.box()

        # Create the right window
        right_x = int((width // 2))
        right_y = 0
        right_h = height
        right_w = int((width // 2))
        right = curses.newwin(right_h, right_w, right_y, right_x)
        right.box()

        # Right: strings
        right_title = 'Tasks'

        # Right: centering calculations
        right_title_x = int((right_w // 2) - (len(right_title) // 2) - len(right_title) % 2)
        # Right: render title
        right.attron(curses.color_pair(1))
        right.addstr(1, 1, right_title)
        right.addstr(1, len(right_title) + 1, ' ' * (right_w - len(right_title) - 2))
        right.attroff(curses.color_pair(1))

        # Right: render booker tasks

        # Left: strings
        left_title = 'stdout'

        # Left: centering calculations
        left_title_x = int((left_w // 2) - (len(left_title) // 2))

        # Left: render text
        left.attron(curses.color_pair(1))
        left.addstr(1, 1, left_title)
        left.addstr(1, len(left_title) + 1, ' ' * (left_w - len(left_title) - 2))
        left.attroff(curses.color_pair(1))

        tasks = booker.tasks()
        if tasks is not None:
            i = 0
            for task in tasks:
                left.addstr(3 + i, 1, str(task.task.function.__name__) + ' in ' + str(task.get_time_until_next_run()) + 's')
                i = i + 1
        else:
            left.addstr(3, 1, 'no tasks :({}'.format(type(tasks)))

        # Position the cursor
        stdscr.move(cursor_y, cursor_x)
        right.move(cursor_y, cursor_x)
        left.move(cursor_y, cursor_x)

        # stdscr: refresh screen
        stdscr.refresh()

        # Right: refresh screen
        right.refresh()

        # Left: refresh screen
        left.refresh()

        # Wait for next input...
        # key = stdscr.getch()

        # while True:
        #     time.sleep(0.5)
        #     stdscr.refresh()
        #     left.refresh()
        #     right.refresh()

        # Enter
        if key == 10:
            sys.stdout.write('YES')

        time.sleep(0.33)

def start():
    curses.wrapper(draw_menu)

def update_tasks():
    tasks = booker.tasks()

def do_something():
    pass

if __name__ == '__main__':
    booker.do(update_tasks, 'every 3 second in 1 second')
    booker.do(do_something, 'every 15 seconds in 1 second')
    start()
