import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "spacex_launch_dash.csv")
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")

def main():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    df = pd.read_csv(DATA_PATH)

    # 1. Pie charts: All sites & Best site (KSC LC-39A)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # All sites: Success share by launch site
    site_success = df[df["class"] == 1]["Launch Site"].value_counts()
    axes[0].pie(site_success, labels=site_success.index, autopct="%1.1f%%", startangle=140,
                colors=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"])
    axes[0].set_title("Total Successful Launches by Site", fontsize=12, fontweight="bold")

    # Site-specific: KSC LC-39A success vs failure
    ksc_df = df[df["Launch Site"] == "KSC LC-39A"]["class"].value_counts().rename({1: "Success", 0: "Failure"})
    axes[1].pie(ksc_df, labels=ksc_df.index, autopct="%1.1f%%", startangle=90, colors=["#2ca02c", "#d9534f"])
    axes[1].set_title("Success vs Failure for KSC LC-39A (Highest Success Rate)", fontsize=12, fontweight="bold")

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "dash_pie_charts.png"), dpi=300)
    plt.close()

    # 2. Scatter plot: Payload vs Launch Outcome colored by Booster Version Category
    plt.figure(figsize=(10, 5.5))
    sns.scatterplot(
        data=df,
        x="Payload Mass (kg)",
        y="class",
        hue="Booster Version Category",
        palette="tab10",
        s=90,
        alpha=0.85
    )
    plt.title("Correlation between Payload Mass and Success Outcome (Colored by Booster Version Category)", fontsize=12, fontweight="bold")
    plt.xlabel("Payload Mass (kg)")
    plt.ylabel("Launch Outcome (0: Failure, 1: Success)")
    plt.yticks([0, 1], ["Failure (0)", "Success (1)"])
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "dash_payload_scatter.png"), dpi=300)
    plt.close()

    print("Dash preview charts saved successfully.")

if __name__ == "__main__":
    main()

