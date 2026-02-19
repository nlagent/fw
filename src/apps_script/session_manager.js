/**
 * session_manager.js — Context Keeper (MCP) — NL-Agent Framework
 *
 * Agente de infraestrutura MCP responsável por preservar e propagar
 * o contexto da sessão do servidor entre interações.
 * Padrão IIFE conforme análise de 215.000 LOC da SEDF.
 *
 * Equivalência:
 *   Context Keeper (teórico) → SessionManager (implementação)
 *   12 referências no codebase SEDF
 */
const SessionManager = (function () {
    // Contexto privado — isolado do escopo global (= Context do MCP)
    const _sessions = {};
    const _defaultTTL = 3600; // 1 hora em segundos

    /**
     * Gera identificador único para sessão.
     * @returns {string} UUID v4
     */
    function _generateId() {
        return "sess-" + Utilities.getUuid();
    }

    /**
     * Verifica se sessão expirou.
     * @param {Object} session
     * @returns {boolean}
     */
    function _isExpired(session) {
        if (!session || !session.createdAt) return true;
        var now = new Date().getTime();
        var elapsed = (now - session.createdAt) / 1000;
        return elapsed > (session.ttl || _defaultTTL);
    }

    // Interface pública — contrato de comunicação (= Tools/Resources do MCP)
    return {
        /**
         * Cria nova sessão com contexto inicial.
         * @param {Object} contexto - Dados iniciais da sessão
         * @param {number} [ttl] - Tempo de vida em segundos
         * @returns {string} ID da sessão criada
         */
        criar: function (contexto, ttl) {
            var id = _generateId();
            _sessions[id] = {
                id: id,
                contexto: contexto || {},
                createdAt: new Date().getTime(),
                updatedAt: new Date().getTime(),
                ttl: ttl || _defaultTTL,
                metadata: { protocol: "MCP", role: "context_keeper" },
            };
            return id;
        },

        /**
         * Obtém contexto da sessão (cópia defensiva).
         * @param {string} sessionId
         * @returns {Object|null} Contexto ou null se expirada/inexistente
         */
        obter: function (sessionId) {
            var session = _sessions[sessionId];
            if (!session || _isExpired(session)) {
                delete _sessions[sessionId];
                return null;
            }
            return JSON.parse(JSON.stringify(session.contexto));
        },

        /**
         * Atualiza dados no contexto da sessão.
         * @param {string} sessionId
         * @param {Object} dados - Dados a mesclar no contexto
         * @returns {boolean} true se atualizado com sucesso
         */
        atualizar: function (sessionId, dados) {
            var session = _sessions[sessionId];
            if (!session || _isExpired(session)) return false;
            for (var key in dados) {
                if (dados.hasOwnProperty(key)) {
                    session.contexto[key] = dados[key];
                }
            }
            session.updatedAt = new Date().getTime();
            return true;
        },

        /**
         * Encerra e remove uma sessão.
         * @param {string} sessionId
         */
        encerrar: function (sessionId) {
            delete _sessions[sessionId];
        },

        /**
         * Lista sessões ativas (não expiradas).
         * @returns {Array<string>} IDs de sessões ativas
         */
        listarAtivas: function () {
            var ativas = [];
            for (var id in _sessions) {
                if (!_isExpired(_sessions[id])) {
                    ativas.push(id);
                }
            }
            return ativas;
        },
    };
})();
