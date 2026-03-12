import streamlit as st
from PIL import Image

# 1. Configuração da página sempre no topo
st.set_page_config(page_title="BRT VisaScore", page_icon="✈️")

# 2. Exibindo a Logo
try:
    logo = Image.open("BRT VISTOS.png")
    st.image(logo, width=200)
except:
    st.title("BRT VisaScore")

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

# 3. Organizando em colunas com index=None para começar vazio
col1, col2 = st.columns(2)

with col1:
    emprego = st.selectbox("Tipo de emprego", [None, "CLT", "Autônomo", "Empresário", "Desempregado"])
    tempo = st.selectbox("Tempo no emprego", [None, "Menos de 1 ano", "1 a 3 anos", "Mais de 3 anos"])
    renda = st.number_input("Renda mensal (R$)", min_value=0, step=500)
    filhos = st.radio("Possui filhos?", ["Sim", "Não"], index=None)
    imovel = st.radio("Possui imóvel?", ["Sim", "Não"], index=None)

with col2:
    carro = st.radio("Possui carro?", ["Sim", "Não"], index=None)
    empresa = st.radio("Possui empresa?", ["Sim", "Não"], index=None)
    viagens = st.radio("Já viajou ao exterior?", ["Sim", "Não"], index=None)
    europa = st.radio("Já viajou para Europa?", ["Sim", "Não"], index=None)
    visto_usa = st.radio("Você já teve visto americano?", ["Sim", "Não"], index=None)
    negado = st.radio("Já teve visto negado?", ["Sim", "Não"], index=None)

# 4. Botão com Validação
if st.button("ANALISAR PERFIL"):
    # Verifica se tudo foi preenchido
    campos = [emprego, tempo, filhos, imovel, carro, empresa, viagens, europa, visto_usa, negado]
    
    if None in campos or renda == 0:
        st.error("Por favor, preencha todos os campos antes de analisar!")
    else:
        score = 0
        positivos = []
        negativos = []

        # Lógica de Pontuação
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
        if visto_usa == "Sim": score += 20; positivos.append("Histórico de visto americano")
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
