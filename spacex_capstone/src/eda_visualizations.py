import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "figure.titlesize": 14
})

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "dataset_part_2.csv")
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")

def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Year"] = pd.to_datetime(df["Date"]).dt.year
    return df

def plot_flight_vs_launchsite(df):
    plt.figure(figsize=(10, 5))
    sns.scatterplot(
        data=df,
        x="FlightNumber",
        y="LaunchSite",
        hue="Class",
        palette={0: "#d9534f", 1: "#2ca02c"},
        s=80,
        alpha=0.85
    )
    plt.title("Flight Number vs Launch Site (Class 0: Failed, 1: Success)")
    plt.xlabel("Flight Number")
    plt.ylabel("Launch Site")
    plt.legend(title="Outcome", labels=["Failure (0)", "Success (1)"])
    plt.tight_layout()
    out = os.path.join(FIGURES_DIR, "eda_flight_vs_launchsite.png")
    plt.savefig(out, dpi=300)
    plt.close()

def plot_payload_vs_launchsite(df):
    plt.figure(figsize=(10, 5))
    sns.scatterplot(
        data=df,
        x="PayloadMass",
        y="LaunchSite",
        hue="Class",
        palette={0: "#d9534f", 1: "#2ca02c"},
        s=80,
        alpha=0.85
    )
    plt.title("Payload Mass (kg) vs Launch Site")
    plt.xlabel("Payload Mass (kg)")
    plt.ylabel("Launch Site")
    plt.legend(title="Outcome", labels=["Failure (0)", "Success (1)"])
    plt.tight_layout()
    out = os.path.join(FIGURES_DIR, "eda_payload_vs_launchsite.png")
    plt.savefig(out, dpi=300)
    plt.close()

def plot_success_by_orbit(df):
    plt.figure(figsize=(10, 5))
    orbit_success = df.groupby("Orbit")["Class"].mean().reset_index()
    orbit_success = orbit_success.sort_values(by="Class", ascending=False)
    
    palette = ["#2ca02c" if val >= 0.7 else "#f0ad4e" if val >= 0.5 else "#d9534f" for val in orbit_success["Class"]]
    sns.barplot(data=orbit_success, x="Orbit", y="Class", palette=palette)
    plt.title("Success Rate by Orbit Type")
    plt.xlabel("Orbit Type")
    plt.ylabel("Success Rate")
    plt.ylim(0, 1.05)
    for idx, row in enumerate(orbit_success.itertuples()):
        plt.text(idx, row.Class + 0.02, f"{row.Class:.2f}", ha="center", fontsize=9)
    plt.tight_layout()
    out = os.path.join(FIGURES_DIR, "eda_success_by_orbit.png")
    plt.savefig(out, dpi=300)
    plt.close()

def plot_flight_vs_orbit(df):
    plt.figure(figsize=(10, 5))
    sns.scatterplot(
        data=df,
        x="FlightNumber",
        y="Orbit",
        hue="Class",
        palette={0: "#d9534f", 1: "#2ca02c"},
        s=80,
        alpha=0.85
    )
    plt.title("Flight Number vs Orbit Type")
    plt.xlabel("Flight Number")
    plt.ylabel("Orbit Type")
    plt.legend(title="Outcome", labels=["Failure (0)", "Success (1)"])
    plt.tight_layout()
    out = os.path.join(FIGURES_DIR, "eda_flight_vs_orbit.png")
    plt.savefig(out, dpi=300)
    plt.close()

def plot_payload_vs_orbit(df):
    plt.figure(figsize=(10, 5))
    sns.scatterplot(
        data=df,
        x="PayloadMass",
        y="Orbit",
        hue="Class",
        palette={0: "#d9534f", 1: "#2ca02c"},
        s=80,
        alpha=0.85
    )
    plt.title("Payload Mass vs Orbit Type")
    plt.xlabel("Payload Mass (kg)")
    plt.ylabel("Orbit Type")
    plt.legend(title="Outcome", labels=["Failure (0)", "Success (1)"])
    plt.tight_layout()
    out = os.path.join(FIGURES_DIR, "eda_payload_vs_orbit.png")
    plt.savefig(out, dpi=300)
    plt.close()

def plot_yearly_trend(df):
    plt.figure(figsize=(10, 5))
    yearly = df.groupby("Year")["Class"].mean().reset_index()
    sns.lineplot(data=yearly, x="Year", y="Class", marker="o", color="#1f77b4", linewidth=2.5, markersize=7)
    plt.title("Yearly Launch Success Rate Trend (2010 - 2020)")
    plt.xlabel("Year")
    plt.ylabel("Success Rate")
    plt.ylim(0, 1.05)
    for _, row in yearly.iterrows():
        plt.text(row["Year"], row["Class"] + 0.03, f"{row['Class']:.2f}", ha="center", fontsize=9)
    plt.tight_layout()
    out = os.path.join(FIGURES_DIR, "eda_yearly_trend.png")
    plt.savefig(out, dpi=300)
    plt.close()

def main():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    df = load_data()
    plot_flight_vs_launchsite(df)
    plot_payload_vs_launchsite(df)
    plot_success_by_orbit(df)
    plot_flight_vs_orbit(df)
    plot_payload_vs_orbit(df)
    plot_yearly_trend(df)
    print("EDA visualization plots generated successfully.")

if __name__ == "__main__":
    main()

