import streamlit as st
import pymongo
import re

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017"
client = pymongo.MongoClient(MONGO_URI)
db = client["your_database"]
collection = db["your_collection"]

st.title("Upload PostgreSQL SQL File & Insert into MongoDB")

# Upload SQL file
uploaded_file = st.file_uploader("Upload an SQL file", type=["sql"])

if uploaded_file is not None:
    try:
        # Read SQL file with proper encoding
        sql_content = uploaded_file.read().decode("utf-8", errors="replace")

        # Extract INSERT statements
        insert_statements = re.findall(r"INSERT INTO\s+(\w+)\s*\((.?)\)\sVALUES\s*\((.*?)\);", sql_content, re.DOTALL)

        if insert_statements:
            parsed_data = []
            for table, columns, values in insert_statements:
                columns = [col.strip() for col in columns.split(",")]
                values_list = values.split("),(")  # Handle multiple rows
                for values in values_list:
                    values = [v.strip().strip("'") for v in values.split(",")]
                    parsed_data.append(dict(zip(columns, values)))

            st.write("Parsed Data Preview:")
            st.write(parsed_data[:5])  # Show first few records

            if st.button("Insert into MongoDB"):
                collection.insert_many(parsed_data)
                st.success("Data successfully inserted into MongoDB!")

        else:
            st.error("No INSERT statements found in the SQL file.")

    except Exception as e:
        st.error(f"Error processing file: {e}")