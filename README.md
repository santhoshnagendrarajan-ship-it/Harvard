# Harvard Art Museum Artifact Explorer

A comprehensive data collection and analysis system that fetches, processes, and visualizes artifact data from the Harvard Art Museum API.

## 📋 Overview

This project provides an interactive web application to explore Harvard Art Museum artifacts across multiple classifications. It fetches real-time data from the Harvard API, stores it in a MySQL database, and offers powerful querying and visualization capabilities.

## ✨ Features

- **Multi-Classification Support**: Explore artworks across 5 major categories:
  - Coins
  - Paintings
  - Sculptures
  - Jewellery
  - Drawings

- **Data Collection**: 
  - Fetches minimum 2,500 records per classification
  - Paginated API calls (25 pages × 100 records)
  - Automatic data extraction and transformation

- **Database Management**:
  - Three normalized MySQL tables
  - Dynamic table creation and management
  - Data persistence and retrieval

- **Interactive UI**:
  - Web-based interface using Streamlit
  - Real-time data preview
  - SQL query execution and results visualization
  - One-click data insertion into database

- **Advanced Analytics**:
  - Pre-written SQL queries
  - Custom query support
  - Data visualization
  - Filtering and sorting capabilities

## 🛠️ Tech Stack

- **Backend**: Python 3.x
- **Frontend**: Streamlit
- **Database**: MySQL
- **API Client**: Requests library
- **Data Processing**: Pandas
- **Database Driver**: mysql-connector-python

## 📦 Installation

### Prerequisites
- Python 3.7+
- MySQL Server (running on localhost:3306)
- pip (Python package manager)

### Setup

1. **Clone or navigate to the project directory**:
   ```bash
   cd d:\GUVI\PROJECTS\Project1
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure MySQL Database**:
   - Start MySQL service
   - Create a database named `harvard`:
     ```sql
     CREATE DATABASE harvard;
     ```
   - Update credentials in `base_code.py` if needed (default: `root` user, password `1302`)

4. **Get API Key**:
   - Harvard Art Museums API key is embedded in `app.py`
   - To use your own key, get it from: https://www.harvardartmuseums.org/api

## 🚀 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Workflow

1. **Select Classification**: Choose an artifact type from the dropdown
   
2. **Collect Data**: Click "Collect Data" button
   - Fetches all records from Harvard API for selected classification
   - Extracts and structures the data
   - Ready for preview

3. **Preview Data**: 
   - "Show Data" - View raw classification data
   - "Show artifact_metadata Data" - View artifact details
   - "Show artifact_media Data" - View media information
   - "Show artifact_colors Data" - View color analysis

4. **Store in Database**: 
   - Click "Insert into SQL" to save data to MySQL
   - Automatically creates/recreates tables
   - Validates and inserts all three data types

5. **Query & Analyze**:
   - View stored table data with "Show [Table] Table" buttons
   - Select from pre-written queries in "Query & Visualization" section
   - Run queries and view results in real-time

## 📁 Project Structure

```
Project1/
├── app.py                          # Main Streamlit application
├── base_code.py                    # Core API & database functions
├── requirements.txt                # Python dependencies
├── query.txt                       # Pre-written SQL queries
├── README.md                       # This file
├── data.json                       # Sample/cached data
├── columns                         # Column reference file
├── tables.txt                      # Table structure reference
├── queries.txt                     # Additional query documentation
└── draftapp/                       # Backup/version files
    ├── base_code.py
    ├── draftapp.py
    ├── v1.0/
    │   ├── app_v1.1.txt
    │   └── base_code_v1.1.txt
    └── basecodev1.txt
```

## 🗄️ Database Schema

### artifact_metadata
Stores core artifact information:
- `id` (PRIMARY KEY)
- `title`, `culture`, `period`, `century`
- `medium`, `dimensions`, `description`
- `department`, `classification`
- `accessionyear`, `accessionmethod`

### artifact_media
Stores media-related information:
- `objectid` (FK to artifact_metadata.id)
- `imagecount`, `mediacount`, `colorcount`
- `rank`, `datebegin`, `dateend`

### artifact_colors
Stores color analysis data:
- `objectid` (FK to artifact_metadata.id)
- `color`, `spectrum`, `hue`
- `percent`, `css3`

## 🔑 Key Functions

### Data Fetching
- `fetch_classification_data(api_key)` - Fetch all classifications
- `fetch_segment_records(api_key, segment)` - Fetch records for specific classification
- `get_segment_record(data, segment_name)` - Find segment by name

### Data Processing
- `build_artifact_metadata(data)` - Extract metadata
- `build_artifact_media(data)` - Extract media information
- `build_artifact_colors(data)` - Extract color data

### Database Operations
- `connect_mysql()` - Establish database connection
- `drop_all_tables(cursor)` - Drop existing tables
- `recreate_artifact_*_table(cursor)` - Create tables
- `insert_artifact_*(data, cursor, connection)` - Insert data into tables

## ⚙️ Configuration

### MySQL Connection
Edit connection parameters in `base_code.py`:
```python
connection = c.connect(
    host='127.0.0.1',
    user='root',
    password='1302',
    database='harvard',
    port=3306
)
```

### API Key
Located in `app.py`:
```python
api_key = "81ecd2aa-fab3-4f24-8503-67ef2e86d595"
```

## 📊 Querying

Pre-written queries are stored in `query.txt` and include analysis such as:
- Artifact counts by classification
- Color analysis and frequency
- Temporal distribution
- Cultural and period-based analysis
- Custom aggregations

## ⚠️ Important Notes

- **API Rate Limits**: The Harvard API has rate limiting. Adjust pagination if needed.
- **Database Reset**: Clicking "Insert into SQL" drops and recreates all tables. Existing data will be lost.
- **Memory**: Loading 2,500+ records may require processing time. Be patient with large classifications.
- **Network**: Requires internet connection to fetch from Harvard API.

## 🐛 Troubleshooting

**MySQL Connection Error**:
- Ensure MySQL server is running
- Check credentials in `base_code.py`
- Verify database `harvard` exists

**API Connection Error**:
- Check internet connection
- Verify API key is valid
- Check Harvard API status

**Data Not Displaying**:
- Click "Collect Data" before viewing
- Ensure data was successfully fetched (check console for errors)
- Verify MySQL connection is active

## 📝 Dependencies

See `requirements.txt`:
```
streamlit
pandas
mysql-connector-python
requests
```

## 🔄 Workflow Diagram

```
API (Harvard Art Museums)
        ↓
fetch_segment_records()
        ↓
build_artifact_* → Streamlit UI
        ↓
insert_artifact_* → MySQL
        ↓
SQL Queries → Visualization
```

## 📚 References

- [Harvard Art Museums API](https://www.harvardartmuseums.org/api)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [MySQL Documentation](https://dev.mysql.com/doc/)

## 👤 Author Notes

This project demonstrates:
- RESTful API integration
- Data transformation and normalization
- Database design and management
- Interactive web application development
- SQL query optimization
- Python best practices

---

**Last Updated**: February 22, 2026
