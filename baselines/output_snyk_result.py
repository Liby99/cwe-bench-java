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
    snyk_dir = f"{target_dir}/snyk-out"
    result_txt_dir = f"{snyk_dir}/stdout.txt"
    if not os.path.exists(result_txt_dir):
      continue
    results_txt = open(result_txt_dir)
    lines = list(results_txt)
    do_read = False

    if cwe == "CWE-022":
      target_str = "Path Traversal"
    elif cwe == "CWE-078":
      target_str = "Command Injection"
    elif cwe == "CWE-079":
      target_str = "(XSS)"
    elif cwe == "CWE-094":
      target_str = "Code Injection"

    has_cwe = False
    for (i, line) in enumerate(lines):
      if " ✗ " in line and target_str in line:
        has_cwe = True
        path = lines[i + 1].split("Path:")[1].strip()
        if ".java," not in path:
          continue
        path_parts = path.split(", line")
        file_name = path_parts[0]
        line_num = path_parts[1].strip()
        info = lines[i + 2].split("Info:")[1].strip()
        results.append([project_slug, cwe, file_name, line_num, info])

    if not has_cwe:
      results.append([project_slug, cwe, "none"])

  writer = csv.writer(open(f"{CWE_BENCH_JAVA_ROOT_DIR}/baselines/results/snyk_result.csv", "w"))
  writer.writerows(results)
