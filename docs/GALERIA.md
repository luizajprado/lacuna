# Como subir uma escultura para a galeria

1. Exporte do TouchDesigner um still (`.jpg`/`.png`) ou um vídeo/gif curto da anomalia.
2. Coloque o arquivo em `site/galeria/` (ex.: `site/galeria/anomalia-2026-10-26.jpg`).
3. Abra `site/galeria.json` e acrescente uma entrada:

```json
[
  {
    "img": "anomalia-2026-10-26.jpg",
    "titulo": "Vênus fabricada nº 1",
    "data": "26 out 2026",
    "nota": "coleta pendendo para a camada antropológica"
  }
]
```

4. Faça commit e push. A galeria no site se monta sozinha a partir desse arquivo.

Campos: `img` (nome do arquivo em `site/galeria/`), `titulo`, `data`, `nota` (opcional).
Sem nenhuma entrada, o site mostra molduras vazias com "a subir do TouchDesigner".
