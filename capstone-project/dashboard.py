# energy_dashboard.py
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

DATA_DIR = "data"
OUTPUT_DIR = "output"


# ------------------------------------------------------------
# TASK 0 – AUTO-CREATE SAMPLE CSV FILES
# ------------------------------------------------------------
def create_sample_csvs():
    os.makedirs(DATA_DIR, exist_ok=True)

    # Library building data
    library_data = """timestamp,kwh,building
2024-01-01 10:00,12,Library
2024-01-01 14:00,15,Library
2024-01-02 11:00,18,Library
2024-01-03 13:00,20,Library
"""

    # Admin building data
    admin_data = """timestamp,kwh,building
2024-01-01 09:00,25,Admin
2024-01-02 10:00,30,Admin
2024-01-03 11:00,22,Admin
2024-01-03 15:00,28,Admin
"""

    with open(f"{DATA_DIR}/library.csv", "w") as f:
        f.write(library_data)

    with open(f"{DATA_DIR}/admin.csv", "w") as f:
        f.write(admin_data)

    print("[INFO] Sample CSV files created.\n")


# ------------------------------------------------------------
# TASK 3 – OOP MODELING
# ------------------------------------------------------------

class Building:
    """Stores readings for each building."""

    def __init__(self, name):
        self.name = name
        self.readings = []  # list → (timestamp, kwh)

    def add_reading(self, timestamp, kwh):
        self.readings.append((timestamp, kwh))

    def total_consumption(self):
        return sum(kwh for _, kwh in self.readings)

    def average_consumption(self):
        if len(self.readings) == 0:
            return 0
        return self.total_consumption() / len(self.readings)

    def report(self):
        return (
            f"Building: {self.name}\n"
            f"Total Consumption: {self.total_consumption()} kWh\n"
            f"Average Consumption: {self.average_consumption():.2f} kWh\n"
        )


class BuildingManager:
    """Stores building objects and generates reports."""

    def __init__(self):
        self.buildings = {}

    def add_record(self, building_name, timestamp, kwh):
        if building_name not in self.buildings:
            self.buildings[building_name] = Building(building_name)
        self.buildings[building_name].add_reading(timestamp, kwh)

    def full_report(self):
        text = "\n=== BUILDING REPORTS ===\n"
        for b in self.buildings.values():
            text += b.report() + "\n"
        return text


# ------------------------------------------------------------
# TASK 1 – DATA INGESTION + VALIDATION
# ------------------------------------------------------------
def read_all_csv():
    frames = []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            try:
                df = pd.read_csv(f"{DATA_DIR}/{file}")
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                frames.append(df)
            except Exception as e:
                print(f"[ERROR] Failed to read {file}: {e}")

    if not frames:
        print("[ERROR] No CSV files found.")
        return pd.DataFrame()

    final_df = pd.concat(frames, ignore_index=True)
    return final_df


# ------------------------------------------------------------
# TASK 2 – AGGREGATION FUNCTIONS
# ------------------------------------------------------------
def daily_totals(df):
    df = df.copy()
    df["date"] = df["timestamp"].dt.date
    return df.groupby(["building", "date"])["kwh"].sum().reset_index()


def weekly_totals(df):
    df = df.copy()
    df["week"] = df["timestamp"].dt.isocalendar().week
    return df.groupby(["building", "week"])["kwh"].sum().reset_index()


def building_summary(df):
    return df.groupby("building")["kwh"].agg(["mean", "min", "max", "sum"]).reset_index()


# ------------------------------------------------------------
# TASK 4 – VISUAL DASHBOARD
# ------------------------------------------------------------
def create_dashboard(df):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    plt.figure(figsize=(8, 5))

    for building, group in df.groupby("building"):
        plt.plot(group["timestamp"], group["kwh"], marker="o", label=building)

    plt.title("Energy Consumption Over Time")
    plt.xlabel("Time")
    plt.ylabel("kWh")
    plt.legend()
    plt.tight_layout()

    path = f"{OUTPUT_DIR}/dashboard.png"
    plt.savefig(path)
    plt.close()

    print(f"[INFO] Dashboard saved to {path}")


# ------------------------------------------------------------
# TASK 5 – DATA EXPORT & SUMMARY
# ------------------------------------------------------------
def save_outputs(df, daily, weekly, manager):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df.to_csv(f"{OUTPUT_DIR}/cleaned_data.csv", index=False)
    daily.to_csv(f"{OUTPUT_DIR}/daily_totals.csv", index=False)
    weekly.to_csv(f"{OUTPUT_DIR}/weekly_totals.csv", index=False)

    # Generate summary text
    highest_building = df.groupby("building")["kwh"].sum().idxmax()
    peak = df.loc[df["kwh"].idxmax()]

    summary = f"""
===============================
  CAMPUS ENERGY SUMMARY REPORT
===============================

Total Campus Consumption: {df['kwh'].sum()} kWh

Highest Consuming Building:
• {highest_building}
• {df.groupby('building')['kwh'].sum().max()} kWh

Peak Usage:
• Building: {peak['building']}
• Time: {peak['timestamp']}
• kWh: {peak['kwh']}

{manager.full_report()}
"""

    with open(f"{OUTPUT_DIR}/summary.txt", "w") as f:
        f.write(summary)

    print("[INFO] Summary saved to output/summary.txt")


# ------------------------------------------------------------
# MAIN PROGRAM
# ------------------------------------------------------------
def main():
    print("=== CAMPUS ENERGY DASHBOARD (FINAL ASSIGNMENT) ===\n")

    create_sample_csvs()

    df = read_all_csv()
    print(df)

    # Build OOP manager
    manager = BuildingManager()
    for _, row in df.iterrows():
        manager.add_record(row["building"], row["timestamp"], row["kwh"])

    # Aggregations
    daily = daily_totals(df)
    weekly = weekly_totals(df)

    # Graph
    create_dashboard(df)

    # Exports
    save_outputs(df, daily, weekly, manager)

    print("\n=== COMPLETED SUCCESSFULLY ===")


if __name__ == "__main__":
    main()
    