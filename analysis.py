from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
DATA = BASE / "student_exam_results.csv"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)
SUBJECTS = ["Mathematics", "Python", "DBMS", "Statistics", "English"]
PASS_MARK = 40

# 1) Load and inspect
raw = pd.read_csv(DATA)
print("Dataset shape:", raw.shape)
print("\\nMissing values before cleaning:\\n", raw.isna().sum())
print("Duplicate rows:", raw.duplicated().sum())

# 2) Validate marks and attendance
for subject in SUBJECTS:
    invalid = raw[subject].notna() & ~raw[subject].between(0, 100)
    if invalid.any():
        raise ValueError(f"Invalid marks in {subject}; marks must be 0-100.")
if not raw["Attendance_Percentage"].between(0, 100).all():
    raise ValueError("Attendance must be between 0 and 100.")
if raw["Student_ID"].duplicated().any():
    raise ValueError("Student_ID values must be unique.")

# 3) Clean missing subject marks using each subject's median
data = raw.copy()
for subject in SUBJECTS:
    data[subject] = data[subject].fillna(data[subject].median())

# 4) Calculate totals, percentages, grades, and pass/fail
data["Total_Marks"] = data[SUBJECTS].sum(axis=1)
data["Percentage"] = (data["Total_Marks"] / (len(SUBJECTS)*100) * 100).round(2)

def grade(p):
    if p >= 90: return "A+"
    if p >= 80: return "A"
    if p >= 70: return "B"
    if p >= 60: return "C"
    if p >= 50: return "D"
    if p >= 40: return "E"
    return "F"

data["Grade"] = data["Percentage"].apply(grade)
data["Result"] = np.where((data[SUBJECTS] >= PASS_MARK).all(axis=1), "Pass", "Fail")
data.to_csv(OUT/"cleaned_student_exam_results.csv", index=False)

# 5) Summary tables
summary = data[SUBJECTS].agg(["mean","median","min","max","std"]).T.round(2)
summary.index.name = "Subject"
summary.to_csv(OUT/"subject_wise_summary.csv")

grade_counts = data["Grade"].value_counts().reindex(["A+","A","B","C","D","E","F"], fill_value=0)
grade_counts.rename_axis("Grade").reset_index(name="Student_Count").to_csv(OUT/"grade_distribution.csv", index=False)
result_counts = data["Result"].value_counts().reindex(["Pass","Fail"], fill_value=0)
result_counts.rename_axis("Result").reset_index(name="Student_Count").to_csv(OUT/"pass_fail_summary.csv", index=False)
data["Attendance_Percentage"].describe().round(2).rename_axis("Statistic").reset_index(name="Value").to_csv(OUT/"attendance_summary.csv", index=False)

corr = data["Attendance_Percentage"].corr(data["Percentage"])
(OUT/"attendance_correlation.txt").write_text(
    f"Pearson correlation between attendance and percentage: {corr:.3f}\\n"
    "Correlation indicates association, not causation.\\n", encoding="utf-8")

# 6) Charts
data[SUBJECTS].mean().sort_values(ascending=False).plot(kind="bar", figsize=(8,5))
plt.title("Average Marks by Subject"); plt.xlabel("Subject"); plt.ylabel("Average / 100")
plt.ylim(0,100); plt.tight_layout(); plt.savefig(OUT/"subject_average_chart.png",dpi=140); plt.close()

data["Grade"].value_counts().reindex(["A+","A","B","C","D","E","F"],fill_value=0).plot(kind="bar",figsize=(7,4))
plt.title("Grade Distribution"); plt.xlabel("Grade"); plt.ylabel("Students")
plt.tight_layout(); plt.savefig(OUT/"grade_distribution_chart.png",dpi=140); plt.close()

data["Result"].value_counts().reindex(["Pass","Fail"],fill_value=0).plot(kind="bar",figsize=(6,4))
plt.title("Pass/Fail Distribution"); plt.xlabel("Result"); plt.ylabel("Students")
plt.tight_layout(); plt.savefig(OUT/"pass_fail_chart.png",dpi=140); plt.close()

plt.figure(figsize=(7,5))
plt.scatter(data["Attendance_Percentage"],data["Percentage"],alpha=.8)
plt.title("Attendance vs Overall Percentage"); plt.xlabel("Attendance (%)"); plt.ylabel("Percentage (%)")
plt.xlim(0,100); plt.ylim(0,100); plt.tight_layout()
plt.savefig(OUT/"attendance_vs_percentage.png",dpi=140); plt.close()

print("\\nSubject averages:\\n", data[SUBJECTS].mean().round(2).sort_values(ascending=False))
print("\\nGrade distribution:\\n", grade_counts)
print("\\nPass/fail:\\n", result_counts)
print(f"\\nAttendance/percentage correlation: {corr:.3f}")
print("Files saved in:", OUT)
