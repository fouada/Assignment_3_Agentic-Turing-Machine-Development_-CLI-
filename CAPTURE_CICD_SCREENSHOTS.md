# How to Capture CI/CD Screenshots for Documentation

## 🎯 Purpose
Capture visual proof that CI/CD pipelines are passing with all tests successful.

## 📸 Screenshots Needed

### Screenshot 1: Workflow Overview (REQUIRED)
**What to show:** All workflows passing with green checkmarks

**How to capture:**
1. Go to: https://github.com/talgoldengoren/Assignment_3_Agentic-Turing-Machine-Development_-CLI-/actions
2. You should see: "Agent Pipeline CI/CD" with a green ✅
3. Take a screenshot showing:
   - The workflow list
   - Green checkmarks
   - "tests_to_get_100" branch
   - Recent run timestamp

**Save as:** `assets/screenshots/01_workflow_overview.png`

### Screenshot 2: Successful Workflow Run (REQUIRED)
**What to show:** The specific successful run details

**How to capture:**
1. Click on the latest "Agent Pipeline CI/CD" run
2. Go to: https://github.com/talgoldengoren/Assignment_3_Agentic-Turing-Machine-Development_-CLI-/actions/runs/19710862586
3. Take a screenshot showing:
   - All 3 jobs with green checkmarks:
     - ✅ Validate Skills & Code
     - ✅ Run Tests & Check Coverage
     - ✅ Run Local Analysis
   - Total runtime
   - Branch name (tests_to_get_100)
   - Commit message

**Save as:** `assets/screenshots/02_successful_run.png`

### Screenshot 3: Test Job Details (REQUIRED)
**What to show:** The "Run Tests & Check Coverage" job results

**How to capture:**
1. On the run page, click "Run Tests & Check Coverage" job
2. Scroll to the "Run tests with coverage" step
3. Take a screenshot showing:
   - "83 passed in X seconds"
   - "Coverage: 86.32%"
   - Green checkmark next to the step
   - "Required test coverage of 85% reached"

**Save as:** `assets/screenshots/03_test_results.png`

### Screenshot 4: Coverage Report (OPTIONAL but NICE)
**What to show:** The uploaded coverage artifact

**How to capture:**
1. On the run page, scroll down to "Artifacts"
2. You should see "coverage-report"
3. Take a screenshot showing the artifact is available

**Save as:** `assets/screenshots/04_coverage_artifact.png`

## 🖼️ Step-by-Step Instructions

### Step 1: Navigate to Actions
```
1. Open your browser
2. Go to: https://github.com/talgoldengoren/Assignment_3_Agentic-Turing-Machine-Development_-CLI-
3. Click the "Actions" tab at the top
```

### Step 2: Take Screenshot 1 - Workflow Overview
```
1. You're now on the Actions page
2. Look for "Agent Pipeline CI/CD" in the workflow list
3. Make sure you can see:
   - Workflow name
   - Green checkmark ✅
   - Branch: tests_to_get_100
   - Recent timestamp
4. Take screenshot (Windows: Win+Shift+S, Mac: Cmd+Shift+4, Linux: Print Screen)
5. Save as: assets/screenshots/01_workflow_overview.png
```

### Step 3: Take Screenshot 2 - Successful Run
```
1. Click on the latest "Agent Pipeline CI/CD" workflow run
2. You should see URL: .../actions/runs/19710862586
3. The page shows:
   - All jobs with status
   - Commit information
   - Workflow file used
4. Take screenshot showing all 3 green jobs:
   ✅ Validate Skills & Code
   ✅ Run Tests & Check Coverage
   ✅ Run Local Analysis
5. Save as: assets/screenshots/02_successful_run.png
```

### Step 4: Take Screenshot 3 - Test Results
```
1. On the run details page, click "Run Tests & Check Coverage"
2. The logs will expand
3. Scroll to the "Run tests with coverage" step (should be green)
4. Click to expand that step
5. Look for output like:
   ============================= 83 passed in 6.95s ==============================
   Coverage: 86.32%
   Required test coverage of 85% reached. Total coverage: 86.32%
6. Take screenshot showing this output
7. Save as: assets/screenshots/03_test_results.png
```

### Step 5: Take Screenshot 4 - Artifacts (Optional)
```
1. Scroll down on the run details page
2. Look for "Artifacts" section
3. You should see "coverage-report" listed
4. Take screenshot
5. Save as: assets/screenshots/04_coverage_artifact.png
```

## 📂 Where to Save Screenshots

```
Assignment_3_Agentic-Turing-Machine-Development_-CLI-/
└── assets/
    └── screenshots/
        ├── 01_workflow_overview.png      (REQUIRED)
        ├── 02_successful_run.png          (REQUIRED)
        ├── 03_test_results.png            (REQUIRED)
        └── 04_coverage_artifact.png       (OPTIONAL)
```

## ✅ After Capturing Screenshots

### Update the Word Document
Add the screenshots to your `WHY_WE_DESERVE_100.docx` in these sections:

**Section 2.1 - CI/CD Pipeline Verification:**
- Add Screenshot 1 (Workflow Overview)
- Add Screenshot 2 (Successful Run)

**Section 8.1 - Detailed Scoring (Category 1: Testing & Quality):**
- Add Screenshot 3 (Test Results)

### Update CI_CD_EVIDENCE.md
```bash
# After saving screenshots, add them to documentation:
# Edit assets/CI_CD_EVIDENCE.md and add:

## Screenshots

### Workflow Overview
![Workflow Overview](screenshots/01_workflow_overview.png)

### Successful Run
![Successful Run](screenshots/02_successful_run.png)

### Test Results
![Test Results](screenshots/03_test_results.png)
```

### Commit the Screenshots
```bash
git add assets/screenshots/*.png
git commit -m "Add CI/CD passing screenshots for 100/100 verification

- Workflow overview showing all passing
- Successful run details
- Test results: 83 passed, 86.32% coverage

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push
```

## 🎯 Checklist

Before submitting your assignment, verify you have:

- [ ] Captured Screenshot 1: Workflow overview
- [ ] Captured Screenshot 2: Successful run details
- [ ] Captured Screenshot 3: Test results output
- [ ] Captured Screenshot 4: Coverage artifacts (optional)
- [ ] Saved all screenshots in `assets/screenshots/`
- [ ] Added screenshots to Word document
- [ ] Updated CI_CD_EVIDENCE.md with screenshot links
- [ ] Committed and pushed screenshots to GitHub

## 📧 Quick Summary for Lecturer

*"All CI/CD pipelines are verified passing on GitHub Actions. Screenshots included in documentation show:*
- *✅ All 3 jobs passing (Validate, Test, Analyze)*
- *✅ 83 tests executed successfully*
- *✅ 86.32% coverage achieved (exceeds 85% requirement)*
- *✅ Artifacts uploaded and available*

*Live verification available at: https://github.com/talgoldengoren/Assignment_3_Agentic-Turing-Machine-Development_-CLI-/actions/runs/19710862586"*

---

**NOTE:** These screenshots provide visual proof that complements the live GitHub Actions page. The lecturer can verify both the screenshots AND visit the live URL to confirm authenticity.
