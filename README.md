# Simulador de Estratégia para Soja

Um simulador completo em Python para análise de estratégias de trading de soja, permitindo modelar diferentes cenários de mercado através de três alavancas principais: Prêmio, Tela (preço base) e Dólar.

## 🚀 Funcionalidades

### Alavancas de Simulação
- **Prêmio**: Diferencial de preço (-0,50 a 2,50 USD)
- **Tela**: Preço base da soja (10,00 a 25,00 USD/bushel)
- **Dólar**: Taxa de câmbio (4,50 a 6,50 BRL/USD)

### Tipos de Cenário
- **Alta**: Valores crescentes com variação percentual configurável
- **Baixa**: Valores decrescentes com variação percentual configurável
- **Neutro**: Sem variação (valores atuais)

### Estratégias de Trading
1. **Sem Travamento**: Exposição total a todas as variáveis
2. **Travar Dólar**: Elimina risco cambial
3. **Travar Soja B3**: Fixa preço no mercado brasileiro
4. **Travar Soja Chicago**: Fixa preço no mercado internacional

## 📁 Estrutura do Projeto

```
simulador-soja/
├── simulador_soja.py          # Classe principal do simulador
├── interface_simulador.py     # Interface de linha de comando
├── teste_simulacao.py         # Testes de validação
├── demo_simulador.py          # Demonstração completa
├── especificacoes_simulador.md # Documentação técnica
├── todo.md                    # Lista de tarefas do projeto
└── README.md                  # Este arquivo
```

## 🛠️ Instalação e Uso

### Pré-requisitos
- Python 3.7 ou superior
- Nenhuma dependência externa necessária (usa apenas bibliotecas padrão)

### Execução

#### Interface Interativa
```bash
python3 interface_simulador.py
```

#### Demonstração Automática
```bash
python3 demo_simulador.py
```

#### Testes de Validação
```bash
python3 teste_simulacao.py
```

## 📊 Exemplo de Uso

### Uso Programático

```python
from simulador_soja import SimuladorSoja, TipoCenario, TipoEstrategia

# Inicializar simulador
simulador = SimuladorSoja()

# Configurar valores das alavancas
simulador.definir_valor_alavanca('premio', 1.20)
simulador.definir_valor_alavanca('tela', 15.00)
simulador.definir_valor_alavanca('dolar', 5.30)

# Definir cenários
simulador.definir_cenario_alavanca('premio', TipoCenario.ALTA, 15.0)
simulador.definir_cenario_alavanca('tela', TipoCenario.ALTA, 10.0)
simulador.definir_cenario_alavanca('dolar', TipoCenario.BAIXA, 5.0)

# Simular estratégia
resultado = simulador.simular_estrategia(TipoEstrategia.TRAVAR_DOLAR)

print(f"Preço final: R$ {resultado.preco_final_brl:.2f}")
print(f"Variação: {resultado.variacao_percentual:.2f}%")
```

### Interface de Linha de Comando

O simulador oferece uma interface completa com menus interativos:

1. **Configurar Alavancas**: Define valores atuais
2. **Definir Cenários**: Configura expectativas de alta/baixa
3. **Simular Estratégias**: Testa estratégias individuais
4. **Comparar Estratégias**: Analisa múltiplas estratégias
5. **Exibir Resumo**: Mostra configuração atual
6. **Salvar/Carregar**: Gerencia configurações
7. **Exemplos Pré-definidos**: Cenários prontos para teste

## 📈 Exemplos de Cenários

### Cenário Otimista
- Prêmio: +20%
- Tela: +15%
- Dólar: +10%

**Resultado**: Sem travamento oferece maior retorno (26,84% de ganho)

### Cenário Pessimista
- Prêmio: -30%
- Tela: -20%
- Dólar: -15%

**Resultado**: Travar soja B3 oferece melhor proteção (0% de variação)

### Cenário Misto
- Prêmio: +25%
- Tela: -10%
- Dólar: +8%

**Resultado**: Estratégias balanceadas reduzem volatilidade

## 🧮 Fórmulas de Cálculo

### Preço Final
```
Preço_Final_BRL = (Tela_USD + Premio_USD) * Dolar_BRL
```

### Valor no Cenário
```
Valor_Cenario = Valor_Atual * (1 ± Variacao_Percentual/100)
```

### Variação Percentual
```
Variacao = ((Preco_Final - Preco_Atual) / Preco_Atual) * 100
```

## 📋 Funcionalidades Avançadas

### Análise de Risco
- **Exposição por Alavanca**: Identifica quais variáveis afetam cada estratégia
- **Volatilidade**: Calcula desvio padrão entre cenários
- **Matriz de Risco/Retorno**: Compara estratégias em diferentes condições

### Persistência de Dados
- **Exportar Configuração**: Salva cenários em JSON
- **Importar Configuração**: Carrega cenários salvos
- **Histórico de Simulações**: Mantém registro das análises

### Validações
- **Ranges de Valores**: Valida limites das alavancas
- **Consistência de Dados**: Verifica integridade dos cálculos
- **Tratamento de Erros**: Gerencia entradas inválidas

## 🎯 Casos de Uso

### Para Produtores
- Avaliar estratégias de venda antecipada
- Comparar travamentos de preço vs. exposição ao mercado
- Analisar impacto de variações cambiais

### Para Traders
- Modelar cenários de mercado
- Otimizar estratégias de hedge
- Avaliar risco/retorno de posições

### Para Analistas
- Realizar análises de sensibilidade
- Gerar relatórios de cenários
- Comparar estratégias de forma sistemática

## 🔧 Personalização

O simulador é facilmente extensível:

### Adicionar Novas Alavancas
```python
# No arquivo simulador_soja.py
self.alavancas['nova_alavanca'] = Alavanca(
    nome="Nova Alavanca",
    valor_atual=0.0,
    valor_minimo=-10.0,
    valor_maximo=10.0,
    unidade="Unidade"
)
```

### Criar Novas Estratégias
```python
# Adicionar ao enum TipoEstrategia
NOVA_ESTRATEGIA = "nova_estrategia"

# Implementar lógica no método simular_estrategia()
elif estrategia == TipoEstrategia.NOVA_ESTRATEGIA:
    # Lógica personalizada
    pass
```

## 📊 Resultados da Demonstração

A demonstração automática (`demo_simulador.py`) mostra:

- **Cenário Otimista**: Ganho de até 21,21% sem travamento
- **Cenário Pessimista**: Proteção total com travamento B3
- **Análise de Volatilidade**: Travamento reduz risco de 16,85 para 0,00
- **Recomendações**: Estratégias adaptadas a cada tipo de cenário

## 🤝 Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Implemente as mudanças
4. Execute os testes de validação
5. Submeta um pull request

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Suporte

Para dúvidas ou sugestões, abra uma issue no repositório GitHub.

---

**Desenvolvido para análise profissional de estratégias de trading de soja** 🌱

