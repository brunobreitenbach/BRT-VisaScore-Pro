import streamlit as st
from PIL import Image
import urllib.parse

# 1. Configuração da Página
st.set_page_config(page_title="BRT VisaScore", page_icon="✈️")

# 2. Estilização: Cor #7a0c1e e remoção de emojis dos botões
st.markdown("""
    <style>
    div.stButton > button:first-child, a[href^="https://wa.me"] button {
        background-color: #7a0c1e !important;
        color: white !important;
        width: 100%;
        font-weight: bold;
        border: none;
    }
    div.stButton > button:hover, a[href^="https://wa.me"] button:hover {
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

# 6. Lógica de Análise (Score total agora 40)
if st.button("ANALISAR PERFIL"):
    if emprego == "Selecione..." or None in [filhos, imovel, viagens, europa, visto_usa, negado]:
        st.error("Por favor, preencha todos os campos para realizarmos o diagnóstico!")
    else:
        # Vínculos (0-10)
        vinc = 0
        if emprego in ["CLT", "Empresário"]: vinc += 5
        if imovel == "Sim": vinc += 3
        if filhos == "Sim": vinc += 2
        
        # Histórico (0-10)
        hist = 0
        if europa == "Sim": hist += 6
        elif viagens == "Sim": hist += 4
        if visto_usa == "Sim": hist += 4
        
        # Financeiro (0-10)
        fin = 10 if renda >= 8000 else (6 if renda >= 4000 else 0)
        
        # Risco (0-10)
        risco = 10
        if negado == "Sim": risco -= 8
        if emprego == "Desempregado": risco -= 5
        
        total = vinc + hist + fin + risco
        
        st.divider()
        st.subheader(f"Score Final: {total}/40")
        
        # Tabela sem o Plano de Viagem
        data = {
            "Categoria": ["Vínculos com Brasil", "Histórico de Viagens", "Situação Financeira", "Risco de Imigração"],
            "Pontos": [f"{vinc}/10", f"{hist}/10", f"{fin}/10", f"{risco}/10"]
        }
        st.table(data)
        
        if total >= 30: st.success("Perfil de alta probabilidade. Pronto para a assessoria!")
        elif total >= 20: st.warning("Perfil bom, mas precisa de estratégia.")
        else: st.error("Perfil requer análise profunda antes de aplicar.")

        st.markdown("---")
        msg = urllib.parse.quote(f"Olá! Fiz a simulação no BRT VisaScore e obtive o score {total}/40. Gostaria de uma consultoria premium.")
        st.link_button("Falar com Especialista", url=f"https://wa.me/5551983117662?text={msg}")
