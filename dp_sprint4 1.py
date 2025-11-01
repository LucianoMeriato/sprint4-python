from dataclasses import dataclass
from functools import lru_cache
from typing import List, Dict, Tuple

@dataclass
class Params:
    c: int = 1
    p: int = 5
    h: int = 0
    S_MAX: int = 5
    Q_MAX: int = 1

def transicao(estoque: int, pedido: int, demanda: int, S_MAX: int) -> Tuple[int, int]:
    s_pre = min(S_MAX, estoque + pedido)
    falta = max(0, demanda - s_pre)
    s_next = max(0, s_pre - demanda)
    return s_next, falta

def custo_dia(pedido: int, falta: int, s_next: int, P: Params) -> int:
    return P.c * pedido + P.p * falta + P.h * s_next

def dp_recursiva_memo(dem: List[int], S0: int, P: Params) -> Tuple[int, Dict[int, Dict]]:
    n = len(dem)

    @lru_cache(maxsize=None)
    def V(i: int, s: int) -> Tuple[int, int]:
        if i == n:
            return (0, 0)
        melhor_custo = 10**12
        melhor_q = 0
        for q in range(P.Q_MAX + 1):
            if s + q > P.S_MAX:
                continue
            s_next, falta = transicao(s, q, dem[i], P.S_MAX)
            total = custo_dia(q, falta, s_next, P) + V(i + 1, s_next)[0]
            if total < melhor_custo:
                melhor_custo, melhor_q = total, q
        return (melhor_custo, melhor_q)

    politica: Dict[int, Dict] = {}
    s = min(S0, P.S_MAX)
    custo_total, _ = V(0, s)
    for i in range(n):
        _, q = V(i, s)
        s_next, falta = transicao(s, q, dem[i], P.S_MAX)
        politica[i] = {
            "dia": i, "estoque_in": s, "demanda": dem[i],
            "pedido": q, "falta": falta, "estoque_out": s_next,
            "custo_dia": custo_dia(q, falta, s_next, P),
        }
        s = s_next
    return custo_total, politica

def dp_bottom_up(dem: List[int], S0: int, P: Params) -> Tuple[int, Dict[int, Dict]]:
    n = len(dem)
    INF = 10**12
    DP = [[INF] * (P.S_MAX + 1) for _ in range(n + 1)]
    choice = [[0] * (P.S_MAX + 1) for _ in range(n)]
    for s in range(P.S_MAX + 1):
        DP[n][s] = 0
    for i in range(n - 1, -1, -1):
        for s in range(P.S_MAX + 1):
            melhor, melhor_q = INF, 0
            for q in range(P.Q_MAX + 1):
                if s + q > P.S_MAX:
                    continue
                s_next, falta = transicao(s, q, dem[i], P.S_MAX)
                total = custo_dia(q, falta, s_next, P) + DP[i + 1][s_next]
                if total < melhor:
                    melhor, melhor_q = total, q
            DP[i][s] = melhor
            choice[i][s] = melhor_q
    politica: Dict[int, Dict] = {}
    s = min(S0, P.S_MAX)
    custo_total = DP[0][s]
    for i in range(n):
        q = choice[i][s]
        s_next, falta = transicao(s, q, dem[i], P.S_MAX)
        politica[i] = {
            "dia": i, "estoque_in": s, "demanda": dem[i],
            "pedido": q, "falta": falta, "estoque_out": s_next,
            "custo_dia": custo_dia(q, falta, s_next, P),
        }
        s = s_next
    return custo_total, politica

def imprime_tabela(politica: Dict[int, Dict], custo_total: int, titulo: str = "") -> None:
    if titulo:
        print(f"\n== {titulo} ==")
    print("dia | Ein | dem | ped | falta | Eout | custo")
    for i in politica:
        r = politica[i]
        print(f"{r['dia']:>3} | {r['estoque_in']:>3} | {r['demanda']:>3} | {r['pedido']:>3} | {r['falta']:>5} | {r['estoque_out']:>4} | {r['custo_dia']:>5}")
    print(f"--> CUSTO TOTAL: {custo_total}")

if __name__ == "__main__":
    demandas = [0, 2, 0, 1, 3]
    S0 = 0
    P = Params(c=1, p=5, h=0, S_MAX=5, Q_MAX=1)
    rec_custo, rec_pol = dp_recursiva_memo(demandas, S0, P)
    it_custo, it_pol = dp_bottom_up(demandas, S0, P)
    assert rec_custo == it_custo
    for k in rec_pol:
        assert rec_pol[k]["pedido"] == it_pol[k]["pedido"]
    print("Parâmetros:", P)
    print("Demandas :", demandas)
    print(f"Estoque inicial (S0): {S0}")
    imprime_tabela(rec_pol, rec_custo, "Política Ótima (validada)")
