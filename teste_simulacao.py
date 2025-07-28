#!/usr/bin/env python3
"""
Script de teste para validar a lógica de simulação do Simulador de Soja
"""

from simulador_soja import SimuladorSoja, TipoCenario, TipoEstrategia

def teste_cenarios_basicos():
    """Testa cenários básicos de simulação"""
    print("=== TESTE DE CENÁRIOS BÁSICOS ===\n")
    
    simulador = SimuladorSoja()
    
    # Configuração inicial
    simulador.definir_valor_alavanca('premio', 1.00)  # USD 1.00 de prêmio
    simulador.definir_valor_alavanca('tela', 15.00)   # USD 15.00 preço base
    simulador.definir_valor_alavanca('dolar', 5.20)   # R$ 5.20 por dólar
    
    print("Configuração inicial:")
    resumo = simulador.obter_resumo_alavancas()
    for nome, dados in resumo.items():
        print(f"  {dados['valor_atual']:.2f} {dados['unidade']} - {nome}")
    
    # Preço atual de referência
    preco_atual_usd = 15.00 + 1.00  # 16.00 USD
    preco_atual_brl = preco_atual_usd * 5.20  # 83.20 BRL
    print(f"\nPreço atual: USD {preco_atual_usd:.2f} = BRL {preco_atual_brl:.2f}")
    
    return simulador, preco_atual_brl

def teste_cenario_otimista():
    """Testa cenário otimista (todas as alavancas favoráveis)"""
    print("\n=== CENÁRIO OTIMISTA ===")
    
    simulador, preco_base = teste_cenarios_basicos()
    
    # Cenário otimista: prêmio sobe, tela sobe, dólar sobe (bom para exportador)
    simulador.definir_cenario_alavanca('premio', TipoCenario.ALTA, 20.0)  # +20%
    simulador.definir_cenario_alavanca('tela', TipoCenario.ALTA, 15.0)    # +15%
    simulador.definir_cenario_alavanca('dolar', TipoCenario.ALTA, 10.0)   # +10%
    
    print("\nCenários definidos:")
    print("  Prêmio: ALTA (+20%)")
    print("  Tela: ALTA (+15%)")
    print("  Dólar: ALTA (+10%)")
    
    # Teste sem travamento
    resultado = simulador.simular_estrategia(TipoEstrategia.SEM_TRAVAMENTO)
    print(f"\nSem travamento:")
    print(f"  Preço final: BRL {resultado.preco_final_brl:.2f}")
    print(f"  Variação: {resultado.variacao_percentual:.2f}%")
    
    # Teste com travamento de dólar
    resultado_dolar = simulador.simular_estrategia(TipoEstrategia.TRAVAR_DOLAR)
    print(f"\nTravando dólar:")
    print(f"  Preço final: BRL {resultado_dolar.preco_final_brl:.2f}")
    print(f"  Variação: {resultado_dolar.variacao_percentual:.2f}%")
    
    return simulador

def teste_cenario_pessimista():
    """Testa cenário pessimista (todas as alavancas desfavoráveis)"""
    print("\n=== CENÁRIO PESSIMISTA ===")
    
    simulador = SimuladorSoja()
    
    # Configuração inicial
    simulador.definir_valor_alavanca('premio', 1.00)
    simulador.definir_valor_alavanca('tela', 15.00)
    simulador.definir_valor_alavanca('dolar', 5.20)
    
    # Cenário pessimista: prêmio cai, tela cai, dólar cai (ruim para exportador)
    simulador.definir_cenario_alavanca('premio', TipoCenario.BAIXA, 30.0)  # -30%
    simulador.definir_cenario_alavanca('tela', TipoCenario.BAIXA, 20.0)    # -20%
    simulador.definir_cenario_alavanca('dolar', TipoCenario.BAIXA, 15.0)   # -15%
    
    print("Cenários definidos:")
    print("  Prêmio: BAIXA (-30%)")
    print("  Tela: BAIXA (-20%)")
    print("  Dólar: BAIXA (-15%)")
    
    # Teste diferentes estratégias
    estrategias = [
        TipoEstrategia.SEM_TRAVAMENTO,
        TipoEstrategia.TRAVAR_DOLAR,
        TipoEstrategia.TRAVAR_SOJA_B3,
        TipoEstrategia.TRAVAR_SOJA_CHICAGO
    ]
    
    resultados = simulador.comparar_estrategias(estrategias)
    
    print("\nComparação de estratégias:")
    for resultado in resultados:
        print(f"  {resultado.estrategia.value}:")
        print(f"    Preço final: BRL {resultado.preco_final_brl:.2f}")
        print(f"    Variação: {resultado.variacao_percentual:.2f}%")
        exposicoes = [k for k, v in resultado.exposicao_risco.items() if v]
        print(f"    Exposição: {', '.join(exposicoes) if exposicoes else 'Nenhuma'}")
    
    return simulador

