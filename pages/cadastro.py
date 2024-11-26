import mysql.connector
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

st.header("Sistema de Escolas")

def validar(nome, email, senha, data_cadastro, data_nascimento, idade):
	if nome=="" or email=="" or senha=="" or data_cadastro=="" or data_nascimento=="" or idade=="":
		return False
	return True

def cadastra_usuario(nome, email, senha, data_cadastro, data_nascimento, idade):
	# inserir os dados de seu MySQL
	conn = mysql.connector.connect(host=st.secrets.DB_HOST, user=st.secrets.DB_USERNAME, password=st.secrets.DB_PASSWORD,
								port = st.secrets.DB_PORT, db=st.secrets.DB_NAME, auth_plugin='mysql_native_password')
	cursor = conn.cursor()
	# ajustar conforme os campos da tabela Usuario de seu banco
	inp = f"INSERT INTO usuario VALUES (ID, '{nome}', '{email}','{idade}','{data_cadastro}',sha('{senha}'), '{data_nascimento}')"
	try:
		cursor.execute(inp)
		st.success("Usuário cadastrado.")
	except Exception as e:
		conn.rollback()
		st.error(f"Erro ao cadastrar o usuário {e}")
	finally:
		cursor.close()
	conn.commit()

with st.form("cadastro"):
    st.title("Cadastro de Usuários")
    nome = st.text_input("Nome:")
    email = st.text_input("Email:")
    senha = st.text_input("Senha:", type="password")
    data_cadastro = datetime.date.today()
    data_nascimento = st.date_input('Data de nascimento:', min_value=datetime.date(1924,1,1), max_value=datetime.date(2024,1,1), format="YYYY-MM-DD")
    idade = data_cadastro.year - data_nascimento.year - ((data_cadastro.month, data_cadastro.day) < (data_nascimento.month,data_nascimento.day))
    submit = st.form_submit_button("Enviar")

if submit and validar(nome, email, senha, data_cadastro, data_nascimento, idade):
	# se o form for submetido e os dados estiverem válidos
	cadastra_usuario(nome, email, senha, data_cadastro, data_nascimento, idade)
	st.switch_page("login.py")
elif submit:
	# se o form for submetido mas com dados inválidos
	st.warning("Dados inválidos")