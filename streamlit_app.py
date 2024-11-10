import streamlit as st
import requests

st.title("AgendAçougue")

api_url = "http://127.0.0.1:5000"  # URL local do backend Flask

# Sessão de registro
st.header("Registrar-se")
nome = st.text_input("Nome")
email = st.text_input("Email")
senha = st.text_input("Senha", type="password")

if st.button("Registrar"):
    response = requests.post(f"{api_url}/register", json={"nome": nome, "email": email, "senha": senha})
    if response.status_code == 200:
        st.success("Registro realizado com sucesso!")
    else:
        st.error("Erro no registro")

# Sessão de login
st.header("Login")
login_email = st.text_input("Email para Login")
login_senha = st.text_input("Senha para Login", type="password")
token = None

if st.button("Login"):
    response = requests.post(f"{api_url}/login", json={"email": login_email, "senha": login_senha})
    if response.status_code == 200:
        token = response.json().get("token")
        st.success("Login realizado com sucesso!")
    else:
        st.error("Email ou senha incorretos")

# Listar serviços disponíveis
if token:
    st.header("Serviços Disponíveis")
    response = requests.get(f"{api_url}/servicos")
    if response.status_code == 200:
        servicos = response.json().get("servicos", [])
        for servico in servicos:
            st.write(f"{servico['nome']}: {servico['descricao']} - R$ {servico['preco']} ({servico['duracao']} minutos)")
    else:
        st.error("Erro ao buscar serviços")

# Agendamento de serviços
if token:
    st.header("Agendar Serviço")
    cliente_id = st.text_input("ID do Cliente")
    servico_id = st.text_input("ID do Serviço")
    data_hora = st.text_input("Data e Hora do Agendamento (YYYY-MM-DD HH:MM)")

    if st.button("Agendar"):
        response = requests.post(f"{api_url}/agendamentos", headers={"Authorization": f"Bearer {token}"}, json={
            "cliente_id": cliente_id,
            "servico_id": servico_id,
            "data_hora": data_hora
        })
        if response.status_code == 200:
            st.success("Agendamento realizado com sucesso!")
        else:
            st.error("Erro ao realizar agendamento")
