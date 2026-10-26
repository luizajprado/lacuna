/**
 * Lacuna — endpoint de coleta (Google Apps Script)
 * Recebe os testemunhos anônimos do site e grava numa planilha.
 *
 * COMO PUBLICAR:
 *  1. Crie uma planilha nova no Google Sheets.
 *  2. Nela: Extensões > Apps Script. Apague o conteúdo e cole este arquivo.
 *  3. Salve. Depois: Implantar > Nova implantação > tipo "App da Web".
 *       - Executar como: Eu
 *       - Quem tem acesso: Qualquer pessoa
 *  4. Copie a URL que termina em /exec e cole em site/config.js (window.LACUNA_ENDPOINT).
 *
 * Nenhum nome/documento deve chegar aqui: o site pede relatos anônimos.
 */

var ABA = 'testemunhos';

function doPost(e) {
  try {
    var dados = JSON.parse(e.postData.contents);
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sh = ss.getSheetByName(ABA) || criarAba(ss);
    sh.appendRow([
      dados.ts || new Date().toISOString(),
      dados.camada || '',
      dados.contexto || '',
      dados.origem || '',
      dados.anexo || ''
    ]);
    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, erro: String(err) });
  }
}

/**
 * O TouchDesigner chama isto (GET) a cada poucos segundos e recebe os números
 * já agregados: contagem por camada, total e o nível de colapso (venus).
 */
function doGet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(ABA);
  var agg = { ok: true, total: 0, hist: 0, antr: 0, soc: 0, venus: 0 };
  if (sh && sh.getLastRow() > 1) {
    var camadas = sh.getRange(2, 2, sh.getLastRow() - 1, 1).getValues(); // coluna "camada"
    camadas.forEach(function (r) {
      var c = (r[0] || '').toString();
      if (agg[c] !== undefined) { agg[c]++; agg.total++; }
    });
    var mx = Math.max(agg.hist, agg.antr, agg.soc);
    var mn = Math.min(agg.hist, agg.antr, agg.soc);
    // colapso na Venus = o quanto a distribuição entre camadas é desigual (essencialização)
    agg.venus = agg.total < 5 ? 0 : Math.max(0, (mx - mn) / (mx + 1));
  }
  return json(agg);
}

function criarAba(ss) {
  var sh = ss.insertSheet(ABA);
  sh.appendRow(['ts', 'camada', 'contexto', 'origem', 'anexo']);
  return sh;
}

function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
