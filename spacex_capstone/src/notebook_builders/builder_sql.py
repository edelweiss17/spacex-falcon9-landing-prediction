import os
import nbformat as nbf

def build_sql_notebook(output_dir):
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell(
            "# SpaceX Falcon 9 Exploratory Data Analysis with SQL\n"
            "This notebook executes all 10 standard SQL analysis queries on the historical SpaceX launch table (`SPACEXTBL`) using SQLite."
        ),
        nbf.v4.new_code_cell(
            "import sqlite3\n"
            "import pandas as pd\n\n"
            "# Load CSV and normalize column names for SQL compatibility\n"
            "df = pd.read_csv('../data/Spacex.csv')\n"
            "df.columns = [c.strip().replace(' ', '_').replace('(', '').replace(')', '').replace('__', '_') for c in df.columns]\n\n"
            "conn = sqlite3.connect(':memory:')\n"
            "df.to_sql('SPACEXTBL', conn, if_exists='replace', index=False)\n"
            "print('Loaded SPACEXTBL into SQLite in-memory database with', len(df), 'rows.')"
        ),
        nbf.v4.new_markdown_cell(
            "## Query 1: Distinct Launch Sites\n"
            "Names of unique launch sites in the SpaceX dataset."
        ),
        nbf.v4.new_code_cell(
            "q1 = pd.read_sql_query('SELECT DISTINCT Launch_Site FROM SPACEXTBL', conn)\n"
            "q1"
        ),
        nbf.v4.new_markdown_cell(
            "## Query 2: Launch Sites Beginning with 'CCA'\n"
            "First 5 launch records where launch site begins with 'CCA'."
        ),
        nbf.v4.new_code_cell(
            "q2 = pd.read_sql_query(\"SELECT Launch_Site FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' LIMIT 5\", conn)\n"
            "q2"
        ),
        nbf.v4.new_markdown_cell(
            "## Query 3: Total Payload Carried by NASA (CRS)\n"
            "Total payload mass delivered by boosters launched for customer NASA (CRS)."
        ),
        nbf.v4.new_code_cell(
            "q3 = pd.read_sql_query(\"SELECT SUM(PAYLOAD_MASS_KG_) AS Total_Payload_Mass FROM SPACEXTBL WHERE Customer = 'NASA (CRS)'\", conn)\n"
            "q3"
        ),
        nbf.v4.new_markdown_cell(
            "## Query 4: Average Payload Carried by Booster Version F9 v1.1\n"
            "Average payload mass carried by F9 v1.1 booster versions."
        ),
        nbf.v4.new_code_cell(
            "q4 = pd.read_sql_query(\"SELECT AVG(PAYLOAD_MASS_KG_) AS Avg_Payload_Mass FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1%'\", conn)\n"
            "q4"
        ),
        nbf.v4.new_markdown_cell(
            "## Query 5: Date of First Successful Ground Landing\n"
            "Earliest successful landing outcome on ground pad."
        ),
        nbf.v4.new_code_cell(
            "q5 = pd.read_sql_query(\"SELECT MIN(Date) AS First_Successful_Ground_Landing FROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)'\", conn)\n"
            "q5"
        ),
        nbf.v4.new_markdown_cell(
            "## Query 6: Boosters with Drone Ship Success & 4000-6000 kg Payload\n"
            "Booster versions that achieved successful drone ship landing with payload between 4000 and 6000 kg."
        ),
        nbf.v4.new_code_cell(
            "q6 = pd.read_sql_query(\"SELECT Booster_Version, PAYLOAD_MASS_KG_ FROM SPACEXTBL WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS_KG_ BETWEEN 4000 AND 6000\", conn)\n"
            "q6"
        ),
        nbf.v4.new_markdown_cell(
            "## Query 7: Total Successful and Failed Mission Outcomes\n"
            "Frequency count of successful versus failed mission outcomes."
        ),
        nbf.v4.new_code_cell(
            "q7 = pd.read_sql_query('SELECT Mission_Outcome, COUNT(*) AS Count FROM SPACEXTBL GROUP BY Mission_Outcome', conn)\n"
            "q7"
        ),
        nbf.v4.new_markdown_cell(
            "## Query 8: Booster Versions with Maximum Payload Mass\n"
            "Boosters that carried the maximum payload mass recorded."
        ),
        nbf.v4.new_code_cell(
            "q8 = pd.read_sql_query('SELECT Booster_Version, PAYLOAD_MASS_KG_ FROM SPACEXTBL WHERE PAYLOAD_MASS_KG_ = (SELECT MAX(PAYLOAD_MASS_KG_) FROM SPACEXTBL)', conn)\n"
            "q8"
        ),
        nbf.v4.new_markdown_cell(
            "## Query 9: Drone Ship Landing Failures in 2015\n"
            "Records of failed drone ship landings during calendar year 2015."
        ),
        nbf.v4.new_code_cell(
            "q9 = pd.read_sql_query(\"SELECT SUBSTR(Date, 6, 2) AS Month, Landing_Outcome, Booster_Version, Launch_Site FROM SPACEXTBL WHERE Landing_Outcome = 'Failure (drone ship)' AND SUBSTR(Date, 1, 4) = '2015'\", conn)\n"
            "q9"
        ),
        nbf.v4.new_markdown_cell(
            "## Query 10: Landing Outcome Rankings (2010-06-04 to 2017-03-20)\n"
            "Ranking of landing outcomes between specified dates in descending order of frequency."
        ),
        nbf.v4.new_code_cell(
            "q10 = pd.read_sql_query(\"SELECT Landing_Outcome, COUNT(*) AS Count FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY Count DESC\", conn)\n"
            "q10"
        )
    ]
    path = os.path.join(output_dir, "03_spacex_eda_sql.ipynb")
    with open(path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    return path

