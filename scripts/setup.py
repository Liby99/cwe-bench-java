import os
import argparse
import csv
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

CWE_BENCH_JAVA_ROOT_DIR = os.path.abspath(os.path.join(__file__, "..", ".."))

def fetch_and_build_one(payload):
  (project, no_build) = payload
  project_slug = project[1]
  print(f"== Processing {project_slug} ==")
  output = subprocess.run(["python", f"{CWE_BENCH_JAVA_ROOT_DIR}/scripts/fetch_one.py", project_slug])
  if output.returncode != 0:
    return
  if not no_build:
    output = subprocess.run(["python", f"{CWE_BENCH_JAVA_ROOT_DIR}/scripts/build_one.py", project_slug])
    if output.returncode != 0:
      return
    print(f"== Done fetching and building {project_slug} ==")
  else:
    print(f"== Done fetching {project_slug} ==")

def parallel_fetch_and_build(projects, no_build):
  results = []
  with ThreadPoolExecutor() as executor:
    # Submit the function to the executor for each struct
    future_to_project = {executor.submit(fetch_and_build_one, (project, no_build)): project for project in projects}

    # Collect the results as they are completed
    for future in as_completed(future_to_project):
      project = future_to_project[future]
      try:
        result = future.result()
        results.append(result)
      except Exception as exc:
        print(f'>> Project {project} generated an exception: {exc}')

  return results

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--no-build", action="store_true")
  parser.add_argument("--filter", nargs="+", type=str)
  parser.add_argument("--exclude", nargs="+", type=str)
  parser.add_argument("--cwe", nargs="+", type=str)
  args = parser.parse_args()

  if not args.no_build:
    subprocess.run(["mkdir", "-p", f"{CWE_BENCH_JAVA_ROOT_DIR}/build-info"])
  subprocess.run(["mkdir", "-p", f"{CWE_BENCH_JAVA_ROOT_DIR}/project-sources"])

  if not args.no_build:
    print(f"====== Setting up JDK ======")
    output = subprocess.run(["python", f"{CWE_BENCH_JAVA_ROOT_DIR}/scripts/setup_jdk.py"])
    if output.returncode != 0: print(f"Failed; aborting"); exit(1)

    print(f"====== Setting up Maven ======")
    output = subprocess.run(["python", f"{CWE_BENCH_JAVA_ROOT_DIR}/scripts/setup_mvn.py"])
    if output.returncode != 0: print(f"Failed; aborting"); exit(1)

    print(f"====== Setting up Gradle ======")
    output = subprocess.run(["python", f"{CWE_BENCH_JAVA_ROOT_DIR}/scripts/setup_gradle.py"])
    if output.returncode != 0: print(f"Failed; aborting"); exit(1)

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

  # Perform fetch and build on the applied
  parallel_fetch_and_build(reader, args.no_build)
