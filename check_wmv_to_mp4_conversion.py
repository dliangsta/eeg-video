import os
from time import sleep, time
from glob import glob
from os import system
from datetime import timedelta


if __name__ == "__main__":
  system("clear")
  prev_time = None
  curr_time = time()
  prev_count = None
  curr_count = len(glob("/share/pi/cleemess/file-conversion-pipeline/*/*/*/*/*.mp4"))
  wmv_fns = glob("/share/pi/cleemess/file-conversion-pipeline/*/*/*/*/*.WMV")
  avg_times = []

  while True:
    mp4_fns = glob("/share/pi/cleemess/file-conversion-pipeline/*/*/*/*/*.mp4")
    prev_count = curr_count
    curr_count = len(mp4_fns)

    if curr_count > prev_count:
      prev_time = curr_time
      curr_time = time()
      for i in range(curr_count - prev_count):
        avg_times.append((curr_time - prev_time) / (curr_count - prev_count))

      while len(avg_times) > 100:
        avg_times.pop(0)

      avg_time = sum(avg_times) / len(avg_times)
      remaining_count = len(wmv_fns) - len(mp4_fns)
      remaining_time = timedelta(seconds=avg_rate * remaining_count)
      print(f"prev: {prev_count:4d}, curr: {curr_count:4d}, total: {len(wmv_fns)}, avg_time: {avg_time:.5f}, remaining: {remaining_count:4d}, remaining_time: {remaining_time}")
