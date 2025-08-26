// src/components/Filtros.js
import React from 'react';

const Filtros = ({ opcoes, filtros, onFiltroChange, onFiltrar }) => {
  return (
    <div className="coluna-filtros">
      <h2>Filtros</h2>
      <select name="ano" value={filtros.ano} onChange={onFiltroChange}>
        <option value="">Todos os Anos</option>
        {opcoes.ano.map(opt => <option key={opt} value={opt}>{opt}</option>)}
      </select>
      <select name="fase" value={filtros.fase} onChange={onFiltroChange}>
        <option value="">Todas as Fases</option>
        {opcoes.fase.map(opt => <option key={opt} value={opt}>Fase {opt}</option>)}
      </select>
      <select name="nivel" value={filtros.nivel} onChange={onFiltroChange}>
        <option value="">Todos os Níveis</option>
        {opcoes.nivel.map(opt => <option key={opt} value={opt}>Nível {opt}</option>)}
      </select>
      <select name="classe" value={filtros.classe} onChange={onFiltroChange}>
        <option value="">Todas as Classes</option>
        {opcoes.classe.map(opt => <option key={opt} value={opt}>{opt}</option>)}
      </select>
      <button onClick={onFiltrar}>Filtrar</button>
    </div>
  );
};

export default Filtros;