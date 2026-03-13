import streamlit as st
from PIL import Image
import urllib.parse

# 1. Configuração da Página
st.set_page_config(page_title="BRT VisaScore", page_icon="✈️")

# 2. Estilização: Cor #7a0c1e, letras maiores e cards Premium
st.markdown("""
    <style>
    label { font-size: 18px !important; font-weight: 600 !important; color: #333 !important; }
    div.stButton > button:first-child, a[href^="https://wa.me"] button {
        background-color: #7a0c1e !important;
        color: white !important;
        width: 100%;
        font-weight: bold;
        border: none;
        padding: 10px;
    }
    div.stButton > button:hover, a[href^="https://wa.me"] button:hover {
        background-color: #a3112a !important;
        color: white !important;
    }
    .metric-card { padding: 15px; border-radius: 10px; background-color: #f8f9fa; border-left: 5px solid #7a0c1e; margin-bottom: 10px; }
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
        # Pontuação 0-40
        vinc = 0
        if emprego in ["CLT", "Empresário"]: vinc += 5
        if imovel == "Sim": vinc += 3
        if filhos == "Sim": vinc += 2
        
        hist = 0
        if europa == "Sim": hist += 6
        elif viagens == "Sim": hist += 4
        if visto_usa == "Sim": hist += 4
        
        fin = 10 if renda >= 8000 else (6 if renda >= 4000 else 0)
        
        # Invertendo a lógica: agora é "Índice de Segurança"
        seg = 10
        if negado == "Sim": seg -= 8
        if emprego == "Desempregado": seg -= 5
        
        total = vinc + hist + fin + seg
        
        st.divider()
        st.subheader("📊 Resultado da Análise de Perfil")
        
        col_score1, col_score2 = st.columns([1, 2])
        col_score1.metric("Score Final", f"{total}/40")
        
        if total >= 30: col_score2.success("### Perfil de Alta Probabilidade")
        elif total >= 20: col_score2.warning("### Perfil Favorável")
        else: col_score2.error("### Perfil com Atenção")
        
        # Exibição em Cartões Premium
        cols = st.columns(2)
        detalhes = [
            ("Vínculos com Brasil", vinc),
            ("Histórico de Viagens", hist),
            ("Situação Financeira", fin),
            ("Índice de Segurança", seg)
        ]
        
        for i, (cat, pts) in enumerate(detalhes):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="metric-card">
                    <h5 style="margin: 0;">{cat}</h5>
                    <p style="font-size: 24px; font-weight: bold; margin: 5px 0;">{pts} / 10</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        
        # Mensagem Premium para WhatsApp
        msg_topo = "Olá! Realizei o diagnóstico no BRT VisaScore e gostaria de avançar com minha consultoria."
        msg_ficha = f"""
*DIAGNÓSTICO VISA SCORE: {total}/40*
--------------------------
*DADOS DO PERFIL:*
💼 Emprego: {emprego} ({tempo})
💰 Renda Mensal: R${renda}
🏠 Imóvel: {imovel} | 👨‍👩‍👧 Filhos: {filhos}
✈️ Histórico de Viagens: {viagens}
🇪🇺 Europa: {europa} | 🇺🇸 Visto EUA: {visto_usa}
❌ Visto Negado: {negado}
--------------------------
Aguardo seu contato para análise estratégica."""
        
        link = f"https://wa.me/5551983117662?text={urllib.parse.quote(msg_topo + msg_ficha)}"
        
        st.link_button("Falar com Especialista", url=link)
