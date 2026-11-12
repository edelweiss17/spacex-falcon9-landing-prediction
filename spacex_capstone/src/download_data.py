import os
import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

URLS = {
    "dataset_part_1.csv": "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv",
    "dataset_part_2.csv": "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv",
    "dataset_part_3.csv": "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv",
    "spacex_launch_dash.csv": "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv",
    "spacex_launch_geo.csv": "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv",
    "Spacex.csv": "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv",
}

def download_file(url, target_path):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    with open(target_path, "wb") as f:
        f.write(response.content)

def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    for filename, url in URLS.items():
        target = os.path.join(DATA_DIR, filename)
        if not os.path.exists(target):
            print(f"Downloading {filename}...")
            download_file(url, target)
        else:
            print(f"Cached: {filename}")
    print("All datasets ready.")

if __name__ == "__main__":
    main()

