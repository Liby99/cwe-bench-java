import os
import argparse
import csv
import json
import subprocess

CWE_BENCH_JAVA_ROOT_DIR = os.path.abspath(os.path.join(__file__, "..", ".."))
JAVA_ENV_DIR = os.path.join(CWE_BENCH_JAVA_ROOT_DIR, "java-env")
JDK_VERSIONS = json.load(open(f"{CWE_BENCH_JAVA_ROOT_DIR}/scripts/jdk_version.json"))

def setup_jdk(version, info):
  print(f">> [CWE-Bench-Java/setup_jdk] Setting up JDK {version}...")
  if os.path.exists(f"{info['dir']}"):
    print(f">> [CWE-Bench-Java/setup_jdk] JDK version {version} found; skipping")
  else:
    print(f">> [CWE-Bench-Java/setup_jdk] JDK version {version} NOT found; setting up...")

    # if not os.path.exists(f"{JAVA_ENV_DIR}/{info['tar_file']}"):
    #   print(f">> [CWE-Bench-Java/setup_jdk] JDK tar {info['tar_file']} NOT found; skipping")

    # print(f">> [CWE-Bench-Java/setup_jdk] Un-tar-ing JDK Binary {version}...")
    # output = subprocess.run(["tar", "xzvf", f"{info['tar_file']}"], cwd=JAVA_ENV_DIR)
    # if output.returncode != 0:
    #   print(f">> [CWE-Bench-Java/setup_jdk] failed...")
    #   exit(1)

if __name__ == "__main__":
  for (version, jdk_info) in JDK_VERSIONS.items():
    setup_jdk(version, jdk_info)
