import streamlit as st
from PIL import Image
import urllib.parse

# 1. Configuração da Página
st.set_page_config(page_title="BRT VisaScore", page_icon="✈️")

# 2. Estilização Personalizada (Cores #7a0c1e e sem emojis)
st.markdown("""
    <style>
    /* Estilização dos botões para cor #7a0c1e */
    div.stButton > button:first-child {
        background-color: #7a0c1e !important;
        color: white !important;
        width: 100%;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #a3112a !important;
        color: white !important;
    }
    /* Estilização específica para o link button */
    a[href^="https://wa.me"] button {
        background-color: #7a0c1e !important;
        color: white !important;
        font-weight: bold;
    }
    a[href^="https://wa.me"] button:hover {
        background-color: #a3112a !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Exibindo Logo
try:
    st.image(Image.open("BRT VISTOS.png"), width=200)
except:
    st.title("BRT VisaScore")

# 4. Título e Explicação
st.title("BRT VisaScore - Visto de Turismo Americano (B1B2)")
st.markdown("""
O VisaScore é uma ferramenta de diagnóstico que avalia o seu perfil consular com base em critérios de elegibilidade. 
O objetivo é identificar pontos fortes e fragilidades no seu histórico, permitindo uma estratégia personalizada para o seu pedido de visto.
""")
st.markdown("---")

# 5. Formulário
col1, col2 = st.columns(2)

with col1:
    emprego = st.selectbox("Tipo de emprego", ["Selecione...", "CLT", "Autônomo", "Empresário", "Desempregado"])
    tempo = st.selectbox("Tempo no emprego", ["Selecione...", "Menos de 1 ano", "1 a 3 anos", "Mais de 3 anos"])
    renda = st.number_input("Renda mensal (R$)", min_value=0, step=500, value=0)
    filhos = st.radio("Possui filhos?", ["Sim", "Não"], index=None)
    imovel = st.radio("Possui imóvel?", ["Sim", "Não"], index=None)

with col2:
    viagens = st.radio("Histórico de viagens ao exterior?", ["Sim", "Não"], index=None)
    europa = st.radio("Já viajou para Europa?", ["Sim", "Não"], index=None)
    visto_usa = st.radio("Já teve visto americano?", ["Sim", "Não"], index=None)
    negado = st.radio("Já teve visto negado?", ["Sim", "Não"], index=None)

# 6. Lógica de Análise
if st.button("ANALISAR PERFIL"):
    if emprego == "Selecione..." or None in [filhos, imovel, viagens, europa, visto_usa, negado]:
        st.error("Por favor, preencha todos os campos para realizarmos o diagnóstico!")
    else:
        # Pontuação 0-50
        vinc = 0
        if emprego in ["CLT", "Empresário"]: vinc += 5
        if imovel == "Sim": vinc += 3
        if filhos == "Sim": vinc += 2
        
        hist = 0
        if europa == "Sim": hist += 6
        elif viagens == "Sim": hist += 4
        if visto_usa == "Sim": hist += 4
        
        fin = 10 if renda >= 8000 else (6 if renda >= 4000 else 0)
        plano = 5
        risco = 10
        if negado == "Sim": risco -= 8
        if emprego == "Desempregado": risco -= 5
        
        total = min(vinc + hist + fin + plano + risco, 50)
        
        st.divider()
        st.subheader(f"Score Final: {total}/50")
        
        data = {
            "Categoria": ["Vínculos com Brasil", "Histórico de Viagens", "Situação Financeira", "Plano de Viagem", "Risco de Imigração"],
            "Pontos": [f"{vinc}/10", f"{hist}/10", f"{fin}/10", f"{plano}/10", f"{risco}/10"]
        }
        st.table(data)
        
        if total >= 35: st.success("Perfil de alta probabilidade. Pronto para a assessoria!")
        elif total >= 25: st.warning("Perfil bom, mas precisa de estratégia.")
        else: st.error("Perfil requer análise profunda antes de aplicar.")

        st.markdown("---")
        msg = urllib.parse.quote(f"Olá! Fiz a simulação no BRT VisaScore e obtive o score {total}/50. Gostaria de uma consultoria premium.")
        st.link_button("Falar com Especialista", url=f"https://wa.me/5551983117662?text={msg}")
