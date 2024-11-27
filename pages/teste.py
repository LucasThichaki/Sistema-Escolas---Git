import streamlit as st
import mysql.connector
import pandas as pd

conn = mysql.connector.connect(host=st.secrets.DB_HOST, user=st.secrets.DB_USERNAME, password=st.secrets.DB_PASSWORD,
								port = st.secrets.DB_PORT, db=st.secrets.DB_NAME, auth_plugin='mysql_native_password')


cursor = conn.cursor()

@st.cache_data
def run_query(query):
	cursor.execute(query)
	return cursor.fetchall()

st.write(columns=cursor.column_names)

inp = f"SELECT * FROM infos_escolas"
res = run_query(inp)
df = pd.DataFrame(res, columns=cursor.column_names)
st.write(df)



