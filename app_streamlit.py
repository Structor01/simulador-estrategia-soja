#!/usr/bin/env python3
"""
Interface Streamlit para o Simulador de Estratégia para Soja
Design profissional inspirado em dashboards financeiros
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from simulador_soja import SimuladorSoja, TipoCenario, TipoEstrategia

# Configuração da página
st.set_page_config(
    page_title="Simulador de Estratégia para Soja",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado para tema profissional com animações
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main > div {
        padding-top: 1rem;
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0E1117 0%, #1A1A2E 50%, #16213E 100%);
        background-attachment: fixed;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #333;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(192, 192, 192, 0.1);
        border-color: #C0C0C0;
    }
    
    .strategy-header {
        background: linear-gradient(135deg, #C0C0C0 0%, #808080 50%, #A0A0A0 100%);
        color: #000;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        font-weight: 700;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(192, 192, 192, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .strategy-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .scenario-tag {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
        transition: all 0.2s ease;
        cursor: default;
    }
    
    .scenario-tag:hover {
        transform: scale(1.05);
    }
    
    .scenario-alta {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
    }
    
    .scenario-baixa {
        background: linear-gradient(135deg, #dc3545 0%, #e74c3c 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
    }
    
    .scenario-neutro {
        background: linear-gradient(135deg, #6c757d 0%, #95a5a6 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(108, 117, 125, 0.3);
    }
    
    .lever-section {
        background: linear-gradient(135deg, #1E1E1E 0%, #2A2A2A 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #C0C0C0;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .lever-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #C0C0C0, transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .lever-section:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 30px rgba(192, 192, 192, 0.1);
        border-left-color: #E0E0E0;
    }
    
    .lever-section:hover::before {
        opacity: 1;
    }
    
    .result-positive {
        color: #28a745;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(40, 167, 69, 0.3);
    }
    
    .result-negative {
        color: #dc3545;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(220, 53, 69, 0.3);
    }
    
    .result-neutral {
        color: #C0C0C0;
        font-weight: 600;
    }
    
    /* Animações para métricas */
    .metric-container {
        background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #333;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-container:hover {
        border-color: #C0C0C0;
        box-shadow: 0 8px 25px rgba(192, 192, 192, 0.1);
    }
    
    /* Estilo para tabelas */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Botões personalizados */
    .stButton > button {
        background: linear-gradient(135deg, #C0C0C0 0%, #808080 100%);
        color: #000;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(192, 192, 192, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(192, 192, 192, 0.3);
        background: linear-gradient(135deg, #E0E0E0 0%, #A0A0A0 100%);
    }
    
    /* Animação de loading */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 1.5s infinite;
    }
    
    /* Scrollbar personalizada */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1E1E1E;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #C0C0C0;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #E0E0E0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def inicializar_simulador():
    """Inicializa o simulador com cache"""
    return SimuladorSoja()

def formatar_moeda_brl(valor):
    """Formata valor em reais"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_moeda_usd(valor):
    """Formata valor em dólares"""
    return f"USD {valor:,.2f}"

def formatar_percentual(valor):
    """Formata percentual"""
    sinal = "+" if valor > 0 else ""
    return f"{sinal}{valor:.2f}%"

def obter_cor_variacao(valor):
    """Retorna cor baseada na variação"""
    if valor > 0:
        return "result-positive"
    elif valor < 0:
        return "result-negative"
    else:
        return "result-neutral"

def criar_grafico_comparacao(resultados):
    """Cria gráfico de comparação de estratégias"""
    estrategias = []
    precos = []
    variacoes = []
    cores = []
    
    for resultado in resultados:
        nome = resultado.estrategia.value.replace("_", " ").title()
        estrategias.append(nome)
        precos.append(resultado.preco_final_brl)
        variacoes.append(resultado.variacao_percentual)
        
        # Cor baseada na variação
        if resultado.variacao_percentual > 0:
            cores.append('#28a745')  # Verde
        elif resultado.variacao_percentual < 0:
            cores.append('#dc3545')  # Vermelho
        else:
            cores.append('#6c757d')  # Cinza
    
    fig = go.Figure()
    
    # Barras de preço
    fig.add_trace(go.Bar(
        x=estrategias,
        y=precos,
        name='Preço Final (BRL)',
        marker_color=cores,
        text=[formatar_moeda_brl(p) for p in precos],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Preço: %{text}<br>Variação: ' + 
                     '<br>'.join([formatar_percentual(v) for v in variacoes]) + '<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': 'Comparação de Estratégias',
            'x': 0.5,
            'font': {'size': 20, 'color': '#C0C0C0'}
        },
        xaxis_title='Estratégias',
        yaxis_title='Preço Final (BRL)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#C0C0C0'},
        xaxis={'color': '#C0C0C0'},
        yaxis={'color': '#C0C0C0'},
        height=400
    )
    
    return fig

