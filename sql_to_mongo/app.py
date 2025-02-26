import streamlit as st
import pymongo
import sqlparse
import tempfile
import os
import re


MONGO_URI = "mongodb://localhost:27017"
mongo_client = pymongo.MongoClient(MONGO_URI)
mongo_db = mongo_client["sql_migration_db"]

st.title("Upload PostgreSQL Dump and Save to MongoDB")

uploaded_file = st.file_uploader("Upload PostgreSQL dump (.sql)", type=["sql"])

if uploaded_file:
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".sql") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_sql_path = temp_file.name

    st.success(f"✅ File uploaded: {uploaded_file.name}")

    
    with open(temp_sql_path, "r", encoding="utf-8") as f:
        sql_dump = f.read()
    
    sql_dump = re.sub(r"--.*?\n", "", sql_dump)  
    sql_dump = re.sub(r"/\*.*?\*/", "", sql_dump, flags=re.DOTALL)  

    parsed_statements = sqlparse.split(sql_dump)
    
    table_schemas = {}

    for statement in parsed_statements:
        statement = statement.strip()
        statement_lower = statement.lower()
        
        st.write(f"📜 Parsed SQL Statement: {statement[:200]}...")  

        try:
            
            if statement_lower.startswith("create table"):
                st.write("🔍 Found CREATE TABLE statement!")

                table_match = re.search(r"create table\s+[`\"']?(\w+)[`\"']?\s*\(", statement, re.IGNORECASE)

                if table_match:
                    table_name = table_match.group(1)
                    st.write(f"🆕 Extracting schema for `{table_name}`")
                    
                    column_definitions = statement.split("(", 1)[1].rsplit(")", 1)[0]
                                        
                    column_matches = re.findall(r"^\s*`?(\w+)`?\s+[\w()]+", column_definitions, re.MULTILINE)
                    column_names = [col for col in column_matches if col.lower() not in ["primary", "key", "foreign", "references"]]

                    if column_names:
                        table_schemas[table_name] = column_names
                        st.write(f"✅ Schema extracted for `{table_name}`: {column_names}")
                    else:
                        st.error(f"⚠️ No columns found in `{table_name}`. Possible SQL syntax issue.")

                else:
                    st.error("⚠️ `CREATE TABLE` regex failed! The statement format may be different.")

            
            elif statement_lower.startswith("insert into"):
                table_name_match = re.search(r"insert into\s+[`\"']?(\w+)[`\"']?", statement, re.IGNORECASE)
                
                if table_name_match:
                    table_name = table_name_match.group(1)

                    
                    if table_name not in table_schemas:
                        st.error(f"⚠️ Skipping `{table_name}`: No schema found.")
                        continue

                    
                    values_start = statement_lower.find("values") + 6
                    values_data = statement[values_start:].strip().strip(";")

                    
                    rows = re.findall(r"\((.*?)\)", values_data)
                    entries = []

                    for row in rows:
                        values = re.split(r",(?=(?:[^']*'[^']*')*[^']*$)", row)  
                        values = [v.strip().strip("'") for v in values]

                        if len(values) != len(table_schemas[table_name]):
                            st.error(f"⚠️ Skipping row in `{table_name}`: Column count mismatch.")
                            continue

                        entry = dict(zip(table_schemas[table_name], values))
                        entries.append(entry)

                    
                    if entries:
                        mongo_db[table_name].insert_many(entries)
                        st.success(f"✅ Inserted {len(entries)} records into `{table_name}`.")

        except Exception as e:
            st.error(f"❌ Error processing statement: {statement[:100]}... | Error: {str(e)}")

    
    os.remove(temp_sql_path)
    st.success("🎉 SQL file processing completed successfully.")
