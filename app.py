import streamlit as st
import pandas as pd
import json
from streamlit_gsheets import GSheetsConnection

# ---------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Gestão Financeira & Cartões",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# CONEXÃO COM GOOGLE SHEETS E SESSÃO
# ---------------------------------------------------------
CARTOES_INFO = {
    "Caixa": {"fechamento": 5, "vencimento": 17},
    "Itaú": {"fechamento": 3, "vencimento": 10},
    "Inter": {"fechamento": 22, "vencimento": 28},
    "Santander": {"fechamento": 5, "vencimento": 10},
    "Magalu": {"fechamento": 1, "vencimento": 25},
    "Mercado Livre": {"fechamento": 1, "vencimento": 15}
}

MESES = ["OUT", "NOV", "DEZ", "JAN"]

# Inicialização padrão
if "despesas_cartoes" not in st.session_state:
    st.session_state["despesas_cartoes"] = {
        "Caixa": [74.90, 210.50, 96.29, 70.00, 288.71, 50.00, 10.21, 10.21, 26.82, 100.00, 10.28, 1.99, 100.00, 18.99, 69.17, 1.99],
        "Itaú": [149.00, 105.82, 10.00, 162.80, 105.60, 17.00, 480.00, 51.00, 7.00, 28.00, 38.90, 27.00, 50.00, 252.69, 41.92],
        "Inter": [67.87, 105.00, 65.18, 10.50, 24.94, 9.94, 47.19, 19.90, 6.50, 270.00, 12.00, 246.61, 100.00, 17.90, 55.05, 47.83, 148.59, 89.02, 54.98, 191.78, 66.66, 90.97, 220.00, 48.88, 792.50, 43.60, 78.75, 92.87, 49.09, 158.72],
        "Santander": [2615.56],
        "Magalu": [123.41, 200.17, 10.00, 225.54, 60.00, 70.00, 10.00, 60.00],
        "Mercado Livre": [179.29, 115.00, 59.04, 192.11, 36.78, 84.15, 112.78, 32.27, 69.90, 46.55]
    }

if "despesas_sem_cartao" not in st.session_state:
    st.session_state["despesas_sem_cartao"] = {
        "CARRO": {"OUT": 2300.0, "NOV": 2300.0, "DEZ": 2300.0, "JAN": 2300.0},
        "M.Livre": {"OUT": 0.0, "NOV": 0.0, "DEZ": 0.0, "JAN": 748.70},
        "LUZ": {"OUT": 0.0, "NOV": 0.0, "DEZ": 0.0, "JAN": 0.0},
        "Shopping": {"OUT": 0.0, "NOV": 0.0, "DEZ": 0.0, "JAN": 0.0}
    }

if "entradas" not in st.session_state:
    st.session_state["entradas"] = {
        "BM": {"OUT": 3900.0, "NOV": 3900.0, "DEZ": 3900.0, "JAN": 3900.0},
        "VR": {"OUT": 2900.0, "NOV": 2900.0, "DEZ": 2900.0, "JAN": 2900.0},
        "FIT": {"OUT": 0.0, "NOV": 0.0, "DEZ": 0.0, "JAN": 0.0},
        "PLR": {"OUT": 5000.0, "NOV": 0.0, "DEZ": 0.0, "JAN": 0.0}
    }

# Tentar carregar/salvar via Google Sheets se configurado
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    conn = None

# ---------------------------------------------------------
# BARRA LATERAL: GERENCIAMENTO DE BACKUP & GOOGLE SHEETS
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Opções de Dados & Backup")
    
    # 1. Exportar Backup Local (JSON)
    dados_completos = {
        "despesas_cartoes": st.session_state["despesas_cartoes"],
        "despesas_sem_cartao": st.session_state["despesas_sem_cartao"],
        "entradas": st.session_state["entradas"]
    }
    json_str = json.dumps(dados_completos, indent=4)
    st.download_button(
        label="📥 Baixar Backup dos Dados (JSON)",
        data=json_str,
        file_name="backup_orcamento.json",
        mime="application/json"
    )
    
    # 2. Importar Backup Local (JSON)
    uploaded_file = st.file_uploader("📤 Carregar Backup (JSON)", type=["json"])
    if uploaded_file is not None:
        try:
            dados_carregados = json.load(uploaded_file)
            st.session_state["despesas_cartoes"] = dados_carregados.get("despesas_cartoes", st.session_state["despesas_cartoes"])
            st.session_state["despesas_sem_cartao"] = dados_carregados.get("despesas_sem_cartao", st.session_state["despesas_sem_cartao"])
            st.session_state["entradas"] = dados_carregados.get("entradas", st.session_state["entradas"])
            st.success("Dados restaurados com sucesso!")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao carregar o arquivo: {e}")

# ---------------------------------------------------------
# CABEÇALHO E ABAS DO APLICATIVO
# ---------------------------------------------------------
st.title("💳 Gestão de Gastos & Cartões")
st.caption("Aplicativo integrado para controle de faturas, despesas fixas e entradas.")

tab_resumo, tab_cartoes, tab_outras_despesas, tab_entradas = st.tabs([
    "📊 Visão Geral", 
    "💳 Cartões de Crédito", 
    "💸 Outras Despesas", 
    "💰 Entradas"
])

