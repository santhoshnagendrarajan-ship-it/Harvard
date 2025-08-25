import streamlit as st
import pandas as pd
import base_code
import mysql.connector as c

# --- Title & Instructions ---
st.title("Harvard Art Museum Artifact Explorer")
st.markdown("""
Select a classification (e.g., Coins, Paintings, Sculptures, Jewellery, Drawings, etc.)  
Collect a minimum of 2500 records for every classification.  
Use the buttons below to fetch, view, and store data.  
Run pre-written queries and visualize results.
""")

# --- Dropdown for Classification ---
classification_options = [
    "Coins", "Paintings", "Sculptures", "Jewellery", "Drawings"
]
selected_classification = st.selectbox(
    "Select Classification", classification_options
)

# --- Session State ---
if "data" not in st.session_state:
    st.session_state.data = None
if "segment_data" not in st.session_state:
    st.session_state.segment_data = None

#api_key = st.text_input("81ecd2aa-fab3-4f24-8503-67ef2e86d595")
api_key ="81ecd2aa-fab3-4f24-8503-67ef2e86d595"

if st.button("Collect Data"):
    # Fetch all classification data
    data = base_code.fetch_classification_data(api_key)
    st.session_state.data = data
    # Find the selected segment's name (classification) and fetch only that segment's data
    segment_name = selected_classification
    # Get all pages for this segment
    #pages = base_code.get_pages()
    # Fetch colors for this segment only
    colors_list = base_code.fetch_segment_records(api_key, segment_name)
    # Filter records for the selected segment only
    segment_records = []
    for record in data['records']:
        if record['name'].lower() == segment_name.lower():
            segment_records.append(record)
    # Store only the selected segment's data for further processing
    st.session_state.segment_data = {
        "records": segment_records
    }
    st.session_state.colors_list = colors_list
    st.success(f"Data for '{segment_name}' fetched successfully!")

if st.button("Show Data"):
    if st.session_state.segment_data and st.session_state.segment_data['records']:
        df = pd.DataFrame(st.session_state.segment_data['records'])
        st.dataframe(df)
    else:
        st.warning("No data fetched yet. Please collect data first.")


if st.button("Show artifact_metadata Data"):
    if st.session_state.segment_data and st.session_state.segment_data['records']:
        metadata = base_code.build_artifact_metadata(st.session_state.colors_list)
        df = pd.DataFrame(metadata)
        st.dataframe(df)
    else:
        st.warning("No data available. Please collect data first.")

if st.button("Show artifact_media Data"):
    if st.session_state.segment_data and st.session_state.segment_data['records']:
        media = base_code.build_artifact_media(st.session_state.colors_list)
        df = pd.DataFrame(media)
        st.dataframe(df)
    else:
        st.warning("No data available. Please collect data first.")

if st.button("Show artifact_colors Data"):
    if st.session_state.segment_data and st.session_state.segment_data['records']:
        colors = base_code.build_artifact_colors(st.session_state.colors_list)
        df = pd.DataFrame(colors)
        st.dataframe(df)
    else:
        st.warning("No data available. Please collect data first.")


if st.button("Insert into SQL"):
    connection, cursor = base_code.connect_mysql()
    base_code.drop_all_tables(cursor)
    base_code.recreate_artifact_metadata_table(cursor)
    base_code.recreate_artifact_media_table(cursor)
    base_code.recreate_artifact_colors_table(cursor)
    artifact_metadata = base_code.build_artifact_metadata(st.session_state.colors_list)
    base_code.insert_artifact_metadata(artifact_metadata, cursor, connection)
    artifact_media = base_code.build_artifact_media(st.session_state.colors_list)
    base_code.insert_artifact_media(artifact_media, cursor, connection)
    artifact_colors = base_code.build_artifact_colors(st.session_state.colors_list)
    base_code.insert_artifact_colors(artifact_colors, cursor, connection)


    st.success("Data inserted into SQL tables!")

def show_sql_table(table_name):
    try:
        connection, cursor = base_code.connect_mysql()
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(result, columns=columns)
        st.subheader(f"{table_name}")
        st.dataframe(df)
    except Exception as e:
        st.warning(f"Could not load {table_name}: {e}")

if st.button("Show artifact_metadata Table"):
    show_sql_table("artifact_metadata")

if st.button("Show artifact_media Table"):
    show_sql_table("artifact_media")

if st.button("Show artifact_colors Table"):
    show_sql_table("artifact_colors")

# --- Query & Visualization Section ---
st.header("Query & Visualization")

# Load pre-written queries from query.txt
with open("query.txt", "r") as f:
    query_lines = f.read().split('\n-- ')
queries = [q.strip() for q in query_lines if q.strip()]
query_titles = [q.split('\n')[0] for q in queries]

selected_query = st.selectbox("Select a Query", query_titles)
if st.button("Run Query"):
    connection, cursor = base_code.connect_mysql()
    query_index = query_titles.index(selected_query)
    sql_query = '\n'.join(queries[query_index].split('\n')[1:])
    cursor.execute(sql_query)
    result = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(result, columns=columns)
    st.dataframe(df)