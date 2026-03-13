import streamlit as st
from PIL import Image
import urllib.parse

# Configuração da Página
st.set_page_config(page_title="BRT VisaScore", page_icon="✈️")

# Estilização Premium
st.markdown("""
    <style>
    label { font-size: 18px !important; font-weight: 600 !important; color: #333 !important; }
    div.stButton > button:first-child, a[href^="https://wa.me"] button {
        background-color: #7a0c1e !important; color: white !important; width: 100%; font-weight: bold; border: none; padding: 10px;
    }
    .card { padding: 15px; border-radius: 10px; background-color: #f8f9fa; border-left: 5px solid #7a0c1e; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("BRT VisaScore - Análise de Perfil")

# Formulário
col1, col2 = st.columns(2)
with col1:
    nome = st.text_input("Nome", placeholder="Preencha aqui")
    idade = st.number_input("Idade", min_value=18, max_value=90, value=None)
    estado_civil = st.selectbox("Estado civil", ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)"], index=None, placeholder="Selecione")
    emprego = st.selectbox("Tipo de emprego", ["CLT", "Autônomo", "Empresário", "Desempregado"], index=None, placeholder="Selecione")
    renda = st.number_input("Renda mensal (R$)", min_value=0, value=None)
    filhos = st.radio("Possui filhos?", ["Sim", "Não"], index=None)
    bens = st.radio("Possui bens (imóveis, carros, investimentos)?", ["Sim", "Não"], index=None)

with col2:
    viagens_ext = st.radio("Já viajou para o exterior?", ["Sim", "Não"], index=None)
    visto_usa = st.radio("Já teve visto de turismo americano?", ["Sim", "Não"], index=None)
    negado = st.radio("Já teve visto negado?", ["Sim", "Não"], index=None)
    proposito = st.selectbox("Propósito da viagem", ["Turismo", "Estudos", "Negócios"], index=None, placeholder="Selecione")
    duracao = st.number_input("Duração da viagem (dias)", min_value=1, max_value=365, value=None)
    processo = st.radio("Responde a algum processo judicial?", ["Sim", "Não"], index=None)

# Lógica de Análise
if st.button("ANALISAR PERFIL"):
    if None in [nome, idade, estado_civil, emprego, renda, filhos, bens, viagens_ext, visto_usa, negado, proposito, duracao, processo]:
        st.error("Por favor, preencha todos os campos.")
    else:
        score = 0
        fortes = []
        atencao = []

        # Pontuação e Lógica de Feedback
        if emprego in ["CLT", "Empresário"]: 
            score += 25
            fortes.append("Vínculos profissionais estabelecidos (CLT/Empresário).")
        elif emprego == "Autônomo": 
            score += 15
        else: 
            atencao.append("Necessário comprovar estabilidade financeira se desempregado.")

        if bens == "Sim": 
            score += 20
            fortes.append("Possui bens que fortalecem o vínculo com o Brasil.")
        else: 
            atencao.append("Considere listar outros vínculos ou garantias.")

        if renda and renda > 5000: 
            score += 15
            fortes.append("Renda mensal condizente com a proposta de viagem.")
        
        if viagens_ext == "Sim": 
            score += 10
            fortes.append("Histórico de viagens internacionais anterior.")
        
        if negado == "Sim": 
            score -= 30
            atencao.append("Histórico de visto negado anterior exige justificativa estratégica.")
        
        if processo == "Sim": 
            score -= 50
            atencao.append("Processo judicial em curso é um ponto de atenção crítico para a imigração.")
        
        score = max(0, min(100, score))
        
        # Exibição dos resultados
        st.divider()
        st.metric("Score de Segurança Consular", f"{score}/100")
        
        col_f, col_a = st.columns(2)
        with col_f:
            st.subheader("Pontos Fortes")
            for f in fortes: st.write(f"- {f}")
            if not fortes: st.write("Nenhum ponto forte identificado.")
        with col_a:
            st.subheader("Pontos de Atenção")
            for a in atencao: st.write(f"- {a}")
            if not atencao: st.write("Perfil equilibrado.")

        # Mensagem para WhatsApp
        msg = f"DIAGNOSTICO: {nome}\nScore: {score}/100\nFortes: {', '.join(fortes)}\nAtenção: {', '.join(atencao)}"
        link = f"https://wa.me/5551983117662?text={urllib.parse.quote('Olá, analisei meu perfil no BRT VisaScore.' + '\n\n' + msg)}"
        st.link_button("Falar com Especialista", url=link)
