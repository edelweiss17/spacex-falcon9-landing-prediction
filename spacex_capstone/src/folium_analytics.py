import os
import folium
from folium.plugins import MarkerCluster, MousePosition
import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "spacex_launch_geo.csv")
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")

def calculate_distance(lat1, lon1, lat2, lon2):
    from math import sin, cos, sqrt, atan2, radians
    r = 6373.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return r * c

def create_folium_map():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)
    df = pd.read_csv(DATA_PATH)

    nasa_coordinate = [29.559684888522208, -95.0830971930759]
    site_map = folium.Map(location=nasa_coordinate, zoom_start=5)

    # 1. Add Launch Site Circles and Markers
    launch_sites_df = df.groupby(["Launch Site"], as_index=False).first()
    for _, row in launch_sites_df.iterrows():
        coord = [row["Lat"], row["Long"]]
        circle = folium.Circle(
            coord,
            radius=1000,
            color="#d35400",
            fill=True
        ).add_child(folium.Popup(row["Launch Site"]))
        marker = folium.map.Marker(
            coord,
            icon=folium.DivIcon(
                icon_size=(20, 20),
                icon_anchor=(0, 0),
                html=f'<div style="font-size: 12px; color: #d35400; font-weight: bold;"><b>{row["Launch Site"]}</b></div>'
            )
        )
        site_map.add_child(circle)
        site_map.add_child(marker)

    # 2. Add MarkerCluster for all launch records
    marker_cluster = MarkerCluster()
    site_map.add_child(marker_cluster)

    for _, row in df.iterrows():
        coord = [row["Lat"], row["Long"]]
        color = "green" if row["class"] == 1 else "red"
        marker = folium.Marker(
            location=coord,
            icon=folium.Icon(color="white", icon_color=color),
            popup=f"{row['Launch Site']} | Outcome: {'Success' if row['class'] == 1 else 'Failure'}"
        )
        marker_cluster.add_child(marker)

    # 3. Proximity points for CCAFS SLC-40
    site_coord = [28.563197, -80.576820]
    coastline_coord = [28.56367, -80.56763]
    highway_coord = [28.56321, -80.57079]
    railway_coord = [28.57205, -80.58525]
    city_coord = [28.61208, -80.80753] # Titusville

    points = {
        "Coastline": coastline_coord,
        "Highway": highway_coord,
        "Railway": railway_coord,
        "City (Titusville)": city_coord
    }

    distances = {}
    for name, pt in points.items():
        dist = calculate_distance(site_coord[0], site_coord[1], pt[0], pt[1])
        distances[name] = dist
        # Add line
        folium.PolyLine(locations=[site_coord, pt], color="blue", weight=2).add_to(site_map)
        # Add distance marker
        folium.Marker(
            pt,
            icon=folium.DivIcon(
                icon_size=(20, 20),
                icon_anchor=(0, 0),
                html=f'<div style="font-size: 11px; color: #00008b; font-weight: bold;">{name}: {dist:.2f} KM</div>'
            )
        ).add_to(site_map)

    html_path = os.path.join(OUTPUT_DIR, "spacex_folium_map.html")
    site_map.save(html_path)

    # Dedicated Map 1: Florida launch sites and MarkerClusters
    m_clusters = folium.Map(location=[28.575, -80.61], zoom_start=12, tiles="OpenStreetMap")
    for _, row in launch_sites_df.iterrows():
        coord = [row["Lat"], row["Long"]]
        folium.Circle(coord, radius=800, color="#d35400", fill=True, fill_opacity=0.25).add_to(m_clusters)
        folium.Marker(
            coord,
            icon=folium.DivIcon(
                icon_size=(160, 30),
                html=f'<div style="font-size: 11px; font-weight: bold; color: #a04000; background: rgba(255,255,255,0.9); padding: 2px 6px; border: 1px solid #d35400; border-radius: 4px;">{row["Launch Site"]}</div>'
            )
        ).add_to(m_clusters)

    cluster_group = MarkerCluster(disableClusteringAtZoom=12).add_to(m_clusters)
    for _, row in df.iterrows():
        coord = [row["Lat"], row["Long"]]
        color = "green" if row["class"] == 1 else "red"
        folium.Marker(
            location=coord,
            icon=folium.Icon(color=color, icon="ok-sign" if row["class"] == 1 else "remove-sign"),
            popup=f"{row['Launch Site']} | Outcome: {'Success' if row['class'] == 1 else 'Failure'}"
        ).add_to(cluster_group)

    clusters_html = os.path.join(OUTPUT_DIR, "map_clusters.html")
    m_clusters.save(clusters_html)

    # Dedicated Map 2: Proximity Analysis centered on CCAFS SLC-40
    m_proximity = folium.Map(location=[28.585, -80.68], zoom_start=12, tiles="OpenStreetMap")
    folium.Circle(site_coord, radius=800, color="#c0392b", fill=True, fill_opacity=0.3).add_to(m_proximity)
    folium.Marker(
        site_coord,
        icon=folium.DivIcon(
            icon_size=(140, 26),
            html='<div style="font-size: 12px; font-weight: bold; color: white; background: #c0392b; padding: 3px 6px; border-radius: 3px;">CCAFS SLC-40</div>'
        )
    ).add_to(m_proximity)

    for name, pt in points.items():
        folium.PolyLine(locations=[site_coord, pt], color="#2980b9", weight=3, dash_array="6, 6").add_to(m_proximity)
        folium.Marker(
            pt,
            icon=folium.DivIcon(
                icon_size=(180, 26),
                html=f'<div style="font-size: 11px; font-weight: bold; color: #1a5276; background: white; border: 1.5px solid #2980b9; padding: 2px 6px; border-radius: 3px;">{name} ({distances[name]:.2f} km)</div>'
            )
        ).add_to(m_proximity)

    proximity_html = os.path.join(OUTPUT_DIR, "map_proximity.html")
    m_proximity.save(proximity_html)

    # Take browser screenshots if Brave is available
    brave_exe = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    clusters_png = os.path.join(FIGURES_DIR, "folium_site_clusters.png")
    proximity_png = os.path.join(FIGURES_DIR, "folium_proximity_distances.png")

    if os.path.exists(brave_exe):
        import subprocess
        subprocess.run([brave_exe, "--headless", "--disable-gpu", "--virtual-time-budget=3000", "--window-size=1200,800", f"--screenshot={clusters_png}", clusters_html], check=True)
        subprocess.run([brave_exe, "--headless", "--disable-gpu", "--virtual-time-budget=3000", "--window-size=1200,800", f"--screenshot={proximity_png}", proximity_html], check=True)
        print("Captured Folium map screenshots via headless browser.")
    else:
        # Fallback matplotlib plots
        fig, ax = plt.subplots(figsize=(10, 6))
        site_counts = df.groupby(["Launch Site", "class"]).size().unstack(fill_value=0)
        site_counts.columns = ["Failure (0)", "Success (1)"]
        site_counts.plot(kind="bar", stacked=True, color=["#d9534f", "#2ca02c"], ax=ax)
        plt.title("Launch Records & Outcomes by Launch Site (Folium MarkerCluster Summary)")
        plt.xlabel("Launch Site")
        plt.ylabel("Number of Launches")
        plt.xticks(rotation=0)
        for i, (idx, row) in enumerate(site_counts.iterrows()):
            total = row["Failure (0)"] + row["Success (1)"]
            succ_rate = (row["Success (1)"] / total) * 100
            ax.text(i, total + 0.5, f"Success: {succ_rate:.1f}%\n(N={total})", ha="center", fontsize=9.5, fontweight="bold")
        plt.ylim(0, max(site_counts.sum(axis=1)) + 5)
        plt.tight_layout()
        plt.savefig(clusters_png, dpi=300)
        plt.close()

        fig, ax = plt.subplots(figsize=(9, 4.5))
        dist_df = pd.DataFrame(list(distances.items()), columns=["Target", "Distance_KM"]).sort_values(by="Distance_KM")
        colors = ["#2b5c8f", "#337ab7", "#5bc0de", "#f0ad4e"]
        bars = ax.barh(dist_df["Target"], dist_df["Distance_KM"], color=colors, height=0.55)
        ax.set_title("Proximity Distance from CCAFS SLC-40 to Geographical Features", fontsize=12, fontweight="bold")
        ax.set_xlabel("Distance (KM)")
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.4, bar.get_y() + bar.get_height() / 2, f"{width:.2f} km", va="center", fontsize=9.5, fontweight="bold")
        ax.set_xlim(0, max(dist_df["Distance_KM"]) + 5)
        plt.tight_layout()
        plt.savefig(proximity_png, dpi=300)
        plt.close()

    print("Folium map HTML and proximity figures generated successfully.")

if __name__ == "__main__":
    create_folium_map()

