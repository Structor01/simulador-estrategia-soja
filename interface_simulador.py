#!/usr/bin/env python3
"""
Interface de linha de comando para o Simulador de Estratégia para Soja
"""

import os
import sys
from typing import List, Optional
from simulador_soja import SimuladorSoja, TipoCenario, TipoEstrategia, ResultadoSimulacao

class InterfaceSimulador:
    """Interface de linha de comando para o simulador"""
    
    def __init__(self):
        self.simulador = SimuladorSoja()
        self.executando = True
    
    def limpar_tela(self):
        """Limpa a tela do terminal"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def exibir_cabecalho(self):
        """Exibe o cabeçalho do simulador"""
        print("=" * 70)
        print("           SIMULADOR DE ESTRATÉGIA PARA SOJA")
        print("=" * 70)
        print()
    
    def exibir_menu_principal(self):
        """Exibe o menu principal"""
        print("MENU PRINCIPAL:")
        print("1. Configurar Alavancas")
        print("2. Definir Cenários")
        print("3. Simular Estratégias")
        print("4. Comparar Estratégias")
        print("5. Exibir Resumo Atual")
        print("6. Salvar/Carregar Configuração")
        print("7. Exemplos Pré-definidos")
        print("0. Sair")
        print()
    
    def obter_opcao(self, prompt: str, opcoes_validas: List[str]) -> str:
        """Obtém uma opção válida do usuário"""
        while True:
            opcao = input(prompt).strip()
            if opcao in opcoes_validas:
                return opcao
            print(f"Opção inválida. Escolha entre: {', '.join(opcoes_validas)}")
    
    def obter_numero(self, prompt: str, minimo: float = None, maximo: float = None) -> float:
        """Obtém um número válido do usuário"""
        while True:
            try:
                valor = float(input(prompt).strip())
                if minimo is not None and valor < minimo:
                    print(f"Valor deve ser maior ou igual a {minimo}")
                    continue
                if maximo is not None and valor > maximo:
                    print(f"Valor deve ser menor ou igual a {maximo}")
                    continue
                return valor
            except ValueError:
                print("Por favor, digite um número válido.")
    
    def configurar_alavancas(self):
        """Menu para configurar valores das alavancas"""
        self.limpar_tela()
        self.exibir_cabecalho()
        print("CONFIGURAÇÃO DE ALAVANCAS")
        print("-" * 30)
        
        for nome, alavanca in self.simulador.alavancas.items():
            print(f"\n{alavanca.nome} ({alavanca.unidade})")
            print(f"Valor atual: {alavanca.valor_atual:.3f}")
            print(f"Range válido: {alavanca.valor_minimo:.2f} a {alavanca.valor_maximo:.2f}")
            
            alterar = self.obter_opcao("Alterar valor? (s/n): ", ["s", "n", "S", "N"])
            if alterar.lower() == 's':
                novo_valor = self.obter_numero(
                    f"Novo valor para {alavanca.nome}: ",
                    alavanca.valor_minimo,
                    alavanca.valor_maximo
                )
                self.simulador.definir_valor_alavanca(nome, novo_valor)
                print(f"✓ {alavanca.nome} atualizado para {novo_valor:.3f}")
        
        input("\nPressione Enter para continuar...")
    
    def definir_cenarios(self):
        """Menu para definir cenários das alavancas"""
        self.limpar_tela()
        self.exibir_cabecalho()
        print("DEFINIÇÃO DE CENÁRIOS")
        print("-" * 25)
        
        for nome, alavanca in self.simulador.alavancas.items():
            print(f"\n{alavanca.nome}")
            print(f"Valor atual: {alavanca.valor_atual:.3f} {alavanca.unidade}")
            print(f"Cenário atual: {alavanca.cenario.value}")
            print(f"Variação atual: {alavanca.variacao_percentual:.1f}%")
            
            print("\nOpções de cenário:")
            print("1. Alta (valores crescentes)")
            print("2. Baixa (valores decrescentes)")
            print("3. Neutro (sem variação)")
            print("4. Manter atual")
            
            opcao = self.obter_opcao("Escolha o cenário: ", ["1", "2", "3", "4"])
            
            if opcao != "4":
                cenarios = {
                    "1": TipoCenario.ALTA,
                    "2": TipoCenario.BAIXA,
                    "3": TipoCenario.NEUTRO
                }
                cenario = cenarios[opcao]
                
                if cenario != TipoCenario.NEUTRO:
                    variacao = self.obter_numero(
                        f"Variação percentual (0-50%): ",
                        0.0, 50.0
                    )
                else:
                    variacao = 0.0
                
                self.simulador.definir_cenario_alavanca(nome, cenario, variacao)
                valor_cenario = self.simulador.calcular_valor_cenario(nome)
                print(f"✓ Cenário definido: {cenario.value} ({variacao:.1f}%)")
                print(f"  Valor no cenário: {valor_cenario:.3f} {alavanca.unidade}")
        
        input("\nPressione Enter para continuar...")
    
    def simular_estrategias(self):
        """Menu para simular estratégias individuais"""
        self.limpar_tela()
        self.exibir_cabecalho()
        print("SIMULAÇÃO DE ESTRATÉGIAS")
        print("-" * 28)
        
        print("Estratégias disponíveis:")
        estrategias = {
            "1": TipoEstrategia.SEM_TRAVAMENTO,
            "2": TipoEstrategia.TRAVAR_DOLAR,
            "3": TipoEstrategia.TRAVAR_SOJA_B3,
            "4": TipoEstrategia.TRAVAR_SOJA_CHICAGO
        }
        
        for key, estrategia in estrategias.items():
            nome_estrategia = estrategia.value.replace("_", " ").title()
            print(f"{key}. {nome_estrategia}")
        
        opcao = self.obter_opcao("\nEscolha a estratégia: ", list(estrategias.keys()))
        estrategia_escolhida = estrategias[opcao]
        
        print(f"\nSimulando: {estrategia_escolhida.value.replace('_', ' ').title()}")
        print("-" * 40)
        
        resultado = self.simulador.simular_estrategia(estrategia_escolhida)
        self.exibir_resultado_detalhado(resultado)
        
        input("\nPressione Enter para continuar...")
    
    def comparar_estrategias(self):
        """Menu para comparar múltiplas estratégias"""
        self.limpar_tela()
        self.exibir_cabecalho()
        print("COMPARAÇÃO DE ESTRATÉGIAS")
        print("-" * 29)
        
        estrategias = [
            TipoEstrategia.SEM_TRAVAMENTO,
            TipoEstrategia.TRAVAR_DOLAR,
            TipoEstrategia.TRAVAR_SOJA_B3,
            TipoEstrategia.TRAVAR_SOJA_CHICAGO
        ]
        
        resultados = self.simulador.comparar_estrategias(estrategias)
        
        print("COMPARAÇÃO DE RESULTADOS:")
        print("=" * 70)
        print(f"{'Estratégia':<20} {'Preço BRL':<12} {'Variação':<10} {'Exposição'}")
        print("-" * 70)
        
        for resultado in resultados:
            nome_estrategia = resultado.estrategia.value.replace("_", " ").title()
            exposicoes = [k for k, v in resultado.exposicao_risco.items() if v]
            exposicao_str = ", ".join(exposicoes) if exposicoes else "Nenhuma"
            
            print(f"{nome_estrategia:<20} "
                  f"R$ {resultado.preco_final_brl:<8.2f} "
                  f"{resultado.variacao_percentual:>6.2f}% "
                  f"{exposicao_str}")
        
        # Encontrar melhor estratégia
        melhor_resultado = max(resultados, key=lambda r: r.preco_final_brl)
        print(f"\n✓ Melhor resultado: {melhor_resultado.estrategia.value.replace('_', ' ').title()}")
        print(f"  Preço: R$ {melhor_resultado.preco_final_brl:.2f}")
        print(f"  Variação: {melhor_resultado.variacao_percentual:.2f}%")
        
        input("\nPressione Enter para continuar...")
    
    def exibir_resultado_detalhado(self, resultado: ResultadoSimulacao):
        """Exibe resultado detalhado de uma simulação"""
        print(f"Estratégia: {resultado.estrategia.value.replace('_', ' ').title()}")
        print(f"Preço final: R$ {resultado.preco_final_brl:.2f} (USD {resultado.preco_final_usd:.2f})")
        print(f"Variação: {resultado.variacao_percentual:.2f}%")
        
        exposicoes = [k for k, v in resultado.exposicao_risco.items() if v]
        print(f"Exposição a risco: {', '.join(exposicoes) if exposicoes else 'Nenhuma'}")
        
        print("\nDetalhes do cálculo:")
        detalhes = resultado.detalhes_calculo
        print(f"  Prêmio no cenário: USD {detalhes['premio_cenario']:.3f}")
        print(f"  Tela no cenário: USD {detalhes['tela_cenario']:.2f}")
        print(f"  Dólar no cenário: R$ {detalhes['dolar_cenario']:.2f}")
        
        if 'dolar_travado' in detalhes:
            print(f"  Dólar travado em: R$ {detalhes['dolar_travado']:.2f}")
        if 'preco_travado_brl' in detalhes:
            print(f"  Preço travado (BRL): R$ {detalhes['preco_travado_brl']:.2f}")
        if 'preco_travado_usd' in detalhes:
            print(f"  Preço travado (USD): USD {detalhes['preco_travado_usd']:.2f}")
    
    def exibir_resumo_atual(self):
        """Exibe resumo da configuração atual"""
        self.limpar_tela()
        self.exibir_cabecalho()
        print("RESUMO DA CONFIGURAÇÃO ATUAL")
        print("-" * 35)
        
        resumo = self.simulador.obter_resumo_alavancas()
        
        for nome, dados in resumo.items():
            print(f"\n{nome.upper()}:")
            print(f"  Valor atual: {dados['valor_atual']:.3f} {dados['unidade']}")
            print(f"  Cenário: {dados['cenario']}")
            print(f"  Variação: {dados['variacao_percentual']:.1f}%")
            print(f"  Valor no cenário: {dados['valor_cenario']:.3f} {dados['unidade']}")
        
        # Calcular preço atual
        preco_usd, preco_brl = self.simulador.calcular_preco_base()
        print(f"\nPREÇO NO CENÁRIO ATUAL:")
        print(f"  USD: {preco_usd:.2f}")
        print(f"  BRL: R$ {preco_brl:.2f}")
        
        input("\nPressione Enter para continuar...")
    
    def salvar_carregar_configuracao(self):
        """Menu para salvar/carregar configurações"""
        self.limpar_tela()
        self.exibir_cabecalho()
        print("SALVAR/CARREGAR CONFIGURAÇÃO")
        print("-" * 33)
        
        print("1. Salvar configuração atual")
        print("2. Carregar configuração")
        print("3. Voltar ao menu principal")
        
        opcao = self.obter_opcao("Escolha uma opção: ", ["1", "2", "3"])
        
        if opcao == "1":
            nome_arquivo = input("Nome do arquivo (sem extensão): ").strip()
            if nome_arquivo:
                arquivo = f"{nome_arquivo}.json"
                try:
                    self.simulador.exportar_configuracao(arquivo)
                    print(f"✓ Configuração salva em {arquivo}")
                except Exception as e:
                    print(f"✗ Erro ao salvar: {e}")
        
        elif opcao == "2":
            nome_arquivo = input("Nome do arquivo (com extensão .json): ").strip()
            if nome_arquivo and os.path.exists(nome_arquivo):
                try:
                    if self.simulador.importar_configuracao(nome_arquivo):
                        print(f"✓ Configuração carregada de {nome_arquivo}")
                    else:
                        print("✗ Erro ao carregar configuração")
                except Exception as e:
                    print(f"✗ Erro ao carregar: {e}")
            else:
                print("✗ Arquivo não encontrado")
        
        if opcao in ["1", "2"]:
            input("\nPressione Enter para continuar...")
    
    def exemplos_predefinidos(self):
        """Menu com exemplos pré-definidos"""
        self.limpar_tela()
        self.exibir_cabecalho()
        print("EXEMPLOS PRÉ-DEFINIDOS")
        print("-" * 23)
        
        print("1. Cenário Otimista (todas as alavancas favoráveis)")
        print("2. Cenário Pessimista (todas as alavancas desfavoráveis)")
        print("3. Cenário Misto (prêmio alto, tela baixa, dólar alto)")
        print("4. Cenário Conservador (variações pequenas)")
        print("5. Voltar ao menu principal")
        
        opcao = self.obter_opcao("Escolha um exemplo: ", ["1", "2", "3", "4", "5"])
        
        if opcao == "5":
            return
        
        # Configurar valores base
        self.simulador.definir_valor_alavanca('premio', 1.00)
        self.simulador.definir_valor_alavanca('tela', 15.00)
        self.simulador.definir_valor_alavanca('dolar', 5.20)
        
        if opcao == "1":  # Otimista
            self.simulador.definir_cenario_alavanca('premio', TipoCenario.ALTA, 20.0)
            self.simulador.definir_cenario_alavanca('tela', TipoCenario.ALTA, 15.0)
            self.simulador.definir_cenario_alavanca('dolar', TipoCenario.ALTA, 10.0)
            print("✓ Cenário Otimista configurado")
            
        elif opcao == "2":  # Pessimista
            self.simulador.definir_cenario_alavanca('premio', TipoCenario.BAIXA, 30.0)
            self.simulador.definir_cenario_alavanca('tela', TipoCenario.BAIXA, 20.0)
            self.simulador.definir_cenario_alavanca('dolar', TipoCenario.BAIXA, 15.0)
            print("✓ Cenário Pessimista configurado")
            
        elif opcao == "3":  # Misto
            self.simulador.definir_cenario_alavanca('premio', TipoCenario.ALTA, 25.0)
            self.simulador.definir_cenario_alavanca('tela', TipoCenario.BAIXA, 10.0)
            self.simulador.definir_cenario_alavanca('dolar', TipoCenario.ALTA, 8.0)
            print("✓ Cenário Misto configurado")
            
        elif opcao == "4":  # Conservador
            self.simulador.definir_cenario_alavanca('premio', TipoCenario.ALTA, 5.0)
            self.simulador.definir_cenario_alavanca('tela', TipoCenario.BAIXA, 3.0)
            self.simulador.definir_cenario_alavanca('dolar', TipoCenario.ALTA, 2.0)
            print("✓ Cenário Conservador configurado")
        
        input("\nPressione Enter para continuar...")
    
    def executar(self):
        """Loop principal da interface"""
        while self.executando:
            self.limpar_tela()
            self.exibir_cabecalho()
            self.exibir_menu_principal()
            
            opcao = self.obter_opcao("Escolha uma opção: ", 
                                   ["0", "1", "2", "3", "4", "5", "6", "7"])
            
            if opcao == "0":
                self.executando = False
                print("\nObrigado por usar o Simulador de Estratégia para Soja!")
                
            elif opcao == "1":
                self.configurar_alavancas()
                
            elif opcao == "2":
                self.definir_cenarios()
                
            elif opcao == "3":
                self.simular_estrategias()
                
            elif opcao == "4":
                self.comparar_estrategias()
                
            elif opcao == "5":
                self.exibir_resumo_atual()
                
            elif opcao == "6":
                self.salvar_carregar_configuracao()
                
            elif opcao == "7":
                self.exemplos_predefinidos()

def main():
    """Função principal"""
    try:
        interface = InterfaceSimulador()
        interface.executar()
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

