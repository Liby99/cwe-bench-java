import os
import argparse
import csv
import subprocess

CWE_BENCH_JAVA_ROOT_DIR = os.path.abspath(os.path.join(__file__, "..", ".."))
JAVA_ENV_DIR = os.path.join(CWE_BENCH_JAVA_ROOT_DIR, "java-env")

MVN_VERSIONS = {
  "3.2.1": {
    "url": "https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/3.2.1/apache-maven-3.2.1-bin.zip",
    "zip_file": "apache-maven-3.2.1-bin.zip",
    "dir": "apache-maven-3.2.1",
  },
  "3.5.0": {
    "url": "https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/3.5.0/apache-maven-3.5.0-bin.zip",
    "zip_file": "apache-maven-3.5.0-bin.zip",
    "dir": "apache-maven-3.5.0",
  },
  "3.9.8": {
    "url": "https://dlcdn.apache.org/maven/maven-3/3.9.8/binaries/apache-maven-3.9.8-bin.zip",
    "zip_file": "apache-maven-3.9.8-bin.zip",
    "dir": "apache-maven-3.9.8",
  },
}

def download_mvn(version, info):
  print(f">> [CWE-Bench-Java/setup_mvn] Fetching Apache Maven {version}...")
  if os.path.exists(f"{JAVA_ENV_DIR}/{info['dir']}"):
    print(f">> [CWE-Bench-Java/setup_mvn] Maven version {version} found; skipping")
  else:
    subprocess.run(["wget", info["url"]], cwd=JAVA_ENV_DIR)

    print(f">> [CWE-Bench-Java/setup_mvn] Unzipping Maven Binary {version}...")
    subprocess.run(["unzip", "-n", info["zip_file"]], cwd=JAVA_ENV_DIR)

    print(f">> [CWE-Bench-Java/setup_mvn] Removing Downloaded File...")
    subprocess.run(["rm", info["zip_file"]], cwd=JAVA_ENV_DIR)

  print(f">> [CWE-Bench-Java/setup_mvn] Testing Downloaded Binary...")
  output = subprocess.run(
    ["mvn", "--help"],
    cwd=JAVA_ENV_DIR,
    env={"PATH": f"{os.environ['PATH']}:{JAVA_ENV_DIR}/{info['dir']}/bin"},
    capture_output=True)

  if output.returncode == 0:
    print(f">> [CWE-Bench-Java/setup_mvn] Maven version {version} successfully installed")
  else:
    print(f">> [CWE-Bench-Java/setup_mvn] Maven version {version} installation failed:")
    print(output.stderr.decode("utf-8"))

if __name__ == "__main__":
  for (version, mvn_info) in MVN_VERSIONS.items():
    download_mvn(version, mvn_info)
