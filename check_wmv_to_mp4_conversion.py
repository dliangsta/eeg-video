from time import sleep, time
from glob import glob
from os import system
import os


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

      avg_rate = sum(avg_times) / len(avg_times)
      remaining_count = len(wmv_fns) - len(mp4_fns)
      remaining_time = avg_rate * remaining_count
      print(f"prev: {prev_count}, curr: {curr_count}, total: {len(wmv_fns)}, avg rate: {avg_rate:.5f}, remaining: {remaining_count}, remaining_time: {remaining_time / 60 / 60:.5f} hours")
