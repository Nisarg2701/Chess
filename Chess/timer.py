import time


def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    print("Time Lapsed = {0}:{1}:{2}".format(int(hours), int(mins), sec))


start_time = time.time()
i = 100000000
while i != 0:
    i = i - 1
end_time = time.time()
time_lapsed = end_time - start_time
time_convert(time_lapsed)
