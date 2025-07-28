# Especificações do Simulador de Estratégia para Soja

## Visão Geral
Simulador para análise de estratégias de trading de soja com três alavancas principais que permitem modelar diferentes cenários de mercado.

## Alavancas Principais

### 1. Prêmio
- **Descrição**: Diferencial de preço da soja em relação ao mercado de referência
- **Range**: -0,50 a 2,50 dólares
- **Unidade**: USD por bushel ou saca
- **Cenários**: Alta (valores positivos crescentes) / Baixa (valores negativos ou decrescentes)

### 2. Tela (Preço Base)
- **Descrição**: Preço base da soja no mercado de referência
- **Unidade**: USD por bushel
- **Cenários**: Alta (preços crescentes) / Baixa (preços decrescentes)
- **Fonte**: Pode ser baseado em Chicago (CBOT) ou B3

### 3. Dólar
- **Descrição**: Taxa de câmbio USD/BRL
- **Unidade**: Reais por dólar
- **Cenários**: Alta (dólar se valorizando) / Baixa (dólar se desvalorizando)
- **Impacto**: Afeta diretamente a conversão de preços para o mercado brasileiro

## Estratégias Disponíveis

### 1. Travamento de Dólar
- **Descrição**: Fixar a taxa de câmbio para eliminar risco cambial
- **Aplicação**: Útil quando se espera volatilidade cambial
- **Resultado**: Preços em reais ficam estáveis independente da variação do dólar

### 2. Travamento de Soja Futura B3
- **Descrição**: Fixar preço da soja no mercado brasileiro
- **Aplicação**: Proteção contra queda de preços no mercado doméstico
- **Resultado**: Preço garantido em reais

### 3. Travamento de Soja Futura Chicago
- **Descrição**: Fixar preço da soja no mercado internacional (CBOT)
- **Aplicação**: Proteção baseada no mercado de referência global
- **Resultado**: Preço garantido em dólares (sujeito a variação cambial se não travado)

### 4. Estratégia Combinada
- **Descrição**: Combinação de travamentos parciais
- **Aplicação**: Diversificação de riscos
- **Resultado**: Exposição controlada a diferentes variáveis

## Cálculos e Fórmulas

### Preço Final em Reais
```
Preço_Final_BRL = (Tela_USD + Premio_USD) * Dolar_BRL
```

### Cenários de Simulação
- **Cenário Otimista**: Todas as alavancas favoráveis
- **Cenário Pessimista**: Todas as alavancas desfavoráveis  
- **Cenários Mistos**: Combinações variadas de alta/baixa

### Análise de Resultado
- **Comparação**: Preço final vs. preço atual
- **Variação**: Percentual de ganho/perda
- **Risco**: Exposição a cada variável

## Funcionalidades do Simulador

1. **Entrada de Dados**
   - Valores atuais das três alavancas
   - Definição de cenários (alta/baixa) para cada alavanca
   - Percentuais de variação esperados

2. **Simulação de Estratégias**
   - Seleção de tipo de travamento
   - Cálculo de resultados para diferentes cenários
   - Comparação entre estratégias

3. **Análise de Resultados**
   - Tabela comparativa de cenários
   - Gráficos de sensibilidade (se implementado)
   - Recomendações baseadas nos resultados

4. **Relatórios**
   - Resumo executivo da análise
   - Detalhamento dos cálculos
   - Matriz de risco/retorno

