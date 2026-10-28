# Lab 6 – Code and Branch Coverage Analysis

**Name:** Arya Devang  **SRN:** PES1UG24AM054
**Module under test:** `visa_application.py` (`visa_fee`, `documents_complete`, `application_status`)

## 1. Baseline (starter test file)
Running the 2 provided tests with `coverage run --branch -m pytest test_visa_application.py` gave **32 %** on `visa_application.py` (23 of 37 statements missed, 6 partial branches). Untested: error handling, group‑A bonus, express/normal surcharges, renewal path, photo check and almost all of `application_status`.

## 2. Code (line) coverage
File: `CodeCoverageTest_visa_application.py` – 11 tests, all pass.
Command: `coverage run -m pytest CodeCoverageTest_visa_application.py` → `coverage report -m`

| Metric | Result |
|---|---|
| Statements | 37 |
| Missed | 1 (line 42, `return "open"`) |
| **Line coverage** | **97 %** (target ≥ 90 %) |

Tests target: both `ValueError` raises, group‑A bonus entry, express and normal rates, the `extra > 5` surcharge (express), renewal / photo failure / success in `documents_complete`, and the `closing`, `closed` and peak‑season outcomes of `application_status`.
Screenshot: `screenshots/code_coverage.png`.

## 3. Branch coverage
File: `BranchCoverageTest_visa_application.py` – 23 tests, all pass.
Command: `coverage run --branch -m pytest BranchCoverageTest_visa_application.py` → `coverage report -m`

| Metric | Result |
|---|---|
| Statements / missed | 37 / 0 |
| Branches / partial | 26 / 0 |
| **Branch coverage** | **100 %** (target ≥ 90 %) |

With only the line‑coverage tests, `coverage --branch` showed 95 % with two gaps: `21->23` (the `speed == "express"` check inside the `extra > 5` block never False) and line 42 (`open` never returned). Added tests:
- `normal` speed with `extra > 5` (closes `21->23`);
- student with group A (the `!= "student"` condition False);
- `extra == 0` and `extra == 5` boundaries (`<= 0` and `> 5` both sides);
- renewal with zero forms (renewal False‑result);
- `application_status` at exact boundaries for express/normal and peak/non‑peak (`open`, `closing`, `closed`).
Screenshot: `screenshots/branch_coverage.png`.

## 4. Line vs. branch coverage – observations
Line coverage reached 97 % quickly because every statement ran at least once, but branch coverage exposed that some decisions (e.g. the express check inside the surcharge block) had only been evaluated one way. Branch coverage forced boundary‑value tests (`extra` = 0, 5; `days_left` = cutoff, cutoff‑15) that are exactly where off‑by‑one bugs (`>=` vs `>`) hide.

## 5. Commits
1. Initial starter files
2. `Lab 6: add code (line) coverage tests` – test file + screenshot
3. `Lab 6: add branch coverage tests` – test file + screenshot + this report
