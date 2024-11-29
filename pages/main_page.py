import streamlit as st
import mysql.connector
import pandas as pd
import time 

st.set_page_config(
    page_title="Tela principal - Sistema Escolas Rio Claro",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed",
)

conn = mysql.connector.connect(host=st.secrets.DB_HOST, user=st.secrets.DB_USERNAME, password=st.secrets.DB_PASSWORD,
								port = st.secrets.DB_PORT, db=st.secrets.DB_NAME, auth_plugin='mysql_native_password')

cursor = conn.cursor()

@st.cache_data
def run_query(query):
    cursor.execute(query)
    res = cursor.fetchall()
    df = pd.DataFrame(res, columns=cursor.column_names)
    return df

if st.session_state["logged_in"] == True:
    st.write('Você está logado como:', st.session_state.user_state['nome'])
    st.session_state.disabled = False
    loginout_button = st.button("Logout", type="primary")
    if loginout_button:
        st.session_state["logged_in"] = False
        st.success("Logged out!")
        time.sleep(0.5)
        st.switch_page("login.py")
else:
    st.write('Você não está logado')
    st.session_state.disabled = True
    loginout_button = st.button("Login", type="primary")
    if loginout_button:
        st.session_state["logged_in"] = False
        time.sleep(0.5)
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
    "Quantidade de alunos por nível de ensino",
    "Gêneros por escola",
    "Idades médias por escola",
    "Informações de infraestrutura",
    "Informações de NSE dos alunos das escolas"
    ] 
