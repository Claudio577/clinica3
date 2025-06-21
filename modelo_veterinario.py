
import pandas as pd
import numpy as np
import re
import unicodedata
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.multioutput import MultiOutputClassifier

# === FUNÇÕES DE UTILIDADE ===

def normalizar(texto):
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8').lower()
    texto = re.sub(r'[^a-z\s]', '', texto)
    return texto

def prever_caso_completo(anamnese, idade, peso, desnutricao, estado_mental_alterado, historico_clinico_grave):
    texto = normalizar(anamnese)
    entrada = {d: int(d in texto) for d in todas_doencas}
    entrada.update({
        "idade": idade,
        "peso": peso,
        "desnutricao": int(desnutricao),
        "estado_mental_alterado": int(estado_mental_alterado),
        "historico_clinico_grave": int(historico_clinico_grave)
    })
    X_input = pd.DataFrame([entrada])
    pred_class = modelo_class.predict(X_input)[0]
    pred_eutanasia_proba = modelo_class.estimators_[-1].predict_proba(X_input)[0][1]
    pred_dias = int(round(modelo_dias.predict(X_input)[0]))
    doencas_detectadas = [d for d in doencas_todas if d in texto]
    doencas_graves_detectadas = [d for d in doencas_detectadas if d in doencas_graves]
    return {
        "Alta": bool(pred_class[0]),
        "Internar": bool(pred_class[1]),
        "Dias Internado": pred_dias,
        "Chance de Eutanásia (%)": round(pred_eutanasia_proba * 100, 2),
        "Doenças Detectadas": doencas_detectadas,
        "Graves Detectadas": doencas_graves_detectadas
    }

# === CARREGAR BASES E TREINAR MODELO ===

doencas_graves = pd.read_csv("doencas_caninas_eutanasia_expandidas.csv")["Doença"].dropna().str.lower().str.strip().tolist()
todas_doencas = ['anemia hemolitica autoimune', 'cinomose', 'displasia coxofemoral', 'doenca do carrapato',
                 'doenca periodontal', 'erlichiose', 'giardiase', 'insuficiencia renal cronica',
                 'leptospirose', 'linfoma', 'pancreatite', 'parvovirose']
doencas_todas = list(set(todas_doencas + doencas_graves))

# Simular base
np.random.seed(42)
n_samples = 300
df = pd.DataFrame({
    "anamnese": np.random.choice([
        "animal com febre e letargia",
        "vomitos persistentes e sangue nas fezes",
        "ictericia e apatia",
        "aumento de linfonodos e emagrecimento",
        "dor abdominal e inapetencia",
        "problemas renais cronicos e perda de apetite"
    ], n_samples),
    "doencas_mencionadas": [np.random.choice(todas_doencas, size=np.random.randint(1, 4), replace=False).tolist() for _ in range(n_samples)],
    "alta": np.random.choice([0, 1], n_samples),
    "internar": np.random.choice([0, 1], n_samples),
    "dias_internado": np.random.randint(0, 10, n_samples),
    "eutanasia": np.random.choice([0, 1], n_samples),
    "idade": np.random.randint(1, 16, size=n_samples),
    "peso": np.round(np.random.uniform(2, 40, size=n_samples), 1),
    "desnutricao": np.random.choice([0, 1], n_samples),
    "estado_mental_alterado": np.random.choice([0, 1], n_samples),
    "historico_clinico_grave": np.random.choice([0, 1], n_samples)
})

for d in todas_doencas:
    df[d] = df['doencas_mencionadas'].apply(lambda x: int(d in x))

X = df[todas_doencas + ["idade", "peso", "desnutricao", "estado_mental_alterado", "historico_clinico_grave"]]
y_class = df[["alta", "internar", "eutanasia"]]
y_reg = df["dias_internado"]

modelo_class = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42))
modelo_class.fit(X, y_class)

modelo_dias = RandomForestRegressor(n_estimators=100, random_state=42)
modelo_dias.fit(X, y_reg)

# EXEMPLO DE USO
if __name__ == "__main__":
    resultado = prever_caso_completo(
        anamnese="Paciente com linfoma canino em estágio terminal e anemia hemolítica autoimune",
        idade=12,
        peso=18,
        desnutricao=1,
        estado_mental_alterado=1,
        historico_clinico_grave=1
    )
    print(resultado)
