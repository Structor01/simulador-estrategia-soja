#!/usr/bin/env python3
"""
Simulador de Estratégia para Soja
Desenvolvido para análise de cenários com três alavancas: Prêmio, Tela e Dólar
"""

import json
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum

class TipoCenario(Enum):
    """Tipos de cenário para cada alavanca"""
    ALTA = "alta"
    BAIXA = "baixa"
    NEUTRO = "neutro"

class TipoEstrategia(Enum):
    """Tipos de estratégia de travamento"""
    SEM_TRAVAMENTO = "sem_travamento"
    TRAVAR_DOLAR = "travar_dolar"
    TRAVAR_SOJA_B3 = "travar_soja_b3"
    TRAVAR_SOJA_CHICAGO = "travar_soja_chicago"
    ESTRATEGIA_COMBINADA = "estrategia_combinada"

@dataclass
class Alavanca:
    """Representa uma alavanca do simulador"""
    nome: str
    valor_atual: float
    valor_minimo: float
    valor_maximo: float
    unidade: str
    cenario: TipoCenario = TipoCenario.NEUTRO
    variacao_percentual: float = 0.0

@dataclass
class ResultadoSimulacao:
    """Resultado de uma simulação"""
    estrategia: TipoEstrategia
    preco_final_brl: float
    preco_final_usd: float
    variacao_percentual: float
    exposicao_risco: Dict[str, bool]
    detalhes_calculo: Dict[str, float]

