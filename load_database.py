import sqlite3
import pandas as pd

def create_links(repid_df_cleaned): 
    links = repid_df_cleaned['Link'].split('&')
    html_links = []

    for link in links:
        html_links.append(f'<a href="{link.strip()}" target="_blank"><i>Reference</i></a>')
    return "<br>".join(html_links)

def clean_data():
    repid_df = pd.read_excel('repid.xlsx')
    repid_df_cleaned = repid_df.drop(columns=["DiseaseName"])
    repid_df_cleaned['Link'] = repid_df_cleaned.apply(create_links, axis=1)
    disease_df = repid_df[['RepidName', 'DiseaseName']]
    region_df = pd.read_excel('coordinate_info.xlsx')
    region_df[["Latitude","Longitude"]] = region_df['Coordinates'].str.split(",",expand=True)
    region_df['Longitude'] = region_df["Longitude"].astype(float)
    region_df['Latitude'] = region_df['Latitude'].astype(float)
    region_df['Frequency'] = region_df['Frequency'].astype(float)
    # Step 1: Connect to your SQLite database (use the same file name you used before)
    conn = sqlite3.connect("repid.db")  # This creates or opens the .db file
    repid_df_cleaned.to_sql('Repid', conn, if_exists = "append", index = False)
    repids_from_db = pd.read_sql_query("SELECT RepID, RepidName FROM Repid", conn)
    disease_df = disease_df.merge(repids_from_db, on = "RepidName", how = 'left')
    disease_df[["DiseaseName", "RepID"]].to_sql("Disease", conn, if_exists = 'replace', index = False)
    region_df = region_df.merge(repids_from_db, on = "RepidName", how = 'left')
    region_df[['Latitude', 'Longitude', 'RepID','Frequency' ]].to_sql('Region', conn, if_exists = 'replace', index= False)
    conn.close()
clean_data()