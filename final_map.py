import os
import sqlite3
import pandas as pd
import requests
import streamlit as st
from streamlit.components.v1 import html
import folium
from folium.plugins import MarkerCluster
from folium import Popup
from load_database import clean_data

st.set_page_config(layout="wide")

# -------------------------------
# Router (no change to map usage)
# -------------------------------
params = st.query_params
view = params.get("view", "main")          # "main" or "table"
table_name_qp = params.get("table", None)  # "Summary Table" | "Population Table"

# -------------------------------
# DB bootstrap (unchanged map)
# -------------------------------
def database_is_empty():
    try:
        conn = sqlite3.connect("repid.db")
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Repid")
        count = cur.fetchone()[0]
        conn.close()
        return count == 0
    except Exception:
        return True

if database_is_empty():
    clean_data()

# -------------------------------
# Helpers used by both views
# -------------------------------
def load_summary_table(table_name):
    tsv_files = {
        "Summary Table": "summary_all.tsv",
        "Population Table": "all_REDatlas.tsv",
    }
    filename = tsv_files.get(table_name)
    summary_path = os.path.join(filename)
    if os.path.exists(summary_path):
        return pd.read_csv(summary_path, sep="\t")

def assign_colors(df, name):
    names = df[name].dropna().unique()
    color_list = [
        'red', 'blue', 'green', 'purple', 'orange', 'yellow', 'brown', "aquamarine",
        'darkred', 'lightred', 'beige', 'darkblue', 'lightblue', 'lightgreen',
        'darkgreen', 'cadetblue', 'darkpurple', 'pink', 'gray', 'black', 'lightgray',
        'cyan', 'magenta', 'navy', 'teal', 'coral', 'olive', 'gold', 'indigo'
    ]
    sorted_names = sorted(names)
    color_map = {name: color_list[i % len(color_list)] for i, name in enumerate(sorted_names)}
    return color_map

def show_color_legend(color_map):
    st.markdown("### Colors Legend", unsafe_allow_html=True)
    for name, color in color_map.items():
        st.markdown(
            f"<div style='display: flex; align-items: center;'>"
            f"<div style='width: 15px; height: 15px; background-color: {color}; margin-right: 10px; border: 1px solid #000;'></div>"
            f"<span>{name}</span></div>",
            unsafe_allow_html=True
        )

def get_regions(repids, diseases):
    conn = sqlite3.connect("repid.db")
    conditions = []
    params = []
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

    if not conditions:
        return pd.DataFrame()  # no input, return empty

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

def style_function(feature):
    continent = feature['properties']['continent']
    return {
        'fillColor': continent_colors.get(continent, 'gray'),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.5
    }

# -------------------------------
# MAIN (MAP) VIEW — UNCHANGED
# -------------------------------
st.title("Disease Region Explorer")

conn = sqlite3.connect("repid.db")
repid_options = pd.read_sql_query("SELECT DISTINCT RepidName FROM Repid", conn)["RepidName"].dropna().unique().tolist()
disease_options = pd.read_sql_query("SELECT DISTINCT DiseaseName FROM Disease", conn)["DiseaseName"].dropna().unique().tolist()
conn.close()

# Inputs
col1, col2, col3, col4 = st.columns(4)
with col1:
    selected_repids = st.multiselect("Select Repid(s):", sorted(repid_options))
with col2:
    selected_diseases = st.multiselect("Select Disease(s):", sorted(disease_options))
with col3:
    search_text = st.text_input("Search by typing Repid (use comma, e.g., ATXN1,ATXN2):")
with col4:
    st.markdown("**Data Tables**")
    # Vertical native buttons (same-tab)
    if st.button("Summary Table (summary_all.tsv)", use_container_width=True):
        st.query_params.update({"view": "table", "table": "Summary Table"})
        st.rerun()
    if st.button("Per-Haplotype Tandem Repeat Table (all_REDatlas.tsv)", use_container_width=True):
        st.query_params.update({"view": "table", "table": "Population Table"})
        st.rerun()

# Parse text input
typed_repids, typed_diseases = [], []
if search_text:
    parts = [x.strip() for x in search_text.split(',') if x.strip()]
    for part in parts:
        if part in repid_options:
            typed_repids.append(part)
        elif part in disease_options:
            typed_diseases.append(part)

final_repids = list(set(selected_repids + typed_repids))
final_diseases = list(set(selected_diseases + typed_diseases))

# World layer
url = "https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/refs/heads/main/countries.geojson"
geojson_data = requests.get(url).json()

continent_colors = {
    "Africa": "#90ee90",
    "Asia": "#ffcccb",
    "Europe": "#add8e6",
    "North America": "#dab6fc",
    "South America": "#ffd580",
    "Oceania": "#ffb6c1",
    "Antarctica": "#d3d3d3"
}

def radius(row):
    if pd.notna(row["Frequency"]):
        radius = row["Frequency"] + 3.5
    else:
        radius = 3
    return radius

