/**
 * event_bus.js — Comunicação Pub/Sub entre Agentes — NL-Agent Framework
 *
 * Implementa o padrão Pub/Sub para comunicação A2A desacoplada.
 * Agentes publicam eventos sem conhecer os consumidores.
 * Padrão IIFE conforme análise da SEDF.
 */
const EventBus = (function () {
    var _assinantes = {};
    var _historico = [];
    var _maxHistorico = 1000;

    return {
        /**
         * Inscreve callback para um tipo de evento.
         * @param {string} evento - Nome do evento
         * @param {Function} callback
         * @param {string} [agente] - Identificador do agente assinante
         * @returns {string} ID da assinatura
         */
        inscrever: function (evento, callback, agente) {
            if (!_assinantes[evento]) _assinantes[evento] = [];
            var subId = "sub-" + Utilities.getUuid();
            _assinantes[evento].push({ id: subId, callback: callback, agente: agente || "anon" });
            return subId;
        },

        /**
         * Remove assinatura pelo ID.
         * @param {string} evento
         * @param {string} subscriptionId
         */
        desinscrever: function (evento, subscriptionId) {
            if (!_assinantes[evento]) return;
            _assinantes[evento] = _assinantes[evento].filter(function (s) {
                return s.id !== subscriptionId;
            });
        },

        /**
         * Publica evento para todos os assinantes.
         * @param {string} evento - Nome do evento
         * @param {*} dados - Payload do evento
         * @param {string} [emissor] - Agente emissor
         */
        publicar: function (evento, dados, emissor) {
            var registro = {
                evento: evento,
                dados: dados,
                emissor: emissor || "system",
                timestamp: new Date().toISOString(),
                entregues: 0,
            };

            var ouvintes = _assinantes[evento] || [];
            for (var i = 0; i < ouvintes.length; i++) {
                try {
                    ouvintes[i].callback(dados, evento);
                    registro.entregues++;
                } catch (e) {
                    Logger.log("EventBus erro [" + evento + " → " + ouvintes[i].agente + "]: " + e.message);
                }
            }

            _historico.push(registro);
            if (_historico.length > _maxHistorico) _historico.shift();
        },

        /**
         * Lista assinantes de um evento.
         * @param {string} evento
         * @returns {Array<string>} Nomes dos agentes inscritos
         */
        assinantes: function (evento) {
            return (_assinantes[evento] || []).map(function (s) { return s.agente; });
        },

        /**
         * Obtém histórico recente de eventos.
         * @param {number} [n] - Últimos N eventos (padrão 10)
         * @returns {Array<Object>}
         */
        historico: function (n) {
            n = n || 10;
            return _historico.slice(-n);
        },
    };
})();
