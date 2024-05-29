@echo off
REM Now execute all test and record the coverage
REM All tests ending with _oracle are skipped by default
cd %~dp0\..
pytest --cov-config=.coveragerc  --cov-branch  --ignore-glob=*_oracle.py ^
     --cov=tsf --cov-report html:docs\coverage tests\tsf
