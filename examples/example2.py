import sys
import time
import booker

def myfunc():
    print('Starting')
    time.sleep(2)
    print('Done')

booker.do(myfunc, 'in 0 seconds')
booker.do(myfunc, 'in 0 seconds')
booker.do(myfunc, 'in 0 seconds')
booker.do(myfunc, 'in 0 seconds')
booker.do(myfunc, 'in 0 seconds')
booker.do(myfunc, 'in 0 seconds')
booker.do(myfunc, 'in 0 seconds')
booker.do(myfunc, 'in 0 seconds')
booker.do(myfunc, 'in 0 seconds')
booker.do(myfunc, 'in 0 seconds')
booker.do(myfunc, 'in 0 seconds')
booker.do(myfunc, 'in 0 seconds')
booker.do(myfunc, 'in 0 seconds')

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)

