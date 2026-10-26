# Lacuna

**Uma obra de arte-pesquisa especulativa e crítica sobre o aliciamento e tráfico de mulheres.**
Autoria: Luiza Jesus do Prado.

Lacuna não mostra uma vítima real. Ela mostra a **vítima-ideal**: um corpo fabricado por
camadas de contexto e fundido por um **algoritmo enviesado**. A tese da obra é que o dado —
as denúncias, os registros, as estatísticas — não revela quem é a vítima; ele a **inventa**,
repetindo o preconteito de quem denuncia e de quem registra. A escultura é esse estereótipo
tomando forma.

A figura é sempre a **vítima**, nunca o aliciador.

## As quatro camadas

A anomalia (o corpo) é esculpida por quatro camadas. As três primeiras entram como dado;
a quarta é o motor que funde tudo.

| camada | o que é | região do corpo |
|---|---|---|
| **histórica** | a herança longa do corpo feminino como ideal projetado — as Vênus paleolíticas, o corpo colonizado, a mulher reduzida a corpo e fertilidade | tronco · ventre |
| **antropológica** | o fenótipo que a denúncia *impõe* ao "tipo" vítima (cor, origem, aparência) — um rosto que não é de ninguém real | rosto · olhos |
| **social** | a vulnerabilidade estrutural: classe, território, periferia, deslocamento | quadril · pernas |
| **algoritmo** | o **escultor**. Lê as três camadas, enviesado pelo próprio dado, e funde tudo numa vítima-ideal. Não é parte do corpo — é a força que o deforma | — |

Quanto mais o algoritmo essencializa (quanto mais desigual fica a distribuição entre camadas),
mais a figura **colapsa na forma das Vênus paleolíticas**: seios, ventre e quadril incham,
braços e cabeça encolhem, o rosto se apaga. É o parâmetro `VENUS` (0→1) no TouchDesigner.

## A linhagem das Vênus

As Vênus paleolíticas (Willendorf, Lespugue, as cicládicas) são **sem rosto**, com os caracteres
sexuais exagerados — a mulher reduzida a corpo e fertilidade, um ideal projetado por quem as
esculpiu. A vítima-ideal é a mesma operação, 25 mil anos depois: sem rosto (ninguém real),
reduzida a um tipo. A escultura *vira* a crítica, na própria forma — sexualidade e gênero
fabricados por um olhar externo.

## O circuito da obra

```
testemunhos / coleta  →  as três camadas (dado)  →  ALGORITMO (escultor, enviesado)
      →  anomalia/escultura no TouchDesigner  →  exporta  →  galeria no site
```

## Estrutura do repositório

```
site/            o site: coleta em tempo real + testemunho anônimo + galeria
  index.html     página única da obra
  galeria.json   lista das esculturas exportadas do TouchDesigner (ver docs/GALERIA.md)
  galeria/       imagens/vídeos das esculturas
touchdesigner/   o que roda no TouchDesigner
  corpo_script_dat.py    gera a nuvem de pontos do corpo (com parâmetro VENUS)
  lacuna_claude_td.py    ponte que manda cada relato para a Claude classificar a camada
data/            esquema dos dados da coleta
docs/            como a coleta funciona e como ligar um backend real
```

## Status

Em construção. A coleta no site roda hoje em modo demonstração (fluxo simulado) + testemunhos
reais guardados no navegador. Para coletar de verdade, ligue um backend — ver `docs/COLETA.md`.

---
Os contextos exibidos são os **vieses que o algoritmo encena**, não verdades sobre vítimas reais.
Este é um trabalho de arte, não um canal oficial de denúncia.
