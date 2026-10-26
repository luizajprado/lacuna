# TouchDesigner — da coleta à escultura

O circuito dentro do TD tem duas metades:

- **o corpo** (gerado uma vez, pesado): a nuvem de pontos da figura;
- **a coleta** (atualiza sempre, leve): os números que chegam da planilha e deformam o corpo.

Elas se encontram na hora de instanciar as partículas.

---

## Parte 1 — o corpo (você já tem)

1. **Script DAT** `corpo` → cole `touchdesigner/corpo_script_dat.py`. Ele gera a tabela com
   `tx ty tz r g b scale reg order` (a casca do corpo).
2. **DAT to CHOP** `corpoCHOP` → entrada = `corpo`, **First Row is: Names**. Agora cada coluna
   virou um canal (`tx`, `ty`, `tz`, `r`, `g`, `b`, `scale`, `reg`, `order`), cada ponto é uma amostra.
3. **Geometry COMP** instanciando por `corpoCHOP`:
   - Instancing **On**, Instance CHOP/DAT = `corpoCHOP`
   - TranslateX/Y/Z = `tx`/`ty`/`tz`, Scale = `scale`
   - Instance Color R/G/B = `r`/`g`/`b`
   - dentro do Geometry, um **Circle/Sphere SOP** pequenino + **Material** aditivo = as partículas
4. **Camera**, **Light**, **Render TOP** → você vê o corpo.

---

## Parte 2 — a coleta chegando

5. **Text DAT** `endpoint` → cole a URL do Apps Script que termina em `/exec`.
6. **Text DAT** `lacuna_poll` → cole `touchdesigner/lacuna_poll.py`.
7. Dois **Table DAT** vazios, nomeados exatamente **`coleta`** e **`pesoreg`** (o script escreve neles).
8. **DAT Execute** `disparo` → marque **Frame Start** e ponha:
   ```python
   def onFrameStart(frame):
       if frame % 300 == 0:          # ~5s a 60fps
           op('lacuna_poll').module.atualizar()
       return
   ```
   (Para testar já: botão direito no `lacuna_poll` > Run, depois na janela Textport digite
   `op('lacuna_poll').module.atualizar()` — as tabelas `coleta` e `pesoreg` devem preencher.)

Agora os números da planilha estão vivos dentro do TD:
- `coleta` → `hist antr soc venus total`
- `pesoreg` → o peso de cada uma das 6 regiões do corpo (reg 0..5)

---

## Parte 3 — a coleta deforma o corpo

**a) VENUS (o colapso no ídolo sem rosto):**
9. **DAT to CHOP** `coletaCHOP` → entrada = `coleta`, **First Row is: Names**.
10. **Select CHOP** `venus` → entrada = `coletaCHOP`, Channel Names = `venus`.
    Pronto: `corpo_script_dat.py` lê `op('venus')[0]` sozinho e re-gera o corpo mais "Vênus"
    quanto maior o valor. (Para não re-cozinhar o corpo pesado a cada frame, deixe o Script DAT
    com **Cook Type = Selective** e force o cook só quando `venus` muda de faixa.)

**b) peso por região (qual camada está "acesa" no corpo):**
11. **DAT to CHOP** `pesoregCHOP` → entrada = `pesoreg`, **First Row is: Names** → canal `w` com 6 amostras.
12. **Lookup CHOP** `pesoPonto`:
    - **Index** = o canal `reg` do `corpoCHOP`
    - **Lookup** = `pesoregCHOP` (canal `w`)
    → agora cada ponto recebe o peso da sua região (0..1).
13. Multiplique esse peso na cor/brilho (e, se quiser, no `scale`) antes de mandar pro Geometry:
    um **Math CHOP** multiplicando `r g b` do `corpoCHOP` por `pesoPonto`. Ligue a saída desse
    Math como a fonte de Instance Color.

Resultado: cada testemunho que entra na planilha muda, em segundos, qual parte do corpo brilha —
a camada histórica acende o tronco, a antropológica o rosto, a social o quadril/pernas — e,
conforme a coleta se concentra, a figura inteira colapsa na Vênus. O algoritmo esculpindo ao vivo.

---

## Mapa dos nomes (precisam bater com os scripts)
`corpo` · `corpoCHOP` · `endpoint` · `lacuna_poll` · `coleta` · `pesoreg` · `coletaCHOP` ·
`venus` · `pesoregCHOP` · `pesoPonto`