def teste_cenario_misto():
    """Testa cenário misto (algumas alavancas favoráveis, outras não)"""
    print("\n=== CENÁRIO MISTO ===")
    
    simulador = SimuladorSoja()
    
    # Configuração inicial
    simulador.definir_valor_alavanca('premio', 0.50)
    simulador.definir_valor_alavanca('tela', 14.00)
    simulador.definir_valor_alavanca('dolar', 5.50)
    
    # Cenário misto: prêmio sobe, tela cai, dólar sobe
    simulador.definir_cenario_alavanca('premio', TipoCenario.ALTA, 25.0)   # +25%
    simulador.definir_cenario_alavanca('tela', TipoCenario.BAIXA, 10.0)    # -10%
    simulador.definir_cenario_alavanca('dolar', TipoCenario.ALTA, 8.0)     # +8%
    
    print("Cenários definidos:")
    print("  Prêmio: ALTA (+25%)")
    print("  Tela: BAIXA (-10%)")
    print("  Dólar: ALTA (+8%)")
    
    # Análise detalhada
    resultado = simulador.simular_estrategia(TipoEstrategia.SEM_TRAVAMENTO)
    
    print(f"\nAnálise detalhada:")
    detalhes = resultado.detalhes_calculo
    print(f"  Prêmio no cenário: USD {detalhes['premio_cenario']:.3f}")
    print(f"  Tela no cenário: USD {detalhes['tela_cenario']:.2f}")
    print(f"  Dólar no cenário: BRL {detalhes['dolar_cenario']:.2f}")
    print(f"  Preço USD base: USD {detalhes['preco_usd_base']:.2f}")
    print(f"  Preço BRL final: BRL {resultado.preco_final_brl:.2f}")
    print(f"  Variação total: {resultado.variacao_percentual:.2f}%")
    
    return simulador

def teste_validacao_ranges():
    """Testa validação de ranges das alavancas"""
    print("\n=== TESTE DE VALIDAÇÃO DE RANGES ===")
    
    simulador = SimuladorSoja()
    
    # Teste valores válidos
    print("Testando valores válidos:")
    print(f"  Prêmio 1.50: {simulador.definir_valor_alavanca('premio', 1.50)}")
    print(f"  Tela 20.00: {simulador.definir_valor_alavanca('tela', 20.00)}")
    print(f"  Dólar 6.00: {simulador.definir_valor_alavanca('dolar', 6.00)}")
    
    # Teste valores inválidos
    print("\nTestando valores inválidos:")
    print(f"  Prêmio 3.00 (>2.50): {simulador.definir_valor_alavanca('premio', 3.00)}")
    print(f"  Prêmio -1.00 (<-0.50): {simulador.definir_valor_alavanca('premio', -1.00)}")
    print(f"  Tela 30.00 (>25.00): {simulador.definir_valor_alavanca('tela', 30.00)}")
    print(f"  Dólar 7.00 (>6.50): {simulador.definir_valor_alavanca('dolar', 7.00)}")

def main():
    """Executa todos os testes"""
    print("SIMULADOR DE ESTRATÉGIA PARA SOJA - TESTES DE VALIDAÇÃO")
    print("=" * 60)
    
    try:
        teste_validacao_ranges()
        teste_cenario_otimista()
        teste_cenario_pessimista()
        teste_cenario_misto()
        
        print("\n" + "=" * 60)
        print("TODOS OS TESTES EXECUTADOS COM SUCESSO!")
        
    except Exception as e:
        print(f"\nERRO DURANTE OS TESTES: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

