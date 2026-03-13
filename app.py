import streamlit as st
from PIL import Image
import urllib.parse

# 1. Configuração da página
st.set_page_config(page_title="BRT VisaScore", page_icon="✈️")

# 2. Carregamento da Logo
try:
    logo = Image.open("BRT VISTOS.png")
    st.image(logo, width=200)
except:
    st.title("BRT VisaScore")

# 3. Estilização do Botão
st.markdown("""
    <style>
    .stButton>button { background-color: #8B0000; color: white; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("BRT VisaScore: Análise de Vínculos Consulares")
st.write("Identifique a força dos seus vínculos com o Brasil para o pedido do visto B1/B2.")

# 4. Formulário
col1, col2 = st.columns(2)

with col1:
    emprego = st.selectbox("Tipo de emprego", ["Selecione aqui...", "CLT", "Autônomo", "Empresário", "Desempregado"])
    tempo = st.selectbox("Tempo no emprego", ["Selecione aqui...", "Menos de 1 ano", "1 a 3 anos", "Mais de 3 anos"])
    renda = st.number_input("Renda mensal (R$)", min_value=0, step=500, value=0)
    filhos = st.radio("Possui filhos?", ["Sim", "Não"], index=None)
    imovel = st.radio("Possui imóvel?", ["Sim", "Não"], index=None)

with col2:
    carro = st.radio("Possui carro?", ["Sim", "Não"], index=None)
    empresa = st.radio("Possui empresa?", ["Sim", "Não"], index=None)
    viagens = st.radio("Já viajou ao exterior?", ["Sim", "Não"], index=None)
    europa = st.radio("Já viajou para Europa?", ["Sim", "Não"], index=None)
    visto_usa = st.radio("Você já teve visto americano?", ["Sim", "Não"], index=None)
    negado = st.radio("Já teve visto negado?", ["Sim", "Não"], index=None)

# 5. Lógica de Análise Premium
if st.button("ANALISAR MEU PERFIL"):
    campos_radio = [filhos, imovel, carro, empresa, viagens, europa, visto_usa, negado]
    
    if emprego == "Selecione aqui..." or None in campos_radio:
        st.error("⚠️ Por favor, responda a todas as perguntas para um diagnóstico preciso.")
    else:
        score = 0
        positivos = []
        negativos = []

        # Pontuação focada em Vínculos (Ancoragem)
        if emprego == "CLT": score += 30; positivos.append("Vínculo CLT (Estabilidade comprovada)")
        elif emprego == "Empresário": score += 35; positivos.append("Empresário (Vínculo de gestão)")
        elif emprego == "Autônomo": score += 15; positivos.append("Renda própria (Autonomia)")
        else: score -= 20; negativos.append("Ausência de vínculo profissional formal")

        if renda >= 6000: score += 20; positivos.append("Renda estável (acima de R$ 6k)")
        
        if imovel == "Sim": score += 25; positivos.append("Possui Imóvel (Vínculo patrimonial)")
        if carro == "Sim": score += 10; positivos.append("Possui Veículo (Vínculo material)")
        if filhos == "Sim": score += 15; positivos.append("Vínculo Familiar")
        
        if europa == "Sim": score += 20; positivos.append("Histórico de viagens à Europa (Turismo qualificado)")
        elif viagens == "Sim": score += 10; positivos.append("Histórico Internacional")
        
        if visto_usa == "Sim": score += 30; positivos.append("Histórico de Visto Americano")
        if negado == "Sim": score -= 50; negativos.append("Histórico de negativa (Exige atenção extra)")

        # 6. Exibição do Diagnóstico
        st.divider()
        st.subheader("📊 Diagnóstico de Consultoria")
        
        if score >= 100: 
            st.success(f"**Perfil Ideal** (Score: {score})")
            st.write("Parabéns! Seu perfil demonstra solidez e forte ancoragem com o Brasil, o que reduz drasticamente o risco de negativa.")
        elif score >= 60: 
            st.success(f"**Perfil Favorável** (Score: {score})")
            st.write("Você possui bons indicadores. Com uma estratégia de entrevista bem montada, suas chances de aprovação são altas.")
        else: 
            st.warning(f"**Perfil com Risco** (Score: {score})")
            st.write("Seu perfil apresenta pontos sensíveis. Recomendamos uma estratégia personalizada antes de submeter o pedido ao consulado.")

        # Detalhamento
        col_pos, col_neg = st.columns(2)
        with col_pos:
            st.markdown("#### ✅ Pontos Fortes")
            for p in positivos: st.markdown(f"- {p}")
        with col_neg:
            st.markdown("#### ⚠️ Áreas de Atenção")
            for n in negativos: st.markdown(f"- {n}")

        # Botão WhatsApp
        st.markdown("---")
        msg = urllib.parse.quote("Olá! Fiz a simulação no BRT VisaScore e gostaria de uma consultoria premium para o meu visto.")
        link = f"https://wa.me/5551983117662?text={msg}"
        st.link_button("Solicitar Consultoria Premium 💼", url=link)
