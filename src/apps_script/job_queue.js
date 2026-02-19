/**
 * job_queue.js — Orquestrador de Tarefas A2A — NL-Agent Framework
 *
 * Implementa o ciclo de vida de tarefas A2A:
 *   submitted → working → completed | failed | canceled
 *
 * Fila priorizada: critica > alta > normal > baixa
 * Retry automático com máximo de 3 tentativas.
 * Padrão IIFE conforme análise da SEDF.
 */
const JobQueue = (function () {
    var _fila = [];
    var _emProcessamento = {};
    var _concluidos = {};
    var _prioridades = { critica: 0, alta: 1, normal: 2, baixa: 3 };

    function _gerarId() {
        return "job-" + Utilities.getUuid();
    }

    function _compararPrioridade(a, b) {
        return (_prioridades[a.prioridade] || 2) - (_prioridades[b.prioridade] || 2);
    }

    return {
        /**
         * Enfileira nova tarefa.
         * @param {Object} tarefa - { tipo, dados, prioridade, maxRetries }
         * @returns {string} ID do job criado
         */
        enfileirar: function (tarefa) {
            var job = {
                id: _gerarId(),
                tipo: tarefa.tipo,
                dados: tarefa.dados || {},
                prioridade: tarefa.prioridade || "normal",
                estado: "submitted",
                tentativas: 0,
                maxTentativas: tarefa.maxRetries || 3,
                criadoEm: new Date().toISOString(),
                atualizadoEm: new Date().toISOString(),
            };
            _fila.push(job);
            return job.id;
        },

        /**
         * Retira próximo job da fila (maior prioridade primeiro).
         * @returns {Object|null} Job ou null se fila vazia
         */
        dequeue: function () {
            if (_fila.length === 0) return null;
            _fila.sort(_compararPrioridade);
            var job = _fila.shift();
            job.estado = "working";
            job.tentativas++;
            job.atualizadoEm = new Date().toISOString();
            _emProcessamento[job.id] = job;
            return job;
        },

        /**
         * Marca job como concluído.
         * @param {string} jobId
         * @param {*} resultado
         */
        completar: function (jobId, resultado) {
            var job = _emProcessamento[jobId];
            if (!job) return;
            job.estado = "completed";
            job.resultado = resultado;
            job.atualizadoEm = new Date().toISOString();
            _concluidos[jobId] = job;
            delete _emProcessamento[jobId];
        },

        /**
         * Marca job como falho. Re-enfileira se dentro do limite de tentativas.
         * @param {string} jobId
         * @param {string} motivo
         * @returns {boolean} true se re-enfileirado, false se falha definitiva
         */
        falhar: function (jobId, motivo) {
            var job = _emProcessamento[jobId];
            if (!job) return false;
            delete _emProcessamento[jobId];
            if (job.tentativas < job.maxTentativas) {
                job.estado = "submitted";
                job.ultimoErro = motivo;
                job.atualizadoEm = new Date().toISOString();
                _fila.push(job);
                return true; // re-enfileirado
            }
            job.estado = "failed";
            job.ultimoErro = motivo;
            _concluidos[jobId] = job;
            return false; // falha definitiva
        },

        /**
         * Cancela um job.
         * @param {string} jobId
         */
        cancelar: function (jobId) {
            // Remover da fila
            _fila = _fila.filter(function (j) { return j.id !== jobId; });
            // Remover de processamento
            var job = _emProcessamento[jobId];
            if (job) {
                job.estado = "canceled";
                _concluidos[jobId] = job;
                delete _emProcessamento[jobId];
            }
        },

        /**
         * Obtém status de um job.
         * @param {string} jobId
         * @returns {Object|null}
         */
        status: function (jobId) {
            if (_emProcessamento[jobId]) return _emProcessamento[jobId];
            if (_concluidos[jobId]) return _concluidos[jobId];
            for (var i = 0; i < _fila.length; i++) {
                if (_fila[i].id === jobId) return _fila[i];
            }
            return null;
        },

        /**
         * Retorna métricas da fila.
         * @returns {Object}
         */
        metricas: function () {
            return {
                naFila: _fila.length,
                emProcessamento: Object.keys(_emProcessamento).length,
                concluidos: Object.keys(_concluidos).length,
            };
        },
    };
})();