with st.container(border=True):
    option = st.selectbox(
        "Que tipo de busca gostaria de realizar?",
        ("Informações gerais", 
        "Alunos, professores e turmas por escola", 
        "Ordernar por número de alunos",
        "Listar todas as turmas de uma escola",
        "Listar alunos e professores de uma escola",
        "Quantidade de alunos por nível de ensino",
        "Gêneros por escola",
        "Idades médias por escola",
        "Informações de infraestrutura",
        "Informações de NSE dos alunos das escolas"
        ),
        index=None,
        placeholder="Escolha a opção...",
    )

    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode("utf-8")

    if option == options[0]:
        inp_opt1 = f"SELECT * FROM infos_escolas"
        df = run_query(inp_opt1)
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
        inp_opt2 = f"SELECT * FROM atd_escola"
        df = run_query(inp_opt2)
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
        inp_opt3 = f"SELECT * FROM total_alunos_ordenado"
        df = run_query(inp_opt3)
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
            inp_opt4 = f"CALL turmas_por_escola ({ecod})"
            df = run_query(inp_opt4)
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
            inp_opt5 = f"CALL professores_alunos ({ecod})"
            df = run_query(inp_opt5)
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
        inp_opt6_1 = f"SELECT * FROM alunos_por_nivel"
        df = run_query(inp_opt6_1)
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

        ecod = st.text_input("Informe o código da escola desejada:")
        button = st.button(label="Buscar", icon="🔍")

        if button:
            inp_opt6_2= f"CALL especifico_alunos_por_nivel ({ecod})"
            dfe = run_query(inp_opt6_2)
            st.write(dfe)
            csv_especifico = convert_df(dfe)

            st.download_button(
                label="Baixar dados como CSV",
                data=csv_especifico,
                file_name="alunos_nivel_especifico.csv",
                mime="text/csv",
                disabled=st.session_state.disabled,
                type="primary",
            )
    
    if option == options[6]:
        st.write("Gênero dos alunos por escola")
        inp_opt7 = f"SELECT * FROM alunos_por_genero"
        df = run_query(inp_opt7)
        st.write(df)
        csv = convert_df(df)

        st.download_button(
                label="Baixar dados como CSV",
                data=csv,
                file_name="alunos_por_genero.csv",
                mime="text/csv",
                disabled=st.session_state.disabled,
                type="primary",
            )

    if option == options[7]:
        st.write("Idades médias dos alunos por escola")
        inp_opt8_1 = f"SELECT * FROM media_idade_alunos"
        dfa = run_query(inp_opt8_1)
        st.write(dfa)
        csv_a = convert_df(dfa)

        st.download_button(
                label="Baixar dados como CSV",
                data=csv_a,
                file_name="idades_medias_alunos.csv",
                mime="text/csv",
                disabled=st.session_state.disabled,
                type="primary",
            )
        
        st.write("Idades médias dos docentes por escola")
        inp_opt8_2 = f"SELECT * FROM media_idade_docentes"
        dfd = run_query(inp_opt8_2)
        st.write(dfd)
        csv_d = convert_df(dfd)

        st.download_button(
                label="Baixar dados como CSV",
                data=csv_d,
                file_name="idades_medias_docentes.csv",
                mime="text/csv",
                disabled=st.session_state.disabled,
                type="primary",
            )

    if option == options[8]:

        st.write("Informações de infraestrutura")   

        inp_opt9_1 = f"SELECT possuem_bib ()"
        df1 = run_query(inp_opt9_1)
        st.write("Total de escolas que possuem biblioteca: ", df1.iloc[0]['possuem_bib ()'])

        inp_opt9_2 = f"SELECT possuem_comput ()"
        df2 = run_query(inp_opt9_2)
        st.write("Total de escolas que possuem computador: ", df2.iloc[0]['possuem_comput ()'])

        inp_opt9_3 = f"SELECT acesso_internet ()"
        df3 = run_query(inp_opt9_3)
        st.write("Total de escolas com acesso à internet: ", df3.iloc[0]['acesso_internet ()'])

    if option == options[9]:
        st.write("Informações de NSE dos alunos das escolas")  

        ecod = st.text_input("Informe o código da escola que deseja buscar")
        button = st.button(label="Buscar", icon="🔍")

        if button:
            inp_opt10_1 = f"SELECT * FROM nse_2015 WHERE CO_ESCOLA = '{ecod}'"
            df = run_query(inp_opt10_1)
            if len(df) == 1:
                st.write(df)
                csv_especifico = convert_df(df)
            else:
                st.error("Escola não consta na tabela, informe outro código de escola")
        else:
            st.write("Dados com todas as escolas")
            inp_opt10_2 = f"SELECT * FROM nse_2015"
            df = run_query(inp_opt10_2)
            st.write(df)

            csv = convert_df(df)
            st.download_button(
                label="Baixar dados como CSV",
                data=csv,
                file_name="nse_escolas.csv",
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
            inp_bookmark_nome = f"SELECT CO_ENTIDADE FROM escola WHERE NO_ENTIDADE = '{nome}'"
            df_entidade = run_query(inp_bookmark_nome)
            if len(df_entidade) == 1:
                inp_bookmark_escola_ja_existe = f"SELECT * FROM bookmark WHERE ID_ESC = {df_entidade.iloc[0]['CO_ENTIDADE']} AND ID_USU = {st.session_state.user_state['ID']}"
                cursor.execute(inp_bookmark_escola_ja_existe)
                res = cursor.fetchall()
                df_bookmark_existe = pd.DataFrame(res, columns=cursor.column_names)
                if len(df_bookmark_existe) >= 1:
                    st.error("Escola já está no bookmark do usuário")
                    conn.rollback()
                else:
                    inp_bookmark_nome1 = f"INSERT INTO bookmark (ID_USU,ID_ESC) VALUES ('{st.session_state.user_state['ID']}','{df_entidade.iloc[0]['CO_ENTIDADE']}')"
                    run_query(inp_bookmark_nome1)
                    st.success("Escola adicionada com sucesso ao bookmark")
                    conn.commit()
            else:
                st.error("Erro ao adicionar a escola")
                conn.rollback()

    elif option == "Código de Entidade":
        co_entidade = st.text_input(label="Informe o codigo da escola:",disabled=st.session_state.disabled)
        button = st.button(label="Adicionar",disabled=st.session_state.disabled)
        if button:
            inp_bookmark_codigo = f"SELECT * FROM escola WHERE CO_ENTIDADE = '{co_entidade}'"
            df_entidade = run_query(inp_bookmark_codigo)
            if len(df_entidade) == 1:
                inp_bookmark_escola_ja_existe = f"SELECT * FROM bookmark WHERE ID_ESC = {co_entidade} AND ID_USU = {st.session_state.user_state['ID']}"
                cursor.execute(inp_bookmark_escola_ja_existe)
                res = cursor.fetchall()
                df_bookmark_existe = pd.DataFrame(res, columns=cursor.column_names)
                if len(df_bookmark_existe) >= 1:
                    st.error("Escola já está no bookmark do usuário")
                    conn.rollback()
                else:
                    inp_bookmark_codigo1 = f"INSERT INTO bookmark (ID_USU,ID_ESC) VALUES ({st.session_state.user_state['ID']},{co_entidade})"
                    run_query(inp_bookmark_codigo1)
                    st.success("Escola adicionada com sucesso ao bookmark")
                    conn.commit()
            else:
                st.error("Erro ao adicionar a escola")
                conn.rollback()

escolas_fav = st.button("Ir para minhas escolas favoritas",disabled=st.session_state.disabled)

if escolas_fav:
    st.switch_page("pages/bookmark.py")