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
  if os.path.exists(f"{JAVA_ENV_DIR}/{info['dir']}"):
    print(f">> [CWE-Bench-Java/setup_jdk] JDK version {version} found; skipping")
  else:
    if not os.path.exists(f"{JAVA_ENV_DIR}/{info['tar']}"):
      print(f">> [CWE-Bench-Java/setup_jdk] JDK tar {info['tar']} NOT found; skipping")
      return

    print(f">> [CWE-Bench-Java/setup_jdk] Un-tar-ing JDK Binary {version}...")
    subprocess.run(["tar", "xzvf", info["zip_file"]], cwd=JAVA_ENV_DIR)

if __name__ == "__main__":
  for (version, jdk_info) in JDK_VERSIONS.items():
    setup_jdk(version, jdk_info)
