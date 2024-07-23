import os
import argparse
import csv
import subprocess
import json

CWE_BENCH_JAVA_ROOT_DIR = os.path.abspath(os.path.join(__file__, "..", ".."))
MAVEN_VERSIONS = json.load(open(f"{CWE_BENCH_JAVA_ROOT_DIR}/scripts/mvn_version.json"))
JDK_VERSIONS = json.load(open(f"{CWE_BENCH_JAVA_ROOT_DIR}/scripts/jdk_version.json"))

ATTEMPTS = [
  { # Attempt 1
    "jdk": "8u202",
    "mvn": "3.5.0",
  },
  { # Attempt 2
    "jdk": "17",
    "mvn": "3.5.0",
  },
  { # Attempt 3
    "jdk": "17",
    "mvn": "3.9.8",
  },
  { # Attempt 4
    "jdk": "8u202",
    "mvn": "3.9.8",
  },
  { # Attempt 5
    "jdk": "7u80",
    "mvn": "3.2.1",
  }
]

def build_one_project_with_attempt(project_slug, attempt) -> bool:
  reader = csv.reader(open(f"{CWE_BENCH_JAVA_ROOT_DIR}/data/project_info.csv"))
  for line in reader:
    if line[1] == project_slug:
      row = line

  target_dir = f"{CWE_BENCH_JAVA_ROOT_DIR}/project-sources/{project_slug}"

  print(f">> [CWE-Bench-Java/build_one] Building `{project_slug}` with MAVEN {attempt['mvn']} and JDK {attempt['jdk']}...")
  mvn_build_cmd = [
    "mvn",
    "clean",
    "package",
    "pom.xml",
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
    capture_output=True
  )

  if output.returncode != 0:
    print(f">> [CWE-Bench-Java/build_one] Attempting build with MAVEN {attempt['mvn']} and JDK {attempt['jdk']} failed with return code {output.returncode}")
    print(f"STDOUT:")
    print(output.stdout.decode("utf-8"))
    print(f"Error message:")
    print(output.stderr.decode("utf-8"))
    return False
  else:
    return True

def build_one_project(project_slug):
  for attempt in ATTEMPTS:
    result = build_one_project_with_attempt(project_slug, attempt)
    if result:
      print(f">> [CWE-Bench-Java/build_one] Build succeeded for project `{project_slug}` with MAVEN {attempt['mvn']} and JDK {attempt['jdk']}")
      break

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("project_slug", type=str)
  args = parser.parse_args()
  build_one_project(args.project_slug)
