import time

def stoppable_sleep(seconds, check_flag_func):
    end_time = time.time() + seconds
    while check_flag_func() and time.time() < end_time:
        time.sleep(1)