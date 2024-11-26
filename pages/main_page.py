import streamlit as st
import mysql.connector
import pandas as pd
from time import sleep
import string

conn = mysql.connector.connect(host=st.secrets.DB_HOST, user=st.secrets.DB_USERNAME, password=st.secrets.DB_PASSWORD,
								port = st.secrets.DB_PORT, db=st.secrets.DB_NAME, auth_plugin='mysql_native_password')

if st.session_state["logged_in"] == True:
    st.write('Você está logado como:', st.session_state.user_state['nome'])
    st.session_state.disabled = False
    loginout_button = st.button("Logout", type="primary")
    if loginout_button:
        st.session_state["logged_in"] = False
        st.success("Logged out!")
        sleep(0.5)
        st.switch_page("login.py")
else:
    st.write('Você não está logado')
    st.session_state.disabled = True
    loginout_button = st.button("Login", type="primary")
    if loginout_button:
        st.session_state["logged_in"] = False
        sleep(0.5)
        st.switch_page("login.py")


st.divider()

st.title("Sistem de transparencia escolar em Rio Claro")

st.divider()

options = [
    "Informações gerais", 
    "Alunos, professores e turmas por escola", 
    "Ordernar por número de alunos",
    "Listar todas as turmas de uma escola",
    "Listar alunos e professores de uma escola",
    "Quantidade de alunos por nível de ensino"
    ] 
with st.container(border=True):
    option = st.selectbox(
        "Que tipo de busca gostaria de realizar?",
        ("Informações gerais", 
        "Alunos, professores e turmas por escola", 
        "Ordernar por número de alunos",
        "Listar todas as turmas de uma escola",
        "Listar alunos e professores de uma escola",
        "Quantidade de alunos por nível de ensino"),
        index=None,
        placeholder="Escolha a opção...",
    )

    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode("utf-8")

    cursor = conn.cursor()

    if option == options[0]:
        inp = f"SELECT * FROM infos_escolas"
        cursor.execute(inp)
        res = cursor.fetchall()
        df = pd.DataFrame(res, columns=cursor.column_names)
        st.write(df)
        csv = convert_df(df)
        st.download_button(
            label="Baixar dados como CSV",
            data=csv,
            file_name="infos_escolas.csv",
            mime="text/csv",
            disabled=st.session_state.disabled,
            type="primary",
        )

    if option == options[1]:
        st.write("Total de Turma/Docente/Aluno por escola")
        inp = f"SELECT * FROM atd_escola"
        cursor.execute(inp)
        res = cursor.fetchall()
        df = pd.DataFrame(res, columns=cursor.column_names)
        st.write(df)
        csv = convert_df(df)
        st.download_button(
            label="Baixar dados como CSV",
            data=csv,
            file_name="total_tda_escola.csv",
            mime="text/csv",
            disabled=st.session_state.disabled,
            type="primary",
        )


    if option == options[2]:
        st.write("Escolas ordenadas por número de alunos")
        inp = f"SELECT * FROM total_alunos_ordenado"
        cursor.execute(inp)
        res = cursor.fetchall()
        df = pd.DataFrame(res, columns=cursor.column_names)
        st.write(df)
        csv = convert_df(df)
        st.download_button(
            label="Baixar dados como CSV",
            data=csv,
            file_name="escolas_por_numero_aluno.csv",
            mime="text/csv",
            disabled=st.session_state.disabled,
            type="primary",
        )

    if option == options[3]:
        st.write("Turmas de uma escola")
        ecod = st.text_input("Informe o código da escola desejada:")
        button = st.button(label="Buscar", icon="🔍")
        if button:
            inp = f"CALL turmas_por_escola ({ecod})"
            cursor.execute(inp)
            res = cursor.fetchall()
            df = pd.DataFrame(res, columns=cursor.column_names)
            st.write(df)
            csv = convert_df(df)
            st.download_button(
                label="Baixar dados como CSV",
                data=csv,
                file_name="turmas_por_escola.csv",
                mime="text/csv",
                disabled=st.session_state.disabled,
                type="primary",
            )

    if option == options[4]:
        st.write("Alunos e Professores de uma escola")
        ecod = st.text_input("Informe o código da escola desejada:")
        button = st.button(label="Buscar", icon="🔍")
        if button:
            inp = f"CALL professores_alunos ({ecod})"
            cursor.execute(inp)
            res = cursor.fetchall()
            df = pd.DataFrame(res, columns=cursor.column_names)
            st.write(df)
            csv = convert_df(df)
            st.download_button(
                label="Baixar dados como CSV",
                data=csv,
                file_name="alunos_prof_escolas.csv",
                mime="text/csv",
                disabled=st.session_state.disabled,
                type="primary",
            )

    if option == options[5]:
        st.write("Alunos pelo nível de ensino")
        inp = f"SELECT * FROM alunos_por_nivel"
        cursor.execute(inp)
        res = cursor.fetchall()
        df = pd.DataFrame(res, columns=cursor.column_names)
        st.write(df)
        csv = convert_df(df)
        st.download_button(
            label="Baixar dados como CSV",
            data=csv,
            file_name="alunos_nivel.csv",
            mime="text/csv",
            disabled=st.session_state.disabled,
            type="primary",
        )

with st.expander("Adicionar uma escola no bookmark"):
    #st.write("Adicionar uma escola no bookmark")
    option = st.selectbox(
        "Escolha a opção desejada:",
        ("Nome", "Código de Entidade"),
        disabled=st.session_state.disabled,
    )

    if option == "Nome":
        nome = st.text_input("Informe o nome da escola:",disabled=st.session_state.disabled)
        button = st.button(label="Adicionar",disabled=st.session_state.disabled)
        if button:
            inp = f"SELECT CO_ENTIDADE FROM escola WHERE NO_ENTIDADE = '{nome}'"
            cursor.execute(inp)
            res = cursor.fetchall()
            df_entidade = pd.DataFrame(res, columns=cursor.column_names)
            if len(df_entidade) == 1:
                inp = f"INSERT INTO bookmark (ID_USU,ID_ESC) VALUES ('{st.session_state.user_state['ID']}','{df_entidade.iloc[0]['CO_ENTIDADE']}')"
                cursor.execute(inp)
                st.success("Escola adicionada com sucesso ao bookmark")
                conn.commit()
            else:
                st.error("Erro ao adicionar a escola")
                conn.rollback()

    elif option == "Código de Entidade":
        co_entidade = st.text_input(label="Informe o codigo da escola:",disabled=st.session_state.disabled)
        button = st.button(label="Adicionar",disabled=st.session_state.disabled)
        if button:
            inp = f"SELECT * FROM escola WHERE CO_ENTIDADE = '{co_entidade}'"
            cursor.execute(inp)
            res = cursor.fetchall()
            df_entidade = pd.DataFrame(res, columns=cursor.column_names)
            if len(df_entidade) == 1:
                inp = f"INSERT INTO bookmark (ID_USU,ID_ESC) VALUES ({st.session_state.user_state['ID']},{co_entidade})"
                cursor.execute(inp)
                st.success("Escola adicionada com sucesso ao bookmark")
                conn.commit()
            else:
                st.error("Erro ao adicionar a escola")
                conn.rollback()

escolas_fav = st.button("Ir para minhas escolas favoritas",disabled=st.session_state.disabled)

if escolas_fav:
    st.switch_page("pages/bookmark.py")