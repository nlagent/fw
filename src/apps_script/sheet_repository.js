/**
 * sheet_repository.js — Abstração CRUD (Sheets-as-Database) — NL-Agent Framework
 *
 * Equivalências:
 *   SpreadsheetApp → Driver de banco de dados
 *   SheetRepository → ORM / DAO
 *   Abas (Sheets)  → Tabelas
 *   COLUMN_SCHEMAS → Migrations de schema
 *
 * Padrão IIFE conforme análise da SEDF.
 */
const SheetRepository = (function () {
    var _cache = {};

    /**
     * Obtém referência à aba.
     * @param {string} spreadsheetId
     * @param {string} sheetName
     * @returns {GoogleAppsScript.Spreadsheet.Sheet}
     */
    function _getSheet(spreadsheetId, sheetName) {
        var key = spreadsheetId + ":" + sheetName;
        if (!_cache[key]) {
            var ss = SpreadsheetApp.openById(spreadsheetId);
            _cache[key] = ss.getSheetByName(sheetName);
        }
        return _cache[key];
    }

    /**
     * Obtém cabeçalhos da aba (primeira linha).
     * @param {GoogleAppsScript.Spreadsheet.Sheet} sheet
     * @returns {Array<string>}
     */
    function _getHeaders(sheet) {
        return sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    }

    /**
     * Converte linha (array) em objeto usando cabeçalhos.
     */
    function _rowToObject(headers, row) {
        var obj = {};
        for (var i = 0; i < headers.length; i++) {
            obj[headers[i]] = row[i];
        }
        return obj;
    }

    return {
        /**
         * Lê todos os registros de uma aba.
         * @param {string} spreadsheetId
         * @param {string} sheetName
         * @returns {Array<Object>}
         */
        findAll: function (spreadsheetId, sheetName) {
            var sheet = _getSheet(spreadsheetId, sheetName);
            if (!sheet || sheet.getLastRow() <= 1) return [];
            var headers = _getHeaders(sheet);
            var data = sheet.getRange(2, 1, sheet.getLastRow() - 1, headers.length).getValues();
            return data.map(function (row) { return _rowToObject(headers, row); });
        },

        /**
         * Busca registros que satisfazem um filtro.
         * @param {string} spreadsheetId
         * @param {string} sheetName
         * @param {Object} filtro - { coluna: valor }
         * @returns {Array<Object>}
         */
        findWhere: function (spreadsheetId, sheetName, filtro) {
            var todos = this.findAll(spreadsheetId, sheetName);
            return todos.filter(function (registro) {
                for (var key in filtro) {
                    if (registro[key] !== filtro[key]) return false;
                }
                return true;
            });
        },

        /**
         * Insere novo registro (append).
         * @param {string} spreadsheetId
         * @param {string} sheetName
         * @param {Object} registro
         * @returns {number} Número da linha inserida
         */
        insert: function (spreadsheetId, sheetName, registro) {
            var sheet = _getSheet(spreadsheetId, sheetName);
            var headers = _getHeaders(sheet);
            var row = headers.map(function (h) { return registro[h] || ""; });
            sheet.appendRow(row);
            return sheet.getLastRow();
        },

        /**
         * Atualiza registro na linha especificada.
         * @param {string} spreadsheetId
         * @param {string} sheetName
         * @param {number} rowNumber - Linha (1-indexed, incluindo cabeçalho)
         * @param {Object} dados
         */
        update: function (spreadsheetId, sheetName, rowNumber, dados) {
            var sheet = _getSheet(spreadsheetId, sheetName);
            var headers = _getHeaders(sheet);
            for (var key in dados) {
                var colIndex = headers.indexOf(key);
                if (colIndex >= 0) {
                    sheet.getRange(rowNumber, colIndex + 1).setValue(dados[key]);
                }
            }
        },

        /**
         * Remove registro (limpa conteúdo da linha).
         * @param {string} spreadsheetId
         * @param {string} sheetName
         * @param {number} rowNumber
         */
        remove: function (spreadsheetId, sheetName, rowNumber) {
            var sheet = _getSheet(spreadsheetId, sheetName);
            sheet.getRange(rowNumber, 1, 1, sheet.getLastColumn()).clearContent();
        },

        /**
         * Conta registros na aba.
         * @param {string} spreadsheetId
         * @param {string} sheetName
         * @returns {number}
         */
        count: function (spreadsheetId, sheetName) {
            var sheet = _getSheet(spreadsheetId, sheetName);
            return sheet ? Math.max(0, sheet.getLastRow() - 1) : 0;
        },

        /**
         * Limpa cache interno de referências.
         */
        clearCache: function () {
            _cache = {};
        },
    };
})();
