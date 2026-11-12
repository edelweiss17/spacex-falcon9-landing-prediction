import os
import nbformat as nbf

def build_viz_notebook(output_dir):
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell(
            "# SpaceX Falcon 9 Exploratory Data Analysis with Data Visualization\n"
            "This notebook explores relationships between flight parameters, orbits, launch sites, and booster landing success, "
            "followed by one-hot encoding feature preparation."
        ),
        nbf.v4.new_code_cell(
            "import pandas as pd\n"
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            "import seaborn as sns\n\n"
            "df = pd.read_csv('../data/dataset_part_2.csv')\n"
            "print('Loaded dataset shape:', df.shape)\n"
            "df.head(3)"
        ),
        nbf.v4.new_markdown_cell(
            "## 1. Flight Number vs. Launch Site\n"
            "Scatter plot of Flight Number vs Launch Site with landing success hue."
        ),
        nbf.v4.new_code_cell(
            "plt.figure(figsize=(11, 5))\n"
            "sns.scatterplot(data=df, x='FlightNumber', y='LaunchSite', hue='Class', palette={0: '#d9534f', 1: '#2ca02c'}, s=80)\n"
            "plt.title('Flight Number vs Launch Site', fontsize=13, fontweight='bold')\n"
            "plt.xlabel('Flight Number', fontsize=11)\n"
            "plt.ylabel('Launch Site', fontsize=11)\n"
            "plt.legend(title='Class', labels=['Failed (0)', 'Success (1)'])\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "## 2. Payload Mass vs. Launch Site\n"
            "Scatter plot of Payload Mass vs Launch Site."
        ),
        nbf.v4.new_code_cell(
            "plt.figure(figsize=(11, 5))\n"
            "sns.scatterplot(data=df, x='PayloadMass', y='LaunchSite', hue='Class', palette={0: '#d9534f', 1: '#2ca02c'}, s=80)\n"
            "plt.title('Payload Mass vs Launch Site', fontsize=13, fontweight='bold')\n"
            "plt.xlabel('Payload Mass (kg)', fontsize=11)\n"
            "plt.ylabel('Launch Site', fontsize=11)\n"
            "plt.legend(title='Class', labels=['Failed (0)', 'Success (1)'])\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "## 3. Success Rate by Orbit Type\n"
            "Bar chart showing landing success percentage across target orbits."
        ),
        nbf.v4.new_code_cell(
            "orbit_success = df.groupby('Orbit')['Class'].mean().reset_index().sort_values(by='Class', ascending=False)\n"
            "plt.figure(figsize=(11, 5))\n"
            "sns.barplot(data=orbit_success, x='Orbit', y='Class', palette='Blues_r')\n"
            "plt.title('Landing Success Rate by Target Orbit', fontsize=13, fontweight='bold')\n"
            "plt.xlabel('Orbit', fontsize=11)\n"
            "plt.ylabel('Success Rate', fontsize=11)\n"
            "plt.ylim(0, 1.1)\n"
            "for i, r in orbit_success.iterrows():\n"
            "    plt.text(orbit_success.index.get_loc(i), r['Class'] + 0.03, f\"{r['Class']*100:.0f}%\", ha='center', fontsize=9)\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "## 4. Flight Number vs. Orbit Type\n"
            "Scatter plot showing how target orbits evolved across cumulative flight experience."
        ),
        nbf.v4.new_code_cell(
            "plt.figure(figsize=(11, 5))\n"
            "sns.scatterplot(data=df, x='FlightNumber', y='Orbit', hue='Class', palette={0: '#d9534f', 1: '#2ca02c'}, s=80)\n"
            "plt.title('Flight Number vs Orbit Type', fontsize=13, fontweight='bold')\n"
            "plt.xlabel('Flight Number', fontsize=11)\n"
            "plt.ylabel('Orbit', fontsize=11)\n"
            "plt.legend(title='Class', labels=['Failed (0)', 'Success (1)'])\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "## 5. Payload Mass vs. Orbit Type\n"
            "Scatter plot analyzing payload mass distribution per orbital profile."
        ),
        nbf.v4.new_code_cell(
            "plt.figure(figsize=(11, 5))\n"
            "sns.scatterplot(data=df, x='PayloadMass', y='Orbit', hue='Class', palette={0: '#d9534f', 1: '#2ca02c'}, s=80)\n"
            "plt.title('Payload Mass vs Orbit Type', fontsize=13, fontweight='bold')\n"
            "plt.xlabel('Payload Mass (kg)', fontsize=11)\n"
            "plt.ylabel('Orbit', fontsize=11)\n"
            "plt.legend(title='Class', labels=['Failed (0)', 'Success (1)'])\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "## 6. Yearly Launch Success Trend\n"
            "Line chart tracking the annual trajectory of landing success rate from 2010 to 2020."
        ),
        nbf.v4.new_code_cell(
            "df['Year'] = pd.DatetimeIndex(df['Date']).year\n"
            "yearly_success = df.groupby('Year')['Class'].mean().reset_index()\n"
            "plt.figure(figsize=(11, 5))\n"
            "sns.lineplot(data=yearly_success, x='Year', y='Class', marker='o', color='#2b6cb0', lw=2.5)\n"
            "plt.title('Yearly First Stage Landing Success Rate Trend (2010-2020)', fontsize=13, fontweight='bold')\n"
            "plt.xlabel('Year', fontsize=11)\n"
            "plt.ylabel('Average Success Rate', fontsize=11)\n"
            "plt.ylim(-0.05, 1.05)\n"
            "plt.grid(True, alpha=0.3)\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "## 7. Feature Engineering & One-Hot Encoding\n"
            "Select analytical features and apply dummy encoding to categorical attributes."
        ),
        nbf.v4.new_code_cell(
            "features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]\n"
            "features_one_hot = pd.get_dummies(features, columns=['Orbit', 'LaunchSite', 'LandingPad', 'Serial'])\n"
            "features_one_hot = features_one_hot.astype('float64')\n"
            "print('Encoded features shape:', features_one_hot.shape)\n"
            "features_one_hot.to_csv('../data/dataset_part_3.csv', index=False)\n"
            "print('Saved dataset_part_3.csv successfully.')"
        )
    ]
    path = os.path.join(output_dir, "04_spacex_eda_dataviz.ipynb")
    with open(path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    return path

