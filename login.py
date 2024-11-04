import streamlit as st

# Dicionário para armazenar os dados de login (em uma aplicação real, use um banco de dados seguro)
users = {"usuario": "senha123"}  # Exemplo simples de usuário e senha

def login():
    st.title("Tela de Login")
    
    # Formulário de login
    with st.form("login_form"):
        username = st.text_input("Nome de usuário")
        password = st.text_input("Senha", type="password")
        login_button = st.form_submit_button("Entrar")
        
        if login_button:
            # Verificar credenciais
            if username in users and users[username] == password:
                st.success("Login realizado com sucesso!")
                return True  # Login bem-sucedido
            else:
                st.error("Usuário ou senha incorretos.")
                return False  # Login falhou

# Chamada da função login
if login():
    st.write("Bem-vindo ao sistema!")
else:
    st.write("Faça login para acessar o conteúdo.")