# ABA 1: VISÃO GERAL
with tab_resumo:
    st.subheader("📌 Resumo Financeiro Mensal")
    
    totais_cartoes_mes = {m: 0.0 for m in MESES}
    detalhes_cartoes_mes = {c: {m: 0.0 for m in MESES} for c in CARTOES_INFO}

    for cartao, lista_gastos in st.session_state["despesas_cartoes"].items():
        soma_cartao = sum(lista_gastos)
        detalhes_cartoes_mes[cartao]["OUT"] = soma_cartao
        totais_cartoes_mes["OUT"] += soma_cartao

    totais_sem_cartao = {m: sum(st.session_state["despesas_sem_cartao"][item][m] for item in st.session_state["despesas_sem_cartao"]) for m in MESES}
    totais_gerais = {m: totais_cartoes_mes[m] + totais_sem_cartao[m] for m in MESES}
    totais_entradas = {m: sum(st.session_state["entradas"][item][m] for item in st.session_state["entradas"]) for m in MESES}
    resultados = {m: totais_entradas[m] - totais_gerais[m] for m in MESES}

    mes_sel = st.selectbox("Selecione o mês para análise:", MESES, index=0)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Entradas", f"R$ {totais_entradas[mes_sel]:,.2f}")
    col2.metric("Total Saídas", f"R$ {totais_gerais[mes_sel]:,.2f}")
    
    res_val = resultados[mes_sel]
    col3.metric("Resultado Final", f"R$ {res_val:,.2f}", delta=f"{res_val:,.2f}")

    st.markdown("---")
    st.subheader("📋 Balanço Comparativo por Mês")
    df_balanco = pd.DataFrame([
        {"Item": "Total Parcelado (Cartões)", **{m: f"R$ {totais_cartoes_mes[m]:,.2f}" for m in MESES}},
        {"Item": "Despesas Sem Cartão", **{m: f"R$ {totais_sem_cartao[m]:,.2f}" for m in MESES}},
        {"Item": "TOTAL GERAL DE GASTOS", **{m: f"R$ {totais_gerais[m]:,.2f}" for m in MESES}},
        {"Item": "TOTAL DE ENTRADAS", **{m: f"R$ {totais_entradas[m]:,.2f}" for m in MESES}},
        {"Item": "RESULTADO (LÍQUIDO)", **{m: f"R$ {resultados[m]:,.2f}" for m in MESES}}
    ])
    st.dataframe(df_balanco, width="stretch", hide_index=True)

# ABA 2: CARTÕES DE CRÉDITO
with tab_cartoes:
    st.subheader("💳 Lançamento e Consulta de Cartões")
    
    cartao_selecionado = st.selectbox("Escolha o Cartão:", list(CARTOES_INFO.keys()))
    info = CARTOES_INFO[cartao_selecionado]
    
    st.info(f"ℹ️ **{cartao_selecionado}**: Fechamento todo **dia {info['fechamento']}** | Vencimento todo **dia {info['vencimento']}**")

    with st.expander("➕ Adicionar Nova Compra no Cartão", expanded=False):
        with st.form("form_compra"):
            descricao = st.text_input("Descrição da Compra / Estabelecimento")
            valor = st.number_input("Valor da Compra (R$)", min_value=0.01, step=10.0)
            parcelas = st.number_input("Número de Parcelas", min_value=1, max_value=48, value=1)
            btn_salvar = st.form_submit_button("Salvar Lançamento")
            
            if btn_salvar:
                val_parcela = valor / parcelas
                st.session_state["despesas_cartoes"][cartao_selecionado].append(val_parcela)
                st.success(f"Compra '{descricao}' adicionada com sucesso!")
                st.rerun()

    st.write("### Itens Registrados nesta Fatura")
    lista_itens = st.session_state["despesas_cartoes"][cartao_selecionado]
    df_itens = pd.DataFrame({
        "Item nº": [i + 1 for i in range(len(lista_itens))],
        "Valor da Parcela (R\()": [f"R\) {v:,.2f}" for v in lista_itens]
    })
    st.dataframe(df_itens, width="stretch")
    st.write(f"**Total acumulado no cartão {cartao_selecionado}:** R$ {sum(lista_itens):,.2f}")

# ABA 3: OUTRAS DESPESAS
with tab_outras_despesas:
    st.subheader("💸 Despesas Fixas e Variáveis (Sem Cartão)")
    for item in st.session_state["despesas_sem_cartao"]:
        st.write(f"#### 🚗 {item}")
        cols = st.columns(4)
        for idx, m in enumerate(MESES):
            val_atual = st.session_state["despesas_sem_cartao"][item][m]
            novo_val = cols[idx].number_input(f"{item} ({m})", value=float(val_atual), step=50.0, key=f"desp_{item}_{m}")
            st.session_state["despesas_sem_cartao"][item][m] = novo_val

# ABA 4: ENTRADAS
with tab_entradas:
    st.subheader("💰 Entradas e Receitas")
    for item in st.session_state["entradas"]:
        st.write(f"#### 💵 {item}")
        cols = st.columns(4)
        for idx, m in enumerate(MESES):
            val_atual = st.session_state["entradas"][item][m]
            novo_val = cols[idx].number_input(f"{item} ({m})", value=float(val_atual), step=100.0, key=f"ent_{item}_{m}")
            st.session_state["entradas"][item][m] = novo_val