# Map render (UNCHANGED)
if final_repids or final_diseases:
    color_map, name, results = get_regions(final_repids, final_diseases)
    show_color_legend(color_map)

    if results.empty:
        st.warning("No matching records found.")
    else:
        m = folium.Map(location=[results['Latitude'].mean(), results['Longitude'].mean()], 
                       zoom_start=2,
                       min_zoom=2,
                       max_bounds=True)
        folium.GeoJson(geojson_data, style_function=style_function).add_to(m)
        marker_cluster = MarkerCluster().add_to(m)

        for _, row in results.iterrows():
            popup_content = f"""
                <h3>{row['DiseaseName']}</h3>
                <i>{row['RepidName']}</i> in {row['RepeatLocation']}<br>
                <b>{row['Link']}</b><br>
                <b>Normal Range:</b> {row['NormalRange']}<br>
            """
            if row['IntermediateRange'] != "-":
                popup_content += f" <b>Intermediate Range:</b> {row['IntermediateRange']}<br>"
            if pd.notna(row.get('FullMutationRange')):
                popup_content += f" <b>Full Mutation Range:</b> {row['FullMutationRange']}"
            radius(row)
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=radius(row),
                color=color_map.get(row[name]),
                fill=True,
                fill_opacity=0.7,
                popup=Popup(popup_content, max_width=700),
                tooltip=row['DiseaseName']
            ).add_to(m)

        html(m._repr_html_(), height=800, width=1400)
else:
    st.info("Please select a Repid, Disease, or enter a search term.")

# -------------------------------
# TABLE VIEW (with Back button)
# -------------------------------
if view == "table":
    st.title("Table Viewer")

    table_options = {
        "Summary Table": "summary_all.tsv",
        "Population Table": "all_REDatlas.tsv"
    }
    chosen_title = table_name_qp if table_name_qp in table_options else "Summary Table"
    tsv_file = table_options[chosen_title]

    # Prefer uploaded copies if available
    if chosen_title == "Summary Table (summary_all.tsv)":
        if os.path.exists("/mnt/data/summary_all.tsv"):
            tsv_file = "/mnt/data/summary_all.tsv"
    elif chosen_title == "Population Table (all_REDatlas.tsv)":
        if os.path.exists("/mnt/data/all_REDatlas.tsv"):
            tsv_file = "/mnt/data/all_REDatlas.tsv"

    # Load table
    if os.path.exists(tsv_file):
        df_table = pd.read_csv(tsv_file, sep="\t")
    else:
        st.error(f"Could not find table file: {tsv_file}")
        st.stop()

    df_table.columns = df_table.columns.str.strip()

    # Filters
    filter_cols = [c for c in ["AlleleClass", "Locus", "Superpopulation", "Population", "Sample"]
                   if c in df_table.columns]

    with st.expander("Filters", expanded=True):
        text_query = st.text_input("Search text (Comma between variables (e.g., ATXN1,ATXN2))")

        selected_filters = {}
        ff_cols = st.multiselect(
            "Choose columns to search with the text query (leave empty to search ALL shown filter columns)",
            filter_cols, default=filter_cols
        )

        fcol1, fcol2, fcol3 = st.columns(3)
        holders = [fcol1, fcol2, fcol3]
        for i, colname in enumerate(filter_cols):
            with holders[i % 3]:
                opts = sorted(df_table[colname].dropna().unique().tolist())
                selected = st.multiselect(colname, opts)
                if selected:
                    selected_filters[colname] = set(selected)

    # Apply filters
    filtered = df_table.copy()

    # 1) Column filters (AND across columns, OR within column)
    for colname, chosen in selected_filters.items():
        filtered = filtered[filtered[colname].isin(chosen)]

    # 2) Text query across chosen columns (AND across terms)
    if text_query and text_query.strip():
        terms = [t.strip().lower() for t in text_query.split(",") if t.strip()]
        cols_to_search = ff_cols if ff_cols else filter_cols if filter_cols else filtered.columns

        def row_matches(s):
            haystack = " | ".join("" if pd.isna(x) else str(x) for x in s.values).lower()
            return all(term in haystack for term in terms)

        filtered = filtered[filtered[cols_to_search].apply(row_matches, axis=1)]

    st.caption(f"Showing {len(filtered):,} of {len(df_table):,} rows from **{chosen_title}**.")
    st.dataframe(filtered, use_container_width=True, height=480)

    st.download_button(
        "Download filtered TSV",
        data=filtered.to_csv(sep="\t", index=False),
        file_name=f"{chosen_title.replace(' ', '_').lower()}_filtered.tsv",
        mime="text/tab-separated-values",
    )

    # NEW: Back to Map (same tab)
    if st.button("⬅︎ Back to Map", use_container_width=True):
        st.query_params.update({"view": "main"})
        st.rerun()

# -------------------------------
# Reference
# -------------------------------
st.markdown("---")
st.markdown("### Reference")
st.markdown(
    """
    Indhu-Shree Rajan-Babu, Readman Chiu, Ben Weisburd, Iris Caglayan, Inanc Birol, Jan M. Friedman. 
    Population-scale disease-associated tandem repeat analysis reveals locus and ancestry-specific insights. 
    medRxiv 2025.10.11.25337795 (2025). doi: https://doi.org/10.1101/2025.10.11.25337795
    """,
    unsafe_allow_html=True
)
