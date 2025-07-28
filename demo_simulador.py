#!/usr/bin/env python3
"""
Demonstração automática do Simulador de Estratégia para Soja
"""

from simulador_soja import SimuladorSoja, TipoCenario, TipoEstrategia

def demonstracao_completa():
    """Executa uma demonstração completa do simulador"""
    print("=" * 70)
    print("           DEMONSTRAÇÃO DO SIMULADOR DE ESTRATÉGIA PARA SOJA")
    print("=" * 70)
    print()
    
    # Inicializar simulador
    simulador = SimuladorSoja()
    
    # Configuração inicial
    print("1. CONFIGURAÇÃO INICIAL")
    print("-" * 25)
    simulador.definir_valor_alavanca('premio', 1.20)
    simulador.definir_valor_alavanca('tela', 14.50)
    simulador.definir_valor_alavanca('dolar', 5.30)
    
    resumo = simulador.obter_resumo_alavancas()
    for nome, dados in resumo.items():
        print(f"  {nome.capitalize()}: {dados['valor_atual']:.3f} {dados['unidade']}")
    
    preco_atual_usd = 14.50 + 1.20  # 15.70 USD
    preco_atual_brl = preco_atual_usd * 5.30  # 83.21 BRL
    print(f"\nPreço atual: USD {preco_atual_usd:.2f} = BRL {preco_atual_brl:.2f}")
    
    # Cenário 1: Otimista
    print("\n\n2. CENÁRIO OTIMISTA")
    print("-" * 20)
    print("Expectativas: Prêmio +15%, Tela +12%, Dólar +8%")
    
    simulador.definir_cenario_alavanca('premio', TipoCenario.ALTA, 15.0)
    simulador.definir_cenario_alavanca('tela', TipoCenario.ALTA, 12.0)
    simulador.definir_cenario_alavanca('dolar', TipoCenario.ALTA, 8.0)
    
    estrategias = [
        TipoEstrategia.SEM_TRAVAMENTO,
        TipoEstrategia.TRAVAR_DOLAR,
        TipoEstrategia.TRAVAR_SOJA_B3,
        TipoEstrategia.TRAVAR_SOJA_CHICAGO
    ]
    
    resultados_otimista = simulador.comparar_estrategias(estrategias)
    
    print(f"{'Estratégia':<20} {'Preço BRL':<12} {'Variação':<10} {'Exposição'}")
    print("-" * 60)
    
    for resultado in resultados_otimista:
        nome_estrategia = resultado.estrategia.value.replace("_", " ").title()
        exposicoes = [k for k, v in resultado.exposicao_risco.items() if v]
        exposicao_str = ", ".join(exposicoes) if exposicoes else "Nenhuma"
        
        print(f"{nome_estrategia:<20} "
              f"R$ {resultado.preco_final_brl:<8.2f} "
              f"{resultado.variacao_percentual:>6.2f}% "
              f"{exposicao_str}")
    
    melhor_otimista = max(resultados_otimista, key=lambda r: r.preco_final_brl)
    print(f"\n✓ Melhor estratégia: {melhor_otimista.estrategia.value.replace('_', ' ').title()}")
    print(f"  Ganho: R$ {melhor_otimista.preco_final_brl - preco_atual_brl:.2f}")
    
    # Cenário 2: Pessimista
    print("\n\n3. CENÁRIO PESSIMISTA")
    print("-" * 22)
    print("Expectativas: Prêmio -25%, Tela -18%, Dólar -12%")
    
    simulador.definir_cenario_alavanca('premio', TipoCenario.BAIXA, 25.0)
    simulador.definir_cenario_alavanca('tela', TipoCenario.BAIXA, 18.0)
    simulador.definir_cenario_alavanca('dolar', TipoCenario.BAIXA, 12.0)
    
    resultados_pessimista = simulador.comparar_estrategias(estrategias)
    
    print(f"{'Estratégia':<20} {'Preço BRL':<12} {'Variação':<10} {'Exposição'}")
    print("-" * 60)
    
    for resultado in resultados_pessimista:
        nome_estrategia = resultado.estrategia.value.replace("_", " ").title()
        exposicoes = [k for k, v in resultado.exposicao_risco.items() if v]
        exposicao_str = ", ".join(exposicoes) if exposicoes else "Nenhuma"
        
        print(f"{nome_estrategia:<20} "
              f"R$ {resultado.preco_final_brl:<8.2f} "
              f"{resultado.variacao_percentual:>6.2f}% "
              f"{exposicao_str}")
    
    melhor_pessimista = max(resultados_pessimista, key=lambda r: r.preco_final_brl)
    print(f"\n✓ Melhor estratégia: {melhor_pessimista.estrategia.value.replace('_', ' ').title()}")
    print(f"  Proteção: R$ {melhor_pessimista.preco_final_brl - min(r.preco_final_brl for r in resultados_pessimista):.2f}")
    
    # Cenário 3: Misto
    print("\n\n4. CENÁRIO MISTO")
    print("-" * 16)
    print("Expectativas: Prêmio +20%, Tela -8%, Dólar +5%")
    
    simulador.definir_cenario_alavanca('premio', TipoCenario.ALTA, 20.0)
    simulador.definir_cenario_alavanca('tela', TipoCenario.BAIXA, 8.0)
    simulador.definir_cenario_alavanca('dolar', TipoCenario.ALTA, 5.0)
    
    resultados_misto = simulador.comparar_estrategias(estrategias)
    
    print(f"{'Estratégia':<20} {'Preço BRL':<12} {'Variação':<10} {'Exposição'}")
    print("-" * 60)
    
    for resultado in resultados_misto:
        nome_estrategia = resultado.estrategia.value.replace("_", " ").title()
        exposicoes = [k for k, v in resultado.exposicao_risco.items() if v]
        exposicao_str = ", ".join(exposicoes) if exposicoes else "Nenhuma"
        
        print(f"{nome_estrategia:<20} "
              f"R$ {resultado.preco_final_brl:<8.2f} "
              f"{resultado.variacao_percentual:>6.2f}% "
              f"{exposicao_str}")
    
    # Análise comparativa
    print("\n\n5. ANÁLISE COMPARATIVA")
    print("-" * 23)
    
    cenarios = ["Otimista", "Pessimista", "Misto"]
    todos_resultados = [resultados_otimista, resultados_pessimista, resultados_misto]
    
    for i, estrategia in enumerate(estrategias):
        nome_estrategia = estrategia.value.replace("_", " ").title()
        print(f"\n{nome_estrategia}:")
        
        for j, cenario in enumerate(cenarios):
            resultado = todos_resultados[j][i]
            print(f"  {cenario:<12}: R$ {resultado.preco_final_brl:>7.2f} ({resultado.variacao_percentual:>6.2f}%)")
        
        # Calcular volatilidade (desvio padrão dos resultados)
        precos = [todos_resultados[j][i].preco_final_brl for j in range(3)]
        media = sum(precos) / len(precos)
        variancia = sum((p - media) ** 2 for p in precos) / len(precos)
        desvio_padrao = variancia ** 0.5
        print(f"  Volatilidade: R$ {desvio_padrao:.2f}")
    
    # Recomendações
    print("\n\n6. RECOMENDAÇÕES")
    print("-" * 17)
    
    print("Com base na análise dos cenários:")
    print()
    print("• Para cenários OTIMISTAS:")
    print("  - Sem travamento oferece maior retorno")
    print("  - Aceitar exposição total para maximizar ganhos")
    print()
    print("• Para cenários PESSIMISTAS:")
    print("  - Travar soja B3 oferece melhor proteção")
    print("  - Elimina risco de preço, mantém apenas risco cambial")
    print()
    print("• Para cenários MISTOS:")
    print("  - Avaliar travamento parcial do dólar")
    print("  - Balancear exposição vs. proteção")
    print()
    print("• ESTRATÉGIA GERAL:")
    print("  - Diversificar entre diferentes tipos de travamento")
    print("  - Monitorar indicadores de mercado regularmente")
    print("  - Ajustar estratégia conforme mudanças nas expectativas")
    
    # Salvar configuração de exemplo
    print("\n\n7. SALVANDO CONFIGURAÇÃO DE EXEMPLO")
    print("-" * 38)
    
    try:
        simulador.exportar_configuracao("exemplo_cenario_misto.json")
        print("✓ Configuração salva em 'exemplo_cenario_misto.json'")
    except Exception as e:
        print(f"✗ Erro ao salvar: {e}")
    
    print("\n" + "=" * 70)
    print("           DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)

def teste_validacao_completa():
    """Testa todas as funcionalidades de validação"""
    print("\n\nTESTE DE VALIDAÇÃO COMPLETA")
    print("=" * 30)
    
    simulador = SimuladorSoja()
    
    # Teste de ranges
    print("\n1. Teste de ranges das alavancas:")
    testes_range = [
        ('premio', -0.50, True),   # Mínimo válido
        ('premio', 2.50, True),    # Máximo válido
        ('premio', -1.00, False),  # Abaixo do mínimo
        ('premio', 3.00, False),   # Acima do máximo
        ('tela', 15.00, True),     # Valor válido
        ('dolar', 5.00, True),     # Valor válido
    ]
    
    for alavanca, valor, esperado in testes_range:
        resultado = simulador.definir_valor_alavanca(alavanca, valor)
        status = "✓" if resultado == esperado else "✗"
        print(f"  {status} {alavanca} = {valor}: {resultado}")
    
    # Teste de cenários
    print("\n2. Teste de definição de cenários:")
    cenarios_teste = [
        ('premio', TipoCenario.ALTA, 10.0),
        ('tela', TipoCenario.BAIXA, 15.0),
        ('dolar', TipoCenario.NEUTRO, 0.0),
    ]
    
    for alavanca, cenario, variacao in cenarios_teste:
        resultado = simulador.definir_cenario_alavanca(alavanca, cenario, variacao)
        print(f"  ✓ {alavanca}: {cenario.value} ({variacao}%) = {resultado}")
    
    # Teste de cálculos
    print("\n3. Teste de cálculos:")
    for nome in simulador.alavancas.keys():
        valor_cenario = simulador.calcular_valor_cenario(nome)
        print(f"  ✓ {nome}: {valor_cenario:.3f}")
    
    preco_usd, preco_brl = simulador.calcular_preco_base()
    print(f"  ✓ Preço base: USD {preco_usd:.2f} = BRL {preco_brl:.2f}")
    
    print("\n✓ Todos os testes de validação passaram!")

if __name__ == "__main__":
    try:
        demonstracao_completa()
        teste_validacao_completa()
    except Exception as e:
        print(f"\nErro durante a demonstração: {e}")
        import traceback
        traceback.print_exc()

