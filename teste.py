import streamlit as st
from pymongo import MongoClient
from PIL import Image
import os

# Conectando ao MongoDB
@st.cache_resource
def init_connection():
    # Substitua pela sua URI de conexão do MongoDB
    client = MongoClient("mongodb://localhost:27017")  # Conexão local
    return client

client = init_connection()

# Selecionando o banco de dados e coleção
db = client["AgroSense"]
colecao = db["imagens"]

# Variável para armazenar o ID da imagem, começa em 1
if 'image_id' not in st.session_state:
    st.session_state['image_id'] = 1  # Inicializa o ID da imagem

# Função para gerar o próximo ID
def generate_image_id():
    image_id = st.session_state['image_id']
    st.session_state['image_id'] += 1  # Incrementa o ID para o próximo upload
    return image_id

# Upload da imagem
uploaded_file = st.file_uploader("Escolha uma imagem", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Gera automaticamente um ID para a imagem
    image_id = generate_image_id()
    
    # Abrir e exibir a imagem
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagem carregada com sucesso!", use_column_width=True)
    
    # Informações da imagem
    image_name = uploaded_file.name

# Exibir as informações da imagem
    st.write(f"**ID**: {image_id}")
    st.write(f"**Nome**: {image_name}") 

 # Salvar a imagem localmente (opcional)
    image_folder = "imagens"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)  # Cria a pasta se não existir

    image_path = os.path.join(image_folder, f"{image_id}_{image_name}")
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"Imagem salva com sucesso: {image_path}")   

# Função para inserir dados no MongoDB
def inserir_dados(nome, tamanho):
    colecao.insert_one({ "nome": nome, "tamanho": tamanho})


# Função para buscar dados do MongoDB
def buscar_dados():
    return list(colecao.find())

# Interface do Streamlit
st.title("Imagens dos bixos")

# Formulário de entrada de dados
st.subheader("Inserir novos dados")

nome = st.text_input("Nome:")
tamanho = st.number_input("tamanho:")

if st.button("Adicionar"):
    inserir_dados(nome, tamanho)
    st.success("Dados inseridos com sucesso!")

# Exibindo os dados armazenados no MongoDB
st.subheader("Dados armazenados")
dados = buscar_dados()
for item in dados:
    st.write(f"Nome: {item['nome']}, Tamanho: {item['tamanho']}")
