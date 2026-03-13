import streamlit as st
from PIL import Image
import urllib.parse

# 1. Configuração da Página
st.set_page_config(page_title="BRT VisaScore", page_icon="✈️")

# 2. Estilização Premium
st.markdown("""
    <style>
    label { font-size: 18px !important; font-weight: 600 !important; color: #333 !important; }
    div.stButton > button:first-child, a[href^="https://wa.me"] button {
        background-color: #7a0c1e !important; color: white !important; width: 100%; font-weight: bold; border: none; padding: 10px;
    }
    .relatorio { padding: 20px; border-radius: 10px; background-color: #ffffff; border: 1px solid #ddd; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Logo e Título
try:
    st.image(Image.open("BRT VISTOS.png"), width=200)
except:
    st.title("BRT VisaScore")

st.title("BRT VisaScore - Análise de Perfil")

# 4. Formulário
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

# 5. Lógica de Diagnóstico
if st.button("ANALISAR PERFIL"):
    if None in [nome, idade, estado_civil, emprego, renda, filhos, bens, viagens_ext, visto_usa, negado, proposito, duracao, processo]:
        st.error("Por favor, preencha todos os campos para realizarmos o diagnóstico!")
    else:
        score = 0
        fortes = []
        atencao = []
        rec = "Recomendamos uma análise de documentação personalizada para mitigar riscos."

        # Lógica de Pesos
        if emprego in ["CLT", "Empresário"]: score += 20; fortes.append("Estabilidade profissional formal.")
        else: atencao.append("Emprego autônomo/desempregado requer prova documental extra.")
        
        if renda and renda > 5000: score += 15; fortes.append("Renda compatível.")
        else: atencao.append("Renda baixa pode gerar dúvida na capacidade financeira.")
        
        if bens == "Sim": score += 15; fortes.append("Vínculo patrimonial robusto.")
        if filhos == "Sim": score += 10; fortes.append("Laços familiares reforçam intenção de retorno.")
        if viagens_ext == "Sim": score += 10; fortes.append("Experiência de viagens internacionais.")
        if visto_usa == "Sim": score += 10; fortes.append("Histórico positivo com o consulado.")
        
        if negado == "Sim": score -= 25; atencao.append("Histórico de visto negado anterior.")
        if processo == "Sim": score -= 40; atencao.append("Processo judicial requer atenção crítica.")
        if duracao and duracao > 30: atencao.append("Viagem longa sem vínculo forte pode levantar suspeitas.")
        if estado_civil == "Solteiro(a)" and not filhos == "Sim": atencao.append("Solteiros sem dependentes exigem laços sociais fortes.")

        score = max(0, min(100, score))

        # 6. Relatório Consultivo
        st.divider()
        st.metric("Score de Segurança Consular", f"{score}/100")
        
        st.subheader("Relatório Estratégico")
        with st.container(border=True):
            st.markdown("#### Pontos Fortes")
            for f in fortes: st.write(f"• {f}")
            st.markdown("#### Pontos de Atenção")
            for a in atencao: st.write(f"• {a}")
            st.markdown("#### Recomendação Especialista")
            st.write(rec if score > 50 else "É indispensável estruturar a estratégia antes de qualquer agendamento.")

        # 7. WhatsApp Premium
        msg = f"DIAGNOSTICO: {nome}\nScore: {score}/100\nFortes: {', '.join(fortes)}\nAtenção: {', '.join(atencao)}"
        link = f"https://wa.me/5551983117662?text={urllib.parse.quote('Olá, analisei meu perfil no BRT VisaScore.' + '\n\n' + msg)}"
        st.link_button("Falar com Especialista", url=link)
