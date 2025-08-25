import requests as R
import json
import pprint
import mysql.connector as c

def fetch_classification_data(api_key):
    url = "https://api.harvardartmuseums.org/classification"
    params = {
        "apikey": api_key,
        "size": 100
    }
    response = R.get(url, params)
    return response.json()

def get_segments(data, min_objectcount=2500):
    segment = []
    for i in data['records']:
        if i['objectcount'] >= min_objectcount:
            segment.append(i["name"])
    return segment

def get_segment_record(data, segment_name):
    """Return the record for the selected segment/classification."""
    for record in data['records']:
        if record['name'].lower() == segment_name.lower():
            return record
    return None

##def get_pages(num_pages=25):
  ##  return [i for i in range(1, num_pages + 1)]

def fetch_segment_records(api_key, segment):
    """Fetch colors for a given classification segment (string) and list of pages."""
    records=[]
    url2 = "https://api.harvardartmuseums.org/object"
    for p in range(1,26):
        params2 = {
            "apikey": api_key,
            "size": 100,
            "page": p,
            "classification": segment
        }
        response2 = R.get(url2, params2)
        data2 = response2.json()
        records.extend(data2.get('records', []))
    return records


def build_artifact_metadata(data2):
    artifact_metadata = []
    for i in data2: 
        print(i)
        artifact_metadata.append(dict(
            id=i.get('id'),
            title=i.get('title'),
            culture=i.get('culture'),
            period=i.get('period'),
            century=i.get('century'),
            medium=i.get('medium'),
            dimensions=i.get('dimensions'),
            description=i.get('description'),
            department=i.get('department'),
            classification=i.get('classification'),
            accessionyear=i.get('accessionyear'),
            accessionmethod=i.get('accessionmethod'),
        ))
    return artifact_metadata

def build_artifact_media(data2):
    artifact_media = []
    for i in data2:
        artifact_media.append(dict(
            objectid=i.get('objectid'),
            imagecount=i.get('imagecount'),
            mediacount=i.get('mediacount'),
            colorcount=i.get('colorcount'),
            rank=i.get('rank'),
            datebegin=i.get('datebegin'),
            dateend=i.get('dateend'),
        ))
    return artifact_media

def build_artifact_colors(data2):
    artifact_colors = []
    for i in data2:
        if 'colors' in i and isinstance(i['colors'], list):
            for c in i['colors']:
                artifact_colors.append(dict(
                    objectid=i.get('objectid'),
                    color=c.get('color'),
                    spectrum=c.get('spectrum'),
                    hue=c.get('hue'),
                    percent=c.get('percent'),
                    css3=c.get('css3'),
                ))
    return artifact_colors

def connect_mysql():
    connection = c.connect(
        host='127.0.0.1',
        user='root',
        password='1302',
        database='harvard',
        port=3306
    )
    cursor = connection.cursor()
    return connection, cursor

def drop_all_tables(cursor):
    
    cursor.execute("DROP TABLE IF EXISTS artifact_colors;")
    cursor.execute("DROP TABLE IF EXISTS artifact_media;")
    cursor.execute("DROP TABLE IF EXISTS artifact_metadata;")


def recreate_artifact_metadata_table(cursor):
    table1 = "artifact_metadata"
    cursor.execute("SHOW TABLES LIKE %s", (table1,))
    result = cursor.fetchone()
    if result:
        print(f"✅ Table '{table1}' already exists. Skipping creation.")
        return
    create_query = (
        "CREATE TABLE artifact_metadata ("
        "id INT PRIMARY KEY,"
        "title VARCHAR(255),"
        "culture VARCHAR(100),"
        "period VARCHAR(100),"
        "century VARCHAR(50),"
        "medium VARCHAR(255),"
        "dimensions VARCHAR(255),"
        "description TEXT,"
        "department VARCHAR(100),"
        "classification VARCHAR(100),"
        "accessionyear INT,"
        "accessionmethod VARCHAR(100)"
        ");"
    )
    cursor.execute(create_query)
    print(f"✅ Table '{table1}' created successfully.")

def recreate_artifact_media_table(cursor):
    table2 = "artifact_media"
    cursor.execute("SHOW TABLES LIKE %s", (table2,))
    result = cursor.fetchone()
    if result:
        print(f"✅ Table '{table2}' already exists. Skipping creation.")
        return
    create_query = """
        CREATE TABLE artifact_media (
            objectid INT,
            imagecount INT,
            mediacount INT,
            colorcount INT,
            `rank` INT,
            datebegin INT,
            dateend INT,
            FOREIGN KEY (objectid) REFERENCES artifact_metadata(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
    """
    cursor.execute(create_query)
    print(f"✅ Table '{table2}' created successfully.")

def recreate_artifact_colors_table(cursor):
    table3 = "artifact_colors"
    cursor.execute("SHOW TABLES LIKE %s", (table3,))
    result = cursor.fetchone()
    if result:
        print(f"✅ Table '{table3}' already exists. Skipping creation.")
        return
    create_query = """
        CREATE TABLE artifact_colors (
        objectid INT,
        color VARCHAR(50),
        spectrum VARCHAR(50),
        hue VARCHAR(50),
        percent FLOAT,
        css3 VARCHAR(50),
        FOREIGN KEY (objectid) REFERENCES artifact_metadata(id)
         ON DELETE CASCADE
         ON UPDATE CASCADE
        );"""
    cursor.execute(create_query)
    print(f"✅ Table '{table3}' created successfully.")

def insert_artifact_metadata(artifact_metadata, cursor, connection):
    for item in artifact_metadata:
        cursor.execute("""
            INSERT IGNORE INTO artifact_metadata (
                id, title, culture, period, century, medium, dimensions, description,
                department, classification, accessionyear, accessionmethod
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item['id'], item['title'], item['culture'], item['period'], item['century'],
            item['medium'], item['dimensions'], item['description'], item['department'],
            item['classification'], item['accessionyear'], item['accessionmethod']
        ))
    connection.commit()

def insert_artifact_media(artifact_media, cursor, connection):
    for item in artifact_media:
        cursor.execute("""
            INSERT IGNORE INTO artifact_media (
                objectid, imagecount, mediacount, colorcount, `rank`, datebegin, dateend
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            item['objectid'], item['imagecount'], item['mediacount'], item['colorcount'],
            item['rank'], item['datebegin'], item['dateend']
        ))
    connection.commit()

def insert_artifact_colors(artifact_colors, cursor, connection):
    for item in artifact_colors:
        cursor.execute("""
            INSERT IGNORE INTO artifact_colors (
                objectid, color, spectrum, hue, percent, css3
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            item['objectid'], item['color'], item['spectrum'], item['hue'],
            item['percent'], item['css3']
        ))
    connection.commit()