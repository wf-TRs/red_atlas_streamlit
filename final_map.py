import streamlit as st
import sqlite3
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from folium import Popup
from streamlit.components.v1 import html
import requests
from load_database import clean_data
import os

st.set_page_config(layout="wide")

# --- Initialize DB ---
def database_is_empty():
    try:
        conn = sqlite3.connect("repid.db")
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Repid")
        count = cur.fetchone()[0]
        conn.close()
        return count == 0
    except:
        return True

if database_is_empty():
    clean_data()

# --- Load TSV table ---
def load_summary_table(table_name):
    tsv_files = {
        "Summary Table": "summary_all.tsv",
        "Population Table": "all_REDatlas.tsv"
    }
    filename = tsv_files.get(table_name)
    if filename and os.path.exists(filename):
        return pd.read_csv(filename, sep="\t")
    return None

# --- Assign colors to legend ---
def assign_colors(df, name):
    unique_names = df[name].dropna().unique()
    color_list = [
        'red', 'blue', 'green', 'purple', 'orange', 'yellow', 'brown', 'aquamarine',
        'darkred', 'lightred', 'beige', 'darkblue', 'lightblue', 'lightgreen',
        'darkgreen', 'cadetblue', 'darkpurple', 'pink', 'gray', 'black', 'lightgray',
        'cyan', 'magenta', 'navy', 'teal', 'coral', 'olive', 'gold', 'indigo'
    ]
    sorted_names = sorted(unique_names)
    return {name: color_list[i % len(color_list)] for i, name in enumerate(sorted_names)}

# --- Display color legend ---
def show_color_legend(color_map):
    st.markdown("### Color Legend")
    for name, color in color_map.items():
        st.markdown(
            f"<div style='display: flex; align-items: center;'>"
            f"<div style='width: 15px; height: 15px; background-color: {color}; margin-right: 10px; border: 1px solid #000;'></div>"
            f"<span>{name}</span></div>",
            unsafe_allow_html=True
        )

# --- SQL query builder ---
def get_regions(repids, diseases):
    conn = sqlite3.connect("repid.db")
    conditions, params = [], []

    if repids:
        placeholders = ','.join(['?'] * len(repids))
        conditions.append(f"re.RepidName IN ({placeholders})")
        params.extend(repids)
        name = "RepidName"
    elif diseases:
        placeholders = ','.join(['?'] * len(diseases))
        conditions.append(f"d.DiseaseName IN ({placeholders})")
        params.extend(diseases)
        name = "DiseaseName"
    else:
        return {}, "", pd.DataFrame()

    where_clause = ' OR '.join(conditions)
    sql = f"""
        SELECT DISTINCT r.Latitude, r.Longitude, d.DiseaseName, re.RepidName, re.Link, re.RepeatLocation, 
                        re.NormalRange, re.IntermediateRange, re.FullMutationRange, r.Frequency
        FROM Region r
        JOIN Repid re ON re.RepID = r.RepID
        JOIN Disease d ON d.RepID = re.RepID
        WHERE {where_clause}
    """
    df = pd.read_sql_query(sql, conn, params=params)
    conn.close()
    color_map = assign_colors(df, name)
    return color_map, name, df

# --- Marker radius function ---
def marker_radius(freq):
    return freq + 3.5 if pd.notna(freq) else 3

# --- Geo styling ---
def style_function(feature):
    continent = feature['properties']['continent']
    return {
        'fillColor': continent_colors.get(continent, 'gray'),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.5
    }

# --- UI ---
st.title("Disease Region Explorer")

conn = sqlite3.connect("repid.db")
repid_options = pd.read_sql_query("SELECT DISTINCT RepidName FROM Repid", conn)["RepidName"].dropna().tolist()
disease_options = pd.read_sql_query("SELECT DISTINCT DiseaseName FROM Disease", conn)["DiseaseName"].dropna().tolist()
conn.close()

# --- Controls ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    selected_repids = st.multiselect("Select Repid(s):", sorted(repid_options))
with col2:
    selected_diseases = st.multiselect("Select Disease(s):", sorted(disease_options))
with col3:
    search_text = st.text_input("Search by typing (use comma):")
with col4:
    selected_table = st.selectbox("Tables:", ["Choose options", "Summary Table", "Population Table"], index=0)

# --- Parse search input ---
typed_repids, typed_diseases = [], []
if search_text:
    for part in [x.strip() for x in search_text.split(',') if x.strip()]:
        if part in repid_options:
            typed_repids.append(part)
        elif part in disease_options:
            typed_diseases.append(part)

final_repids = list(set(selected_repids + typed_repids))
final_diseases = list(set(selected_diseases + typed_diseases))

# --- Load GeoJSON ---
url = "https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/refs/heads/main/countries.geojson"
geojson_data = requests.get(url).json()

# --- Continent colors ---
continent_colors = {
    "Africa": "#90ee90",
    "Asia": "#ffcccb",
    "Europe": "#add8e6",
    "North America": "#dab6fc",
    "South America": "#ffd580",
    "Oceania": "#ffb6c1",
    "Antarctica": "#d3d3d3"
}

# --- Main map logic ---
if final_repids or final_diseases:
    color_map, name, results = get_regions(final_repids, final_diseases)
    show_color_legend(color_map)

    if results.empty:
        st.warning("No matching records found.")
    else:
        m = folium.Map(location=[results['Latitude'].mean(), results['Longitude'].mean()],
                       zoom_start=2, min_zoom=2, max_bounds=True)

        folium.GeoJson(geojson_data, style_function=style_function).add_to(m)
        marker_cluster = MarkerCluster().add_to(m)

        for _, row in results.iterrows():
            popup_html = f"""
                <div style='max-width: 300px;'>
                    <h4>{row['DiseaseName']}</h4>
                    <p><i>{row['RepidName']}</i> in {row['RepeatLocation']}<br>
                    <b>Link:</b> {row['Link']}<br>
                    <b>Normal Range:</b> {row['NormalRange']}<br>"""
            if row['IntermediateRange'] != "-":
                popup_html += f"<b>Intermediate Range:</b> {row['IntermediateRange']}<br>"
            if pd.notna(row['FullMutationRange']):
                popup_html += f"<b>Full Mutation Range:</b> {row['FullMutationRange']}<br>"
            popup_html += "</p></div>"

            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=marker_radius(row["Frequency"]),
                color=color_map.get(row[name], "gray"),
                fill=True,
                fill_opacity=0.7,
                popup=Popup(popup_html, max_width=400),
                tooltip=f"{row['DiseaseName']} ({row['RepidName']})"
            ).add_to(marker_cluster)

        html(m._repr_html_(), height=800, width=1400)
else:
    st.info("Please select a Repid, Disease, or enter a search term.")

# --- Table view ---
if selected_table != "Choose options":
    summary_df = load_summary_table(selected_table)
    if summary_df is not None:
        st.dataframe(summary_df, use_container_width=True)
    else:
        st.warning("Selected table not found.")
