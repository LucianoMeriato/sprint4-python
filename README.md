# sprint4-python


Contexto do problema

Planejar pedidos diários de insumos com capacidade de estoque limitada, custo de compra, penalidade por falta e, opcionalmente, custo de armazenagem. Objetivo: minimizar o custo total ao longo do horizonte.

Estruturas do modelo e justificativas
Estado

O que é: s_i = estoque disponível no início do dia i, com domínio discreto 0..S_MAX.

Onde no código: argumento s das funções de valor; linhas que indexam DP[i][s].

Por que assim: estoque é a informação mínima suficiente para decidir o próximo pedido dado d_i. Manter o estado minimal evita explosão combinatória e torna o Bellman bem-definido.

Decisão

O que é: q_i ∈ {0..Q_MAX} com restrição s_i + q_i ≤ S_MAX.

Onde no código: laços for q in range(P.Q_MAX + 1) nas duas DPs.

Por que assim: decisões discretas refletem lotes unitários ou pequenos, simplificam análise e impressão de política. O limite Q_MAX controla o espaço de ação e reforça cenários de reposição gradual.

Função de transição

O que é:
s_pre = min(S_MAX, s_i + q_i)
falta_i = max(0, d_i − s_pre)
s_{i+1} = max(0, s_pre − d_i)

Onde no código: transicao(...).

Por que assim: captura capacidade, atendimento da demanda e cálculo de faltas sem backorder. Escolha propositalmente didática: uma linha por efeito (chegada do pedido, atendimento, sobra).

Função objetivo

O que é: custo_i = c·q_i + p·falta_i + h·s_{i+1} e minimizar Σ custo_i.

Onde no código: custo_dia(...).

Por que assim: custo linear é o padrão em DP de inventário básica; p alto força evitar falta, h permite penalizar estoques altos quando necessário.

Parâmetros configuráveis

O que é: Params(c, p, h, S_MAX, Q_MAX) via @dataclass.

Onde no código: Params.

Por que assim: centraliza hiperparâmetros, facilita experimentos e deixa o script legível.

Algoritmos e justificativas
DP recursiva com memoization (top-down)

O que faz: avalia a equação de Bellman V(i, s) e memoriza resultados.

Onde no código: dp_recursiva_memo, função interna V com @lru_cache.

Como usa as estruturas: itera sobre q, aplica transicao, soma custo_dia e chama V(i+1, s_next).

Por que usar: espelha diretamente a formulação matemática, é curta, didática e evita recomputações graças à memoização. Boa para explicar a lógica da PD.

DP iterativa (bottom-up)

O que faz: preenche tabela DP[i][s] de trás para frente e guarda choice[i][s].

Onde no código: dp_bottom_up.

Como usa as estruturas: para cada (i,s), testa q, usa transicao e custo_dia, escolhe o mínimo e registra a decisão.

Por que usar: mostra a tabela de valor, tem controle explícito de memória/tempo e é base para extensões com novas restrições. Combina com a exigência de “versão iterativa”.

Reconstrução da política

O que faz: gera, para cada dia, pedido, falta, estoque_in/out, custo_dia.

Onde no código: blocos “Reconstrução” em ambas as DPs, produzindo politica: Dict[int, Dict].

Por que usar: transforma números da DP em plano operacional auditável, útil para relatório e validação.

Verificação de equivalência

O que faz: compara custos totais e sequência de pedidos das duas DPs.

Onde no código: assert rec_custo == it_custo e checagem dos pedido.

Por que usar: garante correção e cumpre a rubrica “mesmos resultados”.

Estruturas de dados e por que foram escolhidas

@dataclass Params: evita dicionários soltos, melhora leitura e muda parâmetros sem efeitos colaterais.

Matriz DP e choice: estruturas padrão em bottom-up; permitem reconstrução determinística.

dict para politica: formato autoexplicativo e pronto para impressão/CSV.

Inteiros para custos: evita ruídos de ponto flutuante em validação com assert.

Complexidade e trade-offs

Tempo: O(n · (S_MAX+1) · (Q_MAX+1)) em ambas as DPs.

Memória: top-down proporcional ao número de estados visitados; bottom-up usa O(n · (S_MAX+1)).

Trade-off: top-down é mais sucinta e visita apenas estados necessários; bottom-up é previsível e mais fácil de estender com novas restrições.

Decisões de modelagem e justificativas

Demanda determinística por dia: encaixa no enunciado e foca a técnica de DP. Probabilístico seria outro escopo.

Sem backorder: “falta” penaliza não atendidos no dia, que é a métrica típica de desperdício/ruptura na área de saúde.

Capacidade S_MAX e limite de pedido Q_MAX: reproduzem restrições físicas/logísticas e mantêm o espaço de busca controlado.

Custo de armazenagem opcional (h): permite comparar cenários com e sem pressão por reduzir estoque.

Política imprimível por dia: atende visibilidade de consumo e facilita auditoria.







**MEMBROS**
Pietro Vitor Pezzente - RM557284
Luciano Henrique Meriato Junior - RM554546
Vinicius Henrique - RM556908
Eric Darakjian - RM557082
Enzo Vinicius – RM558225