def criar_grafico_sensibilidade(simulador):
    """Cria gráfico de análise de sensibilidade"""
    # Variações de -20% a +20%
    variacoes = np.arange(-20, 21, 5)
    
    # Dados para cada alavanca
    dados_premio = []
    dados_tela = []
    dados_dolar = []
    
    # Salvar configuração atual
    config_atual = {
        'premio': (simulador.alavancas['premio'].cenario, simulador.alavancas['premio'].variacao_percentual),
        'tela': (simulador.alavancas['tela'].cenario, simulador.alavancas['tela'].variacao_percentual),
        'dolar': (simulador.alavancas['dolar'].cenario, simulador.alavancas['dolar'].variacao_percentual)
    }
    
    for var in variacoes:
        # Teste variação do prêmio
        simulador.definir_cenario_alavanca('premio', TipoCenario.ALTA if var >= 0 else TipoCenario.BAIXA, abs(var))
        resultado = simulador.simular_estrategia(TipoEstrategia.SEM_TRAVAMENTO)
        dados_premio.append(resultado.preco_final_brl)
        
        # Restaurar prêmio e testar tela
        simulador.definir_cenario_alavanca('premio', config_atual['premio'][0], config_atual['premio'][1])
        simulador.definir_cenario_alavanca('tela', TipoCenario.ALTA if var >= 0 else TipoCenario.BAIXA, abs(var))
        resultado = simulador.simular_estrategia(TipoEstrategia.SEM_TRAVAMENTO)
        dados_tela.append(resultado.preco_final_brl)
        
        # Restaurar tela e testar dólar
        simulador.definir_cenario_alavanca('tela', config_atual['tela'][0], config_atual['tela'][1])
        simulador.definir_cenario_alavanca('dolar', TipoCenario.ALTA if var >= 0 else TipoCenario.BAIXA, abs(var))
        resultado = simulador.simular_estrategia(TipoEstrategia.SEM_TRAVAMENTO)
        dados_dolar.append(resultado.preco_final_brl)
        
        # Restaurar dólar
        simulador.definir_cenario_alavanca('dolar', config_atual['dolar'][0], config_atual['dolar'][1])
    
    # Restaurar configuração original
    for nome, (cenario, variacao) in config_atual.items():
        simulador.definir_cenario_alavanca(nome, cenario, variacao)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=variacoes, y=dados_premio,
        mode='lines+markers',
        name='Prêmio',
        line=dict(color='#FFD700', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=variacoes, y=dados_tela,
        mode='lines+markers',
        name='Tela',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=variacoes, y=dados_dolar,
        mode='lines+markers',
        name='Dólar',
        line=dict(color='#4ECDC4', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title={
            'text': 'Análise de Sensibilidade',
            'x': 0.5,
            'font': {'size': 20, 'color': '#C0C0C0'}
        },
        xaxis_title='Variação (%)',
        yaxis_title='Preço Final (BRL)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': '#C0C0C0'},
        xaxis={'color': '#C0C0C0'},
        yaxis={'color': '#C0C0C0'},
        height=400,
        legend=dict(
            bgcolor='rgba(30,30,30,0.8)',
            bordercolor='#C0C0C0',
            borderwidth=1
        )
    )
    
    return fig

