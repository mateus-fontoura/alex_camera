import streamlit as st
import requests
import json

# Função para enviar a requisição
def send_request(cmd_code, imei):
    url = "http://10.1.0.12:9080/api/config/v1/"
    params = {
        "cmdCode": cmd_code,
        "imei": imei,
        "_method_": "savaInstruction",
        "taskId": "1",
        "userId": "123",
        "cmdId": "1",
        "cmdType": "0",
        "proNo": "8",
        "platform": "web",
        "sender": "tracksolid",
        "sendTime": "1701696837670",
        "language": "en",
        "sync": "true",
        "offLineFlag": "0",
        "offLineInsType": "customIns",
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        data = response.json()

        if data.get('code') == 0:
            if cmd_code == "VERSION":
                version_info = json.loads(data['data'])['_content'].split('[VERSION]')[1].split(',')[0]
                return f"\nVersão: {version_info}"
            else:
                content = json.loads(data['data']).get('_content')
                return f"\nResposta: {content}"
        else:
            return "\nCamera Offline"
    except requests.exceptions.RequestException as e:
        return f"\nErro de conexão, verifique a VPN"

# Interface Streamlit
st.title('Interface de Controle da Câmera')

# Barra lateral com documentação
with st.sidebar:
    st.header("Documentação")
    st.write("""
        - **VERSION**: Obtém a versão da câmera.
        - **DMS_VIRTUAL_SPEED**: Define a velocidade virtual.
        - **REBOOT**: Reinicia a câmera.
        - ...
    """)

# Entradas do usuário
imei = st.text_input('IMEI da Câmera')
cmd_code = st.selectbox('Escolha o Comando', ['VERSION', 'DMS_VIRTUAL_SPEED,60', 'REBOOT'])

# Botão para enviar a requisição
if st.button('Enviar Comando'):
    response = send_request(cmd_code, imei)
    st.write(response)
