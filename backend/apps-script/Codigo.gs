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

function doGet() {
  return json({ ok: true, servico: 'lacuna-coleta' });
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