def main():
    """Função principal da aplicação"""
    
    # Header
    st.markdown("""
    <div class="strategy-header">
        <h1>🌱 SIMULADOR DE ESTRATÉGIA PARA SOJA</h1>
        <p>Análise profissional de cenários e estratégias de trading</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar simulador
    if 'simulador' not in st.session_state:
        st.session_state.simulador = inicializar_simulador()
    
    simulador = st.session_state.simulador
    
    # Layout em colunas para controles
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="lever-section">', unsafe_allow_html=True)
        st.subheader("💰 Prêmio")
        
        premio_valor = st.slider(
            "Valor Atual (USD)",
            min_value=-0.50,
            max_value=2.50,
            value=1.00,
            step=0.01,
            key="premio_valor"
        )
        
        premio_cenario = st.selectbox(
            "Cenário",
            ["Alta", "Baixa", "Neutro"],
            index=0,
            key="premio_cenario"
        )
        
        premio_variacao = st.slider(
            "Variação (%)",
            min_value=0.0,
            max_value=50.0,
            value=15.0,
            step=1.0,
            key="premio_variacao"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="lever-section">', unsafe_allow_html=True)
        st.subheader("📊 Tela (Preço Base)")
        
        tela_valor = st.slider(
            "Valor Atual (USD/bushel)",
            min_value=10.00,
            max_value=25.00,
            value=15.00,
            step=0.01,
            key="tela_valor"
        )
        
        tela_cenario = st.selectbox(
            "Cenário",
            ["Alta", "Baixa", "Neutro"],
            index=0,
            key="tela_cenario"
        )
        
        tela_variacao = st.slider(
            "Variação (%)",
            min_value=0.0,
            max_value=50.0,
            value=12.0,
            step=1.0,
            key="tela_variacao"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="lever-section">', unsafe_allow_html=True)
        st.subheader("💵 Dólar")
        
        dolar_valor = st.slider(
            "Taxa Atual (BRL/USD)",
            min_value=4.50,
            max_value=6.50,
            value=5.20,
            step=0.01,
            key="dolar_valor"
        )
        
        dolar_cenario = st.selectbox(
            "Cenário",
            ["Alta", "Baixa", "Neutro"],
            index=0,
            key="dolar_cenario"
        )
        
        dolar_variacao = st.slider(
            "Variação (%)",
            min_value=0.0,
            max_value=50.0,
            value=8.0,
            step=1.0,
            key="dolar_variacao"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Atualizar simulador com valores da interface
    simulador.definir_valor_alavanca('premio', premio_valor)
    simulador.definir_valor_alavanca('tela', tela_valor)
    simulador.definir_valor_alavanca('dolar', dolar_valor)
    
    # Mapear cenários
    cenario_map = {
        "Alta": TipoCenario.ALTA,
        "Baixa": TipoCenario.BAIXA,
        "Neutro": TipoCenario.NEUTRO
    }
    
    simulador.definir_cenario_alavanca('premio', cenario_map[premio_cenario], premio_variacao)
    simulador.definir_cenario_alavanca('tela', cenario_map[tela_cenario], tela_variacao)
    simulador.definir_cenario_alavanca('dolar', cenario_map[dolar_cenario], dolar_variacao)
    
    # Calcular preço atual e no cenário
    preco_atual_usd = tela_valor + premio_valor
    preco_atual_brl = preco_atual_usd * dolar_valor
    preco_cenario_usd, preco_cenario_brl = simulador.calcular_preco_base()
    
    # Métricas principais
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Preço Atual",
            formatar_moeda_brl(preco_atual_brl),
            formatar_moeda_usd(preco_atual_usd)
        )
    
    with col2:
        st.metric(
            "Preço no Cenário",
            formatar_moeda_brl(preco_cenario_brl),
            formatar_moeda_usd(preco_cenario_usd)
        )
    
    with col3:
        variacao_cenario = ((preco_cenario_brl - preco_atual_brl) / preco_atual_brl) * 100
        st.metric(
            "Variação do Cenário",
            formatar_percentual(variacao_cenario),
            formatar_moeda_brl(preco_cenario_brl - preco_atual_brl)
        )
    
    with col4:
        # Tags de cenário
        tags_html = ""
        for nome, cenario in [("Prêmio", premio_cenario), ("Tela", tela_cenario), ("Dólar", dolar_cenario)]:
            classe = f"scenario-{cenario.lower()}"
            tags_html += f'<span class="scenario-tag {classe}">{nome}: {cenario}</span>'
        
        st.markdown(f"**Cenários Ativos:**<br>{tags_html}", unsafe_allow_html=True)
    
    # Simulação de estratégias
    st.markdown("---")
    st.subheader("🎯 Análise de Estratégias")
    
    estrategias = [
        TipoEstrategia.SEM_TRAVAMENTO,
        TipoEstrategia.TRAVAR_DOLAR,
        TipoEstrategia.TRAVAR_SOJA_B3,
        TipoEstrategia.TRAVAR_SOJA_CHICAGO
    ]
    
    resultados = simulador.comparar_estrategias(estrategias)
    
    # Tabela de resultados
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Criar DataFrame para tabela
        dados_tabela = []
        for resultado in resultados:
            nome_estrategia = resultado.estrategia.value.replace("_", " ").title()
            exposicoes = [k.title() for k, v in resultado.exposicao_risco.items() if v]
            exposicao_str = ", ".join(exposicoes) if exposicoes else "Nenhuma"
            
            dados_tabela.append({
                "Estratégia": nome_estrategia,
                "Preço Final": formatar_moeda_brl(resultado.preco_final_brl),
                "Variação": formatar_percentual(resultado.variacao_percentual),
                "Exposição": exposicao_str
            })
        
        df_resultados = pd.DataFrame(dados_tabela)
        st.dataframe(df_resultados, use_container_width=True)
    
    with col2:
        # Melhor e pior estratégia
        melhor = max(resultados, key=lambda r: r.preco_final_brl)
        pior = min(resultados, key=lambda r: r.preco_final_brl)
        
        st.markdown("**🏆 Melhor Estratégia:**")
        st.success(f"{melhor.estrategia.value.replace('_', ' ').title()}")
        st.write(f"Preço: {formatar_moeda_brl(melhor.preco_final_brl)}")
        st.write(f"Variação: {formatar_percentual(melhor.variacao_percentual)}")
        
        st.markdown("**⚠️ Pior Estratégia:**")
        st.error(f"{pior.estrategia.value.replace('_', ' ').title()}")
        st.write(f"Preço: {formatar_moeda_brl(pior.preco_final_brl)}")
        st.write(f"Variação: {formatar_percentual(pior.variacao_percentual)}")
    
    # Gráficos
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_comparacao = criar_grafico_comparacao(resultados)
        st.plotly_chart(fig_comparacao, use_container_width=True)
    
    with col2:
        fig_sensibilidade = criar_grafico_sensibilidade(simulador)
        st.plotly_chart(fig_sensibilidade, use_container_width=True)
    
    # Análise detalhada
    st.markdown("---")
    st.subheader("📋 Análise Detalhada")
    
    estrategia_selecionada = st.selectbox(
        "Selecione uma estratégia para análise detalhada:",
        [r.estrategia.value.replace("_", " ").title() for r in resultados],
        key="estrategia_detalhada"
    )
    
    # Encontrar resultado selecionado
    resultado_selecionado = None
    for resultado in resultados:
        if resultado.estrategia.value.replace("_", " ").title() == estrategia_selecionada:
            resultado_selecionado = resultado
            break
    
    if resultado_selecionado:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**💹 Resultados Financeiros:**")
            st.write(f"• Preço Final: {formatar_moeda_brl(resultado_selecionado.preco_final_brl)}")
            st.write(f"• Preço em USD: {formatar_moeda_usd(resultado_selecionado.preco_final_usd)}")
            st.write(f"• Variação: {formatar_percentual(resultado_selecionado.variacao_percentual)}")
            st.write(f"• Diferença: {formatar_moeda_brl(resultado_selecionado.preco_final_brl - preco_atual_brl)}")
        
        with col2:
            st.markdown("**⚡ Exposição a Riscos:**")
            for alavanca, exposto in resultado_selecionado.exposicao_risco.items():
                status = "🔴 Exposto" if exposto else "🟢 Protegido"
                st.write(f"• {alavanca.title()}: {status}")
        
        # Detalhes do cálculo
        st.markdown("**🔢 Detalhes do Cálculo:**")
        detalhes = resultado_selecionado.detalhes_calculo
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"Prêmio no cenário: {formatar_moeda_usd(detalhes['premio_cenario'])}")
        with col2:
            st.write(f"Tela no cenário: {formatar_moeda_usd(detalhes['tela_cenario'])}")
        with col3:
            st.write(f"Dólar no cenário: R$ {detalhes['dolar_cenario']:.2f}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Simulador de Estratégia para Soja | Desenvolvido para análise profissional de trading</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

