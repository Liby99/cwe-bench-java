import os
import argparse
import csv
import subprocess

CWE_BENCH_JAVA_ROOT_DIR = os.path.abspath(os.path.join(__file__, "..", ".."))
JAVA_ENV_DIR = os.path.join(CWE_BENCH_JAVA_ROOT_DIR, "java-env")

JDK_VERSIONS = {
  "3.2.1": {
    "url": "https://www.oracle.com/webapps/redirect/signon?nexturl=https://download.oracle.com/otn/java/jdk/11.0.23%2B7/9bd8d305c900ee4fa3e613b59e6f42de/jdk-11.0.23_linux-x64_bin.tar.gz",
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
