# A coleta em tempo real

## Hoje (sem backend)
O site funciona sozinho:
- **fluxo ambiente**: fragmentos de contexto simulados chegam ao vivo, para a obra nunca ficar parada;
- **testemunhos reais**: o formulário anônimo classifica o relato numa das três camadas, mostra na
  figura na hora e guarda no `localStorage` do navegador (fica só naquele navegador, de forma anônima).

Isso já basta para instalação/demonstração. Para acumular testemunhos de vários navegadores num
lugar só, ligue um backend.

## Ligando um backend real (quando quiser)
O caminho pronto é o **Google Apps Script** em `backend/apps-script/Codigo.gs` — ele grava os
testemunhos numa planilha sua. Siga o passo a passo no topo daquele arquivo; ao final você copia a
URL que termina em `/exec` e cola em `site/config.js`:

```js
window.LACUNA_ENDPOINT = "https://script.google.com/macros/s/XXXX/exec";
```

O site então envia cada testemunho como `POST` (text/plain, sem preflight CORS) com o corpo abaixo.

Corpo enviado:
```json
{
  "ts": "2026-10-26T20:44:00.000Z",
  "contexto": "texto anônimo com as palavras da pessoa",
  "origem": "app de relacionamento",
  "camada": "soc",
  "anexo": "print.png"
}
```

Opções simples de endpoint (todas gratuitas para baixo volume), a escolher depois:
- um **Google Apps Script** publicado como web app, escrevendo numa planilha;
- um **form service** (Formspree, Basin) que manda por e-mail;
- uma **serverless function** (Cloudflare Workers, Vercel) gravando num banco.

O anexo (print/e-mail) hoje fica só no navegador. Para guardar a imagem de verdade é preciso um
backend com storage — dá para somar depois, sem mudar o site.

## A classificação pela Claude (TouchDesigner)
No TouchDesigner, `touchdesigner/lacuna_claude_td.py` manda o texto do relato para a API da Anthropic
e recebe de volta a **camada** e uma **legenda crítica**. É o "escultor" fazendo o enviesamento na
frente do público. Guarde a chave fora do código (variável de ambiente `ANTHROPIC_API_KEY` ou um
Text DAT chamado `apikey`).
