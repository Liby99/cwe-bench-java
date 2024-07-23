# CWE-Bench-Java

This repository contains the dataset CWE-Bench-Java presented in the paper [LLM-Assisted Static Analysis for Detecting Security Vulnerabilities](https://arxiv.org/abs/2405.17238).
At a high level, this dataset contains 120 CVEs spanning 4 CWEs, namely path-traversal, OS-command injection, cross-site scripting, and code-injection.
Each CVE includes the buggy and fixed source code of the project, along with the information of the fixed files and functions.
We provide only the seed information in this repository, and we provide scripts for fetching, patching, and building the repositories.
The dataset collection process is illustrated in the figure below:

![dataset-collection-process](resources/dataset-collection.png)

<!-- A model for vulnerability detection should be evaluated on the dataset by outputing a set of vulnerabilities as a set of program traces.
The model should be evaluated with the metric of "at least one output trace passes through a fixed function". -->

## Packaged Data

```
- data/
  - project_info.csv
  - fix_info.csv
- patches/
  - <PROJECT_SLUG>.patch
- advisory/
  - <PROJECT_SLUG>.json
- scripts/
  - setup.py
  - fetch_one.py
  - patch_one.py
  - build_one.py
```

## To-Fetch Data

```
- project-sources/
  - <PROJECT_SLUG>/
```

## Citation

Consider citing our paper:

```
@article{li2024iris,
      title={LLM-Assisted Static Analysis for Detecting Security Vulnerabilities},
      author={Ziyang Li and Saikat Dutta and Mayur Naik},
      year={2024},
      eprint={2405.17238},
      archivePrefix={arXiv},
      primaryClass={cs.CR},
      url={https://arxiv.org/abs/2405.17238},
}
```
