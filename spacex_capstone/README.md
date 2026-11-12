# SpaceX Falcon 9 First Stage Landing Prediction
Applied Data Science Capstone Project

## Project Overview
SpaceX advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars; other providers cost upward of 165 million dollars each, much of the savings is because SpaceX can reuse the first stage. Therefore, if we can predict if the first stage will land, we can determine the cost of a launch. This information can be used if an alternate company wants to bid against SpaceX for a rocket launch.

## Objectives
- Collect historical launch data from SpaceX REST API and Wikipedia using web scraping.
- Perform data wrangling, handle missing values, and engineer binary classification target (`Class`).
- Conduct Exploratory Data Analysis (EDA) using SQL queries and data visualization libraries.
- Build interactive geospatial maps with Folium and a real-time dashboard using Plotly Dash.
- Train and evaluate multiple machine learning classification models (Logistic Regression, Support Vector Machine, Decision Tree, K-Nearest Neighbors) to predict first stage landing success.

## Project Structure
```text
spacex_capstone/
|-- data/
|   |-- dataset_part_1.csv
|   |-- dataset_part_2.csv
|   |-- dataset_part_3.csv
|   |-- Spacex.csv
|   |-- spacex_launch_dash.csv
|   `-- spacex_launch_geo.csv
|-- figures/
|   |-- eda_*.png
|   |-- sql_*.png
|   |-- folium_*.png
|   |-- dash_*.png
|   `-- ml_*.png
|-- src/
|   |-- download_data.py
|   |-- eda_visualizations.py
|   |-- eda_sql.py
|   |-- folium_analytics.py
|   |-- spacex_dash_app.py
|   |-- generate_dash_charts.py
|   |-- predictive_analysis.py
|   |-- generate_process_diagrams.py
|   |-- presentation_helpers.py
|   `-- build_presentation.py
|-- output/
|   |-- Data Science Capstone Project Report.pdf
|   |-- Data Science Capstone Project Report.pptx
|   `-- spacex_folium_map.html
|-- requirements.txt
`-- README.md
```

## Methodology & Results
1. **Data Collection**: 90 Falcon 9 launch records gathered from SpaceX API v4 and scraped from Wikipedia.
2. **Data Wrangling**: Missing payload masses imputed with mean; landing outcomes labeled as 1 (successful landing) or 0 (unsuccessful).
3. **Exploratory Data Analysis**:
   - Orbit Analysis: Orbits ES-L1, GEO, HEO, and SSO achieved 100% success rate.
   - Launch Sites: KSC LC-39A demonstrated the highest recovery success rate (76.9%).
   - Temporal Trend: Success rate increased from 0% in 2010-2012 to nearly 90% by 2020.
4. **Interactive Analytics**:
   - Folium Map: Clustered launch records and analyzed proximity to coastlines (0.58 km), highways (0.60 km), and railways (1.28 km).
   - Plotly Dash: Interactive dashboard filtering payload masses (0 to 10,000 kg) and launch site success rates.
5. **Predictive Modeling**:
   - Decision Tree Classifier: 94.4% test accuracy (Best performing).
   - Logistic Regression: 83.3% test accuracy.
   - Support Vector Machine (SVM): 83.3% test accuracy.
   - K-Nearest Neighbors (KNN): 83.3% test accuracy.

## Installation & Execution
```bash
pip install -r requirements.txt

# Run data collection and EDA
python src/download_data.py
python src/eda_visualizations.py
python src/eda_sql.py
python src/folium_analytics.py

# Launch Plotly Dash Dashboard
python src/spacex_dash_app.py

# Train Machine Learning Models
python src/predictive_analysis.py

# Build PowerPoint presentation and export final PDF
python src/build_presentation.py
```

