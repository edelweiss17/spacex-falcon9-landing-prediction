import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")

def draw_box(ax, x, y, w, h, text, color="#203864", text_color="white", fontsize=10):
    rect = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        linewidth=1.5,
        edgecolor="#14233c",
        facecolor=color
    )
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color=text_color, fontsize=fontsize, fontweight="bold", multialignment="center")

def draw_arrow(ax, x1, y1, x2, y2):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", lw=2, color="#333333")
    )

def generate_api_flowchart():
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")

    draw_box(ax, 0.5, 1.5, 2.0, 1.2, "1. REST API Call\nGET /v4/launches/past\n(SpaceX Public API)", color="#203864")
    draw_arrow(ax, 2.5, 2.1, 3.2, 2.1)

    draw_box(ax, 3.2, 1.5, 2.0, 1.2, "2. JSON Normalization\npd.json_normalize()\nExtract IDs for rocket,\nlaunchpad, payloads", color="#2a4d7a")
    draw_arrow(ax, 5.2, 2.1, 5.9, 2.1)

    draw_box(ax, 5.9, 1.5, 1.8, 1.2, "3. Auxiliary APIs\nFetch booster,\ncore & orbit details", color="#346399")
    draw_arrow(ax, 7.7, 2.1, 8.4, 2.1)

    draw_box(ax, 8.4, 1.5, 1.5, 1.2, "4. Filter Falcon 9\nSave as\ndataset_part_1.csv\n(90 launches)", color="#1e7e34")

    ax.set_title("Data Collection Pipeline: SpaceX REST API Flowchart", fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "process_api_flowchart.png"), dpi=300)
    plt.close()

def generate_scraping_flowchart():
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")

    draw_box(ax, 0.5, 1.5, 2.0, 1.2, "1. Target URL\nWikipedia Falcon 9\nLaunch Records Page", color="#203864")
    draw_arrow(ax, 2.5, 2.1, 3.2, 2.1)

    draw_box(ax, 3.2, 1.5, 2.0, 1.2, "2. HTML Fetch\nrequests.get(url)\nStatus Code 200 OK", color="#2a4d7a")
    draw_arrow(ax, 5.2, 2.1, 5.9, 2.1)

    draw_box(ax, 5.9, 1.5, 2.0, 1.2, "3. BeautifulSoup Parse\nExtract <table> rows\nHandle rowspans & tags", color="#346399")
    draw_arrow(ax, 7.9, 2.1, 8.5, 2.1)

    draw_box(ax, 8.5, 1.5, 1.4, 1.2, "4. DataFrame\nExport\nlaunch records", color="#1e7e34")

    ax.set_title("Data Collection Pipeline: Web Scraping with BeautifulSoup Flowchart", fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "process_scraping_flowchart.png"), dpi=300)
    plt.close()

def generate_wrangling_flowchart():
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")

    draw_box(ax, 0.5, 1.5, 2.0, 1.2, "1. Raw Dataset\n90 Falcon 9 launches\nMissing values in\nPayloadMass", color="#203864")
    draw_arrow(ax, 2.5, 2.1, 3.2, 2.1)

    draw_box(ax, 3.2, 1.5, 2.0, 1.2, "2. Imputation\nReplace missing\nPayloadMass with\ncolumn mean", color="#2a4d7a")
    draw_arrow(ax, 5.2, 2.1, 5.9, 2.1)

    draw_box(ax, 5.9, 1.5, 2.1, 1.2, "3. Outcome Mapping\nSuccess: True ASDS/RTLS/Ocean\nFailure: False/None\nCreate Class (1 or 0)", color="#346399")
    draw_arrow(ax, 8.0, 2.1, 8.6, 2.1)

    draw_box(ax, 8.6, 1.5, 1.3, 1.2, "4. Clean Data\ndataset_part_2\nReady for EDA", color="#1e7e34")

    ax.set_title("Data Wrangling & Transformation Methodology Flowchart", fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "process_wrangling_flowchart.png"), dpi=300)
    plt.close()

def main():
    os.makedirs(FIGURES_DIR, exist_ok=True)
    generate_api_flowchart()
    generate_scraping_flowchart()
    generate_wrangling_flowchart()
    print("Process diagrams generated successfully.")

if __name__ == "__main__":
    main()

