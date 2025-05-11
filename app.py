import streamlit as st
from PIL import Image
import math

st.set_page_config(page_title="Calculadora de Pulverização Agrícola", layout="centered")

# Título
st.title("💧 Calculadora de Pulverização Agrícola - (PSI)")

# Escolha de parâmetros
st.header("🔧 Quais parâmetros você deseja usar?")
usar_velocidade = st.checkbox("Velocidade (km/h)", value=True)
usar_largura = st.checkbox("Largura da barra (m)", value=True)
usar_taxa_aplicacao = st.checkbox("Taxa de aplicação (L/ha)", value=True)
usar_espacamento = st.checkbox("Espaçamento entre bicos (cm)", value=False)
usar_num_bicos = st.checkbox("Número de bicos", value=True)

# Entradas de parâmetros
st.header("📥 Entrada de Parâmetros")
if usar_velocidade:
    velocidade = st.number_input("Velocidade (km/h)", min_value=0.0, step=0.1)
else:
    velocidade = None

if usar_largura:
    largura = st.number_input("Largura da barra (m)", min_value=0.0, step=0.1)
else:
    largura = None

if usar_taxa_aplicacao:
    taxa_aplicacao = st.number_input("Taxa de aplicação (L/ha)", min_value=0.0, step=0.1)
else:
    taxa_aplicacao = None

if usar_espacamento:
    espacamento_bicos = st.number_input("Espaçamento entre bicos (cm)", min_value=0.1, step=0.1)
else:
    espacamento_bicos = None

if usar_num_bicos:
    numero_bicos = st.number_input("Número de bicos utilizados", min_value=1, step=1)
else:
    numero_bicos = None

# Seção: Pressão e bico
st.header("⚙️ Pressão de Trabalho e Tipo de Bico")
pressao_trabalho_psi = st.selectbox(
    "Pressão de trabalho (PSI)", 
    options=[7, 10, 15, 20, 30, 40, 43.5, 45, 50, 60, 70, 80, 90, 100, 120, 150, 180, 200, 250, 300]
)

bicos = {
    "Verde Claro (0.4)": 0.4,
    "Amarelo (0.6)": 0.6,
    "Azul (0.8)": 0.8,
    "Vermelho (1.0)": 1.0,
    "Marrom (1.2)": 1.2,
    "Cinza (1.6)": 1.6,
    "Branco (2.0)": 2.0,
    "Violeta (2.4)": 2.4,
    "Laranja (3.2)": 3.2,
    "Turquesa (4.0)": 4.0
}

bico_escolhido = st.selectbox("Bico (cor e vazão nominal a 43.5 PSI)", list(bicos.keys()))
vazao_nominal = bicos[bico_escolhido]
vazao_ajustada = vazao_nominal * (pressao_trabalho_psi / 43.5) ** 0.5

# Cálculos adaptativos
st.header("📊 Resultados")

# Verifica se todos os dados necessários para calcular estão disponíveis
if taxa_aplicacao and velocidade:
    if espacamento_bicos:
        q = (taxa_aplicacao * velocidade * espacamento_bicos) / 60000
        st.write(f"🔹 Vazão necessária por bico (q): **{q:.2f} L/min**")
        st.write(f"🔹 Vazão fornecida pelo bico `{bico_escolhido}`: **{vazao_ajustada:.2f} L/min**")

        if abs(vazao_ajustada - q) < 0.1:
            st.success("✅ Vazão do bico compatível com a necessidade.")
        elif vazao_ajustada > q:
            st.warning("⚠️ Bico pode estar aplicando *mais* do que o necessário.")
        else:
            st.warning("⚠️ Bico pode estar aplicando *menos* do que o necessário.")

    if numero_bicos:
        Q = numero_bicos * vazao_ajustada
        st.write(f"🔹 Vazão total fornecida pelos bicos: **{Q:.2f} L/min**")

        if largura:
            Q_necessaria = (velocidade * largura * taxa_aplicacao) / 600
            st.write(f"🔹 Vazão total necessária (Q): **{Q_necessaria:.2f} L/min**")

            if abs(Q - Q_necessaria) < 0.5:
                st.success("✅ Vazão total compatível.")
            elif Q > Q_necessaria:
                st.warning("⚠️ Sistema pode aplicar *mais* do que o necessário.")
            else:
                st.warning("⚠️ Sistema pode aplicar *menos* do que o necessário.")

else:
    st.info("⚠️ Preencha os campos mínimos: velocidade, taxa de aplicação e pelo menos um entre espaçamento ou número de bicos.")

# Exibir imagem da tabela
st.header("📘 Tabela de Vazão e Tamanho de Gota (Jacto - pág. 07)")
try:
    image = Image.open("TabelaBicos.png")
    st.image(image, caption="Tabela de Bicos - Manual Jacto 2022 (pág. 07)", use_column_width=True)
except:
    st.warning("⚠️ Imagem da tabela 'TabelaBicos.png' não encontrada.")
