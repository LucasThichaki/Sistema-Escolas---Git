#from st_pages import hide_pages
from time import sleep
import streamlit as st
import mysql.connector 
import pandas as pd

if 'user_state' not in st.session_state:
    st.session_state.user_state = {
        'ID':'',
        'nome':'',
        'email': '',
        'password': '',
        'logged_in': False
    }

def log_in():
    st.session_state["logged_in"] = True
    #hide_pages([])
    st.success("Logged in!")
    sleep(0.5)
    st.switch_page("pages/main_page.py")


def log_out():
    st.session_state["logged_in"] = False
    st.success("Logged out!")
    sleep(0.5)

if not st.session_state.get("logged_in", False):
    with st.form("login"):
        st.title("Login do Usuário")
        email = st.text_input("Email:", key="email")
        senha = st.text_input("Senha:", type="password", key="senha")
        submit = st.form_submit_button("Logar", type="primary",use_container_width=True)
        cadastrar_button = st.form_submit_button("Cadastrar",use_container_width=True)
        guest_button = st.form_submit_button("Entrar como Convidado",use_container_width=True)

    conn = mysql.connector.connect(host=st.secrets.DB_HOST, user=st.secrets.DB_USERNAME, password=st.secrets.DB_PASSWORD,
								port = st.secrets.DB_PORT, db=st.secrets.DB_NAME, auth_plugin='mysql_native_password')
    cursor = conn.cursor()
    inp = f"SELECT * FROM usuario WHERE email = '{email}' AND senha = sha('{senha}')"
    cursor.execute(inp)
    res = cursor.fetchall()
    df = pd.DataFrame(res, columns=cursor.column_names)

    if submit and len(df) == 1:
        st.session_state.user_state['ID'] = df.iloc[0]['ID']
        st.session_state.user_state['nome'] = df.iloc[0]['NOME']
        st.session_state.user_state['email'] = email
        st.session_state.user_state['password'] = senha
        st.session_state.user_state['logged_in'] = True
        st.session_state["logged_in"] = True
        #hide_pages([])
        st.success("Logged in!")
        sleep(0.5)
        st.switch_page("pages/main_page.py")
    elif submit:
        st.error("Email ou senha inserida incorretamente")

else:
    st.write("Logged in!")
    st.button("log out", on_click=log_out)

if guest_button:
    st.session_state.user_state['logged_in'] = False
    st.session_state["logged_in"] = False
    sleep(0.5)
    st.switch_page("pages/main_page.py")

if cadastrar_button:
    sleep(0.5)
    st.switch_page("pages/cadastro.py")