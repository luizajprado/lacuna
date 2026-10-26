# -*- coding: utf-8 -*-
# Lacuna x Claude x TouchDesigner — ponte de classificacao
# -------------------------------------------------------------
# Cola este codigo num Text DAT no TouchDesigner (ex.: nomeado "claude_bridge").
# Ele manda um relato/denuncia para a API da Anthropic (Claude) e recebe:
#   - "regiao": qual parte da anomalia aquilo tendencia
#   - "legenda": uma frase critica curta, gerada na hora
#
# Nao usa bibliotecas externas (so a stdlib do Python que vem no TouchDesigner).
#
# COMO USAR no TD:
#   1) Guarde sua API key fora do codigo. Opcoes:
#        - variavel de ambiente ANTHROPIC_API_KEY, ou
#        - um Text DAT chamado "apikey" com a chave na 1a linha.
#   2) Chame de outro DAT/CHOP/execute:
#        res = op('claude_bridge').module.classificar("texto do relato aqui")
#        print(res)  ->  {'regiao': 'boca', 'legenda': '...'}
#   3) Use res['regiao'] para empurrar a particula daquela regiao e
#      res['legenda'] para o texto na tela.
#
# A chamada e SINCRONA (trava por ~1-2s). Para nao travar o render,
# rode num thread (exemplo no fim) ou num Execute DAT disparado por evento.

import json
import os
import urllib.request
import urllib.error

# ------- configuracao -------
MODELO = "claude-sonnet-5-5"   # troque por outro modelo da sua conta se quiser
MAX_TOKENS = 300
ENDPOINT = "https://api.anthropic.com/v1/messages"

# As regioes da anomalia (devem bater com as do visual)
REGIOES = ["olhos", "boca", "rosto", "pescoco", "contorno", "ombros"]

# O que cada regiao representa — dado a Claude para classificar bem
_INSTRUCAO = (
    "Voce analisa um relato anonimo sobre aliciamento de mulheres para "
    "exploracao/trafico, dentro de uma obra de arte critica e especulativa. "
    "NUNCA cite nomes de pessoas. Classifique o relato em UMA destas regioes, "
    "pela caracteristica dominante do aliciamento:\n"
    "- olhos: como a abordam / o primeiro contato\n"
    "- boca: a promessa feita (emprego, vida melhor)\n"
    "- rosto: a fachada de quem alicia (empresa, agencia, pessoa de confianca)\n"
    "- pescoco: o controle sobre o corpo (ameaca, retencao, vigilancia)\n"
    "- contorno: a rota / o deslocamento para fora do territorio\n"
    "- ombros: a divida / o peso economico\n"
    "Responda SO com JSON valido, sem texto fora dele, no formato:\n"
    '{"regiao": "<uma das seis>", "legenda": "<frase critica curta em portugues, '
    "ate 90 caracteres, sobre como o dado tendencia a imagem da vitima-ideal, "
    'sem culpar a vitima>"}'
)


def _get_api_key():
    k = os.environ.get("ANTHROPIC_API_KEY")
    if k:
        return k.strip()
    try:
        d = op('apikey')               # Text DAT chamado "apikey"
        if d is not None:
            return d.text.strip()
    except Exception:
        pass
    raise RuntimeError("API key nao encontrada (env ANTHROPIC_API_KEY ou Text DAT 'apikey').")


def classificar(relato, timeout=20):
    """Manda o relato para Claude e devolve {'regiao':..., 'legenda':...}."""
    relato = (relato or "").strip()
    if len(relato) < 3:
        return {"regiao": "rosto", "legenda": "relato curto demais"}

    api_key = _get_api_key()
    corpo = {
        "model": MODELO,
        "max_tokens": MAX_TOKENS,
        "messages": [
            {"role": "user", "content": _INSTRUCAO + "\n\nRelato:\n" + relato}
        ],
    }
    dados = json.dumps(corpo).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=dados, method="POST")
    req.add_header("x-api-key", api_key)
    req.add_header("anthropic-version", "2023-06-01")
    req.add_header("content-type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            resp = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detalhe = e.read().decode("utf-8", "ignore")[:200]
        return {"regiao": "rosto", "legenda": "erro %s" % e.code, "erro": detalhe}
    except Exception as e:
        return {"regiao": "rosto", "legenda": "sem conexao", "erro": str(e)}

    # Texto da resposta
    txt = ""
    for bloco in resp.get("content", []):
        if bloco.get("type") == "text":
            txt += bloco.get("text", "")
    txt = txt.strip()

    # Parse tolerante do JSON (pega do primeiro { ao ultimo })
    try:
        i, j = txt.find("{"), txt.rfind("}")
        out = json.loads(txt[i:j + 1])
    except Exception:
        return {"regiao": "rosto", "legenda": txt[:90] or "sem resposta"}

    reg = out.get("regiao", "rosto")
    if reg not in REGIOES:
        reg = "rosto"
    leg = (out.get("legenda") or "").strip()[:120]
    return {"regiao": reg, "legenda": leg}


# ------- exemplo nao-bloqueante (opcional) -------
# Rode a classificacao num thread para nao travar o TD; ao terminar,
# escreve o resultado num Table DAT chamado "saida" (regiao | legenda).
def classificar_async(relato, saida_dat="saida"):
    import threading

    def _run():
        res = classificar(relato)
        try:
            t = op(saida_dat)
            t.clear()
            t.appendRow([res.get("regiao", ""), res.get("legenda", "")])
        except Exception as e:
            print("falha ao escrever saida:", e)

    threading.Thread(target=_run, daemon=True).start()


# Teste rapido (rode este DAT com o botao direito > Run):
# print(classificar("vaga de modelo na Europa, passagem paga, melhor nao contar pra familia"))
