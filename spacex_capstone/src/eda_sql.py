import os
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "Spacex.csv")
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")

def setup_database():
    df = pd.read_csv(DATA_PATH)
    # Match standard column naming
    df.columns = [c.strip().replace(" ", "_").replace("(", "").replace(")", "").replace("__", "_") for c in df.columns]
    
    conn = sqlite3.connect(":memory:")
    df.to_sql("SPACEXTBL", conn, if_exists="replace", index=False)
    return conn

def execute_queries(conn):
    queries = {
        "Q1": (
            "Display distinct launch sites",
            "SELECT DISTINCT Launch_Site FROM SPACEXTBL"
        ),
        "Q2": (
            "5 records where launch sites begin with 'CCA'",
            "SELECT Launch_Site FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' LIMIT 5"
        ),
        "Q3": (
            "Total payload mass carried by boosters launched by NASA (CRS)",
            "SELECT SUM(PAYLOAD_MASS_KG_) AS Total_Payload_Mass FROM SPACEXTBL WHERE Customer = 'NASA (CRS)'"
        ),
        "Q4": (
            "Average payload mass carried by booster version F9 v1.1",
            "SELECT AVG(PAYLOAD_MASS_KG_) AS Avg_Payload_Mass FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1%'"
        ),
        "Q5": (
            "Date of the first successful landing outcome on ground pad",
            "SELECT MIN(Date) AS First_Successful_Ground_Landing FROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)'"
        ),
        "Q6": (
            "Boosters with drone ship success and payload between 4000 and 6000 kg",
            "SELECT Booster_Version FROM SPACEXTBL WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS_KG_ BETWEEN 4000 AND 6000"
        ),
        "Q7": (
            "Total number of successful and failure mission outcomes",
            "SELECT Mission_Outcome, COUNT(*) AS Total FROM SPACEXTBL GROUP BY Mission_Outcome"
        ),
        "Q8": (
            "Booster versions that carried the maximum payload mass",
            "SELECT Booster_Version, PAYLOAD_MASS_KG_ FROM SPACEXTBL WHERE PAYLOAD_MASS_KG_ = (SELECT MAX(PAYLOAD_MASS_KG_) FROM SPACEXTBL)"
        ),
        "Q9": (
            "Failure landing outcomes on drone ship, booster versions, and launch site for 2015",
            "SELECT substr(Date, 6, 2) AS Month, Booster_Version, Launch_Site, Landing_Outcome FROM SPACEXTBL WHERE Landing_Outcome = 'Failure (drone ship)' AND substr(Date, 1, 4) = '2015'"
        ),
        "Q10": (
            "Rank landing outcomes between 2010-06-04 and 2017-03-20 in descending order",
            "SELECT Landing_Outcome, COUNT(*) AS Count FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY Count DESC"
        ),
    }

    results = {}
    for key, (desc, query) in queries.items():
        res_df = pd.read_sql_query(query, conn)
        results[key] = {
            "description": desc,
            "query": query,
            "result": res_df
        }
    return results

def render_summary_images(results):
    os.makedirs(FIGURES_DIR, exist_ok=True)
    
    # Render Part 1: Q1 to Q5
    fig, axes = plt.subplots(5, 1, figsize=(11, 8.5))
    fig.suptitle("SQL Analysis Results - Part 1 (Queries 1 to 5)", fontsize=14, fontweight="bold", y=0.98)
    
    for i, q_key in enumerate(["Q1", "Q2", "Q3", "Q4", "Q5"]):
        ax = axes[i]
        ax.axis("off")
        item = results[q_key]
        rdf = item["result"]
        
        # Display description and SQL
        text_header = f"{q_key}: {item['description']}\nSQL: {item['query']}"
        ax.text(0.01, 0.95, text_header, fontsize=9.5, fontweight="bold", verticalalignment="top", fontfamily="sans-serif")
        
        # Render table
        table_data = [rdf.columns.tolist()] + rdf.values.tolist()
        t = ax.table(cellText=table_data, loc="center", cellLoc="center", bbox=[0.05, 0.05, 0.9, 0.55])
        t.auto_set_font_size(False)
        t.set_fontsize(8.5)
        for c in range(len(rdf.columns)):
            t[0, c].set_facecolor("#203864")
            t[0, c].set_text_props(color="white", weight="bold")
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(FIGURES_DIR, "sql_results_part1.png"), dpi=300)
    plt.close()

    # Render Part 2: Q6 to Q10
    fig, axes = plt.subplots(5, 1, figsize=(11, 9))
    fig.suptitle("SQL Analysis Results - Part 2 (Queries 6 to 10)", fontsize=14, fontweight="bold", y=0.98)
    
    for i, q_key in enumerate(["Q6", "Q7", "Q8", "Q9", "Q10"]):
        ax = axes[i]
        ax.axis("off")
        item = results[q_key]
        rdf = item["result"]
        
        text_header = f"{q_key}: {item['description']}\nSQL: {item['query']}"
        ax.text(0.01, 0.95, text_header, fontsize=9.5, fontweight="bold", verticalalignment="top", fontfamily="sans-serif")
        
        table_data = [rdf.columns.tolist()] + rdf.head(6).values.tolist()
        t = ax.table(cellText=table_data, loc="center", cellLoc="center", bbox=[0.05, 0.05, 0.9, 0.55])
        t.auto_set_font_size(False)
        t.set_fontsize(8.5)
        for c in range(len(rdf.columns)):
            t[0, c].set_facecolor("#203864")
            t[0, c].set_text_props(color="white", weight="bold")
            
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(FIGURES_DIR, "sql_results_part2.png"), dpi=300)
    plt.close()

def main():
    conn = setup_database()
    results = execute_queries(conn)
    for k, v in results.items():
        print(f"=== {k}: {v['description']} ===")
        print(v["result"])
        print()
    render_summary_images(results)
    conn.close()
    print("SQL execution and result tables rendered successfully.")

if __name__ == "__main__":
    main()

