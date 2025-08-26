// src/components/ListaQuestoes.js
import React from 'react';
import CardQuestao from './CardQuestao';

const ListaQuestoes = ({ questoes, loading }) => {
  return (
    <div className="coluna-questoes">
      {loading ? (
        <p>Carregando...</p>
      ) : (
        <>
          {questoes.length > 0 ? (
            questoes.map((q, index) => (
              <CardQuestao key={index} questao={q} />
            ))
          ) : (
            <p>Nenhuma questão encontrada para os filtros selecionados.</p>
          )}
        </>
      )}
    </div>
  );
};

export default ListaQuestoes;