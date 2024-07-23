"""
Usage: python fetch_one.py <project_slug>

The script fetches one project from Github, checking out the buggy commit,
and then patches it with the essential information for it to be buildable.
The project is specified with the Project Slug that contains project name,
CVE ID, and version tag.

Example:

``` bash
$ python fetch_one.py apache__camel_CVE-2018-8041_2.20.3
```
"""

import os
import argparse
import csv
import subprocess

CWE_BENCH_JAVA_ROOT_DIR = os.path.abspath(os.path.join(__file__, "..", ".."))

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("project_slug", type=str)
  args = parser.parse_args()

  project_slug = args.project_slug
  reader = csv.reader(open(f"{CWE_BENCH_JAVA_ROOT_DIR}/data/project_info.csv"))
  for line in reader:
    if line[1] == project_slug:
      row = line

  target_dir = f"{CWE_BENCH_JAVA_ROOT_DIR}/project-sources/{project_slug}"

  print(f">> [CWE-Bench-Java/build_one] Building `{project_slug}` with Maven...")
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
  subprocess.run(mvn_build_cmd, cwd=target_dir)
