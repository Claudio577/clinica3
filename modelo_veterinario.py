import streamlit as st
from modelo_veterinario import prever_caso_completo

st.set_page_config(page_title="Previsão Clínica Veterinária", page_icon="🐶")

st.title("🐾 Previsão Clínica Veterinária")
st.markdown("Este sistema usa inteligência artificial para prever a situação de um paciente canino com base na anamnese e em fatores clínicos.")

# Entradas do usuário
anamnese = st.text_area("📝 Digite a anamnese do paciente:")

col1, col2 = st.columns(2)
with col1:
    idade = st.slider("Idade do animal (anos)", 1, 20, 5)
    desnutricao = st.checkbox("Desnutrido?")
    historico_grave = st.checkbox("Histórico clínico grave?")
with col2:
    peso = st.slider("Peso (kg)", 1.0, 60.0, 15.0, step=0.5)
    estado_mental = st.checkbox("Estado mental alterado?")

# Botão de previsão
if st.button("🔍 Prever"):
    if not anamnese.strip():
        st.warning("Por favor, insira a anamnese.")
    else:
        resultado = prever_caso_completo(
            anamnese=anamnese,
            idade=idade,
            peso=peso,
            desnutricao=desnutricao,
            estado_mental_alterado=estado_mental,
            historico_clinico_grave=historico_grave
        )

        st.subheader("📋 Resultado da Análise")
        st.markdown(f"**Alta:** {'✅ Sim' if resultado['Alta'] else '❌ Não'}")
        st.markdown(f"**Internar:** {'✅ Sim' if resultado['Internar'] else '❌ Não'}")
        st.markdown(f"**Dias Internado:** `{resultado['Dias Internado']}` dia(s)")
        st.markdown(f"**Chance de Eutanásia (%):** `{resultado['Chance de Eutanásia (%)']}%`")

        st.markdown("**🧬 Doenças Detectadas:**")
        st.write(", ".join(resultado['Doenças Detectadas']) if resultado['Doenças Detectadas'] else "Nenhuma identificada.")

        st.markdown("**🚨 Doenças Graves Detectadas:**")
        st.write(", ".join(resultado['Graves Detectadas']) if resultado['Graves Detectadas'] else "Nenhuma grave detectada.")
