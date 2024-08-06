import os
import argparse
import csv
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

CWE_BENCH_JAVA_ROOT_DIR = os.path.abspath(os.path.join(__file__, "..", ".."))

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--filter", nargs="+", type=str)
  parser.add_argument("--exclude", nargs="+", type=str)
  parser.add_argument("--cwe", nargs="+", type=str)
  args = parser.parse_args()

  print(f"====== Fetching and Building Repositories ======")
  reader = list(csv.reader(open(f"{CWE_BENCH_JAVA_ROOT_DIR}/data/project_info.csv")))[1:]

  # Perform run
  results = []
  for project in reader:
    project_slug = project[1]
    print(project_slug)
    cwe = project[3]
    target_dir = f"{CWE_BENCH_JAVA_ROOT_DIR}/project-sources/{project_slug}"
    infer_dir = f"{target_dir}/infer-out"
    result_txt_dir = f"{infer_dir}/report.txt"
    if not os.path.exists(result_txt_dir):
      continue
    results_txt = open(result_txt_dir)
    do_read = False
    for result_txt_line in results_txt:
      if not do_read and "Issue Type(ISSUED_TYPE_ID)" in result_txt_line:
        do_read = True
      elif do_read:
        parts = result_txt_line.strip().split(": ")
        kind = parts[0]
        num = parts[1]
        results.append([project_slug, cwe, kind, num])

  writer = csv.writer(open(f"{CWE_BENCH_JAVA_ROOT_DIR}/baselines/results/infer_result.csv", "w"))
  writer.writerows(results)
