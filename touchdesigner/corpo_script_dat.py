# Lacuna - corpo da anomalia (gerado por dados, com linhagem das Venus antigas)
# Cole este codigo DENTRO de um Script DAT no TouchDesigner.
# Ele gera a nuvem de pontos de um corpo feminino inteiro, por metaballs.
#
# NOVO: parametro VENUS (0..1). Em 0 a figura e um corpo "contemporaneo";
# em 1 ela colapsa na forma das Venus paleoliticas (Willendorf, Lespugue):
# seios, ventre e quadril inflam, membros e cabeca encolhem, o rosto se apaga.
# A ideia: quanto MAIS os dados essencializam a vitima, mais a anomalia
# vira um idolo sem rosto - a vitima-ideal fabricada, como a Venus foi
# fabricada como ideal do feminino/fertilidade.
#
# Ligue VENUS a um CHOP depois (ex.: media dos pesos / nivel de estereotipia).
# Colunas: tx ty tz r g b scale reg order
#   reg = regiao (0 cabeca/olhos, 1 boca, 2 rosto, 3 tronco, 4 quadril/pernas, 5 bracos)
#   order = ordem de surgimento (0..1) para a figura se montar aos poucos

import math, random

N = 5000

# ---- quanto a figura pende para a Venus antiga (0..1) ----
# Troque por um valor vindo de CHOP:  VENUS = op('venus')[0] or 0.0
VENUS = 0.0

# Esferas do corpo: (x, y, z, raio_base, regiao, venus_mult)
# venus_mult: quanto o raio cresce(>1) ou encolhe(<1) quando VENUS=1
BALLS = [
    (0.00, 1.78, 0.00, 0.15, 0, 0.55),   # cabeca  -> encolhe
    (0.00, 1.80, 0.07, 0.10, 0, 0.45),   # testa/olhos
    (0.00, 1.66, 0.09, 0.07, 1, 0.45),   # boca
    (0.00, 1.60, 0.00, 0.07, 0, 0.70),   # pescoco
    (-0.20, 1.50, 0.0, 0.11, 5, 0.70),   # ombro E
    (0.20, 1.50, 0.0, 0.11, 5, 0.70),    # ombro D
    (0.00, 1.38, 0.0, 0.19, 3, 1.15),    # peito
    (-0.09, 1.34, 0.11, 0.08, 3, 1.85),  # seio E  -> infla
    (0.09, 1.34, 0.11, 0.08, 3, 1.85),   # seio D  -> infla
    (0.00, 1.16, 0.05, 0.14, 3, 1.95),   # ventre  -> infla forte
    (0.00, 1.14, 0.0, 0.15, 3, 1.25),    # cintura
    (0.00, 0.94, 0.0, 0.24, 4, 1.65),    # quadril -> infla
    (-0.11, 0.66, 0.0, 0.14, 4, 1.25),   # coxa E
    (0.11, 0.66, 0.0, 0.14, 4, 1.25),    # coxa D
    (-0.11, 0.40, 0.0, 0.10, 4, 0.75),   # joelho E -> afina
    (0.11, 0.40, 0.0, 0.10, 4, 0.75),    # joelho D
    (-0.11, 0.12, 0.02, 0.09, 4, 0.60),  # panturrilha E -> some
    (0.11, 0.12, 0.02, 0.09, 4, 0.60),   # panturrilha D
    (-0.30, 1.34, 0.0, 0.09, 5, 0.60),   # braco E -> encolhe (Venus quase sem bracos)
    (0.30, 1.34, 0.0, 0.09, 5, 0.60),    # braco D
    (-0.34, 1.10, 0.0, 0.08, 5, 0.50),   # antebraco E
    (0.34, 1.10, 0.0, 0.08, 5, 0.50),    # antebraco D
    (-0.36, 0.88, 0.0, 0.07, 5, 0.45),   # mao E
    (0.36, 0.88, 0.0, 0.07, 5, 0.45),    # mao D
]

EYES = [(-0.11, 1.80, 0.17), (0.11, 1.80, 0.17)]
MOUTH = (0.0, 1.66, 0.19)

def _r(base, vmult, v):
    # raio interpolado entre contemporaneo (v=0) e Venus (v=1)
    return base * (1.0 + (vmult - 1.0) * v)

def field(x, y, z, v):
    f = 0.0
    for bx, by, bz, base, _, vm in BALLS:
        r = _r(base, vm, v)
        dx, dy, dz = x-bx, y-by, z-bz
        f += r*r / (dx*dx + dy*dy + dz*dz + 6e-4)
    return f

def nearest_reg(x, y, z, v):
    best, bd = 3, 1e9
    for bx, by, bz, base, reg, vm in BALLS:
        d = (x-bx)**2 + (y-by)**2 + (z-bz)**2
        if d < bd:
            bd, best = d, reg
    # olhos e boca na frente da cabeca — SE a figura ainda tem rosto.
    # Quanto maior VENUS, mais o rosto se apaga (menos pontos viram rosto).
    rosto_ativo = (1.0 - v) > 0.35
    if z > 0.05 and rosto_ativo:
        for ex, ey, ez in EYES:
            if (x-ex)**2 + (y-ey)**2 + (z-ez)**2 < 0.004:
                return 0
        if (x-MOUTH[0])**2 + (y-MOUTH[1])**2 + (z-MOUTH[2])**2 < 0.004:
            return 1
    return best

def onCook(scriptOp):
    # le VENUS de um CHOP 'venus' se existir; senao usa a constante acima
    v = VENUS
    try:
        c = op('venus')
        if c is not None:
            v = float(c[0])
    except Exception:
        pass
    v = max(0.0, min(1.0, v))

    scriptOp.clear()
    scriptOp.appendRow(['tx', 'ty', 'tz', 'r', 'g', 'b', 'scale', 'reg', 'order'])
    rng = random.Random(20261026)
    got = 0
    tries = 0
    while got < N and tries < N*60:
        tries += 1
        x = -0.5 + rng.random()*1.0
        y = rng.random()*1.95
        z = -0.28 + rng.random()*0.56
        f = field(x, y, z, v)
        if f < 1.1 or f > 1.7:      # casca (superficie), nao preenchido
            continue
        reg = nearest_reg(x, y, z, v)
        g = 0.82 + rng.random()*0.18          # tom claro
        sc = 0.7 + rng.random()*0.5
        if reg in (0, 1):
            sc *= 1.15
        scriptOp.appendRow([round(x,4), round(y,4), round(z,4),
                            round(g,3), round(g*0.98,3), round(g*0.95,3),
                            round(sc,3), reg, round(rng.random(),4)])
        got += 1
    return
