import streamlit as st
from PIL import Image
import urllib.parse

st.set_page_config(page_title="BRT VisaScore", page_icon="✈️")

# Exibindo Logo
try:
    st.image(Image.open("BRT VISTOS.png"), width=200)
except:
    st.title("BRT VisaScore")

st.title("BRT VisaScore: Diagnóstico Consular")

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

if st.button("ANALISAR PERFIL"):
    if emprego == "Selecione..." or None in [filhos, imovel, viagens, europa, visto_usa, negado]:
        st.error("Preencha todos os campos!")
    else:
        # 1. Vínculos (0-10)
        vinc = 0
        if emprego in ["CLT", "Empresário"]: vinc += 5
        if imovel == "Sim": vinc += 3
        if filhos == "Sim": vinc += 2
        
        # 2. Histórico de Viagens (0-10)
        hist = 0
        if europa == "Sim": hist += 6
        elif viagens == "Sim": hist += 4
        if visto_usa == "Sim": hist += 4
        
        # 3. Financeiro (0-10)
        fin = 0
        if renda >= 8000: fin = 10
        elif renda >= 4000: fin = 6
        
        # 4. Plano de Viagem (Simulado como fixo ou adaptável)
        plano = 5 # Base para um plano padrão
        
        # 5. Risco de Imigração (0-10)
        risco = 10
        if negado == "Sim": risco -= 8
        if emprego == "Desempregado": risco -= 5
        
        total = vinc + hist + fin + plano + risco
        
        # Exibição Profissional
        st.divider()
        st.subheader(f"Score Final: {total}/50")
        
        # Criando tabela de resumo
        data = {
            "Categoria": ["Vínculos com Brasil", "Histórico de Viagens", "Situação Financeira", "Plano de Viagem", "Risco de Imigração"],
            "Pontos": [f"{vinc}/10", f"{hist}/10", f"{fin}/10", f"{plano}/10", f"{risco}/10"]
        }
        st.table(data)
        
        if total >= 35: st.success("Perfil de alta probabilidade. Pronto para a assessoria!")
        elif total >= 25: st.warning("Perfil bom, mas precisa de estratégia.")
        else: st.error("Perfil requer análise profunda antes de aplicar.")

        st.link_button("Falar com Especialista", url=f"https://wa.me/5551983117662?text=Fiz o score e tirei {total}/50. Preciso de consultoria.")
