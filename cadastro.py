import streamlit as st
from pymongo import MongoClient
import hashlib  
from pymongo.errors import ConnectionFailure, OperationFailure

# Configuração de Conexão com MongoDB Atlas (substitua as credenciais pelo seu URI)
MONGO_URI = "mongodb+srv://agrosense:<db_password>@agrosense.ex6w7.mongodb.net/"

# Conexão com o MongoDB Atlas
try:
    client = MongoClient(MONGO_URI)
    db = client.get_database("AgroSense")  # Nome do banco de dados
    collection = db["usuarios"]                # Nome da coleção para armazenar os dados de cadastro
    st.success("Conexão com MongoDB estabelecida com sucesso.")
except ConnectionFailure:
    st.error("Erro ao conectar-se ao MongoDB. Verifique suas credenciais e conexão com a internet.")
except Exception as e:
    st.error(f"Erro inesperado ao conectar-se ao MongoDB: {e}")

# Função para salvar os dados no MongoDB
def salvar_dados(nome, cpf, celular, endereco, empresa, profissao, email, senha):
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()  # Criptografa a senha com SHA-256
    dados = {
        "nome": nome,
        "cpf": cpf,
        "celular": celular,
        "endereco": endereco,
        "empresa": empresa,
        "email": email,
        "profissão": profissao,
        "senha": senha_hash  # Armazena a senha criptografada
    }
    # Inserir dados na coleção "usuarios"
    collection.insert_one(dados)
    st.success("Cadastro realizado com sucesso!")
       
  

# Interface de cadastro
st.title("Cadastro de Usuário")

# Formulário de cadastro
with st.form("form_cadastro"):
    nome = st.text_input("Nome Completo")
    cpf = st.text_input("CPF")
    celular = st.text_input("Número de Celular")
    endereco = st.text_area("Endereço")
    empresa = st.text_input("Empresa")
    email = st.text_input("E-mail")
    profissao = st.text_input("Profissão")
    senha = st.text_input("Senha", type="password")  # Campo de senha
    submit_button = st.form_submit_button("Cadastrar")

    # Verificar se o formulário foi submetido
    if submit_button:
        # Verificação simples de preenchimento de campos
        if not all([nome, cpf, celular, endereco, empresa, email, profissao, senha]):
            st.error("Por favor, preencha todos os campos.")
        else:
            # Salvar dados no MongoDB
            salvar_dados(nome, cpf, celular, endereco, empresa, email, profissao, senha)

