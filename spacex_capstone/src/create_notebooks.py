import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from notebook_builders.builder_api import build_api_notebook
from notebook_builders.builder_wrangling import build_wrangling_notebook
from notebook_builders.builder_sql import build_sql_notebook
from notebook_builders.builder_viz import build_viz_notebook
from notebook_builders.builder_ml import build_ml_notebook

NOTEBOOKS_DIR = os.path.join(os.path.dirname(__file__), "..", "notebooks")
os.makedirs(NOTEBOOKS_DIR, exist_ok=True)

def main():
    p1 = build_api_notebook(NOTEBOOKS_DIR)
    p2 = build_wrangling_notebook(NOTEBOOKS_DIR)
    p3 = build_sql_notebook(NOTEBOOKS_DIR)
    p4 = build_viz_notebook(NOTEBOOKS_DIR)
    p5 = build_ml_notebook(NOTEBOOKS_DIR)

    print("Generated all 5 notebooks:")
    for p in [p1, p2, p3, p4, p5]:
        print(f" - {os.path.basename(p)}")

if __name__ == "__main__":
    main()
