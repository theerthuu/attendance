import csv
import os
from datetime import datetime

DATA_DIR = "data"
FILE_PATH = os.path.join(DATA_DIR, "attendance.csv")


# ---------------- FILE SETUP ----------------

def ensure_file():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Subject", "Status"])


def load_data():
    ensure_file()
    with open(FILE_PATH, "r") as f:
        return list(csv.DictReader(f))


def pause():
    input("\nPress Enter to continue...")


def percentage(p, t):
    return round((p / t) * 100, 2) if t else 0.0


# ---------------- ADD ATTENDANCE ----------------

def add_attendance():
    date = input("Enter date (YYYY-MM-DD) [Enter = today]: ").strip()
    if not date:
        date = datetime.today().strftime("%Y-%m-%d")

    subject = input("Enter subject: ").strip()
    status = input("Present or Absent (P/A): ").upper().strip()

    if status not in ["P", "A"]:
        print("❌ Invalid status")
        pause()
        return

    ensure_file()
    with open(FILE_PATH, "a", newline="") as f:
        csv.writer(f).writerow([date, subject, status])

    print("✅ Attendance recorded")
    pause()


# ---------------- SUMMARY LOGIC ----------------

def overall_summary(data):
    p = sum(1 for r in data if r["Status"] == "P")
    a = sum(1 for r in data if r["Status"] == "A")
    t = p + a

    print("\n📊 OVERALL ATTENDANCE")
    print(f"Present : {p}")
    print(f"Absent  : {a}")
    print(f"Percent : {percentage(p, t)}%")


def subject_summary(data):
    print("\n📚 SUBJECT-WISE ATTENDANCE")
    subjects = {}

    for r in data:
        s = r["Subject"]
        subjects.setdefault(s, {"P": 0, "A": 0})
        subjects[s][r["Status"]] += 1

    for s, d in subjects.items():
        t = d["P"] + d["A"]
        print(f"{s} → P:{d['P']} A:{d['A']} %:{percentage(d['P'], t)}%")


def monthly_summary(data):
    month = input("\nEnter month (YYYY-MM): ").strip()
    filtered = [r for r in data if r["Date"].startswith(month)]

    if not filtered:
        print("⚠️ No data for this month")
        return

    print(f"\n📅 MONTHLY SUMMARY ({month})")
    overall_summary(filtered)


def subject_monthly_summary(data):
    month = input("\nEnter month (YYYY-MM): ").strip()
    filtered = [r for r in data if r["Date"].startswith(month)]

    if not filtered:
        print("⚠️ No data for this month")
        return

    print(f"\n📅 SUBJECT-WISE MONTHLY ({month})")
    subject_summary(filtered)


def target_analysis(data):
    try:
        target = float(input("\nEnter target percentage: "))
    except ValueError:
        print("❌ Invalid number")
        return

    subjects = {}

    for r in data:
        s = r["Subject"]
        subjects.setdefault(s, {"P": 0, "A": 0})
        subjects[s][r["Status"]] += 1

    print("\n🎯 TARGET ANALYSIS")

    for s, d in subjects.items():
        p, a = d["P"], d["A"]
        t = p + a
        cur = percentage(p, t)

        if cur >= target:
            print(f"{s}: ✅ Target achieved ({cur}%)")
        else:
            needed = 0
            while percentage(p + needed, t + needed) < target:
                needed += 1
            print(f"{s}: Attend next {needed} classes to reach {target}%")


# ---------------- SUMMARY MENU ----------------

def summary_menu():
    data = load_data()

    if not data:
        print("⚠️ No attendance data available")
        pause()
        return

    while True:
        print("\n===== SUMMARY MENU =====")
        print("1. Overall Summary")
        print("2. Subject-wise Summary")
        print("3. Monthly Summary")
        print("4. Subject-wise Monthly Summary")
        print("5. Target Analysis")
        print("6. Back")

        choice = input("Choose option: ").strip()

        if choice == "1":
            overall_summary(data)
        elif choice == "2":
            subject_summary(data)
        elif choice == "3":
            monthly_summary(data)
        elif choice == "4":
            subject_monthly_summary(data)
        elif choice == "5":
            target_analysis(data)
        elif choice == "6":
            return
        else:
            print("❌ Invalid choice")

        pause()


# ---------------- RESET DATA ----------------

def reset_data():
    confirm = input("Delete ALL attendance data? (yes/no): ").lower()
    if confirm == "yes" and os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)
        print("🗑️ Data deleted")
    pause()


# ---------------- MAIN ----------------

def main():
    while True:
        print("\n===== ATTENDANCE TRACKER =====")
        print("1. Add Attendance")
        print("2. View Summary")
        print("3. Reset Data")
        print("4. Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            add_attendance()
        elif choice == "2":
            summary_menu()
        elif choice == "3":
            reset_data()
        elif choice == "4":
            print("👋 Goodbye")
            break
        else:
            print("❌ Invalid choice")
            pause()


if __name__ == "__main__":
    main()
