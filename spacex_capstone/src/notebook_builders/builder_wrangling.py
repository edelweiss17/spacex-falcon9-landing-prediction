import os
import nbformat as nbf

def build_wrangling_notebook(output_dir):
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell(
            "# SpaceX Falcon 9 Data Wrangling\n"
            "This notebook cleans raw launch data, imputes missing payload values, "
            "categorizes landing outcomes, and constructs the binary classification target `Class`."
        ),
        nbf.v4.new_code_cell(
            "import pandas as pd\n"
            "import numpy as np\n\n"
            "df = pd.read_csv('../data/dataset_part_1.csv')\n"
            "print('Loaded dataset shape:', df.shape)\n"
            "df.head(5)"
        ),
        nbf.v4.new_markdown_cell(
            "## 1. Missing Value Analysis & Imputation\n"
            "Check null values in the dataset and impute missing `PayloadMass` values with the column mean."
        ),
        nbf.v4.new_code_cell(
            "print('Null values count:')\n"
            "print(df.isnull().sum())\n\n"
            "mean_payload = df['PayloadMass'].mean()\n"
            "df['PayloadMass'] = df['PayloadMass'].fillna(mean_payload)\n"
            "print(f'\\nImputed missing PayloadMass with mean: {mean_payload:.2f} kg')\n"
            "print('Remaining nulls in PayloadMass:', df['PayloadMass'].isnull().sum())"
        ),
        nbf.v4.new_markdown_cell(
            "## 2. Launch Site and Orbit Distribution\n"
            "Analyze mission counts by launch complex and orbital target."
        ),
        nbf.v4.new_code_cell(
            "print('Launch Site Distribution:')\n"
            "print(df['LaunchSite'].value_counts())\n\n"
            "print('\\nOrbit Target Distribution:')\n"
            "print(df['Orbit'].value_counts())"
        ),
        nbf.v4.new_markdown_cell(
            "## 3. Landing Outcome Categorization\n"
            "The `Outcome` column records landing type and success status. "
            "We map successful recoveries (`True Ocean`, `True RTLS`, `True ASDS`) to 1, and all failures/unattempted recoveries to 0."
        ),
        nbf.v4.new_code_cell(
            "landing_outcomes = df['Outcome'].value_counts()\n"
            "print('Outcome Frequency Breakdown:')\n"
            "print(landing_outcomes)\n\n"
            "successful_outcomes = {'True ASDS', 'True RTLS', 'True Ocean'}\n"
            "landing_class = [1 if outcome in successful_outcomes else 0 for outcome in df['Outcome']]\n"
            "df['Class'] = landing_class\n\n"
            "print(f'\\nOverall Landing Success Rate: {df[\"Class\"].mean() * 100:.2f}%')\n"
            "print(df['Class'].value_counts())"
        ),
        nbf.v4.new_markdown_cell(
            "## 4. Export Cleaned Dataset\n"
            "Verify and save as `dataset_part_2.csv`."
        ),
        nbf.v4.new_code_cell(
            "df.to_csv('../data/dataset_part_2.csv', index=False)\n"
            "print('Saved dataset_part_2.csv successfully. Shape:', df.shape)"
        )
    ]
    path = os.path.join(output_dir, "02_spacex_data_wrangling.ipynb")
    with open(path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    return path

