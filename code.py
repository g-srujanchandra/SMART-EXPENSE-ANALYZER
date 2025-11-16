import pandas as pd
from pathlib import Path

# -------- SAFE PATH HANDLING --------
BASE_DIR = Path(__file__).parent
CSV_PATH = BASE_DIR / "expenses.csv"
REPORT_PATH = BASE_DIR / "Expense_Report.txt"

# -------- CHECK CSV EXISTS --------
if not CSV_PATH.exists():
    raise FileNotFoundError(
        f"ERROR: Could not find 'expenses.csv'\n"
        f"Expected at: {CSV_PATH}\n"
        f"Make sure the file is inside the SAME folder as code.py"
    )

# -------- CATEGORY KEYWORDS --------
CATEGORIES = {
    "Food": ["swiggy", "zomato", "pizza", "hotel", "restaurant", "food"],
    "Transport": ["uber", "ola", "bus", "train", "petrol", "diesel"],
    "Utilities": ["electricity", "water", "recharge", "gas", "internet", "wifi"],
    "Shopping": ["amazon", "flipkart", "shopping", "store", "mall"],
    "Entertainment": ["netflix", "spotify", "movie", "gaming", "cinema"],
    "Other": []
}

# ---- FUNCTION: Auto categorize ----
def categorize(description):
    if pd.isna(description):
        return "Other"
    desc = description.lower()
    for category, keywords in CATEGORIES.items():
        if any(keyword in desc for keyword in keywords):
            return category
    return "Other"

# -------- LOAD CSV SAFELY --------
try:
    df = pd.read_csv(CSV_PATH)
except Exception as e:
    raise ValueError(f"Failed to read CSV file: {e}")

# -------- CHECK REQUIRED COLUMNS --------
required_columns = {"Description", "Amount"}
if not required_columns.issubset(df.columns):
    raise ValueError(
        f"CSV format incorrect!\nRequired columns: {required_columns}\nFound columns: {list(df.columns)}"
    )

# ---- Add categories ----
df["Category"] = df["Description"].apply(categorize)

# ---- Calculate totals ----
total_expense = df["Amount"].sum()
category_totals = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

# ---- Find highest spending category ----
highest_category = category_totals.idxmax()

# ---- Prediction Model ----
daily_avg = df["Amount"].mean()
predicted_monthly = round(daily_avg * 30, 2)

# ---- AI FEEDBACK LOGIC ----
feedback = []

category_advice = {
    "Food": "You are spending the most on food. Try cooking more often!",
    "Shopping": "Your shopping expenses are high. Try reducing impulse buys.",
    "Entertainment": "Entertainment is taking a major share. Cut unused subscriptions.",
    "Transport": "Transport spending is high. Consider shared rides or public transport.",
    "Utilities": "Utility bills seem heavy. Review usage or switch cheaper plans."
}

feedback.append(category_advice.get(highest_category, "You are spending wisely!"))

if predicted_monthly > 10000:
    feedback.append("⚠ Warning: You may cross ₹10,000 this month!")
else:
    feedback.append("✔ Spending is under control. Keep it up!")

# -------- EXPORT REPORT --------
with open(REPORT_PATH, "w", encoding="utf-8") as file:
    file.write("******** SMART EXPENSE ANALYZER REPORT ********\n\n")
    file.write(f"Total Spent: ₹{total_expense}\n")
    file.write(f"Highest Spending Category: {highest_category}\n\n")

    file.write("----- Category Wise Breakdown -----\n")
    for cat, amount in category_totals.items():
        file.write(f"{cat:15} : ₹{amount}\n")

    file.write("\nPredicted Monthly Expense: ₹" + str(predicted_monthly) + "\n\n")

    file.write("----- AI Suggestions -----\n")
    for tip in feedback:
        file.write("- " + tip + "\n")

print(f"Analysis Complete! Report generated at:\n{REPORT_PATH}")
