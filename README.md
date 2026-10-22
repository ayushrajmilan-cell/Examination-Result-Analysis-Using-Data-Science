# Examination Result Analysis Using Data Science

## Objective
Analyze student results using Python, pandas, NumPy and Matplotlib: clean data, calculate total marks and percentage, assign grades, summarize pass/fail outcomes, compare subjects, and explore attendance versus marks.

## Dataset
`student_exam_results.csv` is a synthetic practice dataset of 60 students. It includes attendance and marks in Mathematics, Python, DBMS, Statistics and English. Five subject marks are intentionally missing to demonstrate median imputation. No real student personal data is included.

## Setup
Install Python 3.9+, then run:
```bash
pip install -r requirements.txt
python analysis.py
```

## Generated outputs
The script creates an `outputs/` directory containing cleaned data, subject summary, grade distribution, pass/fail summary, attendance summary, correlation text, and four charts.

## Rules used
- Missing subject marks are filled with the median of that subject.
- Percentage = total marks / 500 × 100.
- Grades: A+ (90+), A (80–89.99), B (70–79.99), C (60–69.99), D (50–59.99), E (40–49.99), F (below 40).
- Pass requires at least 40 marks in every subject.
- Correlation shows association; it does not prove causation.

Use the generated outputs for the PBL report only after running and checking them. This is synthetic sample data, not official student records.
