import os
import argparse
import csv
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

CWE_BENCH_JAVA_ROOT_DIR = os.path.abspath(os.path.join(__file__, "..", ".."))

def run_one(payload):
  (project,) = payload
  project_slug = project[1]
  print(f"== Processing {project_slug} ==")
  if os.path.exists(f"{CWE_BENCH_JAVA_ROOT_DIR}/project-sources/{project_slug}/snyk-out/stdout.txt"):
    print(f"  ==> Skipping {project_slug} since its already ran")
    return 1

  snyk_out_dir = f"{CWE_BENCH_JAVA_ROOT_DIR}/project-sources/{project_slug}/snyk-out"
  os.makedirs(snyk_out_dir, exist_ok=True)

  output = subprocess.run(
    ["snyk", "code", "test"],
    cwd=f"{CWE_BENCH_JAVA_ROOT_DIR}/project-sources/{project_slug}",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
  )

  print(output.stdout)
  print(output.stderr)

  f = open(f"{snyk_out_dir}/stdout.txt", "w")
  f.write(output.stdout)
  f = open(f"{snyk_out_dir}/stderr.txt", "w")
  f.write(output.stderr)
  return 1

def parallel_run(projects):
  results = []
  with ThreadPoolExecutor() as executor:
    # Submit the function to the executor for each struct
    future_to_project = {executor.submit(run_one, (project,)): project for project in projects}

    # Collect the results as they are completed
    for future in as_completed(future_to_project):
      project = future_to_project[future]
      try:
        result = future.result()
        results.append(result)
      except Exception as exc:
        print(f'>> Project {project} generated an exception: {exc}')

  num_succeed = len([result for result in results if result == 1])
  print(f"Executed: {len(projects)}; Success: {num_succeed}")

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--filter", nargs="+", type=str)
  parser.add_argument("--exclude", nargs="+", type=str)
  parser.add_argument("--cwe", nargs="+", type=str)
  args = parser.parse_args()

  print(f"====== Fetching and Building Repositories ======")
  reader = list(csv.reader(open(f"{CWE_BENCH_JAVA_ROOT_DIR}/data/project_info.csv")))[1:]

  # Apply the filters
  projects = []
  for project in reader:
    project_slug = project[1]
    project_cwe_id = project[3]

    is_queried_cwe = True
    if args.cwe is not None and len(args.cwe) > 0:
      is_queried_cwe = any(cwe == project_cwe_id for cwe in args.cwe)

    inclusive = True
    if args.filter is not None and len(args.filter) > 0:
      inclusive = any(f in project_slug for f in args.filter)

    exclusive = False
    if args.exclude is not None and len(args.exclude) > 0:
      exclusive = any(f in project_slug for f in args.exclude)
    if is_queried_cwe and inclusive and not exclusive:
      projects.append(project)

  # Perform run
  parallel_run(projects)