class SimuladorSoja:
    """Simulador principal para estratégias de soja"""
    
    def __init__(self):
        """Inicializa o simulador com valores padrão"""
        self.alavancas = {
            'premio': Alavanca(
                nome="Prêmio",
                valor_atual=0.0,
                valor_minimo=-0.50,
                valor_maximo=2.50,
                unidade="USD/bushel"
            ),
            'tela': Alavanca(
                nome="Tela (Preço Base)",
                valor_atual=15.00,
                valor_minimo=10.00,
                valor_maximo=25.00,
                unidade="USD/bushel"
            ),
            'dolar': Alavanca(
                nome="Dólar",
                valor_atual=5.20,
                valor_minimo=4.50,
                valor_maximo=6.50,
                unidade="BRL/USD"
            )
        }
        
        self.preco_referencia_brl = 0.0
        self.historico_simulacoes = []
    
    def definir_valor_alavanca(self, nome_alavanca: str, valor: float) -> bool:
        """Define o valor atual de uma alavanca"""
        if nome_alavanca not in self.alavancas:
            return False
        
        alavanca = self.alavancas[nome_alavanca]
        if alavanca.valor_minimo <= valor <= alavanca.valor_maximo:
            alavanca.valor_atual = valor
            return True
        return False
    
    def definir_cenario_alavanca(self, nome_alavanca: str, cenario: TipoCenario, variacao_percentual: float = 0.0) -> bool:
        """Define o cenário e variação percentual de uma alavanca"""
        if nome_alavanca not in self.alavancas:
            return False
        
        alavanca = self.alavancas[nome_alavanca]
        alavanca.cenario = cenario
        alavanca.variacao_percentual = variacao_percentual
        return True
    
    def calcular_valor_cenario(self, nome_alavanca: str) -> float:
        """Calcula o valor da alavanca considerando o cenário definido"""
        alavanca = self.alavancas[nome_alavanca]
        valor_base = alavanca.valor_atual
        
        if alavanca.cenario == TipoCenario.ALTA:
            return valor_base * (1 + alavanca.variacao_percentual / 100)
        elif alavanca.cenario == TipoCenario.BAIXA:
            return valor_base * (1 - alavanca.variacao_percentual / 100)
        else:  # NEUTRO
            return valor_base
    
    def calcular_preco_base(self) -> Tuple[float, float]:
        """Calcula preço base em USD e BRL considerando os cenários"""
        premio_cenario = self.calcular_valor_cenario('premio')
        tela_cenario = self.calcular_valor_cenario('tela')
        dolar_cenario = self.calcular_valor_cenario('dolar')
        
        preco_usd = tela_cenario + premio_cenario
        preco_brl = preco_usd * dolar_cenario
        
        return preco_usd, preco_brl
    
    def simular_estrategia(self, estrategia: TipoEstrategia, **kwargs) -> ResultadoSimulacao:
        """Simula uma estratégia específica"""
        preco_usd_base, preco_brl_base = self.calcular_preco_base()
        
        # Valores atuais (sem cenário) para comparação
        preco_atual_usd = self.alavancas['tela'].valor_atual + self.alavancas['premio'].valor_atual
        preco_atual_brl = preco_atual_usd * self.alavancas['dolar'].valor_atual
        
        exposicao_risco = {
            'premio': True,
            'tela': True,
            'dolar': True
        }
        
        preco_final_usd = preco_usd_base
        preco_final_brl = preco_brl_base
        
        detalhes_calculo = {
            'premio_cenario': self.calcular_valor_cenario('premio'),
            'tela_cenario': self.calcular_valor_cenario('tela'),
            'dolar_cenario': self.calcular_valor_cenario('dolar'),
            'preco_usd_base': preco_usd_base,
            'preco_brl_base': preco_brl_base
        }
        
        if estrategia == TipoEstrategia.TRAVAR_DOLAR:
            # Trava o dólar no valor atual
            preco_final_brl = preco_usd_base * self.alavancas['dolar'].valor_atual
            exposicao_risco['dolar'] = False
            detalhes_calculo['dolar_travado'] = self.alavancas['dolar'].valor_atual
            
        elif estrategia == TipoEstrategia.TRAVAR_SOJA_B3:
            # Trava o preço em reais
            preco_final_brl = preco_atual_brl
            preco_final_usd = preco_final_brl / self.calcular_valor_cenario('dolar')
            exposicao_risco['premio'] = False
            exposicao_risco['tela'] = False
            detalhes_calculo['preco_travado_brl'] = preco_atual_brl
            
        elif estrategia == TipoEstrategia.TRAVAR_SOJA_CHICAGO:
            # Trava o preço em dólares
            preco_final_usd = preco_atual_usd
            preco_final_brl = preco_final_usd * self.calcular_valor_cenario('dolar')
            exposicao_risco['premio'] = False
            exposicao_risco['tela'] = False
            detalhes_calculo['preco_travado_usd'] = preco_atual_usd
        
        # Calcula variação percentual em relação ao preço atual
        variacao_percentual = ((preco_final_brl - preco_atual_brl) / preco_atual_brl) * 100
        
        resultado = ResultadoSimulacao(
            estrategia=estrategia,
            preco_final_brl=preco_final_brl,
            preco_final_usd=preco_final_usd,
            variacao_percentual=variacao_percentual,
            exposicao_risco=exposicao_risco,
            detalhes_calculo=detalhes_calculo
        )
        
        self.historico_simulacoes.append(resultado)
        return resultado
    
    def comparar_estrategias(self, estrategias: List[TipoEstrategia]) -> List[ResultadoSimulacao]:
        """Compara múltiplas estratégias"""
        resultados = []
        for estrategia in estrategias:
            resultado = self.simular_estrategia(estrategia)
            resultados.append(resultado)
        return resultados
    
    def obter_resumo_alavancas(self) -> Dict:
        """Retorna resumo atual das alavancas"""
        resumo = {}
        for nome, alavanca in self.alavancas.items():
            resumo[nome] = {
                'valor_atual': alavanca.valor_atual,
                'valor_cenario': self.calcular_valor_cenario(nome),
                'cenario': alavanca.cenario.value,
                'variacao_percentual': alavanca.variacao_percentual,
                'unidade': alavanca.unidade
            }
        return resumo
    
    def exportar_configuracao(self, arquivo: str):
        """Exporta configuração atual para arquivo JSON"""
        config = {
            'alavancas': {},
            'historico_simulacoes': []
        }
        
        for nome, alavanca in self.alavancas.items():
            config['alavancas'][nome] = {
                'valor_atual': alavanca.valor_atual,
                'cenario': alavanca.cenario.value,
                'variacao_percentual': alavanca.variacao_percentual
            }
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def importar_configuracao(self, arquivo: str):
        """Importa configuração de arquivo JSON"""
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            for nome, dados in config['alavancas'].items():
                if nome in self.alavancas:
                    self.definir_valor_alavanca(nome, dados['valor_atual'])
                    cenario = TipoCenario(dados['cenario'])
                    self.definir_cenario_alavanca(nome, cenario, dados['variacao_percentual'])
            
            return True
        except Exception as e:
            print(f"Erro ao importar configuração: {e}")
            return False

if __name__ == "__main__":
    # Teste básico da estrutura
    simulador = SimuladorSoja()
    print("Simulador de Estratégia para Soja inicializado com sucesso!")
    print(f"Alavancas disponíveis: {list(simulador.alavancas.keys())}")

