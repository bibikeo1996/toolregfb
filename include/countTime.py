import time
import sys

def demthoigian(seconds):
    for i in range(1, seconds + 1):
        sys.stdout.write('\r' + str(i))
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write('\n')    