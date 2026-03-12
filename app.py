import streamlit as st

from PIL import Image

# Tenta carregar a imagem (o nome deve ser igual ao arquivo que você subiu)
try:
    logo = Image.open("BRT VISTOS.png")
    st.image(logo, width=200) # Ajuste a largura como quiser
except:
    st.write("Logo não encontrada")

# Configuração da página
st.set_page_config(page_title="BRT VisaScore", page_icon="✈️")

# Estilização básica (opcional para simular o botão vermelho)
st.markdown("""
    <style>
    .stButton>button {
        background-color: #8B0000;
        color: white;
        width: 100%;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("BRT VisaScore - Análise de Perfil Consular")

# Organizando em colunas
col1, col2 = st.columns(2)

with col1:
    emprego = st.selectbox("Tipo de emprego", ["CLT", "Autônomo", "Empresário", "Desempregado"])
    tempo = st.selectbox("Tempo no emprego", ["Menos de 1 ano", "1 a 3 anos", "Mais de 3 anos"])
    renda = st.number_input("Renda mensal (R$)", min_value=0, step=500)
    filhos = st.radio("Possui filhos?", ["Sim", "Não"])
    imovel = st.radio("Possui imóvel?", ["Sim", "Não"])

with col2:
    carro = st.radio("Possui carro?", ["Sim", "Não"])
    empresa = st.radio("Possui empresa?", ["Sim", "Não"])
    viagens = st.radio("Já viajou ao exterior?", ["Sim", "Não"])
    europa = st.radio("Já viajou para Europa?", ["Sim", "Não"])
    negado = st.radio("Já teve visto americano negado?", ["Sim", "Não"])

if st.button("ANALISAR PERFIL"):
    score = 0
    positivos = []
    negativos = []

    # Lógica de Pontuação (Sua lógica original adaptada)
    if emprego == "CLT": score += 20; positivos.append("Emprego formal CLT")
    elif emprego == "Empresário": score += 25; positivos.append("Empresário com fortes vínculos")
    elif emprego == "Autônomo": score += 10; positivos.append("Renda própria como autônomo")
    else: score -= 30; negativos.append("Ausência de vínculo profissional")

    if tempo == "Mais de 3 anos": score += 15; positivos.append("Estabilidade profissional")
    elif tempo == "1 a 3 anos": score += 10
    
    if renda >= 15000: score += 25; positivos.append("Alta renda mensal")
    elif renda >= 4000: score += 10; positivos.append("Renda compatível")
    else: negativos.append("Renda considerada baixa")

    if filhos == "Sim": score += 10; positivos.append("Possui filhos no Brasil")
    if imovel == "Sim": score += 15; positivos.append("Possui imóvel")
    if viagens == "Sim": score += 15; positivos.append("Histórico internacional")
    else: negativos.append("Sem histórico internacional")
    
    if negado == "Sim": score -= 40; negativos.append("Histórico de visto negado")

    # Exibição do Resultado
    st.divider()
    if score >= 120: st.balloons(); st.success(f"Chance MUITO ALTA (Score: {score})")
    elif score >= 90: st.success(f"Boa chance de aprovação (Score: {score})")
    elif score >= 70: st.warning(f"Chance moderada (Score: {score})")
    else: st.error(f"Alto risco de negativa (Score: {score})")

    st.subheader("Detalhes da Análise:")
    for p in positivos: st.write(f"✅ {p}")
    for n in negativos: st.write(f"⚠️ {n}")
