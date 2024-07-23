import os
import argparse
import csv
import subprocess
import json
import sys

CWE_BENCH_JAVA_ROOT_DIR = os.path.abspath(os.path.join(__file__, "..", ".."))
MAVEN_VERSIONS = json.load(open(f"{CWE_BENCH_JAVA_ROOT_DIR}/scripts/mvn_version.json"))
JDK_VERSIONS = json.load(open(f"{CWE_BENCH_JAVA_ROOT_DIR}/scripts/jdk_version.json"))

ATTEMPTS = [
  { # Attempt 1
    "jdk": "8u202",
    "mvn": "3.5.0",
  },
  # { # Attempt 2
  #   "jdk": "17",
  #   "mvn": "3.5.0",
  # },
  # { # Attempt 3
  #   "jdk": "17",
  #   "mvn": "3.9.8",
  # },
  # { # Attempt 4
  #   "jdk": "8u202",
  #   "mvn": "3.9.8",
  # },
  # { # Attempt 5
  #   "jdk": "7u80",
  #   "mvn": "3.2.1",
  # }
]

NEWLY_BUILT = "newly-built"
ALREDY_BUILT = "already-built"
FAILED = "failed"

def build_one_project_with_attempt(project_slug, attempt):
  reader = list(csv.reader(open(f"{CWE_BENCH_JAVA_ROOT_DIR}/data/project_info.csv")))[1:]
  for line in reader:
    if line[1] == project_slug:
      row = line

  target_dir = f"{CWE_BENCH_JAVA_ROOT_DIR}/project-sources/{project_slug}"

  # Checking if the repo has been built already
  if is_built(project_slug):
    print(f">> [CWE-Bench-Java/build_one] {project_slug} is already built...")
    return ALREDY_BUILT

  print(f">> [CWE-Bench-Java/build_one] Building `{project_slug}` with MAVEN {attempt['mvn']} and JDK {attempt['jdk']}...")
  mvn_build_cmd = [
    "mvn",
    "clean",
    "package",
    "-B",
    "-V",
    "-e",
    "-Dfindbugs.skip",
    "-Dcheckstyle.skip",
    "-Dpmd.skip=true",
    "-Dspotbugs.skip",
    "-Denforcer.skip",
    "-Dmaven.javadoc.skip",
    "-DskipTests",
    "-Dmaven.test.skip.exec",
    "-Dlicense.skip=true",
    "-Drat.skip=true",
    "-Dspotless.check.skip=true"
  ]
  output = subprocess.run(
    mvn_build_cmd,
    cwd=target_dir,
    env={
      "PATH": f"{os.environ['PATH']}:{CWE_BENCH_JAVA_ROOT_DIR}/java-env/{MAVEN_VERSIONS[attempt['mvn']]['dir']}/bin",
      "JAVA_HOME": f"{CWE_BENCH_JAVA_ROOT_DIR}/java-env/{JDK_VERSIONS[attempt['jdk']]['dir']}",
    },
    stdout=subprocess.PIPE,
  )

  if output.returncode != 0:
    print(f">> [CWE-Bench-Java/build_one] Attempting build `{project_slug}` with MAVEN {attempt['mvn']} and JDK {attempt['jdk']} failed with return code {output.returncode}")
    print(f"STDOUT:")
    print(output.stdout.decode("utf-8"))
    print(f"Error message:")
    print(output.stderr.decode("utf-8"))
    return FAILED
  else:
    print(f">> [CWE-Bench-Java/build_one] Build succeeded for project `{project_slug}` with MAVEN {attempt['mvn']} and JDK {attempt['jdk']}")
    print(f">> [CWE-Bench-Java/build_one] Dumping build information")
    json.dump(attempt, open(f"{CWE_BENCH_JAVA_ROOT_DIR}/build-info/{project_slug}.json", "w"))
    return NEWLY_BUILT

def is_built(project_slug) -> bool:
  if os.path.exists(f"{CWE_BENCH_JAVA_ROOT_DIR}/build-info/{project_slug}.json"):
    return True
  else:
    return False

def save_build_result(project_slug, result, attempt):
  build_result_dir = f"{CWE_BENCH_JAVA_ROOT_DIR}/build-info/result.csv"

  rows = []
  if os.path.exists(build_result_dir):
    rows = list(csv.reader(open(build_result_dir)))[1:]

  existed_and_mutated = False
  for row in rows:
    if row[0] == project_slug:
      existed_and_mutated = True
      row[1] = "success" if result else "failure"
      row[2] = attempt["jdk"]
      row[3] = attempt["mvn"]

  if not existed_and_mutated:
    rows.append([project_slug, "success" if result else "failure", attempt["jdk"], attempt["mvn"]])

  writer = csv.writer(open(build_result_dir, "w"))
  writer.writerow(["project_slug", "status", "jdk_version", "mvn_version"])
  writer.writerows(rows)

def build_one_project(project_slug):
  for attempt in ATTEMPTS:
    result = build_one_project_with_attempt(project_slug, attempt)
    if result == NEWLY_BUILT:
      save_build_result(project_slug, True, attempt)
      return
    elif result == ALREDY_BUILT:
      return
  save_build_result(project_slug, False, {"jdk": "n/a", "mvn": "n/a"})

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("project_slug", type=str)
  args = parser.parse_args()
  build_one_project(args.project_slug)
