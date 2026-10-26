# -*- coding: utf-8 -*-
# Lacuna — ponte coleta -> TouchDesigner
# ------------------------------------------------------------------
# Busca os numeros da coleta (planilha via Apps Script) e escreve dentro do TD.
# Cole num Text DAT chamado "lacuna_poll".
#
# O QUE ELE CRIA (em Table DATs, que viram CHOP depois):
#   op('coleta')   -> hist antr soc venus total   (1 linha de valores)
#   op('pesoreg')  -> peso por regiao do corpo (6 linhas, reg 0..5)
#
# COMO DISPARAR (a cada ~5s, sem travar o render):
#   Opcao simples — um DAT Execute com onFrameStart:
#     def onFrameStart(frame):
#         if frame % 300 == 0:              # ~5s a 60fps
#             op('lacuna_poll').module.atualizar()
#         return
#
# ENDEREItO DO ENDPOINT:
#   defina URL abaixo, OU crie um Text DAT chamado "endpoint" com a URL /exec.

import json, urllib.request, threading

URL = ""   # cole aqui a URL que termina em /exec (ou use o Text DAT 'endpoint')

# regiao do corpo -> camada que a alimenta
#   0 cabeca/olhos, 1 boca, 2 rosto -> antropologica
#   3 tronco/ventre                 -> historica
#   4 quadril/pernas                -> social
#   5 bracos                        -> estrutural (media)
REG_CAMADA = ['antr', 'antr', 'antr', 'hist', 'soc', 'mix']


def _url():
    if URL:
        return URL.strip()
    try:
        d = op('endpoint')
        if d is not None and d.text.strip():
            return d.text.strip()
    except Exception:
        pass
    return ""


def _aplicar(d):
    hist = float(d.get('hist', 0)); antr = float(d.get('antr', 0))
    soc = float(d.get('soc', 0)); venus = float(d.get('venus', 0))
    total = float(d.get('total', 0))

    # tabela de valores -> vira CHOP com "DAT to CHOP" (First Row is Names)
    t = op('coleta')
    if t is not None:
        t.clear()
        t.appendRow(['hist', 'antr', 'soc', 'venus', 'total'])
        t.appendRow([hist, antr, soc, venus, total])

    # peso por camada, normalizado pela camada mais forte (0..1)
    mx = max(hist, antr, soc, 1.0)
    w = {'hist': hist / mx, 'antr': antr / mx, 'soc': soc / mx}
    w['mix'] = (w['hist'] + w['soc']) / 2.0

    # peso por regiao (6 linhas, na ordem reg 0..5)
    p = op('pesoreg')
    if p is not None:
        p.clear()
        p.appendRow(['w'])
        for cam in REG_CAMADA:
            p.appendRow([round(w[cam], 4)])


def _run():
    u = _url()
    if not u:
        print('lacuna: defina a URL do endpoint (URL ou Text DAT "endpoint")')
        return
    try:
        with urllib.request.urlopen(u, timeout=15) as r:
            d = json.loads(r.read().decode('utf-8'))
    except Exception as e:
        print('lacuna: erro ao buscar coleta:', e)
        return
    _aplicar(d)


def atualizar():
    """Busca a coleta num thread para nao travar o render."""
    threading.Thread(target=_run, daemon=True).start()


# teste manual: botao direito no DAT > Run, depois:
# op('lacuna_poll').module.atualizar()
