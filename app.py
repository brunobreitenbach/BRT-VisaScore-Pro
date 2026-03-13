import streamlit as st
from PIL import Image
import urllib.parse

# 1. Configuração da Página
st.set_page_config(page_title="BRT VisaScore", page_icon="✈️")

# 2. Estilização: Cor #7a0c1e e fonte grande
st.markdown("""
    <style>
    label { font-size: 18px !important; font-weight: 600 !important; color: #333 !important; }
    div.stButton > button:first-child, a[href^="https://wa.me"] button {
        background-color: #7a0c1e !important; color: white !important; width: 100%; font-weight: bold; border: none; padding: 10px;
    }
    .metric-card { padding: 15px; border-radius: 10px; background-color: #f8f9fa; border-left: 5px solid #7a0c1e; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Logo e Título
try:
    st.image(Image.open("BRT VISTOS.png"), width=200)
except:
    st.title("BRT VisaScore")

st.title("BRT VisaScore - Análise de Perfil")

# 4. Formulário Detalhado
col1, col2 = st.columns(2)
with col1:
    nome = st.text_input("Nome")
    idade = st.number_input("Idade", min_value=18, max_value=90)
    estado_civil = st.selectbox("Estado civil", ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)"])
    emprego = st.selectbox("Tipo de emprego", ["CLT", "Autônomo", "Empresário", "Desempregado"])
    renda = st.number_input("Renda mensal (R$)", min_value=0)
    filhos = st.radio("Possui filhos?", ["Sim", "Não"])
    bens = st.radio("Possui bens (imóveis, carros, investimentos)?", ["Sim", "Não"])

with col2:
    viagens_ext = st.radio("Já viajou para o exterior?", ["Sim", "Não"])
    visto_usa = st.radio("Já teve visto de turismo americano?", ["Sim", "Não"])
    negado = st.radio("Já teve visto negado?", ["Sim", "Não"])
    proposito = st.selectbox("Propósito da viagem", ["Turismo", "Estudos", "Negócios"])
    duracao = st.number_input("Duração da viagem (dias)", min_value=1, max_value=365)
    processo = st.radio("Responde a algum processo judicial?", ["Sim", "Não"])

# 5. Lógica de Pontuação (Total 100)
if st.button("ANALISAR PERFIL"):
    score = 0
    # Critérios (Pesos)
    if emprego in ["CLT", "Empresário"]: score += 20
    elif emprego == "Autônomo": score += 15
    
    if renda > 5000: score += 15
    elif renda > 2000: score += 10
    
    if bens == "Sim": score += 15
    if filhos == "Sim": score += 5
    if viagens_ext == "Sim": score += 10
    if visto_usa == "Sim": score += 10
    
    # Penalidades
    if negado == "Sim": score -= 30
    if processo == "Sim": score -= 50
    if emprego == "Desempregado": score -= 10
    
    score = max(0, min(100, score)) # Limita entre 0 e 100

    # Exibição
    st.divider()
    st.metric("Score Final", f"{score}/100")
    
    if score >= 70: st.success("Perfil excelente para aplicação.")
    elif score >= 40: st.warning("Perfil regular. Necessita de estratégia.")
    else: st.error("Perfil requer análise profunda antes de qualquer tentativa.")

    # 6. Mensagem Premium
    ficha = (
        f"\n\nDIAGNÓSTICO: {nome}\n"
        f"Score: {score}/100\n"
        f"Idade: {idade} | Civil: {estado_civil}\n"
        f"Emprego: {emprego} | Renda: R${renda}\n"
        f"Bens: {bens} | Filhos: {filhos}\n"
        f"Viagens Ext: {viagens_ext} | Visto USA: {visto_usa}\n"
        f"Negado: {negado} | Processo: {processo}\n"
        f"Propósito: {proposito} | Duração: {duracao} dias"
    )
    link = f"https://wa.me/5551983117662?text={urllib.parse.quote('Olá! Fiz a análise no BRT VisaScore.' + ficha)}"
    st.link_button("Falar com Especialista", url=link)
