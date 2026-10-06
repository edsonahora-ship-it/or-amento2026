import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA (Interface Otimizada para Celular)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Gestão Financeira & Cartões",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilização visual para dispositivos móveis
st.markdown("""
    
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# INICIALIZAÇÃO DO ESTADO DE DADOS (Sessão)
# ---------------------------------------------------------
# Cartões cadastrados com seus respectivos dias de fechamento e vencimento conforme a planilha
CARTOES_INFO = {
    "Caixa": {"fechamento": 5, "vencimento": 17},
    "Itaú": {"fechamento": 3, "vencimento": 10},
    "Inter": {"fechamento": 22, "vencimento": 28},
    "Santander": {"fechamento": 5, "vencimento": 10},
    "Magalu": {"fechamento": 1, "vencimento": 25},
    "Mercado Livre": {"fechamento": 1, "vencimento": 15}
}

MESES = ["OUT", "NOV", "DEZ", "JAN"]

if "despesas_cartoes" not in st.session_state:
    # Dados iniciais baseados na planilha modelo
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

# ---------------------------------------------------------
# CABEÇALHO DO APLICATIVO
# ---------------------------------------------------------
st.title("💳 Gestão de Gastos & Cartões")
st.caption("Aplicativo integrado para controle de faturas, despesas fixas e entradas.")

# Navegação por Abas para facilidade de uso em telas de celular
tab_resumo, tab_cartoes, tab_outras_despesas, tab_entradas = st.tabs([
    "📊 Visão Geral", 
    "💳 Cartões de Crédito", 
    "💸 Outras Despesas", 
    "💰 Entradas"
])

# ---------------------------------------------------------
# ABA 1: VISÃO GERAL E RESULTADO FINANCEIRO
# ---------------------------------------------------------
with tab_resumo:
    st.subheader("📌 Resumo Financeiro Mensal")
    
    # Cálculo das faturas por cartão para cada mês
    totais_cartoes_mes = {m: 0.0 for m in MESES}
    detalhes_cartoes_mes = {c: {m: 0.0 for m in MESES} for c in CARTOES_INFO}

    for cartao, lista_gastos in st.session_state["despesas_cartoes"].items():
        soma_cartao = sum(lista_gastos)
        # Distribuição ilustrativa para simular a consolidação dos meses da planilha
        detalhes_cartoes_mes[cartao]["OUT"] = soma_cartao
        totais_cartoes_mes["OUT"] += soma_cartao

    # Totais de despesas sem cartão por mês
    totais_sem_cartao = {m: sum(st.session_state["despesas_sem_cartao"][item][m] for item in st.session_state["despesas_sem_cartao"]) for m in MESES}
    
    # Totais gerais de gastos
    totais_gerais = {m: totais_cartoes_mes[m] + totais_sem_cartao[m] for m in MESES}
    
    # Totais de entradas
    totais_entradas = {m: sum(st.session_state["entradas"][item][m] for item in st.session_state["entradas"]) for m in MESES}
    
    # Resultado líquido (Entradas - Saídas)
    resultados = {m: totais_entradas[m] - totais_gerais[m] for m in MESES}

    # Exibição de Cartões de Métricas para o Mês Selecionado
    mes_sel = st.selectbox("Selecione o mês para análise:", MESES, index=0)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Entradas", f"R$ {totais_entradas[mes_sel]:,.2f}")
    col2.metric("Total Saídas", f"R$ {totais_gerais[mes_sel]:,.2f}")
    
    res_val = resultados[mes_sel]
    col3.metric("Resultado Final", f"R$ {res_val:,.2f}", delta=f"{res_val:,.2f}")

    st.markdown("---")
    
    # Tabela comparativa Geral
    st.subheader("📋 Balanço Comparativo por Mês")
    df_balanco = pd.DataFrame([
        {"Item": "Total Parcelado (Cartões)", **{m: f"R$ {totais_cartoes_mes[m]:,.2f}" for m in MESES}},
        {"Item": "Despesas Sem Cartão", **{m: f"R$ {totais_sem_cartao[m]:,.2f}" for m in MESES}},
        {"Item": "TOTAL GERAL DE GASTOS", **{m: f"R$ {totais_gerais[m]:,.2f}" for m in MESES}},
        {"Item": "TOTAL DE ENTRADAS", **{m: f"R$ {totais_entradas[m]:,.2f}" for m in MESES}},
        {"Item": "RESULTADO (LÍQUIDO)", **{m: f"R$ {resultados[m]:,.2f}" for m in MESES}}
    ])
    st.dataframe(df_balanco, use_container_width=True, hide_index=True)

    # Seção de Gastos por Dia (baseado na lógica de dias até o vencimento)
    st.markdown("---")
    st.subheader("📅 Projeção de Gastos por Dia")
    st.caption("Cálculo da estimativa de gasto diário com base nos dias restantes de cada cartão.")
    
    gastos_dia_data = []
    for c_nome, c_info in CARTOES_INFO.items():
        venc = c_info["vencimento"]
        fatura_out = detalhes_cartoes_mes[c_nome]["OUT"]
        gasto_diario = fatura_out / venc if venc > 0 else 0.0
        gastos_dia_data.append({
            "Cartão": c_nome,
            "Fechamento": f"Dia {c_info['fechamento']}",
            "Vencimento": f"Dia {c_info['vencimento']}",
            "Fatura (OUT)": f"R$ {fatura_out:,.2f}",
            "Gasto Média/Dia": f"R$ {gasto_diario:,.2f}"
        })
    
    st.dataframe(pd.DataFrame(gastos_dia_data), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# ABA 2: GERENCIAMENTO DE CARTÕES DE CRÉDITO
# ---------------------------------------------------------
with tab_cartoes:
    st.subheader("💳 Lançamento e Consulta de Cartões")
    
    cartao_selecionado = st.selectbox("Escolha o Cartão:", list(CARTOES_INFO.keys()))
    info = CARTOES_INFO[cartao_selecionado]
    
    st.info(f"ℹ️ **{cartao_selecionado}**: Fechamento todo **dia {info['fechamento']}** | Vencimento todo **dia {info['vencimento']}**")

    # Formulário para adicionar nova compra
    with st.expander("➕ Adicionar Nova Compra no Cartão", expanded=False):
        with st.form("form_compra"):
            descricao = st.text_input("Descrição da Compra / Estabelecimento")
            valor = st.number_input("Valor da Compra (R$)", min_value=0.01, step=10.0)
            parcelas = st.number_input("Número de Parcelas", min_value=1, max_value=48, value=1)
            btn_salvar = st.form_submit_button("Salvar Lançamento")
            
            if btn_salvar:
                val_parcela = valor / parcelas
                st.session_state["despesas_cartoes"][cartao_selecionado].append(val_parcela)
                st.success(f"Compra '{descricao}' adicionada com sucesso! Valor por parcela: R$ {val_parcela:,.2f}")
                st.rerun()

    # Exibição das despesas registradas no cartão
    st.write("### Itens Registrados nesta Fatura")
    lista_itens = st.session_state["despesas_cartoes"][cartao_selecionado]
    df_itens = pd.DataFrame({
        "Item nº": [i + 1 for i in range(len(lista_itens))],
        "Valor da Parcela (R\()": [f"R\) {v:,.2f}" for v in lista_itens]
    })
    st.dataframe(df_itens, use_container_width=True)
    st.write(f"**Total acumulado no cartão {cartao_selecionado}:** R$ {sum(lista_itens):,.2f}")

# ---------------------------------------------------------
# ABA 3: OUTRAS DESPESAS (SEM CARTÃO)
# ---------------------------------------------------------
with tab_outras_despesas:
    st.subheader("💸 Despesas Fixas e Variáveis (Sem Cartão)")
    st.caption("Edite diretamente os valores dos gastos não atrelados aos cartões de crédito.")

    for item in st.session_state["despesas_sem_cartao"]:
        st.write(f"#### 🚗 {item}")
        cols = st.columns(4)
        for idx, m in enumerate(MESES):
            val_atual = st.session_state["despesas_sem_cartao"][item][m]
            novo_val = cols[idx].number_input(f"{item} ({m})", value=float(val_atual), step=50.0, key=f"desp_{item}_{m}")
            st.session_state["despesas_sem_cartao"][item][m] = novo_val

# ---------------------------------------------------------
# ABA 4: ENTRADAS E RENDIMENTOS
# ---------------------------------------------------------
with tab_entradas:
    st.subheader("💰 Entradas e Receitas")
    st.caption("Gerencie os valores recebidos por fonte e mês.")

    for item in st.session_state["entradas"]:
        st.write(f"#### 💵 {item}")
        cols = st.columns(4)
        for idx, m in enumerate(MESES):
            val_atual = st.session_state["entradas"][item][m]
            novo_val = cols[idx].number_input(f"{item} ({m})", value=float(val_atual), step=100.0, key=f"ent_{item}_{m}")
            st.session_state["entradas"][item][m] = novo_val