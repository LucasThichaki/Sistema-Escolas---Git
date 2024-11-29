import mysql.connector
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Bookmark - Sistema Escolas Rio Claro",
    page_icon="⭐",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("Suas escolas :rainbow[favoritas]")
st.balloons()

conn = mysql.connector.connect(host=st.secrets.DB_HOST, user=st.secrets.DB_USERNAME, password=st.secrets.DB_PASSWORD,port = st.secrets.DB_PORT, db=st.secrets.DB_NAME, auth_plugin='mysql_native_password')
cursor = conn.cursor()

inp = f"SELECT NO_ENTIDADE FROM escola CROSS JOIN (SELECT ID_ESC FROM bookmark WHERE ID_USU = {st.session_state.user_state['ID']}) as user_bookmark WHERE CO_ENTIDADE = ID_ESC"
cursor.execute(inp)
res = cursor.fetchall()
df = pd.DataFrame(res, columns=cursor.column_names)
if len(df) != 0:
    st.write(df)
else:
    st.write("Usuário não tem nenhuma escola no bookmark!")

button = st.button("Voltar para pagina inicial")

if button:
    st.switch_page("pages/main_page.py")
